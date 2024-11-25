import random
import os
import tkinter as tk
from tkinter import messagebox
 
 
from PIL import Image, ImageTk
 
# File paths for saving data
USER_DATA_FILE = "users.txt"
TRANSACTION_HISTORY_FILE = "transactions.txt"
bg_path = r"C:\Users\Brainwave11\Pictures\Kwakho\images\bank.png"
 
 
# File paths for saving data
user_data_file = "users.txt"
transaction_history_file = "transactions.txt"
 
# Generate a random account number
def generate_account_number():
    return random.randint(1000000000, 9999999999)
 
# Class for the BankingApp
class BankingApp:
    def __init__(self):
        self.users = self.load_users()  # Load all users from the file
        self.logged_in_user = None
 
    def load_users(self):
        """Load users from the user data file"""
        users = []
        try:
            if os.path.exists(user_data_file):
                with open(user_data_file, 'r') as file:
                    for line in file:
                        parts = line.strip().split(',')
                        if len(parts) == 5:
                            user_id, password, name, account_number, balance = parts
                            users.append({
                                'user_id': user_id,
                                'password': password,
                                'name': name,
                                'account_number': account_number,
                                'balance': float(balance)
                            })
        except FileNotFoundError:
            print("Error: users.txt not found.")
        return users
 
    def save_user(self, user):
        """Save a single user to the file"""
        with open(user_data_file, "a") as file:
            file.write(f"{user['user_id']},{user['password']},{user['name']},{user['account_number']},{user['balance']}\n")
 
    def create_account(self, name, surname, phone, identification, password):
        """Create a new account"""
        if any(user['user_id'] == name for user in self.users):
            return False, "User with this ID already exists."
 
        account_number = str(generate_account_number())
        initial_balance = 0.0
 
        new_user = {
            "user_id": identification,
            "password": password,
            "name": name,
            "account_number": account_number,
            "balance": initial_balance
        }
        self.users.append(new_user)
        self.save_user(new_user)
        return True, f"Account created successfully! Your account number is {account_number}."
 
    def login(self, user_id, password):
        """User login"""
        user = next((u for u in self.users if u['user_id'] == user_id), None)
        if user and user['password'] == password:
            self.logged_in_user = user
            return True, f"Login successful! Welcome, {user['name']}."
        else:
            return False, "Invalid login credentials."
 
    def deposit(self, amount):
        """Deposit funds into the account"""
        if not self.logged_in_user:
            return False, "Please login first."
 
        if amount <= 0:
            return False, "Amount should be greater than 0."
 
        self.logged_in_user["balance"] += amount
        self.save_transaction("Deposit", amount)
        return True, f"Deposited {amount}. Your new balance is: {self.logged_in_user['balance']}."
 
    def withdraw(self, amount):
        """Withdraw funds from the account"""
        if not self.logged_in_user:
            return False, "Please login first."
 
        if amount <= 0:
            return False, "Amount should be greater than 0."
 
        if amount > self.logged_in_user["balance"]:
            return False, "Insufficient funds."
 
        self.logged_in_user["balance"] -= amount
        self.save_transaction("Withdrawal", amount)
        return True, f"Withdrew {amount}. Your new balance is: {self.logged_in_user['balance']}."
 
    def transfer(self, recipient_id, amount):
        """Transfer funds to another account"""
        if not self.logged_in_user:
            return False, "Please login first."
 
        if recipient_id == self.logged_in_user['account_number']:
            return False, "You cannot transfer funds to your own account."
 
        recipient = self.find_user_by_account_number(recipient_id)
        if not recipient:
            return False, "Recipient account not found."
 
        if amount <= 0:
            return False, "The transfer amount must be greater than zero."
 
        if amount > self.logged_in_user["balance"]:
            return False, "Insufficient funds."
 
        self.logged_in_user["balance"] -= amount
        recipient["balance"] += amount
        self.save_transaction("Transfer", amount, recipient_id)
 
        return True, f"Transferred {amount} to {recipient['name']}. Your new balance is: {self.logged_in_user['balance']}."
    
 
    def find_user_by_account_number(self, account_number):
        """Find user by account number"""
        for user in self.users:
            if user['account_number'] == account_number:
                return user
        return None
 
    def save_transaction(self, transaction_type, amount, recipient_id=None):
        """Save transaction details to the transaction history"""
        with open(transaction_history_file, "a") as file:
            file.write(f"{self.logged_in_user['account_number']},{transaction_type},{amount},{recipient_id or 'N/A'},{self.logged_in_user['balance']}\n")
 
    def show_balance(self):
        """Show current account balance"""
        if not self.logged_in_user:
            return False, "Please login first."
 
        return True, f"Your current balance is: {self.logged_in_user['balance']}."
 
    def show_transaction_history(self):
        """Show transaction history"""
        if not self.logged_in_user:
            return False, "Please login first."
 
        history = []
        if os.path.exists(transaction_history_file):
            with open(transaction_history_file, "r") as file:
                lines = file.readlines()
                for line in lines:
                    transaction = line.strip().split(",")
                    if transaction[0] == self.logged_in_user['account_number']:
                        history.append({
                            "Type": transaction[1],
                            "Amount": transaction[2],
                            "Recipient": transaction[3],
                            "Balance": transaction[4]
                        })
        if not history:
            return False, "No transactions found."
 
        return True, history
 
 
class BankingAppUI:
 
    def __init__(self, banking_app):
        self.banking_app = banking_app
        self.root = tk.Tk()
        self.root.title("Banking App")
 
        # Set background color for the entire window to light blue
        self.root.configure(bg='lightblue')
 
        # Main Menu
        self.main_menu()
        self.root.mainloop()
 
       
    def setup_background(self):
        """Set up the background image."""
     
        bg_path = r"C:\Users\Brainwave11\Pictures\Kwakho\images\bank.png"
        try:
            if os.path.exists(bg_path):
                bg_img = Image.open(bg_path)
                bg_img = bg_img.resize((800, 600), Image.LANCZOS)
                self.bg_image = ImageTk.PhotoImage(bg_img)
 
                self.bg_label = tk.Label(self.root, image=self.bg_image)
                self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except FileNotFoundError:
            print("Background image not found. Defaulting to plain background.")
            self.bg_label = None
 
    def main_menu(self):
        self.clear_window()
 
        # Create a container with a phone-like appearance (frame inside remains white)
        container = tk.Frame(self.root, bg="#ffffff", bd=0, relief="solid", width=500, height=600)
        container.pack_propagate(False)
        container.pack(pady=80)
 
        # Label to represent phone screen title
        tk.Label(container, text="Welcome to the Banking App", font=("Arial", 16), bg="white").pack(pady=10)
 
 
 
 
 
        # Create a frame for the buttons to manage their layout
        button_frame = tk.Frame(container, bg='white')
        button_frame.pack(pady=20)
 
        button_width = 15
 
        # Create buttons
        tk.Button(button_frame, text="Create Account", command=self.create_account_ui, width=button_width, height=3, bg="lightblue", fg="white").grid(row=0, column=0, padx=10)
        tk.Button(button_frame, text="Login", command=self.login_ui, width=button_width, height=3, bg="lightblue", fg="white").grid(row=0, column=1, padx=10)
        tk.Button(button_frame, text="Exit", command=self.root.quit, width=button_width, height=3, bg="lightblue", fg="white").grid(row=1, column=0, columnspan=2, pady=10)
 

    def create_account_ui(self):
        self.clear_window()
 
        container = tk.Frame(self.root, bg="#ffffff", bd=0, relief="solid", width=500, height=700)
        container.pack_propagate(False)
        container.pack(pady=80)
 
        tk.Label(container, text="Create Account", font=("Arial", 16), bg="white").pack(pady=10)
 
        input_frame = tk.Frame(container, bg="white")
        input_frame.pack(pady=10)
 
        # Create account fields
        self.create_input_field(input_frame, "First Name:", 1)
        self.create_input_field(input_frame, "Last Name:", 2)
        self.create_input_field(input_frame, "Phone Number:", 3)
        self.create_input_field(input_frame, "User ID (ID Number):", 4)
        self.create_input_field(input_frame, "Password:", 5, show="*")
 
        def create_account():
            name = self.get_input(1)
            surname = self.get_input(2)
            phone = self.get_input(3)
            identification = self.get_input(4)
            password = self.get_input(5)
 
            success, message = self.banking_app.create_account(name, surname, phone, identification, password)
            self.show_message(success, message)
 
        submit_button = tk.Button(container, text="Submit", command=create_account, width=15, height=2, bg="lightblue", fg="white")
        submit_button.pack(pady=20)
 
        # Back to main menu button
        back_button = tk.Button(container, text="Back", command=self.main_menu, width=15, height=2, bg="lightblue", fg="white")
        back_button.pack()
 
 
    def login_ui(self):
        self.clear_window()
 
        # Create a container with a phone-like appearance (frame inside remains white)
        container = tk.Frame(self.root, bg="#ffffff", bd=0, relief="solid", width=500, height=600)  # Removed border and widened width
        container.pack_propagate(False)
        container.pack(pady=80)  # Adjusted vertical padding
 
        # Label to represent phone screen title
        tk.Label(container, text="Login", font=("Arial", 16), bg="white").pack(pady=10)
 
        # Create a frame for the input fields
        input_frame = tk.Frame(container, bg="white")
        input_frame.pack(pady=10)
 
        self.create_input_field(input_frame, "Username:", 1)
        self.create_input_field(input_frame, "Password:", 2, show="*")
 
        def login():
            identification = self.get_input(1)
            password = self.get_input(2)
 
            if not identification or not password:
                messagebox.showerror("Error", "Both fields are required.")
                return
 
            success, message = self.banking_app.login(identification, password)
            if success:
                messagebox.showinfo("Success", message)
                self.dashboard_ui()
            else:
                messagebox.showerror("Login Failed", message)
 
        # Create horizontal buttons for submit and back
        button_frame = tk.Frame(container, bg="white")
        button_frame.pack(pady=10)
 
        tk.Button(button_frame, text="Login", command=login, bg="lightblue", fg="white", width=15, height=3).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="Back", command=self.main_menu, bg="lightblue", fg="white", width=15, height=3).grid(row=0, column=1, padx=5)
 
 
    def dashboard_ui(self):
        self.clear_window()
 
       
        container = tk.Frame(self.root, bg="#ffffff", bd=0, relief="solid", width=500, height=600)
        container.pack_propagate(False)
        container.pack(pady=80)
 
        # Show the user info on the dashboard
        tk.Label(container, text=f"Welcome {self.banking_app.logged_in_user['name']}", font=("Arial", 16), bg="white").pack(pady=10)
 
        balance_label = tk.Label(container, text=f"Balance: R{self.banking_app.logged_in_user['balance']:.2f}", font=("Arial", 14), bg="white")
        balance_label.pack(pady=5)
       
        button_frame = tk.Frame(container, bg='white')
        button_frame.pack(pady=20)
 
        # Dashboard Buttons
        tk.Button(button_frame, text="Transaction History", command=self.show_transaction_history_ui, width=15, height=3, bg="lightblue", fg="white").grid(row=0, column=0, padx=10, pady=10)
        tk.Button(button_frame, text="Deposit", command=self.deposit, width=15, height=3, bg="lightblue", fg="white").grid(row=0, column=1, padx=10, pady=10)
        tk.Button(button_frame, text="Withdraw", command=self.withdraw, width=15, height=3, bg="lightblue", fg="white").grid(row=1, column=0, padx=10, pady=10)
        tk.Button(button_frame, text="Transfer", command=self.transfer, width=15, height=3, bg="lightblue", fg="white").grid(row=1, column=1, padx=10, pady=10)
 
        tk.Button(button_frame, text="Logout", command=self.main_menu, width=15, height=3, bg="lightblue", fg="white").grid(row=2, column=0, columnspan=2, pady=10)
 
    def view_balance(self):
        success, message = self.banking_app.show_balance()
        self.show_message(success, message)
 
    def deposit(self):
        self.clear_window()
 
        container = tk.Frame(self.root, bg="#ffffff", bd=0, relief="solid", width=500, height=600)
        container.pack_propagate(False)
        container.pack(pady=80)
 
        tk.Label(container, text="Deposit", font=("Arial", 16), bg="white").pack(pady=10)
 
        input_frame = tk.Frame(container, bg="white")
        input_frame.pack(pady=10)
 
        self.create_input_field(input_frame, "Deposit Amount:", 1)
 
        def submit_deposit():
            amount = float(self.get_input(1))
            success, message = self.banking_app.deposit(amount)
            self.show_message(success, message)
 
        deposit_button = tk.Button(container, text="Deposit", command=submit_deposit, width=15, height=2, bg="lightblue", fg="white")
        deposit_button.pack(pady=20)
 
        back_button = tk.Button(container, text="Back", command=self.dashboard_ui, width=15, height=2, bg="lightblue", fg="white")
        back_button.pack()
 
    def withdraw(self):
        self.clear_window()
 
        container = tk.Frame(self.root, bg="#ffffff", bd=0, relief="solid", width=500, height=600)
        container.pack_propagate(False)
        container.pack(pady=80)
 
        tk.Label(container, text="Withdraw", font=("Arial", 16), bg="white").pack(pady=10)
 
        input_frame = tk.Frame(container, bg="white")
        input_frame.pack(pady=10)
 
        self.create_input_field(input_frame, "Withdraw Amount:", 1)
 
        def submit_withdrawal():
            amount = float(self.get_input(1))
            success, message = self.banking_app.withdraw(amount)
            self.show_message(success, message)
 
        withdraw_button = tk.Button(container, text="Withdraw", command=submit_withdrawal, width=15, height=2, bg="lightblue", fg="white")
        withdraw_button.pack(pady=20)
 
        back_button = tk.Button(container, text="Back", command=self.dashboard_ui, width=15, height=2, bg="lightblue", fg="white")
        back_button.pack()
 
    def transfer(self):
        self.clear_window()
 
        container = tk.Frame(self.root, bg="#ffffff", bd=0, relief="solid", width=500, height=600)
        container.pack_propagate(False)
        container.pack(pady=80)
 
        tk.Label(container, text="Transfer Funds", font=("Arial", 16), bg="white").pack(pady=10)
 
        input_frame = tk.Frame(container, bg="white")
        input_frame.pack(pady=10)
 
        self.create_input_field(input_frame, "Recipient Account Number:", 1)
        self.create_input_field(input_frame, "Transfer Amount:", 2)
 
        def submit_transfer():
            recipient_account = self.get_input(1)
            amount = float(self.get_input(2))
            success, message = self.banking_app.transfer(recipient_account, amount)
            self.show_message(success, message)
 
        transfer_button = tk.Button(container, text="Transfer", command=submit_transfer, width=15, height=2, bg="lightblue", fg="white")
        transfer_button.pack(pady=20)
 
        back_button = tk.Button(container, text="Back", command=self.dashboard_ui, width=15, height=2, bg="lightblue", fg="white")
        back_button.pack
 
        # Back to main menu button
        back_button = tk.Button(container, text="Back", command=self.main_menu, width=15, height=2, bg="lightblue", fg="white")
        back_button.pack()
    def create_input_field(self, parent_frame, label_text, row, show=None):
        label = tk.Label(parent_frame, text=label_text, bg="white")
        label.grid(row=row, column=0, padx=10, pady=5, sticky="e")
 
        entry = tk.Entry(parent_frame, show=show if show else None, width=30)
        entry.grid(row=row, column=1, padx=10, pady=5)
 
        setattr(self, f"entry_{row}", entry)  # Save entry as a class attribute
 
    def get_input(self, row):
        return getattr(self, f"entry_{row}").get()
 
    def show_message(self, success, message):
        messagebox.showinfo("Result", message) if success else messagebox.showerror("Error", message)
 
    def show_transaction_history_ui(self):
        success, transaction_history = self.banking_app.show_transaction_history()
        if success:
            transaction_str = "\n".join([f"{t['Type']} - {t['Amount']} (Balance: {t['Balance']})" for t in transaction_history])
            messagebox.showinfo("Transaction History", transaction_str)
        else:
            messagebox.showerror("Error", transaction_history)
 
 
    def clear_window(self):
        """Clear the window before loading a new UI."""
        for widget in self.root.winfo_children():
            widget.destroy()
 
# Create a BankingApp instance and start the UI
app = BankingApp()
ui = BankingAppUI(app)