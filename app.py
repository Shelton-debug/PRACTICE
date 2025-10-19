import sqlite3

conn = sqlite3.connect('bank.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS accounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    pin TEXT NOT NULL,
    balance REAL NOT NULL DEFAULT 0.0
)
''')
conn.commit()

def create_account():
    name = input("Enter your name: ")
    pin = input("Set a 4-digit PIN: ")
    
    if len(pin) != 4 or not pin.isdigit():
        print("PIN must be a 4-digit number.")
        return
    cursor.execute('INSERT INTO accounts (name, pin) VALUES (?, ?)', (name, pin))
    conn.commit()
    print("Account created successfully!")

def login():
    name = input("Enter your account number: ")
    pin = input("Enter your PIN: ")

    cursor.execute('SELECT * FROM accounts WHERE name = ? AND pin = ?', (name, pin))
    account = cursor.fetchone()
    
    if account:
        print("Login successful!")
        return account
    else:
        print("Invalid name or PIN.")
        return None
    
def check_balance(account):
    cursor.execute('SELECT balance FROM accounts WHERE id = ?', (account[0],))
    balance = cursor.fetchone()[0]
    print(f"Your current balance is: ${balance:.2f}")
    
def deposit(account):
    amount = float(input("Enter amount to deposit: "))
    cursor.execute('UPDATE accounts SET balance = balance + ? WHERE id = ?', (amount, account[0]))
    conn.commit()
    print(f"${amount:.2f} deposited successfully!")
    
def withdraw(account):
    amount = float(input("Enter amount to withdraw: "))
    cursor.execute('SELECT balance FROM accounts WHERE id = ?', (account[0],))
    balance = cursor.fetchone()[0]
    
    if amount > balance:
        print("Insufficient funds.")
    else:
        cursor.execute('UPDATE accounts SET balance = balance - ? WHERE id = ?', (amount, account[0]))
        conn.commit()
        print(f"${amount:.2f} withdrawn successfully!")
        

def main():
    while True:
        print("\nWelcome to the Banking System")
        print("1. Create Account")
        print("2. Login")
        print("3. Exit")
        choice = input("Choose an option: ")
        
        if choice == '1':
            create_account()
        elif choice == '2':
            account = login()
            if account:
                while True:
                    print("\n1. Check Balance")
                    print("2. Deposit")
                    print("3. Withdraw")
                    print("4. Logout")
                    sub_choice = input("Choose an option: ")
                    
                    if sub_choice == '1':
                        check_balance(account)
                    elif sub_choice == '2':
                        deposit(account)
                    elif sub_choice == '3':
                        withdraw(account)
                    elif sub_choice == '4':
                        print("Logged out successfully.")
                        break
                    else:
                        print("Invalid option.")
        elif choice == '3':
            print("Thank you for using the Banking System. Goodbye!")
            break
        else:
            print("Invalid option.")
            
if __name__ == "__main__":
    main()
    conn.close()