import tkinter as tk
from tkinter import messagebox, ttk
from controllers.login_system import LoginSystem

class LoginView:
    def __init__(self, root, show_signup_screen_callback):
        self.root = root
        self.show_signup_screen_callback = show_signup_screen_callback
        self.root.title("Login")
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
            messagebox.showerror("Login", "Invalid username or password.")

    def show_admin_view(self):
        # Destroy current widgets (Login form)
        for widget in self.root.winfo_children():
            widget.destroy()

        # Create menu bar for admin view
        menu_bar = tk.Menu(self.root)
        
        # Material Management menu
        material_menu = tk.Menu(menu_bar, tearoff=0)
        material_menu.add_command(label="Upload Material", command=self.upload_material)
        material_menu.add_command(label="Create Material", command=self.create_material)
        material_menu.add_command(label="View Material Report", command=self.view_material_report)
        material_menu.add_command(label="Add Material Type", command=self.add_material_type)
        menu_bar.add_cascade(label="Material Management", menu=material_menu)

        # Vendor Management menu
        vendor_menu = tk.Menu(menu_bar, tearoff=0)
        vendor_menu.add_command(label="Upload Vendor", command=self.upload_vendor)
        vendor_menu.add_command(label="Add Vendor", command=self.create_vendor)
        vendor_menu.add_command(label="Vendor Report", command=self.view_vendor_report)
        menu_bar.add_cascade(label="Vendor Management", menu=vendor_menu)

        # Stock Management menu
        stock_menu = tk.Menu(menu_bar, tearoff=0)
        stock_menu.add_command(label="Upload Stock", command=self.upload_stock)
        stock_menu.add_command(label="Update Stock", command=self.update_stock)
        stock_menu.add_command(label="Stock Report", command=self.view_stock_report)
        menu_bar.add_cascade(label="Stock Management", menu=stock_menu)

        # Order Management menu
        order_menu = tk.Menu(menu_bar, tearoff=0)
        order_menu.add_command(label="Manage Orders", command=self.manage_orders)
        order_menu.add_command(label="Order Report", command=self.view_order_report)
        menu_bar.add_cascade(label="Order Management", menu=order_menu)

        # User Management menu
        user_menu = tk.Menu(menu_bar, tearoff=0)
        user_menu.add_command(label="View User", command=self.view_user)
        user_menu.add_command(label="User Management", command=self.manage_users)
        menu_bar.add_cascade(label="User Management", menu=user_menu)

        # Configure the menu bar
        self.root.config(menu=menu_bar)

        # Admin Dashboard Content
        admin_frame = ttk.Frame(self.root, padding="20")
        admin_frame.pack(padx=20, pady=30)

        ttk.Label(admin_frame, text="Admin Dashboard", font=("Helvetica", 18, "bold"), foreground="#4CAF50").grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Example buttons for Admin actions
        ttk.Button(admin_frame, text="Manage Users", width=20).grid(row=1, column=0, pady=10)
        ttk.Button(admin_frame, text="Manage Orders", width=20).grid(row=2, column=0, pady=10)
        ttk.Button(admin_frame, text="View Reports", width=20).grid(row=3, column=0, pady=10)
        ttk.Button(admin_frame, text="Logout", width=20, command=self.logout).grid(row=4, column=0, pady=10)

    def logout(self):
        # Clear current admin view and show login screen
        for widget in self.root.winfo_children():
            widget.destroy()
        self.create_login_form()  # Go back to login screen

    # Example placeholder functions for menu commands
    def upload_material(self):
        pass

    def create_material(self):
        pass

    def view_material_report(self):
        pass

    def add_material_type(self):
        pass

    def upload_vendor(self):
        pass

    def create_vendor(self):
        pass

    def view_vendor_report(self):
        pass

    def upload_stock(self):
        pass

    def update_stock(self):
        pass

    def view_stock_report(self):
        pass

    def manage_orders(self):
        pass

    def view_order_report(self):
        pass

    def view_user(self):
        pass

    def manage_users(self):
        pass
