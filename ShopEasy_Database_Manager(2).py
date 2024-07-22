from tabulate import tabulate

import mysql.connector

# Connect to the MySQL database
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="shop"
)

mycursor = mydb.cursor()
print("Connected to the database and ready for operations.")

def add_record(table):
    print(f"Enter the details for the {table} table")
    SHOP_NO = int(input("Enter the Shop No.: "))
    SHOP_NAME = input("Enter the Name of the Shop: ")
    PRODUCTS = input("Enter the Name of Products: ")
    PRICE_RANGE = input("Enter the Price range: ")
    OFFERS = input("Enter the Offers: ")

    sql = f"INSERT INTO {table} (SHOP_NO, SHOP_NAME, PRODUCTS, PRICE_RANGE, OFFERS) VALUES (%s, %s, %s, %s, %s)"
    values = (SHOP_NO, SHOP_NAME, PRODUCTS, PRICE_RANGE, OFFERS)
    try:
        mycursor.execute(sql, values)
        mydb.commit()
        print("Record saved")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        mydb.rollback()

def display_records(table):
    try:
        mycursor.execute(f"SELECT * FROM {table}")
        result = mycursor.fetchall()
        # Get column names
        column_names = [i[0] for i in mycursor.description]
        # Print the result in table format
        print(tabulate(result, headers=column_names, tablefmt='grid'))
    except mysql.connector.Error as err:
        print(f"Error: {err}")

def search_record(table):
    num = int(input("Enter the Shop No. to be searched: "))
    sql = f"SELECT * FROM {table} WHERE SHOP_NO = %s"
    try:
        mycursor.execute(sql, (num,))
        shop = mycursor.fetchall()
        if shop:
            print("Details of the Shop:")
            for rec in shop:
                print(rec)
        else:
            print("No such Shop available")
    except mysql.connector.Error as err:
        print(f"Error: {err}")

def update_offer(table):
    shop = int(input("Enter the Shop No. whose offer must be updated: "))
    newoff = input("Enter the new offer: ")
    sql = f"UPDATE {table} SET OFFERS = %s WHERE SHOP_NO = %s"
    try:
        mycursor.execute(sql, (newoff, shop))
        mydb.commit()
        print("Offer is updated")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        mydb.rollback()

def delete_record(table):
    shop = int(input("Enter the Shop No. to be deleted: "))
    sql = f"DELETE FROM {table} WHERE SHOP_NO = %s"
    try:
        mycursor.execute(sql, (shop,))
        mydb.commit()
        print("One record is deleted")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        mydb.rollback()

# Menu loop
while True:
    print("\nMENU")
    print("1. Add records")
    print("2. Display all records")
    print("3. Search record by Shop No.")
    print("4. Update Offer by Shop No.")
    print("5. Delete record by Shop No.")
    print("6. Exit")
    ch = int(input("Enter your choice: "))

    if ch == 6:
        break
    elif ch in [1, 2, 3, 4, 5]:
        table_choice = input("Select table (FOOD/CLOTHING/SHOES): ").upper()
        if table_choice not in ["FOOD", "CLOTHING", "SHOES"]:
            print("Invalid table choice. Please select either FOOD or CLOTHING.")
            continue
        
        if ch == 1:
            add_record(table_choice)
        elif ch == 2:
            display_records(table_choice)
        elif ch == 3:
            search_record(table_choice)
        elif ch == 4:
            update_offer(table_choice)
        elif ch == 5:
            delete_record(table_choice)

# Close the database connection
mycursor.close()
mydb.close()
print("Database connection closed.")
