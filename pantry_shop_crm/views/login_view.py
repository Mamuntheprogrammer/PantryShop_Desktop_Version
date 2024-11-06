 
import tkinter as tk
from tkinter import messagebox
from controllers.login_system import LoginSystem

class LoginView:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("400x300")
        
        self.create_login_form()

    def create_login_form(self):
        # Username label and input
        tk.Label(self.root, text="Username:").pack(pady=10)
        self.username_entry = tk.Entry(self.root, width=30)
        self.username_entry.pack(pady=5)

        # Password label and input
        tk.Label(self.root, text="Password:").pack(pady=10)
        self.password_entry = tk.Entry(self.root, width=30, show="*")
        self.password_entry.pack(pady=5)

        # Login Button
        login_button = tk.Button(self.root, text="Login", width=20, command=self.handle_login)
        login_button.pack(pady=20)

    def handle_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        login_system = LoginSystem(username, password)
        if login_system.authenticate():
            messagebox.showinfo("Login", "Login successful!")
            self.root.destroy()  # Close login window
            # Open the main dashboard window here (not implemented in this snippet)
        else:
            messagebox.showerror("Login", "Invalid username or password.")

