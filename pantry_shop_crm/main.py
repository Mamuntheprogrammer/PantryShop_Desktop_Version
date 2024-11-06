import tkinter as tk
from tkinter import messagebox
from models.database import Database  # Import the database setup class

class PantryShopCRMApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pantry Shop CRM")
        self.root.geometry("500x400")
        
        # Initialize the database and create tables if necessary
        self.db = Database()
        
        self.create_menu()

    def create_menu(self):
        # Create menu buttons
        menu_frame = tk.Frame(self.root)
        menu_frame.pack(pady=100)

        # Login Button
        login_button = tk.Button(menu_frame, text="Login", width=20, height=2, command=self.show_login_screen)
        login_button.grid(row=0, column=0, padx=10, pady=10)

        # Exit Button
        exit_button = tk.Button(menu_frame, text="Exit", width=20, height=2, command=self.root.quit)
        exit_button.grid(row=1, column=0, padx=10, pady=10)

    def show_login_screen(self):
        # Hide menu and show login form
        for widget in self.root.winfo_children():
            widget.destroy()

        self.create_login_form()

    def create_login_form(self):
        # Create the login form
        tk.Label(self.root, text="Username:").pack(pady=10)
        self.username_entry = tk.Entry(self.root, width=30)
        self.username_entry.pack(pady=5)

        tk.Label(self.root, text="Password:").pack(pady=10)
        self.password_entry = tk.Entry(self.root, width=30, show="*")
        self.password_entry.pack(pady=5)

        login_button = tk.Button(self.root, text="Login", width=20, command=self.handle_login)
        login_button.pack(pady=20)

    def handle_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Here we call the authentication logic (not shown in this snippet)
        # For now, let's simulate success
        messagebox.showinfo("Login", "Login successful!")
        self.show_dashboard()

    def show_dashboard(self):
        # Hide login screen and show the dashboard or next screen
        for widget in self.root.winfo_children():
            widget.destroy()

        dashboard_label = tk.Label(self.root, text="Welcome to the Dashboard", font=("Arial", 24))
        dashboard_label.pack(pady=100)

# Main execution
if __name__ == "__main__":
    root = tk.Tk()
    app = PantryShopCRMApp(root)
    root.mainloop()
