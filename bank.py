import tkinter as tk
from tkinter import messagebox
import sqlite3

# Database setup
def init_db():
    conn = sqlite3.connect("bank.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL,
            balance REAL DEFAULT 0.0
        )
    """)
    conn.commit()
    conn.close()

# Register user
def register_user(username, password):
    try:
        conn = sqlite3.connect("bank.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False

# Login user
def login_user(username, password):
    conn = sqlite3.connect("bank.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user

# Update balance
def update_balance(username, amount):
    conn = sqlite3.connect("bank.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET balance = balance + ? WHERE username = ?", (amount, username))
    conn.commit()
    conn.close()

# Get balance
def get_balance(username):
    conn = sqlite3.connect("bank.db")
    cursor = conn.cursor()
    cursor.execute("SELECT balance FROM users WHERE username = ?", (username,))
    balance = cursor.fetchone()[0]
    conn.close()
    return balance

# GUI Functions
def login():
    username = entry_username.get()
    password = entry_password.get()

    if login_user(username, password):
        messagebox.showinfo("Login Success", f"Welcome {username}!")
        open_dashboard(username)
    else:
        messagebox.showerror("Login Failed", "Invalid username or password.")

def register():
    username = entry_username.get()
    password = entry_password.get()

    if register_user(username, password):
        messagebox.showinfo("Registration Success", "You have registered successfully!")
    else:
        messagebox.showerror("Registration Failed", "Username already exists.")

def deposit(username):
    amount = float(entry_amount.get())
    update_balance(username, amount)
    messagebox.showinfo("Deposit Success", f"Deposited {amount} successfully.")
    refresh_balance(username)

def withdraw(username):
    amount = float(entry_amount.get())
    balance = get_balance(username)

    if amount > balance:
        messagebox.showerror("Withdraw Failed", "Insufficient balance.")
    else:
        update_balance(username, -amount)
        messagebox.showinfo("Withdraw Success", f"Withdrawn {amount} successfully.")
        refresh_balance(username)

def refresh_balance(username):
    balance = get_balance(username)
    label_balance.config(text=f"Balance: {balance}")

def open_dashboard(username):
    dashboard = tk.Toplevel(root)
    dashboard.title("Dashboard")

    global label_balance, entry_amount

    tk.Label(dashboard, text=f"Welcome, {username}", font=("Arial", 16)).pack(pady=10)

    balance = get_balance(username)
    label_balance = tk.Label(dashboard, text=f"Balance: {balance}", font=("Arial", 14))
    label_balance.pack(pady=10)

    tk.Label(dashboard, text="Amount:").pack()
    entry_amount = tk.Entry(dashboard)
    entry_amount.pack(pady=5)

    tk.Button(dashboard, text="Deposit", command=lambda: deposit(username)).pack(pady=5)
    tk.Button(dashboard, text="Withdraw", command=lambda: withdraw(username)).pack(pady=5)

# Main Application
init_db()

root = tk.Tk()
root.title("Bank Transaction Management")

# Login/Register Frame
tk.Label(root, text="Bank Management System", font=("Arial", 18)).pack(pady=10)

frame = tk.Frame(root)
frame.pack(pady=20)

# Username
entry_username = tk.Entry(frame, width=30)
entry_username.grid(row=0, column=1, padx=10, pady=5)
tk.Label(frame, text="Username:").grid(row=0, column=0)

# Password
entry_password = tk.Entry(frame, width=30, show="*")
entry_password.grid(row=1, column=1, padx=10, pady=5)
tk.Label(frame, text="Password:").grid(row=1, column=0)

# Buttons
tk.Button(frame, text="Login", command=login).grid(row=2, column=0, pady=10)
tk.Button(frame, text="Register", command=register).grid(row=2, column=1, pady=10)

root.mainloop()
