import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
from datetime import datetime

# --- DATABASE SETUP ---
conn = sqlite3.connect("pos_system.db")
cursor = conn.cursor()

# Create tables
cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS products(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE,
    price REAL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS sales(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name TEXT,
    quantity INTEGER,
    total REAL,
    date TEXT
)
""")

# Add default admin account if none
cursor.execute("SELECT * FROM users WHERE username='admin'")
if not cursor.fetchone():
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", ("admin", "1234"))
    conn.commit()


# --- HELPER FUNCTIONS ---
def get_products():
    cursor.execute("SELECT name, price FROM products")
    return dict(cursor.fetchall())


def add_default_products():
    cursor.execute("SELECT COUNT(*) FROM products")
    if cursor.fetchone()[0] == 0:
        items = [
            ("Bread", 60),
            ("Milk", 50),
            ("Sugar", 120),
            ("Rice", 200),
            ("Tea Leaves", 90),
            ("Cooking Oil", 350)
        ]
        cursor.executemany("INSERT OR IGNORE INTO products (name, price) VALUES (?, ?)", items)
        conn.commit()


add_default_products()


# --- LOGIN SCREEN ---
def login_screen():
    def login_user():
        user = entry_user.get()
        pwd = entry_pass.get()

        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (user, pwd))
        if cursor.fetchone():
            messagebox.showinfo("Success", f"Welcome {user}!")
            login.destroy()
            main_admin_panel()
        else:
            messagebox.showerror("Error", "Invalid credentials")

    login = tk.Tk()
    login.title("Admin Login")
    login.geometry("300x200")

    tk.Label(login, text="Username").pack(pady=5)
    entry_user = tk.Entry(login)
    entry_user.pack()

    tk.Label(login, text="Password").pack(pady=5)
    entry_pass = tk.Entry(login, show="*")
    entry_pass.pack()

    tk.Button(login, text="Login", command=login_user, bg="#4CAF50", fg="white").pack(pady=10)

    login.mainloop()


# --- ADMIN DASHBOARD ---
def main_admin_panel():
    def open_pos_window():
        admin.destroy()
        main_pos_window()

    def open_product_manager():
        product_manager_window()

    def open_sales_report():
        sales_report_window()

    admin = tk.Tk()
    admin.title("Admin Dashboard")
    admin.geometry("300x250")

    tk.Label(admin, text="🏪 Python POS - Admin Panel", font=("Arial", 12, "bold")).pack(pady=10)

    tk.Button(admin, text="🛍 Open POS (Sales Window)", width=25, bg="#2196F3", fg="white",
              command=open_pos_window).pack(pady=5)

    tk.Button(admin, text="📦 Manage Products", width=25, bg="#4CAF50", fg="white",
              command=open_product_manager).pack(pady=5)

    tk.Button(admin, text="📊 View Sales Report", width=25, bg="#9C27B0", fg="white",
              command=open_sales_report).pack(pady=5)

    tk.Button(admin, text="Exit", width=25, bg="#f44336", fg="white", command=admin.destroy).pack(pady=10)

    admin.mainloop()


# --- PRODUCT MANAGEMENT WINDOW ---
def product_manager_window():
    def refresh_table():
        for row in tree.get_children():
            tree.delete(row)
        cursor.execute("SELECT id, name, price FROM products")
        for prod in cursor.fetchall():
            tree.insert("", tk.END, values=prod)

    def add_product():
        name = name_var.get().strip()
        try:
            price = float(price_var.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid price")
            return

        if not name:
            messagebox.showerror("Error", "Product name required")
            return

        try:
            cursor.execute("INSERT INTO products (name, price) VALUES (?, ?)", (name, price))
            conn.commit()
            refresh_table()
            messagebox.showinfo("Success", f"Product '{name}' added!")
            name_var.set("")
            price_var.set("")
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Product already exists")

    def delete_product():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select a product to delete")
            return
        item = tree.item(selected[0])["values"]
        prod_id = item[0]
        cursor.execute("DELETE FROM products WHERE id=?", (prod_id,))
        conn.commit()
        refresh_table()
        messagebox.showinfo("Deleted", f"Deleted product ID {prod_id}")

    win = tk.Toplevel()
    win.title("📦 Manage Products")
    win.geometry("500x400")

    tk.Label(win, text="Add New Product", font=("Arial", 11, "bold")).pack(pady=5)
    frame = tk.Frame(win)
    frame.pack()

    tk.Label(frame, text="Name").grid(row=0, column=0, padx=5, pady=5)
    name_var = tk.StringVar()
    tk.Entry(frame, textvariable=name_var).grid(row=0, column=1, padx=5)

    tk.Label(frame, text="Price (Ksh)").grid(row=1, column=0, padx=5)
    price_var = tk.StringVar()
    tk.Entry(frame, textvariable=price_var).grid(row=1, column=1, padx=5)

    tk.Button(frame, text="Add Product", command=add_product, bg="#4CAF50", fg="white").grid(row=2, column=0, columnspan=2, pady=10)

    # Product table
    columns = ("ID", "Name", "Price")
    tree = ttk.Treeview(win, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=120)
    tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    tk.Button(win, text="Remove Selected Product", command=delete_product, bg="#f44336", fg="white").pack(pady=5)
    refresh_table()


# --- POS WINDOW ---
def main_pos_window():
    products = get_products()
    cart = {}

    def add_to_cart():
        item = product_var.get()
        qty = qty_var.get()
        if qty <= 0:
            messagebox.showerror("Error", "Quantity must be greater than 0")
            return
        cart[item] = cart.get(item, 0) + qty
        update_cart_display()

    def update_cart_display():
        text_cart.delete(1.0, tk.END)
        total = 0
        for p, q in cart.items():
            price = products[p] * q
            total += price
            text_cart.insert(tk.END, f"{p} x{q} = Ksh {price}\n")
        label_total.config(text=f"Total: Ksh {total}")
        return total

    def process_payment():
        if not cart:
            messagebox.showerror("Error", "No items in cart")
            return

        total = update_cart_display()
        paid = paid_var.get()

        if paid < total:
            messagebox.showerror("Error", "Insufficient payment")
            return

        balance = paid - total

        # Record sale in DB
        for p, q in cart.items():
            cursor.execute("INSERT INTO sales (product_name, quantity, total, date) VALUES (?, ?, ?, ?)",
                           (p, q, products[p] * q, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        conn.commit()

        show_receipt(total, paid, balance)
        cart.clear()
        update_cart_display()

    def show_receipt(total, paid, balance):
        receipt = tk.Toplevel(pos)
        receipt.title("Receipt")
        text = tk.Text(receipt, width=40, height=20)
        text.pack(padx=10, pady=10)
        text.insert(tk.END, "    PYTHON POS RECEIPT\n")
        text.insert(tk.END, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        text.insert(tk.END, "-"*35 + "\n")
        for p, q in cart.items():
            price = products[p] * q
            text.insert(tk.END, f"{p:<15} x{q:<3} = {price}\n")
        text.insert(tk.END, "-"*35 + "\n")
        text.insert(tk.END, f"Total: {total}\nPaid: {paid}\nBalance: {balance}\n")
        text.insert(tk.END, "\nThank you!\n")
        tk.Button(receipt, text="Close", command=receipt.destroy).pack(pady=5)

    pos = tk.Toplevel()
    pos.title("🧾 Python POS Machine")
    pos.geometry("500x550")

    products = get_products()

    tk.Label(pos, text="Select Product").pack(pady=5)
    product_var = tk.StringVar(value=list(products.keys())[0])
    tk.OptionMenu(pos, product_var, *products.keys()).pack()

    tk.Label(pos, text="Quantity").pack(pady=5)
    qty_var = tk.IntVar(value=1)
    tk.Entry(pos, textvariable=qty_var, width=10).pack()

    tk.Button(pos, text="Add to Cart", command=add_to_cart, bg="#4CAF50", fg="white").pack(pady=5)

    text_cart = tk.Text(pos, width=40, height=10)
    text_cart.pack()

    label_total = tk.Label(pos, text="Total: Ksh 0", font=("Arial", 12, "bold"))
    label_total.pack(pady=5)

    tk.Label(pos, text="Amount Paid").pack()
    paid_var = tk.DoubleVar(value=0)
    tk.Entry(pos, textvariable=paid_var, width=15).pack()

    tk.Button(pos, text="Process Payment", command=process_payment, bg="#2196F3", fg="white").pack(pady=10)

    tk.Button(pos, text="View Sales Report", command=sales_report_window, bg="#9C27B0", fg="white").pack(pady=5)


# --- SALES REPORT WINDOW ---
def sales_report_window():
    report = tk.Toplevel()
    report.title("📊 Sales Report")
    report.geometry("500x300")

    tree = ttk.Treeview(report, columns=("Product", "Qty", "Total", "Date"), show="headings")
    for col in ("Product", "Qty", "Total", "Date"):
        tree.heading(col, text=col)
        tree.column(col, width=100)
    tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    cursor.execute("SELECT product_name, quantity, total, date FROM sales")
    for row in cursor.fetchall():
        tree.insert("", tk.END, values=row)


# --- RUN PROGRAM ---
login_screen()