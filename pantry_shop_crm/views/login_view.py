import tkinter as tk
from tkinter import messagebox, ttk
from controllers.login_system import LoginSystem

class LoginView:
    def __init__(self, root, show_signup_screen_callback):
        self.root = root
        self.show_signup_screen_callback = show_signup_screen_callback
        self.root.title("Food Pantry Management System")
        self.root.geometry("900x600")
        self.root.config(bg="#f4f4f4")

        self.create_login_form()

    def create_login_form(self):
        # Frame for the login form
        form_frame = ttk.Frame(self.root, padding="20")
        form_frame.pack(padx=20, pady=30)

        # Title Label
        ttk.Label(form_frame, text="Login", font=("Helvetica", 18, "bold"), foreground="#4CAF50").grid(row=0, column=0, columnspan=3, pady=(0, 20))

        # Username and Password input
        ttk.Label(form_frame, text="Username:", font=("Helvetica", 12)).grid(row=1, column=0, sticky="w", pady=5)
        self.username_entry = ttk.Entry(form_frame, width=30, font=("Helvetica", 12))
        self.username_entry.grid(row=1, column=1, columnspan=2, pady=5)

        ttk.Label(form_frame, text="Password:", font=("Helvetica", 12)).grid(row=2, column=0, sticky="w", pady=5)
        self.password_entry = ttk.Entry(form_frame, width=30, font=("Helvetica", 12), show="*")
        self.password_entry.grid(row=2, column=1, columnspan=2, pady=5)

        # Login and Sign Up Buttons
        login_button = ttk.Button(form_frame, text="Login", width=10, command=self.handle_login)
        login_button.grid(row=4, column=1, sticky="e", padx=(0, 5), pady=(20, 0))

        signup_button = ttk.Button(form_frame, text="Sign Up", width=10, command=self.show_signup_screen_callback)
        signup_button.grid(row=4, column=2, sticky="w", padx=(5, 0), pady=(20, 0))

        exit_button = tk.Button(form_frame, text="Exit", width=20, height=2, command=self.root.quit)
        exit_button.grid(row=5, column=1, columnspan=3, pady=(20, 0))

    def handle_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        login_system = LoginSystem(username, password)
        if login_system.authenticate():
            messagebox.showinfo("Login", "Login successful!")
            self.show_admin_view()  # Navigate to admin view
        else:
            self.show_user_view()  # Navigate to user view if login as a user
            # Uncomment if you want to show an error on invalid credentials
            # messagebox.showerror("Login", "Invalid username or password.")

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
