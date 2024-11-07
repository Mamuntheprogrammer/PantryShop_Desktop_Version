import tkinter as tk
from tkinter import ttk

class AdminView:
    def __init__(self, root):
        self.root = root
        self.root.title("Admin Dashboard")
        self.root.geometry("900x600")
        self.create_admin_menu()  # Setup the menu
        self.create_admin_dashboard()  # Setup the dashboard

    def create_admin_menu(self):
        # Create the menu bar
        menu_bar = tk.Menu(self.root, bg="#333", fg="#FFF", font=("Helvetica", 10))

        # Material Management menu
        material_menu = tk.Menu(menu_bar, tearoff=0, bg="#333", fg="#FFF", activebackground="#002bb2")
        material_menu.add_command(label="Upload Material", command=self.upload_material)
        material_menu.add_separator()
        material_menu.add_command(label="Create Material", command=self.create_material)
        material_menu.add_separator()
        material_menu.add_command(label="View Material Report", command=self.view_material_report)
        material_menu.add_separator()
        material_menu.add_command(label="Add Material Type", command=self.add_material_type)
        menu_bar.add_cascade(label="Material Management", menu=material_menu)

        # Vendor Management menu
        vendor_menu = tk.Menu(menu_bar, tearoff=0, bg="#333", fg="#FFF", activebackground="#002bb2")
        vendor_menu.add_command(label="Upload Vendor", command=self.upload_vendor)
        vendor_menu.add_separator()
        vendor_menu.add_command(label="Add Vendor", command=self.add_vendor)
        vendor_menu.add_separator()
        vendor_menu.add_command(label="Vendor Report", command=self.view_vendor_report)
        menu_bar.add_cascade(label="Vendor Management", menu=vendor_menu)

        # Stock Management menu
        stock_menu = tk.Menu(menu_bar, tearoff=0, bg="#333", fg="#FFF", activebackground="#002bb2")
        stock_menu.add_command(label="Upload Stock", command=self.upload_stock)
        stock_menu.add_separator()
        stock_menu.add_command(label="Update Stock", command=self.update_stock)
        stock_menu.add_separator()
        stock_menu.add_command(label="Stock Report", command=self.view_stock_report)
        menu_bar.add_cascade(label="Stock Management", menu=stock_menu)

        # Order Management menu
        order_menu = tk.Menu(menu_bar, tearoff=0, bg="#333", fg="#FFF", activebackground="#002bb2")
        order_menu.add_command(label="Manage Orders", command=self.manage_orders)
        order_menu.add_separator()
        order_menu.add_command(label="Order Report", command=self.view_order_report)
        menu_bar.add_cascade(label="Order Management", menu=order_menu)

        # User Management menu
        user_menu = tk.Menu(menu_bar, tearoff=0, bg="#333", fg="#FFF", activebackground="#002bb2")
        user_menu.add_command(label="View User", command=self.view_user)
        user_menu.add_separator()
        user_menu.add_command(label="User Management", command=self.user_management)
        menu_bar.add_cascade(label="User Management", menu=user_menu)

        # Configure the root window to display this menu
        self.root.config(menu=menu_bar)

    def create_admin_dashboard(self):
        # Admin dashboard frame with buttons
        dashboard_frame = ttk.Frame(self.root, padding="20")
        dashboard_frame.pack(padx=20, pady=30)

        # Admin Dashboard Title
        ttk.Label(dashboard_frame, text="Admin Dashboard", font=("Helvetica", 18, "bold"), foreground="#4CAF50").grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Example buttons for the Admin
        ttk.Button(dashboard_frame, text="Manage Users", width=20, command=self.manage_users).grid(row=1, column=0, pady=10)
        ttk.Button(dashboard_frame, text="Manage Orders", width=20, command=self.manage_orders).grid(row=2, column=0, pady=10)
        ttk.Button(dashboard_frame, text="View Reports", width=20, command=self.view_reports).grid(row=3, column=0, pady=10)
        ttk.Button(dashboard_frame, text="Logout", width=20, command=self.logout).grid(row=4, column=0, pady=10)

    def logout(self):
        self.root.destroy()  # Close the admin window

    # Placeholder methods for menu commands
    def upload_material(self):
        print("Upload Material")

    def create_material(self):
        print("Create Material")

    def view_material_report(self):
        print("View Material Report")

    def add_material_type(self):
        print("Add Material Type")

    def upload_vendor(self):
        print("Upload Vendor")

    def add_vendor(self):
        print("Add Vendor")

    def view_vendor_report(self):
        print("View Vendor Report")

    def upload_stock(self):
        print("Upload Stock")

    def update_stock(self):
        print("Update Stock")

    def view_stock_report(self):
        print("Stock Report")

    def manage_orders(self):
        print("Manage Orders")

    def view_order_report(self):
        print("Order Report")

    def view_user(self):
        print("View User")

    def user_management(self):
        print("User Management")

    def manage_users(self):
        print("Manage Users")

    def view_reports(self):
        print("View Reports")
