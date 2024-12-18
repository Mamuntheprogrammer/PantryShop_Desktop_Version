import tkinter as tk
from tkinter import messagebox, ttk
from controllers.login_manager import LoginManager
from .loader import Loader  # Import the Loader

class LoginView:
    def __init__(self, root, show_signup_screen_callback):
        self.root = root
        self.loader = Loader(root)  # Initialize the Loader
        self.show_signup_screen_callback = show_signup_screen_callback
        self.root.title("Food Pantry Management System")
        self.root.geometry("1150x675")
        self.root.config(bg="#f4f4f4")

        self.create_login_form()

    def create_login_form(self):
        # Frame for the login form
        form_frame = ttk.Frame(self.root, padding="20")
        form_frame.pack(padx=20, pady=30)

        # Title Label
        ttk.Label(form_frame, text="Login", font=("Helvetica", 18, "bold"), foreground="#4CAF50").grid(row=0, column=0, columnspan=3, pady=(0, 20))

        # email and Password input
        ttk.Label(form_frame, text="Email:", font=("Helvetica", 12)).grid(row=1, column=0, sticky="w", pady=5)
        self.email_entry = ttk.Entry(form_frame, width=30, font=("Helvetica", 12))
        self.email_entry.grid(row=1, column=1, columnspan=2, pady=5)

        ttk.Label(form_frame, text="Password:", font=("Helvetica", 12)).grid(row=2, column=0, sticky="w", pady=5)
        self.password_entry = ttk.Entry(form_frame, width=30, font=("Helvetica", 12), show="*")
        self.password_entry.grid(row=2, column=1, columnspan=2, pady=5)

        # Login and Sign Up Buttons
        login_button = ttk.Button(form_frame, text="Login", width=10, command=self.handle_login)
        login_button.grid(row=4, column=1, sticky="e", padx=(0, 5), pady=(20, 0))

        signup_button = ttk.Button(form_frame, text="Sign Up", width=10, command=self.show_signup_screen_callback)
        signup_button.grid(row=4, column=2, sticky="w", padx=(5, 0), pady=(20, 0))

        exit_button = ttk.Button(form_frame, text="Exit", width=20, command=self.root.quit)
        exit_button.grid(row=5, column=1, columnspan=2, pady=(20, 0))


    def handle_login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        # print(email,password)

        # Create an instance of LoginManager with email and password
        login_manager = LoginManager(email, password)

        # Call the authenticate method
        user_role = login_manager.authenticate()
        # print(user_role)

        if user_role == "Admin":
            messagebox.showinfo("Login", "Login successful!")
            self.loader.show()  # Show loader
            self.root.after(2000, self.show_admin_view)  # Simulate delay for loading
            # self.show_admin_view()  # Navigate to admin view
        elif user_role == "User":
            messagebox.showinfo("Login", "Login successful!")
            self.show_user_view()  # Navigate to admin view
        # else:
        #     print("Invalid credentials.")



    def show_admin_view(self):
        # Destroy current widgets (Login form)
        self.clear_all_widgets()

        from .admin_view_2 import AdminView
        AdminView(self.root, self.logout)

    def show_user_view(self):
        # Destroy current widgets (Login form)
        self.clear_all_widgets()

        from .user_view_2 import UserView
        UserView(self.root, self.logout)

    def logout(self):
        # Clear all widgets and menus from the admin or user view
        self.clear_all_widgets()
        # Display the login screen again
        self.create_login_form()

    def clear_all_widgets(self):
        """Clears all widgets, including menus, from the root window."""
        for widget in self.root.winfo_children():
            widget.destroy()
        self.root.config(menu=None)  # Clear any leftover menu bars
