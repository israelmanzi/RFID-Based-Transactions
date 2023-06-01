#include <SPI.h>
#include <MFRC522.h>
#define RST_PIN 9
#define SS_PIN 10
MFRC522 mfrc522(SS_PIN, RST_PIN);
MFRC522::MIFARE_Key key;
MFRC522::StatusCode card_status;

byte nuidPICC[4];

void setup() {
  Serial.begin(9600);
  SPI.begin();
  mfrc522.PCD_Init();
  //  Serial.println(F("Enter data, ending with #"));
  Serial.println("");
}

void loop() {
  for (byte i = 0; i < 6; i++) {
    key.keyByte[i] = 0xFF;
  }
  if (!mfrc522.PICC_IsNewCardPresent()) {
    return;
  }

  if (!mfrc522.PICC_ReadCardSerial()) {
    Serial.println("[Bring PIIC closer to PCD]");
    return;
  }

  for (byte i = 0; i < 4; i++) {
    nuidPICC[i] = mfrc522.uid.uidByte[i];
  }

  Serial.print("UUID: ");
  printHex(mfrc522.uid.uidByte, mfrc522.uid.size);
  Serial.println();

  byte buffr[16];
  byte block = 4;
  byte len;

  Serial.setTimeout(1000L);
  //  len = Serial.readBytesUntil('#', (char *) buffr, 16);
  Serial.println("[PIIC ready!]");
  //  if (len > 0) {
  //    for (byte i = len; i < 16; i++) {
  //      buffr[i] = ' '; //We have to pad array items with spaces.
  //    }
  //    String mString;
  //    mString = String((char*)buffr);
  //
  //    Serial.println(" ");
  //    writeBytesToBlock(block, buffr);
  //    Serial.println(" ");
  //    Serial.print("Successfully saved on PICC!");
  ////    Serial.print(block);
  ////    Serial.print(":");
  ////    Serial.println(mString);
  //    Serial.println("Note: To rewrite to this PICC, take it away from the PCD, and bring it closer again.");
  //  }

  Serial.println(F("\n*** Balance on the PICC ***\n"));
  String balance = readBytesFromBlock();
  Serial.println("Balance: " + balance);
  Serial.println(F("\n***************************\n"));
  delay(1000);

  while (!Serial.available()) {
    delay(3);
  }

  Serial.println();
  String res = Serial.readString();
  Serial.println("Detected: " + res);

  char charArray[res.length() + 1];
  res.toCharArray(charArray, sizeof(charArray));

  byte* byteArray = (byte*)charArray;

  writeBytesToBlock(block, byteArray, res);

  mfrc522.PICC_HaltA();
  mfrc522.PCD_StopCrypto1();
  delay(500);
}

void printHex(byte *buffer, byte bufferSize) {
  for (byte i = 0; i < bufferSize; i++) {
    Serial.print(buffer[i] < 0x10 ? " 0" : " ");
    Serial.print(buffer[i], HEX);
  }
  delay(500);
}

void writeBytesToBlock(byte block, byte buff[], String resp) {
  card_status = mfrc522.PCD_Authenticate(MFRC522::PICC_CMD_MF_AUTH_KEY_A, block, &key, &(mfrc522.uid));

  if (card_status != MFRC522::STATUS_OK) {
    Serial.print(F("PCD_Authenticate() failed: "));
    Serial.println(mfrc522.GetStatusCodeName(card_status));
    Serial.println("Data not saved.");
    return;
  }

  else {
    Serial.println(F("PCD_Authenticate() success: "));
  }
  // Write block
  card_status = mfrc522.MIFARE_Write(block, buff, 16);

  if (card_status != MFRC522::STATUS_OK) {
    Serial.print(F("MIFARE_Write() failed: "));
    Serial.println(mfrc522.GetStatusCodeName(card_status));
    Serial.println("Data not saved.");
    return;
  }
  else {
    Serial.println("Data saved: " + resp);
  }
}

String readBytesFromBlock() {
  byte blockNumber = 4;

  card_status = mfrc522.PCD_Authenticate(MFRC522::PICC_CMD_MF_AUTH_KEY_A, blockNumber, &key, &(mfrc522.uid));
  if (card_status != MFRC522::STATUS_OK) {
    Serial.print(F("Authentication failed: "));
    Serial.println(mfrc522.GetStatusCodeName(card_status));
    return;
  }
  byte arrayAddress[18];
  byte buffersize = sizeof(arrayAddress);
  card_status = mfrc522.MIFARE_Read(blockNumber, arrayAddress, &buffersize);
  if (card_status != MFRC522::STATUS_OK) {
    Serial.print(F("Reading failed: "));
    Serial.println(mfrc522.GetStatusCodeName(card_status));
    return;
  }

  String value = "";
  for (uint8_t i = 0; i < 16; i++) {
    value += (char)arrayAddress[i];
  }
  value.trim();
  return value;
}
