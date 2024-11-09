import tkinter as tk
from tkinter import ttk
import pandas as pd  # Import pandas for exporting data
from datetime import datetime

class AdminView:
    def __init__(self, root):
        self.root = root
        self.root.title("Admin Dashboard")
        self.root.geometry("900x600")

        self.current_frame = None  # Track the current visible frame
        self.create_admin_menu()  # Setup the menu
        self.create_admin_dashboard()  # Setup the dashboard with central content frame

    def create_admin_menu(self):
        # Create the menu bar
        menu_bar = tk.Menu(self.root, bg="#333", fg="#FFF", font=("Helvetica", 10))

        # Material Management menu
        material_menu = tk.Menu(menu_bar, tearoff=0, bg="#333", fg="#FFF", activebackground="#002bb2")
        material_menu.add_command(label="Upload Material", command=self.show_upload_material_frame)
        material_menu.add_command(label="Create Material", command=self.show_create_material_frame)
        material_menu.add_command(label="View Material Report", command=self.show_view_material_report_frame)
        material_menu.add_command(label="Create Material type", command=self.show_create_material_type_frame)  # Fixed reference
        menu_bar.add_cascade(label="Material Management", menu=material_menu)


        # Vendor Management menu
        vendor_menu = tk.Menu(menu_bar, tearoff=0, bg="#333", fg="#FFF", activebackground="#002bb2")
        vendor_menu.add_command(label="Add Vendor", command=self.show_add_vendor_frame)
        vendor_menu.add_command(label="Vendor Report", command=self.show_vendor_report_frame)
        menu_bar.add_cascade(label="Vendor Management", menu=vendor_menu)

        # Stock Management menu
        stock_menu = tk.Menu(menu_bar, tearoff=0, bg="#333", fg="#FFF", activebackground="#002bb2")
        stock_menu.add_command(label="Upload Stock", command=self.show_upload_stock_frame)
        stock_menu.add_command(label="Update Stock", command=self.show_update_stock_frame)
        stock_menu.add_command(label="Stock Report", command=self.show_stock_report_frame)
        menu_bar.add_cascade(label="Stock Management", menu=stock_menu)

        # Order Management menu
        order_menu = tk.Menu(menu_bar, tearoff=0, bg="#333", fg="#FFF", activebackground="#002bb2")
        order_menu.add_command(label="Create Order", command=self.show_create_order_frame)
        order_menu.add_command(label="View Order Report", command=self.show_order_report_frame)
        menu_bar.add_cascade(label="Order Management", menu=order_menu)

        # User Management menu
        user_menu = tk.Menu(menu_bar, tearoff=0, bg="#333", fg="#FFF", activebackground="#002bb2")
        user_menu.add_command(label="Add User", command=self.show_add_user_frame)
        user_menu.add_command(label="View User List", command=self.show_user_list_frame)
        menu_bar.add_cascade(label="User Management", menu=user_menu)

        # Configure the root window to display this menu
        self.root.config(menu=menu_bar)

    def create_admin_dashboard(self):
        # Main dashboard frame
        dashboard_frame = ttk.Frame(self.root, padding="20")
        dashboard_frame.pack(fill="both", expand=True)

        # Content frame where each menu option frame will be displayed
        self.content_frame = ttk.Frame(dashboard_frame, padding="20", relief="solid")
        self.content_frame.pack(expand=True, fill="both")

        # Show a default welcome message in the content frame
        self.show_welcome_message()

    def show_frame(self, frame):
        """Display the given frame in the content area, hiding any existing frame."""
        if self.current_frame is not None:
            self.current_frame.pack_forget()
        frame.pack(expand=True, fill="both")
        self.current_frame = frame

    def show_welcome_message(self):
        """Display a welcome message when no specific view is selected."""
        welcome_frame = ttk.Frame(self.content_frame)
        ttk.Label(welcome_frame, text="Welcome to the Admin Dashboard", font=("Helvetica", 16)).pack(pady=20)
        self.show_frame(welcome_frame)

    # -------------------- Material Management Views --------------------

    def show_upload_material_frame(self):
        # Clear any existing content and create a new frame
        frame = ttk.Frame(self.content_frame)
        
        # Title for the upload section
        ttk.Label(frame, text="Upload Material", font=("Helvetica", 16)).pack(pady=20)
        
        # Entry field for the file path
        file_path_entry = ttk.Entry(frame, width=40)
        file_path_entry.pack(pady=5, padx=10)

        # Button to select file and display the file path in the entry field
        def select_file():
            from tkinter import filedialog
            file_path = filedialog.askopenfilename(title="Select a File", filetypes=[("All Files", "*.*")])
            file_path_entry.delete(0, tk.END)
            file_path_entry.insert(0, file_path)

        select_file_button = ttk.Button(frame, text="Select File", command=select_file)
        select_file_button.pack(pady=5)

        # Upload button
        upload_button = ttk.Button(frame, text="Upload", command=self.upload_material)
        upload_button.pack(pady=10)

        # Home button to navigate back to the welcome message frame
        home_button = ttk.Button(frame, text="Home", command=self.show_welcome_message)
        home_button.pack(pady=10)

        # Display the frame
        self.show_frame(frame)




    def show_create_material_frame(self):
        # Create a new frame for the create material form
        frame = ttk.Frame(self.content_frame)
        
        # Title for the frame
        ttk.Label(frame, text="Create Material", font=("Helvetica", 16)).pack(pady=20)

        # Field labels and entry widgets
        fields = {
            "Material ID": ttk.Entry(frame),
            "Material Name": ttk.Entry(frame, width=40),
            "Material Type": ttk.Entry(frame),
            "Description": ttk.Entry(frame, width=20),
            "Current Stock": ttk.Entry(frame),
            "Status": ttk.Entry(frame, width=20),
            "Created Date": ttk.Entry(frame),
            "Created By": ttk.Entry(frame)
        }

        # Display the fields in the frame
        for label_text, entry_widget in fields.items():
            ttk.Label(frame, text=label_text).pack(anchor="w", padx=10)
            entry_widget.pack(pady=5, padx=10)

        # Create Material button to save the new material
        create_button = ttk.Button(frame, text="Create Material", command=self.create_material)
        create_button.pack(pady=10)

        # Home button to go back to the welcome frame
        home_button = ttk.Button(frame, text="Home", command=self.show_welcome_message)
        home_button.pack(pady=10)

        # Show this frame
        self.show_frame(frame)





    def show_view_material_report_frame(self):
        # Create a new frame for the Material Report
        frame = ttk.Frame(self.content_frame)

        # Title for the report
        ttk.Label(frame, text="Material Report", font=("Helvetica", 16)).pack(pady=20)

        # Table frame for the report
        table_frame = ttk.Frame(frame)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Dummy data for material report (replace this with real data as needed)
        material_data = [
            {"material_id": i, "material_name": f"Material {i}", "material_type": "Type A" if i % 2 == 0 else "Type B",
            "current_stock": 100 + i, "status": "Active" if i % 2 == 0 else "Inactive"}
            for i in range(1, 31)  # 30 sample records
        ]
        
        # Convert dummy data to DataFrame for pagination and export purposes
        self.material_df = pd.DataFrame(material_data)

        # Display the first 15 rows initially
        self.current_page = 0
        self.page_size = 15
        self.display_material_page(table_frame)

        # Pagination controls
        pagination_frame = ttk.Frame(frame)
        pagination_frame.pack(pady=10)

        ttk.Button(pagination_frame, text="Previous", command=lambda: self.change_material_page(-1)).grid(row=0, column=0, padx=5)
        ttk.Button(pagination_frame, text="Next", command=lambda: self.change_material_page(1)).grid(row=0, column=1, padx=5)

        # Export button
        export_button = ttk.Button(frame, text="Export", command=self.export_material_report)
        export_button.pack(pady=10)

        # Home button to return to the welcome frame
        home_button = ttk.Button(frame, text="Home", command=self.show_welcome_message)
        home_button.pack(pady=10)

        # Display this frame
        self.show_frame(frame)

    def display_material_page(self, parent):
        # Clear existing table if any
        for widget in parent.winfo_children():
            widget.destroy()

        # Frame to hold the Treeview and scrollbars
        tree_frame = ttk.Frame(parent)
        tree_frame.pack(fill="both", expand=True)

        # Define columns for the Treeview
        columns = ("material_id", "material_name", "material_type", "current_stock", "status")
        self.material_tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=self.page_size)

        # Define column headings and set anchor to center
        for col in columns:
            self.material_tree.heading(col, text=col.replace("_", " ").title())
            self.material_tree.column(col, anchor="center")

        # Vertical scrollbar
        vert_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.material_tree.yview)
        vert_scrollbar.pack(side="right", fill="y")

        # Horizontal scrollbar
        horiz_scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.material_tree.xview)
        horiz_scrollbar.pack(side="bottom", fill="x")

        # Configure scrollbars for the Treeview
        self.material_tree.configure(yscrollcommand=vert_scrollbar.set, xscrollcommand=horiz_scrollbar.set)
        self.material_tree.pack(fill="both", expand=True)

        # Load the current page of material data
        start_idx = self.current_page * self.page_size
        end_idx = start_idx + self.page_size
        for _, row in self.material_df.iloc[start_idx:end_idx].iterrows():
            self.material_tree.insert("", "end", values=list(row))

    def change_material_page(self, direction):
        # Change page based on the direction (-1 for previous, +1 for next)
        max_page = len(self.material_df) // self.page_size
        self.current_page = min(max(0, self.current_page + direction), max_page)
        
        # Refresh the displayed page
        self.display_material_page(self.material_tree.master)

    def export_material_report(self):
        # Export the material data to a CSV file
        self.material_df.to_csv("material_report.csv", index=False)
        print("Material report exported to 'material_report.csv'")




    def show_create_material_type_frame(self):
        # Create a new frame for creating a material type
        frame = ttk.Frame(self.content_frame)

        # Title for the frame
        ttk.Label(frame, text="Create Material Type", font=("Helvetica", 16)).pack(pady=20)

        # Field entries
        form_frame = ttk.Frame(frame)
        form_frame.pack(pady=10)

        # ID entry
        ttk.Label(form_frame, text="ID:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.material_type_id_entry = ttk.Entry(form_frame)
        self.material_type_id_entry.grid(row=0, column=1, padx=5, pady=5)

        # Material Type entry
        ttk.Label(form_frame, text="Material Type:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.material_type_entry = ttk.Entry(form_frame)
        self.material_type_entry.grid(row=1, column=1, padx=5, pady=5)

        # Material Description entry
        ttk.Label(form_frame, text="Material Description:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.material_desc_entry = ttk.Entry(form_frame)
        self.material_desc_entry.grid(row=2, column=1, padx=5, pady=5)

        # Created Date (auto-populated with current date)
        ttk.Label(form_frame, text="Created Date:").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.created_date_entry = ttk.Entry(form_frame)
        self.created_date_entry.insert(0, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        self.created_date_entry.config(state="readonly")  # Read-only
        self.created_date_entry.grid(row=3, column=1, padx=5, pady=5)

        # Created By entry
        ttk.Label(form_frame, text="Created By:").grid(row=4, column=0, sticky="w", padx=5, pady=5)
        self.created_by_entry = ttk.Entry(form_frame)
        self.created_by_entry.grid(row=4, column=1, padx=5, pady=5)

        # "Create Material Type" button
        create_button = ttk.Button(frame, text="Create Material Type", command=self.create_material_type)
        create_button.pack(pady=10)

        # Home button to return to the welcome frame
        home_button = ttk.Button(frame, text="Home", command=self.show_welcome_message)
        home_button.pack(pady=10)

        # Display this frame
        self.show_frame(frame)

    # -------------------- Vendor Management Views --------------------
    def show_add_vendor_frame(self):
        # Create a new frame for adding a vendor
        frame = ttk.Frame(self.content_frame)

        # Title for the frame
        ttk.Label(frame, text="Add Vendor", font=("Helvetica", 16)).pack(pady=20)

        # Frame for form fields
        form_frame = ttk.Frame(frame)
        form_frame.pack(pady=10)

        # Vendor ID
        ttk.Label(form_frame, text="Vendor ID:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.vendor_id_entry = ttk.Entry(form_frame)
        self.vendor_id_entry.grid(row=0, column=1, padx=5, pady=5)

        # Vendor Name
        ttk.Label(form_frame, text="Vendor Name:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.vendor_name_entry = ttk.Entry(form_frame)
        self.vendor_name_entry.grid(row=1, column=1, padx=5, pady=5)

        # Contact First Name
        ttk.Label(form_frame, text="Contact First Name:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.contact_fname_entry = ttk.Entry(form_frame)
        self.contact_fname_entry.grid(row=2, column=1, padx=5, pady=5)

        # Contact Last Name
        ttk.Label(form_frame, text="Contact Last Name:").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.contact_lname_entry = ttk.Entry(form_frame)
        self.contact_lname_entry.grid(row=3, column=1, padx=5, pady=5)

        # Contact Email
        ttk.Label(form_frame, text="Contact Email:").grid(row=4, column=0, sticky="w", padx=5, pady=5)
        self.contact_email_entry = ttk.Entry(form_frame)
        self.contact_email_entry.grid(row=4, column=1, padx=5, pady=5)

        # Contact Phone
        ttk.Label(form_frame, text="Contact Phone:").grid(row=5, column=0, sticky="w", padx=5, pady=5)
        self.contact_phone_entry = ttk.Entry(form_frame)
        self.contact_phone_entry.grid(row=5, column=1, padx=5, pady=5)

        # Address Key
        ttk.Label(form_frame, text="Address Key:").grid(row=6, column=0, sticky="w", padx=5, pady=5)
        self.address_key_entry = ttk.Entry(form_frame)
        self.address_key_entry.grid(row=6, column=1, padx=5, pady=5)

        # Is Active (checkbox for boolean value)
        self.is_active_var = tk.BooleanVar()
        ttk.Checkbutton(form_frame, text="Is Active", variable=self.is_active_var).grid(row=7, column=0, columnspan=2, sticky="w", padx=5, pady=5)

        # Created Date (auto-populated with current date)
        ttk.Label(form_frame, text="Created Date:").grid(row=8, column=0, sticky="w", padx=5, pady=5)
        self.created_date_entry = ttk.Entry(form_frame)
        self.created_date_entry.insert(0, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        self.created_date_entry.config(state="readonly")  # Read-only
        self.created_date_entry.grid(row=8, column=1, padx=5, pady=5)

        # Created By
        ttk.Label(form_frame, text="Created By:").grid(row=9, column=0, sticky="w", padx=5, pady=5)
        self.created_by_entry = ttk.Entry(form_frame)
        self.created_by_entry.grid(row=9, column=1, padx=5, pady=5)

        # Add Vendor button
        add_vendor_button = ttk.Button(frame, text="Add Vendor", command=self.add_vendor)
        add_vendor_button.pack(pady=10)

        # Home button to return to the welcome frame
        home_button = ttk.Button(frame, text="Home", command=self.show_welcome_message)
        home_button.pack(pady=10)

        # Display this frame
        self.show_frame(frame)

    def show_vendor_report_frame(self):
        # Create a new frame for the Vendor Report
        frame = ttk.Frame(self.content_frame)

        # Title for the report
        ttk.Label(frame, text="Vendor Report", font=("Helvetica", 16)).pack(pady=20)

        # Table frame for the report
        table_frame = ttk.Frame(frame)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Dummy vendor data (replace this with real data as needed)
        vendor_data = [
            {"vendor_id": 1, "vendor_name": "Vendor A", "contact_fname": "John", "contact_lname": "Doe",
             "contact_email": "john@example.com", "contact_phone": "1234567890", "is_active": True, "created_date": "2024-01-01"},
            {"vendor_id": 2, "vendor_name": "Vendor B", "contact_fname": "Jane", "contact_lname": "Doe",
             "contact_email": "jane@example.com", "contact_phone": "0987654321", "is_active": False, "created_date": "2024-01-02"},
            # Add more records as needed
        ]
        
        # Convert dummy data to DataFrame for pagination and export purposes
        self.vendor_df = pd.DataFrame(vendor_data)

        # Display the first 15 rows initially
        self.current_page = 0
        self.page_size = 15
        self.display_vendor_page(table_frame)

        # Pagination controls
        pagination_frame = ttk.Frame(frame)
        pagination_frame.pack(pady=10)

        ttk.Button(pagination_frame, text="Previous", command=lambda: self.change_page(-1)).grid(row=0, column=0, padx=5)
        ttk.Button(pagination_frame, text="Next", command=lambda: self.change_page(1)).grid(row=0, column=1, padx=5)

        # Export button
        export_button = ttk.Button(frame, text="Export", command=self.export_vendor_report)
        export_button.pack(pady=10)

        # Home button to return to the welcome frame
        home_button = ttk.Button(frame, text="Home", command=self.show_welcome_message)
        home_button.pack(pady=10)

        # Display this frame
        self.show_frame(frame)

    def display_vendor_page(self, parent):
        # Clear existing table if any
        for widget in parent.winfo_children():
            widget.destroy()

        # Frame to hold the Treeview and scrollbars
        tree_frame = ttk.Frame(parent)
        tree_frame.pack(fill="both", expand=True)

        # Define columns for the Treeview
        columns = ("vendor_id", "vendor_name", "contact_fname", "contact_lname", "contact_email", "contact_phone", "is_active", "created_date")
        self.vendor_tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=self.page_size)

        # Define column headings and set anchor to center
        for col in columns:
            self.vendor_tree.heading(col, text=col.replace("_", " ").title())
            self.vendor_tree.column(col, anchor="center")

        # Vertical scrollbar
        vert_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.vendor_tree.yview)
        vert_scrollbar.pack(side="right", fill="y")

        # Horizontal scrollbar
        horiz_scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.vendor_tree.xview)
        horiz_scrollbar.pack(side="bottom", fill="x")

        # Configure scrollbars for the Treeview
        self.vendor_tree.configure(yscrollcommand=vert_scrollbar.set, xscrollcommand=horiz_scrollbar.set)
        self.vendor_tree.pack(fill="both", expand=True)

        # Load the current page of vendor data
        start_idx = self.current_page * self.page_size
        end_idx = start_idx + self.page_size
        for _, row in self.vendor_df.iloc[start_idx:end_idx].iterrows():
            self.vendor_tree.insert("", "end", values=list(row))


    def change_page(self, direction):
        # Change page based on the direction (-1 for previous, +1 for next)
        max_page = len(self.vendor_df) // self.page_size
        self.current_page = min(max(0, self.current_page + direction), max_page)
        
        # Refresh the displayed page
        self.display_vendor_page(self.vendor_tree.master)

    def export_vendor_report(self):
        # Export the vendor data to a CSV file
        self.vendor_df.to_csv("vendor_report.csv", index=False)
        print("Vendor report exported to 'vendor_report.csv'")

    # -------------------- Stock Management Views --------------------
    def show_upload_stock_frame(self):
        frame = ttk.Frame(self.content_frame)
        ttk.Label(frame, text="Upload Stock", font=("Helvetica", 16)).pack(pady=20)
        ttk.Button(frame, text="Upload Stock", command=self.upload_stock).pack()
        self.show_frame(frame)

    def show_update_stock_frame(self):
        frame = ttk.Frame(self.content_frame)
        ttk.Label(frame, text="Update Stock", font=("Helvetica", 16)).pack(pady=20)
        ttk.Button(frame, text="Update Stock", command=self.update_stock).pack()
        self.show_frame(frame)

    def show_stock_report_frame(self):
        frame = ttk.Frame(self.content_frame)
        ttk.Label(frame, text="Stock Report", font=("Helvetica", 16)).pack(pady=20)
        ttk.Button(frame, text="View Stock Report", command=self.view_stock_report).pack()
        self.show_frame(frame)

    # -------------------- Order Management Views --------------------
    def show_create_order_frame(self):
        frame = ttk.Frame(self.content_frame)
        ttk.Label(frame, text="Create Order", font=("Helvetica", 16)).pack(pady=20)
        ttk.Button(frame, text="Create Order", command=self.create_order).pack()
        self.show_frame(frame)

    def show_order_report_frame(self):
        frame = ttk.Frame(self.content_frame)
        ttk.Label(frame, text="Order Report", font=("Helvetica", 16)).pack(pady=20)
        ttk.Button(frame, text="View Order Report", command=self.view_order_report).pack()
        self.show_frame(frame)

    # -------------------- User Management Views --------------------
    def show_add_user_frame(self):
        frame = ttk.Frame(self.content_frame)
        ttk.Label(frame, text="Add User", font=("Helvetica", 16)).pack(pady=20)
        ttk.Button(frame, text="Add User", command=self.add_user).pack()
        self.show_frame(frame)

    def show_user_list_frame(self):
        frame = ttk.Frame(self.content_frame)
        ttk.Label(frame, text="User List", font=("Helvetica", 16)).pack(pady=20)
        ttk.Button(frame, text="View User List", command=self.view_user_list).pack()
        self.show_frame(frame)

    # -------------------- Action Methods --------------------
    # (Action methods as defined in your initial code...)


    # Placeholder methods
    def upload_material(self):
        print("Uploading Material")

    def create_material(self):
        print("Creating Material")

    def view_material_report(self):
        print("Viewing Material Report")

    def create_material_type(self):
        print("Creating Material")

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
