import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register():
    username  = input('enter username: ')
    age = input('enter age: ')
    email = input('enter email: ')
    password = input('enter password: ')
    confirm = input('confirm password: ')
    
    if password != confirm:
        print("Passwords do not match.")
        return
    
    with open('users.txt', 'a') as f:
        f.write(f"{username},{age},{email},{hash_password(password)}\n")
    print("Registration successful.")
    
def login():
    username = input('enter username: ')
    password = input('enter password: ')
    
    hashed_password = hash_password(password)
    
    with open('users.txt', 'r') as f:
        for line in f:
            user, age, email, stored_hashed_password = line.strip().split(',')
            if user == username and stored_hashed_password == hashed_password:
                print("Login successful.")
                return
    print("Invalid username or password.")
    
def get_users():
    users = []
    with open('users.txt', 'r') as f:
        for line in f:
            user, age, email, _ = line.strip().split(',')
            users.append({'username': user, 'age': age, 'email': email})
    return users
    
def main():
    while True:
        print("Welcome to the User System")
        print("1. Register")
        print("2. Login")
        print("3. View Users")
        print("4. Exit")
        choice = input("Choose an option: ")
        if choice == "1":
            register()
        elif choice == "2":
            login()
        elif choice == "3":
            users = get_users()
            for user in users:
                print(f"Username: {user['username']}, Age: {user['age']}, Email: {user['email']}")  
        elif choice == "4":
            print("Exiting the User System. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
if __name__ == "__main__":
    main()