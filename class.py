import tkinter as tk 
from tkinter import messagebox
import hashlib 
import os

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def save_user(username, password):
    hashed_password = hash_password(password)
    with open("users.txt", "a") as f:
        f.write(f"{username},{hashed_password}\n")

def user_exists(username):
    if not os.path.exists("users.txt"):
        return False
    with open("users.txt", "r") as f:
        for line in f:
            stored_username, _ = line.strip().split(",")
            if stored_username == username:
                return True
    return False

def register():
    username = entry_username.get()
    password = entry_password.get()
    confirm = entry_confirm.get()
    
    if not username or not password or not confirm:
        messagebox.showerror("Error", "All fields are required.")
        return

    if password != confirm:
        messagebox.showerror("Error", "Passwords do not match.")
        return

    if user_exists(username):
        messagebox.showerror("Error", "Username already exists!")
    else:
        save_user(username, password)
        messagebox.showinfo("Success", "User registered successfully!")

def log_in():
    username = entry_username.get()
    password = entry_password.get()
    
    if not username or not password:
        messagebox.showerror("Error", "All fields are required.")
        return

    hashed_password = hash_password(password)
    if not os.path.exists("users.txt"):
        messagebox.showerror("Error", "No users registered.")
        return

    with open("users.txt", "r") as f:
        for line in f:
            stored_username, stored_hashed_password = line.strip().split(",")
            if stored_username == username and stored_hashed_password == hashed_password:
                messagebox.showinfo("Success", "Login successful!")
                return
    messagebox.showerror("Error", "Invalid username or password.")

def clear_entries():
    entry_username.delete(0, tk.END)
    entry_password.delete(0, tk.END)
    entry_confirm.delete(0, tk.END)
    
root = tk.Tk()
root.title("User Registration and Login")
root.geometry("300x250")

tk.Label(root, text="Username:").pack(pady=5)
entry_username = tk.Entry(root)
entry_username.pack(pady=5)

tk.Label(root, text="Password:").pack(pady=5)
entry_password = tk.Entry(root, show="*")
entry_password.pack(pady=5)

tk.Label(root, text="Confirm Password:").pack(pady=5)
entry_confirm = tk.Entry(root, show="*")
entry_confirm.pack(pady=5)

tk.Button(root, text="Clear", command=clear_entries).pack(pady=5)

tk.Button(root, text="Register", command=register).pack(pady=10)
tk.Button(root, text="Log In", command=log_in).pack(pady=5)

root.mainloop()