import tkinter as tk
from tkinter import ttk
import pandas as pd  # Import pandas for exporting data
from datetime import datetime,date
from tkinter import messagebox,Tk, StringVar, IntVar
from tkinter.simpledialog import askstring

class AdminView:
    def __init__(self, root,show_login_screen_callback):
        self.root = root
        self.show_login_screen_callback = show_login_screen_callback
        self.root.title("Admin Dashboard")
        self.root.geometry("900x600")
        self.current_frame = None
        self.create_admin_menu()  # Setup the menu
        self.create_admin_dashboard()  # Setup the dashboard with frames and buttons

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
        order_menu.add_command(label="manage Order", command=self.show_manage_order_frame)
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
        

        # # Align the Back button below the Submit button, centered
        # back_button = ttk.Button(welcome_frame, text="Back", width=20, command=self.show_login_screen_callback)
        # back_button.pack(pady=5)

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
        # Clear any existing content and create a new frame
        frame = ttk.Frame(self.content_frame)
        
        # Title for the upload section
        ttk.Label(frame, text="Upload Stock", font=("Helvetica", 16)).pack(pady=20)
        
        # Entry field for the file path
        file_path_entry = ttk.Entry(frame, width=40)
        file_path_entry.pack(pady=5, padx=10)

        # Button to select file and display the file path in the entry field
        def select_file():
            from tkinter import filedialog
            file_path = filedialog.askopenfilename(title="Select Stock File", filetypes=[("Excel Files", "*.xlsx *.xls")])
            file_path_entry.delete(0, tk.END)
            file_path_entry.insert(0, file_path)

        select_file_button = ttk.Button(frame, text="Select File", command=select_file)
        select_file_button.pack(pady=5)

        # Upload button
        upload_button = ttk.Button(frame, text="Upload Stock", command=self.upload_stock)
        upload_button.pack(pady=10)

        # Home button to navigate back to the welcome message frame
        home_button = ttk.Button(frame, text="Home", command=self.show_welcome_message)
        home_button.pack(pady=10)

        # Display the frame
        self.show_frame(frame)




    def show_update_stock_frame(self):
        # Create a new frame for updating stock
        frame = ttk.Frame(self.content_frame)

        # Title for the update section
        ttk.Label(frame, text="Update Stock", font=("Helvetica", 16)).pack(pady=20)
        
        # Material and Batch Search Section
        search_frame = ttk.Frame(frame)
        search_frame.pack(pady=10)

        # Material Name Label and Entry
        ttk.Label(search_frame, text="Material Name:", width=15, anchor="w").grid(row=0, column=0, padx=5, pady=5)
        self.material_search_entry = ttk.Entry(search_frame, width=40)
        self.material_search_entry.grid(row=0, column=1, padx=5, pady=5)

        # Batch Number Label and Entry
        ttk.Label(search_frame, text="Batch Number:", width=15, anchor="w").grid(row=1, column=0, padx=5, pady=5)
        self.batch_search_entry = ttk.Entry(search_frame, width=40)
        self.batch_search_entry.grid(row=1, column=1, padx=5, pady=5)

        # Search Button aligned to the right of the search section
        search_button = ttk.Button(search_frame, text="Search", command=self.search_stock)
        search_button.grid(row=0, column=2, rowspan=2, padx=5, pady=5)

        # Stock details section (after searching)
        details_frame = ttk.Frame(frame)
        details_frame.pack(pady=10)

        # Quantity Label and Entry
        ttk.Label(details_frame, text="Quantity:", width=15, anchor="w").grid(row=0, column=0, padx=5, pady=5)
        self.quantity_entry = ttk.Entry(details_frame, width=40)
        self.quantity_entry.grid(row=0, column=1, padx=5, pady=5)

        # Unit Price Label and Entry
        ttk.Label(details_frame, text="Unit Price:", width=15, anchor="w").grid(row=1, column=0, padx=5, pady=5)
        self.unit_price_entry = ttk.Entry(details_frame, width=40)
        self.unit_price_entry.grid(row=1, column=1, padx=5, pady=5)

        # Total Value Label and Entry (calculated as Quantity * Unit Price)
        ttk.Label(details_frame, text="Total Value:", width=15, anchor="w").grid(row=2, column=0, padx=5, pady=5)
        self.total_value_entry = ttk.Entry(details_frame, width=40)
        self.total_value_entry.grid(row=2, column=1, padx=5, pady=5)

        # Status Label and Entry (Active/Inactive)
        ttk.Label(details_frame, text="Status:", width=15, anchor="w").grid(row=3, column=0, padx=5, pady=5)
        self.status_entry = ttk.Entry(details_frame, width=40)
        self.status_entry.grid(row=3, column=1, padx=5, pady=5)

        # Expiry Date Label and Entry
        ttk.Label(details_frame, text="Expiry Date:", width=15, anchor="w").grid(row=4, column=0, padx=5, pady=5)
        self.expiry_date_entry = ttk.Entry(details_frame, width=40)
        self.expiry_date_entry.grid(row=4, column=1, padx=5, pady=5)

        # Vendor ID Label and Entry
        ttk.Label(details_frame, text="Vendor ID:", width=15, anchor="w").grid(row=5, column=0, padx=5, pady=5)
        self.vendor_id_entry = ttk.Entry(details_frame, width=40)
        self.vendor_id_entry.grid(row=5, column=1, padx=5, pady=5)

        # Purchase Date Label and Entry
        ttk.Label(details_frame, text="Purchase Date:", width=15, anchor="w").grid(row=6, column=0, padx=5, pady=5)
        self.purchase_date_entry = ttk.Entry(details_frame, width=40)
        self.purchase_date_entry.grid(row=6, column=1, padx=5, pady=5)

        # Reorder Level Label and Entry
        ttk.Label(details_frame, text="Reorder Level:", width=15, anchor="w").grid(row=7, column=0, padx=5, pady=5)
        self.reorder_level_entry = ttk.Entry(details_frame, width=40)
        self.reorder_level_entry.grid(row=7, column=1, padx=5, pady=5)

        # Location Label and Entry
        ttk.Label(details_frame, text="Location:", width=15, anchor="w").grid(row=8, column=0, padx=5, pady=5)
        self.location_entry = ttk.Entry(details_frame, width=40)
        self.location_entry.grid(row=8, column=1, padx=5, pady=5)

        # Button to update stock after editing
        update_button = ttk.Button(frame, text="Update Stock", command=self.update_stock_details)
        update_button.pack(pady=10)

        # Home button to navigate back to the welcome message frame
        home_button = ttk.Button(frame, text="Home", command=self.show_welcome_message)
        home_button.pack(pady=10)
        
        # Show the frame
        self.show_frame(frame)

    def search_stock(self):
        # Get material name and batch number from entries
        material_name = self.material_search_entry.get()
        batch_number = self.batch_search_entry.get()

        # Implement your search logic here (for example, searching in a database)
        self.search_and_display_stock(material_name, batch_number)

    def search_and_display_stock(self, material_name, batch_number):
        # Simulate fetching stock data for the material and batch (replace with real data retrieval logic)
        stock_data = {
            "material_name": material_name,
            "batch_number": batch_number,
            "quantity": 100,
            "unit_price": 50,
            "total_value": 5000,
            "status": "Active",
            "expiry_date": "2025-12-31",
            "vendor_id": 1,
            "purchase_date": "2024-10-15",
            "reorder_level": 10,
            "location": "Warehouse A",
            "stock_id": 1  # Dummy stock ID for demonstration purposes
        }
        
        # Check if material and batch are valid (dummy check here)
        if stock_data["material_name"] == material_name and stock_data["batch_number"] == batch_number:
            # Populate the fields with the fetched stock data
            self.selected_stock_id = stock_data["stock_id"]
            self.quantity_entry.delete(0, tk.END)
            self.quantity_entry.insert(0, stock_data["quantity"])
            self.unit_price_entry.delete(0, tk.END)
            self.unit_price_entry.insert(0, stock_data["unit_price"])
            self.total_value_entry.delete(0, tk.END)
            self.total_value_entry.insert(0, stock_data["total_value"])
            self.status_entry.delete(0, tk.END)
            self.status_entry.insert(0, stock_data["status"])
            self.expiry_date_entry.delete(0, tk.END)
            self.expiry_date_entry.insert(0, stock_data["expiry_date"])
            self.vendor_id_entry.delete(0, tk.END)
            self.vendor_id_entry.insert(0, stock_data["vendor_id"])
            self.purchase_date_entry.delete(0, tk.END)
            self.purchase_date_entry.insert(0, stock_data["purchase_date"])
            self.reorder_level_entry.delete(0, tk.END)
            self.reorder_level_entry.insert(0, stock_data["reorder_level"])
            self.location_entry.delete(0, tk.END)
            self.location_entry.insert(0, stock_data["location"])
        else:
            print("Stock not found for the given material and batch.")

    def update_stock_details(self):
        # Implement the logic to update the stock record in your system
        stock_id = self.selected_stock_id  # Assuming the stock ID is selected during the search
        quantity = self.quantity_entry.get()
        unit_price = self.unit_price_entry.get()
        total_value = self.total_value_entry.get()
        status = self.status_entry.get()
        expiry_date = self.expiry_date_entry.get()
        vendor_id = self.vendor_id_entry.get()
        purchase_date = self.purchase_date_entry.get()
        reorder_level = self.reorder_level_entry.get()
        location = self.location_entry.get()
        
        # Update the stock data here (for example, update in a database)
        print(f"Updated stock: {stock_id}, Quantity: {quantity}, Unit Price: {unit_price}, Total Value: {total_value}, "
            f"Status: {status}, Expiry Date: {expiry_date}, Vendor ID: {vendor_id}, Purchase Date: {purchase_date}, "
            f"Reorder Level: {reorder_level}, Location: {location}")
        
        # Clear the fields or show a success message after update
        self.clear_fields()

    def clear_fields(self):
        # Clear all the fields after updating
        self.material_search_entry.delete(0, tk.END)
        self.batch_search_entry.delete(0, tk.END)
        self.quantity_entry.delete(0, tk.END)
        self.unit_price_entry.delete(0, tk.END)
        self.total_value_entry.delete(0, tk.END)
        self.status_entry.delete(0, tk.END)





    def show_stock_report_frame(self):
        # Create a new frame for the Stock Report
        frame = ttk.Frame(self.content_frame)

        # Title for the report
        ttk.Label(frame, text="Stock Report", font=("Helvetica", 16)).pack(pady=20)

        # Table frame for the report
        table_frame = ttk.Frame(frame)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Dummy data for stock report (replace this with real data as needed)
        stock_data = [
            {"stock_id": i, "material_name": f"Material {i}", "batch_number": f"Batch {i}",
            "quantity": 100 + i, "unit_price": 10 + i, "total_value": (100 + i) * (10 + i),
            "status": "Active" if i % 2 == 0 else "Inactive", "expiry_date": "2024-12-31", "vendor_name": f"Vendor {i}"}
            for i in range(1, 31)  # 30 sample records
        ]

        # Convert dummy data to DataFrame for pagination and export purposes
        self.stock_df = pd.DataFrame(stock_data)

        # Display the first 15 rows initially
        self.current_page = 0
        self.page_size = 15
        self.display_stock_page(table_frame)

        # Pagination controls
        pagination_frame = ttk.Frame(frame)
        pagination_frame.pack(pady=10)

        ttk.Button(pagination_frame, text="Previous", command=lambda: self.change_stock_page(-1)).grid(row=0, column=0, padx=5)
        ttk.Button(pagination_frame, text="Next", command=lambda: self.change_stock_page(1)).grid(row=0, column=1, padx=5)

        # Export button
        export_button = ttk.Button(frame, text="Export", command=self.export_stock_report)
        export_button.pack(pady=10)

        # Home button to return to the welcome frame
        home_button = ttk.Button(frame, text="Home", command=self.show_welcome_message)
        home_button.pack(pady=10)

        # Display this frame
        self.show_frame(frame)

    def display_stock_page(self, parent):
        # Clear existing table if any
        for widget in parent.winfo_children():
            widget.destroy()

        # Frame to hold the Treeview and scrollbars
        tree_frame = ttk.Frame(parent)
        tree_frame.pack(fill="both", expand=True)

        # Define columns for the Treeview
        columns = ("stock_id", "material_name", "batch_number", "quantity", "unit_price", "total_value", "status", "expiry_date", "vendor_name")
        self.stock_tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=self.page_size)

        # Define column headings and set anchor to center
        for col in columns:
            self.stock_tree.heading(col, text=col.replace("_", " ").title())
            self.stock_tree.column(col, anchor="center")

        # Vertical scrollbar
        vert_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.stock_tree.yview)
        vert_scrollbar.pack(side="right", fill="y")

        # Horizontal scrollbar
        horiz_scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.stock_tree.xview)
        horiz_scrollbar.pack(side="bottom", fill="x")

        # Configure scrollbars for the Treeview
        self.stock_tree.configure(yscrollcommand=vert_scrollbar.set, xscrollcommand=horiz_scrollbar.set)
        self.stock_tree.pack(fill="both", expand=True)

        # Load the current page of stock data
        start_idx = self.current_page * self.page_size
        end_idx = start_idx + self.page_size
        for _, row in self.stock_df.iloc[start_idx:end_idx].iterrows():
            self.stock_tree.insert("", "end", values=list(row))

    def change_stock_page(self, direction):
        # Change page based on the direction (-1 for previous, +1 for next)
        max_page = len(self.stock_df) // self.page_size
        self.current_page = min(max(0, self.current_page + direction), max_page)
        
        # Refresh the displayed page
        self.display_stock_page(self.stock_tree.master)

    def export_stock_report(self):
        # Export the stock data to a CSV file
        self.stock_df.to_csv("stock_report.csv", index=False)
        print("Stock report exported to 'stock_report.csv'")





    # -------------------- Order Management Views --------------------


    # def show_manage_order_frame(self):
    #     frame = ttk.Frame(self.content_frame)
    #     ttk.Label(frame, text="manage Order", font=("Helvetica", 16)).pack(pady=20) 
    #     ttk.Button(frame, text="Manage Order", command=self.manage_order).pack() 
    #     self.show_frame(frame)


    def show_manage_order_frame(self):
        # Create a new frame for managing orders
        frame = ttk.Frame(self.content_frame)

        # Title for the frame
        title_label = ttk.Label(frame, text="Manage Orders", font=("Helvetica", 16))
        title_label.grid(row=0, column=0, columnspan=2, pady=20)

        # Filter options (Order ID, Pickup Date, User ID)
        filter_frame = ttk.Frame(frame)
        filter_frame.grid(row=1, column=0, columnspan=2, pady=10)

        ttk.Label(filter_frame, text="Order ID:").grid(row=0, column=0, padx=5)
        self.order_id_entry = ttk.Entry(filter_frame)
        self.order_id_entry.grid(row=0, column=1, padx=5)

        ttk.Label(filter_frame, text="Pickup Date:").grid(row=0, column=2, padx=5)
        self.pickup_date_entry = ttk.Entry(filter_frame)
        self.pickup_date_entry.grid(row=0, column=3, padx=5)

        ttk.Label(filter_frame, text="User ID:").grid(row=0, column=4, padx=5)
        self.user_id_entry = ttk.Entry(filter_frame)
        self.user_id_entry.grid(row=0, column=5, padx=5)

        # Filter button
        filter_button = ttk.Button(filter_frame, text="Filter", command=self.apply_filters)
        filter_button.grid(row=0, column=6, padx=10)

        # Tree view for displaying orders
        columns = ("Order ID", "User ID", "Pickup Date", "Order Date", "Status")
        self.order_tree = ttk.Treeview(frame, columns=columns, show="headings", height=11)
        for col in columns:
            self.order_tree.heading(col, text=col)
            self.order_tree.column(col, width=100)

        # Scrollbars for the tree view
        vscrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.order_tree.yview)
        vscrollbar.grid(row=2, column=1, sticky="ns")
        self.order_tree.configure(yscrollcommand=vscrollbar.set)

        hscrollbar = ttk.Scrollbar(frame, orient="horizontal", command=self.order_tree.xview)
        hscrollbar.grid(row=3, column=0, sticky="ew")
        self.order_tree.configure(xscrollcommand=hscrollbar.set)

        self.order_tree.grid(row=2, column=0, sticky="nsew")

        # Pagination controls
        pagination_frame = ttk.Frame(frame)
        pagination_frame.grid(row=4, column=0, pady=10)

        ttk.Button(pagination_frame, text="Previous", command=lambda: self.change_page(-1)).grid(row=0, column=0, padx=5)
        ttk.Button(pagination_frame, text="Next", command=lambda: self.change_page(1)).grid(row=0, column=1, padx=5)

        # Action buttons for the selected order
        action_frame = ttk.Frame(frame)
        action_frame.grid(row=2, column=2, padx=10, sticky="n")

        approve_button = ttk.Button(action_frame, text="Approve", command=self.approve_selected_order)
        approve_button.pack(pady=5)

        view_button = ttk.Button(action_frame, text="View", command=self.view_selected_order)
        view_button.pack(pady=5)

        print_button = ttk.Button(action_frame, text="Print", command=self.print_selected_order)
        print_button.pack(pady=5)

        # Home button to return to the welcome frame
        home_button = ttk.Button(frame, text="Home", command=self.show_welcome_message)
        home_button.grid(row=5, column=0, columnspan=2, pady=10)

        # Display this frame
        self.show_frame(frame)

        # Load initial data and display first page
        self.orders = self.load_order_data()  # Load your data here
        self.filtered_orders = self.orders
        self.current_page = 0
        self.page_size = 10
        self.display_orders_list()

    def display_orders_list(self):
        # Clear the tree view
        for row in self.order_tree.get_children():
            self.order_tree.delete(row)

        # Get the current page of orders
        start_idx = self.current_page * self.page_size
        end_idx = start_idx + self.page_size
        current_orders = self.filtered_orders[start_idx:end_idx]

        # Insert the orders into the tree view
        for order in current_orders:
            self.order_tree.insert("", "end", values=(order["order_id"], order["user_id"], order["pickup_date"], order["order_date"], order["order_status"]))

    def apply_filters(self):
        # Apply filters based on the entries
        order_id = self.order_id_entry.get().strip()
        pickup_date = self.pickup_date_entry.get().strip()
        user_id = self.user_id_entry.get().strip()

        if not (order_id or pickup_date or user_id):
            # Reset to all orders if no filter is entered
            self.filtered_orders = self.orders
        else:
            # Filter orders based on input criteria
            self.filtered_orders = [
                order for order in self.orders
                if (not order_id or str(order["order_id"]) == order_id) and
                (not pickup_date or order["pickup_date"] == pickup_date) and
                (not user_id or str(order["user_id"]) == user_id)
            ]

        # Reset to the first page after filtering
        self.current_page = 0
        self.display_orders_list()

    def change_page(self, direction):
        # Change page based on the direction (-1 for previous, +1 for next)
        if 0 <= self.current_page + direction < len(self.filtered_orders) // self.page_size + 1:
            self.current_page += direction
            self.display_orders_list()

    def approve_selected_order(self):
        # Approve or unapprove the selected order
        selected_item = self.order_tree.selection()
        if selected_item:
            order_id = self.order_tree.item(selected_item)["values"][0]
            for order in self.orders:
                if order["order_id"] == order_id:
                    order["order_status"] = "Approved" if order["order_status"] == "Pending" else "Pending"
                    self.display_orders_list()
                    break
        else:
            messagebox.showwarning("No selection", "Please select an order to approve.")

    def view_selected_order(self):
        # View details of the selected order
        selected_item = self.order_tree.selection()
        if selected_item:
            order_id = self.order_tree.item(selected_item)["values"][0]
            for order in self.orders:
                if order["order_id"] == order_id:
                    self.show_order_details(order)
                    break
        else:
            messagebox.showwarning("No selection", "Please select an order to view.")

    def print_selected_order(self):
        # Print the selected order
        selected_item = self.order_tree.selection()
        if selected_item:
            order_id = self.order_tree.item(selected_item)["values"][0]
            for order in self.orders:
                if order["order_id"] == order_id:
                    self.print_order(order)
                    break
        else:
            messagebox.showwarning("No selection", "Please select an order to print.")

    def load_order_data(self):
        # Sample data loader function (replace this with actual data loading logic)
        return [
            {"order_id": i, "user_id": i % 5, "order_date": f"2024-11-{i:02}", "pickup_date": f"2024-11-{i+1:02}", "order_status": "Pending"}
            for i in range(1, 101)  # 100 sample orders
        ]

    def show_order_details(self, order):
        # Function to display order details in a popup
        order_details = f"Order ID: {order['order_id']}\nUser ID: {order['user_id']}\nOrder Date: {order['order_date']}\nPickup Date: {order['pickup_date']}\nStatus: {order['order_status']}"
        messagebox.showinfo("Order Details", order_details)

    def print_order(self, order):
        # Function to print order details (simulate)
        print(f"Printing Order ID: {order['order_id']}")



#-------------


    def show_order_report_frame(self):
        # Create a new frame for Order Report
        frame = ttk.Frame(self.content_frame)
        
        # Title for the report
        ttk.Label(frame, text="Order Report", font=("Helvetica", 16)).pack(pady=20)
        
        # Table frame for the report
        table_frame = ttk.Frame(frame)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Sample order data (replace with real data)
        order_data = [
            {"order_id": i, "user_id": f"User {i}", "order_date": f"2024-11-{i:02}", 
            "pickup_date": f"2024-11-{i+2:02}", "status": "Approved" if i % 2 == 0 else "Pending"}
            for i in range(1, 31)  # 30 sample records
        ]
        
        # Convert sample data to DataFrame for pagination and export
        self.order_df = pd.DataFrame(order_data)
        
        # Display the first 15 rows initially
        self.current_order_page = 0
        self.order_page_size = 15
        self.display_order_page(table_frame)
        
        # Pagination controls
        pagination_frame = ttk.Frame(frame)
        pagination_frame.pack(pady=10)
        
        ttk.Button(pagination_frame, text="Previous", command=lambda: self.change_order_page(-1)).grid(row=0, column=0, padx=5)
        ttk.Button(pagination_frame, text="Next", command=lambda: self.change_order_page(1)).grid(row=0, column=1, padx=5)
        
        # Export button
        export_button = ttk.Button(frame, text="Export", command=self.export_order_report)
        export_button.pack(pady=10)
        
        # Home button to return to the welcome frame
        home_button = ttk.Button(frame, text="Home", command=self.show_welcome_message)
        home_button.pack(pady=10)
        
        # Display this frame
        self.show_frame(frame)

    def display_order_page(self, parent):
        # Clear existing table if any
        for widget in parent.winfo_children():
            widget.destroy()
        
        # Frame to hold the Treeview and scrollbars
        tree_frame = ttk.Frame(parent)
        tree_frame.pack(fill="both", expand=True)
        
        # Define columns for the Treeview
        columns = ("order_id", "user_id", "order_date", "pickup_date", "status")
        self.order_tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=self.order_page_size)
        
        # Define column headings and set anchor to center
        for col in columns:
            self.order_tree.heading(col, text=col.replace("_", " ").title())
            self.order_tree.column(col, anchor="center")
        
        # Vertical scrollbar
        vert_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.order_tree.yview)
        vert_scrollbar.pack(side="right", fill="y")
        
        # Horizontal scrollbar
        horiz_scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.order_tree.xview)
        horiz_scrollbar.pack(side="bottom", fill="x")
        
        # Configure scrollbars for the Treeview
        self.order_tree.configure(yscrollcommand=vert_scrollbar.set, xscrollcommand=horiz_scrollbar.set)
        self.order_tree.pack(fill="both", expand=True)
        
        # Load the current page of order data
        start_idx = self.current_order_page * self.order_page_size
        end_idx = start_idx + self.order_page_size
        for _, row in self.order_df.iloc[start_idx:end_idx].iterrows():
            self.order_tree.insert("", "end", values=list(row))

    def change_order_page(self, direction):
        # Change page based on the direction (-1 for previous, +1 for next)
        max_page = len(self.order_df) // self.order_page_size
        self.current_order_page = min(max(0, self.current_order_page + direction), max_page)
        
        # Refresh the displayed page
        self.display_order_page(self.order_tree.master)

    def export_order_report(self):
        # Export the order data to a CSV file
        self.order_df.to_csv("order_report.csv", index=False)
        messagebox.showinfo("Export Successful", "Order report exported to 'order_report.csv'")


    # -------------------- User Management Views --------------------
    
    def show_add_user_frame(self):
        # Create a main frame for the Add User view
        frame = ttk.Frame(self.content_frame)
        frame.pack(fill="both", expand=True)
        
        # Title label
        ttk.Label(frame, text="Add or Edit User", font=("Helvetica", 16)).pack(pady=20)
        
        # Frame for loading user
        load_user_frame = ttk.Frame(frame)
        load_user_frame.pack(fill="x", padx=10, pady=5)
        
        # User ID field to load existing user data
        ttk.Label(load_user_frame, text="User ID (Enter to Edit Existing User):").pack(side="left")
        user_id_var = StringVar()
        ttk.Entry(load_user_frame, textvariable=user_id_var).pack(side="left", padx=5)
        ttk.Button(load_user_frame, text="Load User", command=lambda: load_user(user_id_var)).pack(side="left", padx=5)
        
        # User details frame for input fields
        user_details_frame = ttk.LabelFrame(frame, text="User Details", padding=(10, 10))
        user_details_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Define variables for each user attribute
        username_var = StringVar()
        first_name_var = StringVar()
        last_name_var = StringVar()
        email_var = StringVar()
        user_type_var = StringVar()
        departname_var = StringVar()
        phone_var = StringVar()
        age_var = IntVar()
        max_hour_var = IntVar()
        reference_var = StringVar()
        student_status_var = StringVar()

        # User detail fields layout
        fields = [
            ("Username", username_var),
            ("First Name", first_name_var),
            ("Last Name", last_name_var),
            ("Email", email_var),
            ("User Type", user_type_var),
            ("Department", departname_var),
            ("Phone", phone_var),
            ("Age", age_var),
            ("Max Hour", max_hour_var),
            ("Reference", reference_var),
            ("Student Status", student_status_var),
        ]

        # Populate the details section with labels and entry widgets
        for i, (label_text, var) in enumerate(fields):
            ttk.Label(user_details_frame, text=label_text + ":").grid(row=i, column=0, sticky="e", padx=5, pady=2)
            ttk.Entry(user_details_frame, textvariable=var).grid(row=i, column=1, sticky="w", padx=5, pady=2)

        # Action buttons for Add and Update User
        actions_frame = ttk.Frame(frame)
        actions_frame.pack(pady=10)
        
        ttk.Button(actions_frame, text="Add User", command=lambda: add_user()).grid(row=0, column=0, padx=10)
        ttk.Button(actions_frame, text="Update User", command=lambda: update_user()).grid(row=0, column=1, padx=10)
        
        # Function to load existing user data
        def load_user(user_id_var):
            user_id = user_id_var.get()
            if user_id and user_id.isdigit():
                user_id = int(user_id)
                
                # Load data for testing purposes (use actual data loading in real app)
                dummy_data = {
                    1: {"user_id": 1, "username": "john_doe", "first_name": "John", "last_name": "Doe", 
                        "email": "john@example.com", "user_type": "student", "departname": "Computer Science", 
                        "phone": "1234567890", "age": 22, "max_hour": 40, "reference": "Prof. Smith", 
                        "student_status": "Active"},
                    2: {"user_id": 2, "username": "jane_doe", "first_name": "Jane", "last_name": "Doe", 
                        "email": "jane@example.com", "user_type": "staff", "departname": "Mathematics", 
                        "phone": "0987654321", "age": 30, "max_hour": 35, "reference": "Prof. Johnson", 
                        "student_status": "Inactive"},
                    # Add more dummy users as needed
                }
                
                if user_id in dummy_data:
                    user_data = dummy_data[user_id]
                    username_var.set(user_data["username"])
                    first_name_var.set(user_data["first_name"])
                    last_name_var.set(user_data["last_name"])
                    email_var.set(user_data["email"])
                    user_type_var.set(user_data["user_type"])
                    departname_var.set(user_data["departname"])
                    phone_var.set(user_data["phone"])
                    age_var.set(user_data["age"])
                    max_hour_var.set(user_data["max_hour"])
                    reference_var.set(user_data["reference"])
                    student_status_var.set(user_data["student_status"])
                else:
                    messagebox.showinfo("User Not Found", f"No user found with ID {user_id}")
            else:
                messagebox.showwarning("Invalid ID", "Please enter a valid user ID.")

        # Function to add a new user
        def add_user():
            # Collect user details and print or process them (use actual saving in real app)
            new_user_data = {
                "username": username_var.get(),
                "first_name": first_name_var.get(),
                "last_name": last_name_var.get(),
                "email": email_var.get(),
                "user_type": user_type_var.get(),
                "departname": departname_var.get(),
                "phone": phone_var.get(),
                "age": age_var.get(),
                "max_hour": max_hour_var.get(),
                "reference": reference_var.get(),
                "student_status": student_status_var.get(),
            }
            print("New user data:", new_user_data)
            messagebox.showinfo("User Added", "New user has been successfully added.")

        # Function to update existing user data
        def update_user():
            user_id = user_id_var.get()
            if user_id and user_id.isdigit():
                # Collect and print updated user data (use actual updating in real app)
                updated_user_data = {
                    "username": username_var.get(),
                    "first_name": first_name_var.get(),
                    "last_name": last_name_var.get(),
                    "email": email_var.get(),
                    "user_type": user_type_var.get(),
                    "departname": departname_var.get(),
                    "phone": phone_var.get(),
                    "age": age_var.get(),
                    "max_hour": max_hour_var.get(),
                    "reference": reference_var.get(),
                    "student_status": student_status_var.get(),
                }
                print("Updated user data:", updated_user_data)
                messagebox.showinfo("User Updated", "User has been successfully updated.")
            else:
                messagebox.showwarning("Update Error", "Please load a valid user to update.")

        # Display this frame
        self.show_frame(frame)


    def show_user_list_frame(self):
        # Create a new frame for the User List
        frame = ttk.Frame(self.content_frame)

        # Title for the report
        ttk.Label(frame, text="User List", font=("Helvetica", 16)).pack(pady=20)

        # Table frame for the report
        table_frame = ttk.Frame(frame)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Dummy data for user list (replace this with real data as needed)
        user_data = [
            {"user_id": i, "username": f"user_{i}", "first_name": f"First {i}", "last_name": f"Last {i}",
            "email": f"user{i}@example.com", "user_type": "student" if i % 2 == 0 else "teacher",
            "departname": "Computer Science", "phone": f"12345678{i}", "age": 20 + (i % 5), 
            "max_hour": 40, "reference": f"Prof. {i}", "student_status": "Active" if i % 2 == 0 else "Inactive"}
            for i in range(1, 31)  # 30 sample records
        ]

        # Convert dummy data to DataFrame for pagination and export purposes
        self.user_df = pd.DataFrame(user_data)

        # Display the first 15 rows initially
        self.current_page = 0
        self.page_size = 15
        self.display_user_page(table_frame)

        # Pagination controls
        pagination_frame = ttk.Frame(frame)
        pagination_frame.pack(pady=10)

        ttk.Button(pagination_frame, text="Previous", command=lambda: self.change_user_page(-1)).grid(row=0, column=0, padx=5)
        ttk.Button(pagination_frame, text="Next", command=lambda: self.change_user_page(1)).grid(row=0, column=1, padx=5)

        # Export button
        export_button = ttk.Button(frame, text="Export", command=self.export_user_report)
        export_button.pack(pady=10)

        # Home button to return to the welcome frame
        home_button = ttk.Button(frame, text="Home", command=self.show_welcome_message)
        home_button.pack(pady=10)

        # Display this frame
        self.show_frame(frame)

    def display_user_page(self, parent):
        # Clear existing table if any
        for widget in parent.winfo_children():
            widget.destroy()

        # Frame to hold the Treeview and scrollbars
        tree_frame = ttk.Frame(parent)
        tree_frame.pack(fill="both", expand=True)

        # Define columns for the Treeview
        columns = ("user_id", "username", "first_name", "last_name", "email", "user_type", "departname", "phone", "age", "max_hour", "reference", "student_status")
        self.user_tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=self.page_size)

        # Define column headings and set anchor to center
        for col in columns:
            self.user_tree.heading(col, text=col.replace("_", " ").title())
            self.user_tree.column(col, anchor="center")

        # Vertical scrollbar
        vert_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.user_tree.yview)
        vert_scrollbar.pack(side="right", fill="y")

        # Horizontal scrollbar
        horiz_scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.user_tree.xview)
        horiz_scrollbar.pack(side="bottom", fill="x")

        # Configure scrollbars for the Treeview
        self.user_tree.configure(yscrollcommand=vert_scrollbar.set, xscrollcommand=horiz_scrollbar.set)
        self.user_tree.pack(fill="both", expand=True)

        # Load the current page of user data
        start_idx = self.current_page * self.page_size
        end_idx = start_idx + self.page_size
        for _, row in self.user_df.iloc[start_idx:end_idx].iterrows():
            self.user_tree.insert("", "end", values=list(row))

    def change_user_page(self, direction):
        # Change page based on the direction (-1 for previous, +1 for next)
        max_page = len(self.user_df) // self.page_size
        self.current_page = min(max(0, self.current_page + direction), max_page)
        
        # Refresh the displayed page
        self.display_user_page(self.user_tree.master)

    def export_user_report(self):
        # Export the user data to a CSV file
        self.user_df.to_csv("user_report.csv", index=False)
        print("User report exported to 'user_report.csv'")


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

    def manage_order(self):
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
