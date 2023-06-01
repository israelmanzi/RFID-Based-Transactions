import serial
from datetime import datetime

ser = serial.Serial(
    port='COM15',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

open('uuid_store.txt', 'w').close()

print("Program start ....")
print("Waiting for PICC ...")

# collection with { id, name, price } of sample products
products = [
    {"id": 1, "name": "Coca Cola", "price": 2},
    {"id": 2, "name": "Fanta", "price": 2},
    {"id": 3, "name": "Sprite", "price": 2},
    {"id": 4, "name": "Red Bull", "price": 3},
    {"id": 5, "name": "Monster", "price": 3},
    {"id": 6, "name": "Pepsi", "price": 2},
    {"id": 7, "name": "7up", "price": 2},
    {"id": 8, "name": "Dr Pepper", "price": 2},
    {"id": 9, "name": "Lipton Ice Tea", "price": 2},
    {"id": 10, "name": "Snickers", "price": 2},
    {"id": 11, "name": "Mars", "price": 2},
    {"id": 12, "name": "Twix", "price": 2},
    {"id": 13, "name": "KitKat", "price": 2},
    {"id": 14, "name": "Milky Way", "price": 2},
    {"id": 15, "name": "Bounty", "price": 2},
    {"id": 16, "name": "M&M's", "price": 2},
    {"id": 17, "name": "Doritos", "price": 2},
    {"id": 18, "name": "Lays", "price": 2},
    {"id": 19, "name": "Pringles", "price": 2},
    {"id": 20, "name": "Cheetos", "price": 2},
    {"id": 21, "name": "Chio", "price": 2},
    {"id": 22, "name": "Lay's Oven Baked", "price": 2},
    {"id": 23, "name": "Lay's Sensations", "price": 2},
]

purchased = products[0]

ser.flush()

if __name__ == '__main__':
    while True:
        balance = 0

        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').strip()
            # print(line)

            if (line.startswith("UUID: ")):
                print("##################################################")
                print("\tCard detected!")
                print("\tUUID: " + line.removeprefix("UUID: "))
                print("##################################################")

                # store uuid in file "uuid_store.txt"
                with open("uuid_store.txt", "w") as file:
                    file.write(line.removeprefix("UUID: "))

            if (line.startswith("Balance: ")):
                print("##################################################")
                balance = int(line.removeprefix("Balance: "))
                print("\tCurrent balance: $" + line.removeprefix("Balance: "))
                print("##################################################")

                product_to_purchase = int(input("\tEnter product id: "))

                product = next(
                    (item for item in products if item["id"] == product_to_purchase), None)

                if (product):
                    print("##################################################")
                    print(f"\tProduct: {product['name']}")
                    print(f"\tPrice: ${product['price']}")
                    print("##################################################")

                    if (balance >= product["price"]):
                        balance -= product["price"]
                        ser.write(f"{balance}\n".encode('utf-8'))

                        purchased = product

                        # print(f"New balance: {balance}")
                    else:
                        print("Insufficient funds")
                        ser.write("Insufficient funds\n".encode('utf-8'))

            # if (line.startswith("Detected: ")):
                # print(f"Detected {line.removeprefix('Detected: ')}")

            if (line.startswith("Data saved: ")):
                print("\tSaving data ...")
                balance = int(line.removeprefix("Data saved: "))
                # store logs in file "transaction_logs.txt" { id, name, price, balance }
                with open("transaction_logs.txt", "a+") as file:
                    file.write(
                        f"{purchased['id']}, {purchased['name']}, {purchased['price']}, {balance}, {datetime.now()}\n")

                print("\tData saved!")

            elif (line.startswith("Data not saved.")):
                print("\tData not saved!")
                print("The last transaction was not saved. Please try again & try to place the card on the reader for a longer time at a smaller distance.")
        else:
            continue

        # balance = 0
        # if ser.in_waiting > 0:
        #     line = ser.readline().decode('utf-8').strip()

        #     print(line)

        #     if (line.startswith("Balance: ")):
        #         print(line)
        #         balance = int(line.removeprefix("Balance: "))

        #         print(f"Balance on PICC: {balance}")

        #         if True:
        #             product_id = int(input("Enter product id: "))

        #             product = next((item for item in products if item["id"] == product_id), None)

        #             ser.write(f"{products[0]['id'] + products[0]['price']}#\n".encode('utf-8'))

        #             if (product):
        #                 print(f"Product: {product['name']}")
        #                 print(f"Price: {product['price']}")

        #                 if (balance >= product["price"]):
        #                     balance -= product["price"]
        #                     print(f"Balance: {balance}")
        #                     # ser.write(f"New: {balance}\n".encode('utf-8'))
        #                     print(f"New balance: {balance}")
        #                     ser.write(balance)
        #                 else:
        #                     print("Insufficient funds")
        #                     # ser.write("Insufficient funds\n".encode('utf-8'))
        #             else:
        #                 print("Product not found")
        #                 # ser.write("Product not found\n".encode('utf-8'))

            # else:
            # print(line)

            # if (line.startswith("[PIIC ready!]")):
            # # if (line.startswith("Enter funds you want to store to the card, ending with #!")):
            #     print("Enter funds you want to store to the card, ending with #")
            #     funds = int(input("Enter funds: "))
            #     ser.write(f"{funds}#\n".encode('utf-8'))

            #     balance += funds

            #     print(f"Balance: {balance}")

            # elif (line.startswith("Funds: ")):
            #     balance = int(line.removeprefix("Funds: "))

            #     print(f"Balance on PICC: {balance}")

            #     while True:
            #         product_id = int(input("Enter product id: "))

            #         product = next((item for item in products if item["id"] == product_id), None)

            #         if (product):
            #             print(f"Product: {product['name']}")
            #             print(f"Price: {product['price']}")

            #             if (balance >= product["price"]):
            #                 balance -= product["price"]
            #                 print(f"Balance: {balance}")
            #                 # ser.write(f"New: {balance}\n".encode('utf-8'))
            #                 print(f"New balance: {balance}")
            #                 ser.write(balance)
            #             else:
            #                 print("Insufficient funds")
            #                 # ser.write("Insufficient funds\n".encode('utf-8'))
            #         else:
            #             print("Product not found")
            #             # ser.write("Product not found\n".encode('utf-8'))

            # # else:
            # #     print(line)
            #     # ser.write(line.encode('utf-8'))
