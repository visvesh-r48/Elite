import mysql.connector
import unittest

#Connect to SQL
mydb = mysql.connector.connect(host = "localhost", user = "root", password = "My$QLMy$QL1!", database = "bank")

cursor = mydb.cursor()

create_table_sql = """
CREATE TABLE accounts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    pin INT,
    balance DOUBLE
)
"""

#cursor.execute(create_table_sql)

#mydb.commit()

#Create lists to store current account data
data = []

names = []
pins = []
balances = []

#Add data to names
column_name = "name"
cursor.execute("SELECT " + column_name + " FROM accounts")
rows = cursor.fetchall()
for row in rows:
    names.append(row[0].lower())

#Add data to pins
column_pin = "pin"
cursor.execute("SELECT " + column_pin + " FROM accounts")
rows = cursor.fetchall()
for row in rows:
    pins.append(row[0])

#Add data to balances
column_balance = "balance"
cursor.execute("SELECT " + column_balance + " FROM accounts")
rows = cursor.fetchall()
for row in rows:
    balances.append(row[0])
    
#Function to create an account
def create_account():
    name = input("Please enter your full name\n")
    while name.lower() in names:
        print(f"An account with the name {name.title()} already exists.")
        name = input("Please enter your full name\n")
    
    pin = input("Please enter a PIN number (>= 4 characters)\n")
    
    while(pin.isalpha() or len(pin) < 4):
        print("Invalid PIN. Please enter PIN again.")
        pin = input("Please enter a PIN number (>= 4 characters)\n")
    
    data.append((name, pin, 0.0))

    insert_data_sql = """
    INSERT INTO accounts (name, pin, balance) VALUES (%s, %s, %s)
    """
    cursor.executemany(insert_data_sql, data)
    mydb.commit()
    print("Account successfully created.")

#Function to sign in to an account
def sign_in():
    while True:
        user_name = input("Please enter your name\n")
        user_pin = int(input("Please enter your PIN number\n"))

        if(user_name.lower() in names and user_pin in pins):
            if(names.index(user_name.lower()) == pins.index(user_pin)):
                print(f"Successfully signed in as {user_name}")
                
                while True:
                    options = input("Choose an action to perform.(-1 to exit)\n1.Check balance\n2.Make a deposit\n3.Make a withdrawal\n4.Edit profile\n5.Close account\n")
                    if(options == "-1"):
                        print("Thank you for visiting our bank.")
                        exit()
                    elif(options == "1"):
                        print(f"Current amount: ${check_balance(user_name)}")
                    elif(options == "2"):
                        print(f"New amount: ${deposit(user_name)}")
                    elif(options == "3"):
                        print(f"New amount: ${withdrawal(user_name)}")
                    elif(options == "4"):
                        edit_profile(user_name)
                    elif(options == "5"):
                        close_account(user_name)
                    else:
                        print("Invalid input.")
        else:
            print("Invalid account details.")

    
    
        
        
#Function to check the balance of an account
def check_balance(name):
    name_index = names.index(name.lower())
    return round(balances[name_index],2)

#Function to deposit money into an account
def deposit(name):
    amount = float(input("Enter the amount you want to deposit\n"))
    name_index = names.index(name.lower())
    amount += balances[name_index]

    update_sql = "UPDATE accounts SET balance = %s WHERE name = %s"
    cursor.execute(update_sql, (amount, name))

    mydb.commit()
    balances[name_index] = amount
    print("Deposit complete.")
    return round(amount,2)

#Function to withdraw money from an account
def withdrawal(name):
    amount = float(input("Enter the amount you want to withdraw\n"))
    name_index = names.index(name.lower())
    balance = balances[name_index] - amount
    if(balance < 0):
        balance += amount
        print("Not enough in balance to withdraw.")
    else:
        update_sql = "UPDATE accounts SET balance = %s WHERE name = %s"
        cursor.execute(update_sql, (balance, name))

        mydb.commit()
        balances[name_index] = balance

        print("Withdrawal complete.")
    return round(balance,2)

#Function to edit an account profile
def edit_profile(name):
    choose = input("Enter 1 to change your name or 2 to change your PIN(-1 to exit)\n")
    if(choose == "-1"):
        print("Thank you for visiting our bank.")
        exit()
    elif(choose == "1"):
        new_name = input("Enter your new name\n")
        name_index = names.index(name.lower())
        update_sql = "UPDATE accounts SET name = %s WHERE name = %s"
        cursor.execute(update_sql, (new_name, name))
        mydb.commit()
        names[name_index] = new_name.lower()
        print("Name successfully updated.")
    elif(choose == "2"):
        while True:
            name_index = names.index(name.lower())
            pin_confirm = int(input("Enter your old pin to confirm\n"))
            if(pin_confirm == pins[name_index]):
                new_pin = input("Enter your new pin (>= 4 characters)\n")
                while(new_pin.isalpha() or len(new_pin) < 4):
                    print("Invalid PIN. Please enter a new PIN.")
                    new_pin = input("Enter your new pin (>= 4 characters)\n")
            else:
                print("Incorrect PIN.")
                continue
            update_sql = "UPDATE accounts SET pin = %s WHERE name = %s"
            cursor.execute(update_sql, (new_pin, name))
            mydb.commit()
            pins[name_index] = new_pin
            print("PIN successfully updated.")
            break

#Function to close an account
def close_account(name):
    while True:
        name_index = names.index(name.lower())
        pin_confirm = int(input("Enter your old pin to confirm\n"))
        if(pin_confirm == pins[name_index]):
            check = input("Are you sure you want to close your account(Y/N)\n")
            if(check.lower() == "y" or check.lower() == "yes"):
                delete_sql = "DELETE FROM accounts WHERE name = %s"
                cursor.execute(delete_sql, (name,))
                mydb.commit()
                print(f"Account with the name {name} has been closed")
                names.pop(name_index)
                pins.pop(name_index)
                balances.pop(name_index)
                exit()
            else:
                break
        else:
            print("Incorrect PIN.")
            continue


#UnitTest for function
'''
class TestCheckBalanceFunction(unittest.TestCase):
    def test_check_balance(self):
        self.assertEqual(check_balance("Bob Joe"), 209.71)
if __name__ == '__main__':
    unittest.main()
'''
    
    
#Loop though functions until user exits
print("Hello, welcome to the Banking District.")

while True:
    choice = input("Enter 1 to make a new account or 2 to sign in with an existing account(-1 to exit)\n")
    if(choice == "-1"):
        print("Thank you for visiting our bank.")
        exit()
    elif(choice == "1"):
        create_account()
    elif(choice == "2"):
        sign_in()
    else:
        print("Invalid input.")

    





cursor.close()
mydb.close()





