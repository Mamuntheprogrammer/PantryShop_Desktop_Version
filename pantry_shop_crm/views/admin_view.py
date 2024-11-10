import tkinter as tk
from tkinter import ttk

class AdminView:
    def __init__(self, root,show_login_screen_callback):
        self.root = root
        self.show_login_screen_callback = show_login_screen_callback
        self.root.title("Admin Dashboard")
        self.root.geometry("900x600")
        
        self.create_admin_menu()  # Setup the menu
        self.create_admin_dashboard()  # Setup the dashboard with frames and buttons

    def create_admin_menu(self):
        # Create the menu bar
        menu_bar = tk.Menu(self.root, bg="#333", fg="#FFF", font=("Helvetica", 10))

        # Material Management menu
        material_menu = tk.Menu(menu_bar, tearoff=0, bg="#333", fg="#FFF", activebackground="#002bb2")
        material_menu.add_command(label="Upload Material", command=self.upload_material)
        material_menu.add_command(label="Create Material", command=self.create_material)
        material_menu.add_command(label="View Material Report", command=self.view_material_report)
        menu_bar.add_cascade(label="Material Management", menu=material_menu)

        # Vendor Management menu
        vendor_menu = tk.Menu(menu_bar, tearoff=0, bg="#333", fg="#FFF", activebackground="#002bb2")
        vendor_menu.add_command(label="Add Vendor", command=self.add_vendor)
        vendor_menu.add_command(label="Vendor Report", command=self.view_vendor_report)
        menu_bar.add_cascade(label="Vendor Management", menu=vendor_menu)

        # Stock Management menu
        stock_menu = tk.Menu(menu_bar, tearoff=0, bg="#333", fg="#FFF", activebackground="#002bb2")
        stock_menu.add_command(label="Upload Stock", command=self.upload_stock)
        stock_menu.add_command(label="Update Stock", command=self.update_stock)
        stock_menu.add_command(label="Stock Report", command=self.view_stock_report)
        menu_bar.add_cascade(label="Stock Management", menu=stock_menu)

        # Order Management menu
        order_menu = tk.Menu(menu_bar, tearoff=0, bg="#333", fg="#FFF", activebackground="#002bb2")
        order_menu.add_command(label="Create Order", command=self.create_order)
        order_menu.add_command(label="View Order Report", command=self.view_order_report)
        menu_bar.add_cascade(label="Order Management", menu=order_menu)

        # User Management menu
        user_menu = tk.Menu(menu_bar, tearoff=0, bg="#333", fg="#FFF", activebackground="#002bb2")
        user_menu.add_command(label="Add User", command=self.add_user)
        user_menu.add_command(label="View User List", command=self.view_user_list)
        menu_bar.add_cascade(label="User Management", menu=user_menu)

        # Configure the root window to display this menu
        self.root.config(menu=menu_bar)

    def create_admin_dashboard(self):
        # Body frame containing all other frames
        dashboard_frame = ttk.Frame(self.root, padding="20")
        dashboard_frame.pack(fill="both", expand=True)

        # Create frames for all sections, visible when the view is loaded
        self.create_material_management_frame(dashboard_frame)
        self.create_vendor_management_frame(dashboard_frame)
        self.create_stock_management_frame(dashboard_frame)
        self.create_order_management_frame(dashboard_frame)
        self.create_user_management_frame(dashboard_frame)

        # Create the Logout and Back buttons at the bottom-right corner
        self.create_bottom_buttons(dashboard_frame)

    # -------------------- Material Management Frame --------------------

    def create_material_management_frame(self, parent_frame):
        material_frame = ttk.Frame(parent_frame, padding="20", relief="solid", width=200, height=200)
        material_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        ttk.Label(material_frame, text="Material Management", font=("Helvetica", 16, "bold"), foreground="#4CAF50").grid(row=0, column=0, columnspan=2, pady=20)
        ttk.Button(material_frame, text="Upload Material", width=20, command=self.upload_material).grid(row=1, column=0, pady=10)
        ttk.Button(material_frame, text="Create Material", width=20, command=self.create_material).grid(row=2, column=0, pady=10)
        ttk.Button(material_frame, text="View Material Report", width=20, command=self.view_material_report).grid(row=3, column=0, pady=10)

    # -------------------- Vendor Management Frame --------------------

    def create_vendor_management_frame(self, parent_frame):
        vendor_frame = ttk.Frame(parent_frame, padding="20", relief="solid", width=200, height=200)
        vendor_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        ttk.Label(vendor_frame, text="Vendor Management", font=("Helvetica", 16, "bold"), foreground="#4CAF50").grid(row=0, column=0, columnspan=2, pady=20)
        ttk.Button(vendor_frame, text="Add Vendor", width=20, command=self.add_vendor).grid(row=1, column=0, pady=10)
        ttk.Button(vendor_frame, text="Vendor Report", width=20, command=self.view_vendor_report).grid(row=2, column=0, pady=10)

    # -------------------- Stock Management Frame --------------------

    def create_stock_management_frame(self, parent_frame):
        stock_frame = ttk.Frame(parent_frame, padding="20", relief="solid", width=200, height=200)
        stock_frame.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

        ttk.Label(stock_frame, text="Stock Management", font=("Helvetica", 16, "bold"), foreground="#4CAF50").grid(row=0, column=0, columnspan=2, pady=20)
        ttk.Button(stock_frame, text="Upload Stock", width=20, command=self.upload_stock).grid(row=1, column=0, pady=10)
        ttk.Button(stock_frame, text="Update Stock", width=20, command=self.update_stock).grid(row=2, column=0, pady=10)
        ttk.Button(stock_frame, text="Stock Report", width=20, command=self.view_stock_report).grid(row=3, column=0, pady=10)

    # -------------------- Order Management Frame --------------------

    def create_order_management_frame(self, parent_frame):
        order_frame = ttk.Frame(parent_frame, padding="20", relief="solid", width=200, height=200)
        order_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        ttk.Label(order_frame, text="Order Management", font=("Helvetica", 16, "bold"), foreground="#4CAF50").grid(row=0, column=0, columnspan=2, pady=20)
        ttk.Button(order_frame, text="Create Order", width=20, command=self.create_order).grid(row=1, column=0, pady=10)
        ttk.Button(order_frame, text="View Order Report", width=20, command=self.view_order_report).grid(row=2, column=0, pady=10)

    # -------------------- User Management Frame --------------------

    def create_user_management_frame(self, parent_frame):
        user_frame = ttk.Frame(parent_frame, padding="20", relief="solid", width=200, height=200)
        user_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        ttk.Label(user_frame, text="User Management", font=("Helvetica", 16, "bold"), foreground="#4CAF50").grid(row=0, column=0, columnspan=2, pady=20)
        ttk.Button(user_frame, text="Add User", width=20, command=self.add_user).grid(row=1, column=0, pady=10)
        ttk.Button(user_frame, text="View User List", width=20, command=self.view_user_list).grid(row=2, column=0, pady=10)

    # -------------------- Bottom Buttons (Logout and Back) --------------------

    def create_bottom_buttons(self, parent_frame):
        # Create Logout and Back buttons and place them in the bottom-right corner
        bottom_frame = ttk.Frame(parent_frame, padding="10")
        bottom_frame.grid(row=2, column=2, sticky="se", padx=10, pady=10)

        ttk.Button(bottom_frame, text="Logout", width=15).grid(row=0, column=1, padx=10, pady=5)
        ttk.Button(bottom_frame, text="Back", width=15).grid(row=0, column=0, padx=10, pady=5)

    # -------------------- Action Methods --------------------

    def upload_material(self):
        print("Uploading Material")

    def create_material(self):
        print("Creating Material")

    def view_material_report(self):
        print("Viewing Material Report")

    def add_vendor(self):
        print("Adding Vendor")

    def view_vendor_report(self):
        print("Viewing Vendor Report")

    def upload_stock(self):
        print("Uploading Stock")

    def update_stock(self):
        print("Updating Stock")

    def view_stock_report(self):
        print("Viewing Stock Report")

    def create_order(self):
        print("Creating Order")

    def view_order_report(self):
        print("Viewing Order Report")

    def add_user(self):
        print("Adding User")

    def view_user_list(self):
        print("Viewing User List")


if __name__ == "__main__":
    root = tk.Tk()
    admin_view = AdminView(root)
    root.mainloop()
