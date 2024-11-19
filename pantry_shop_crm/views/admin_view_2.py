import tkinter as tk
from tkinter import ttk
import pandas as pd  # Import pandas for exporting data
from datetime import datetime,date,timedelta
from tkinter import messagebox,Tk, StringVar, IntVar,BooleanVar
from tkinter.simpledialog import askstring
import tkinter.messagebox as MessageBox
import os
from tkcalendar import DateEntry
from ttkthemes import ThemedTk



#----------- import session for id and role --------
from controllers import session
#----------- controllers imports -----------

from controllers.upfile_manager import UploadFileManager
from controllers.material_manager import MaterialManager
from controllers.vendor_manager import VendorManager  # Import VendorManager
from controllers.user_manager import UserManager
from controllers.order_manager import OrderManager
from controllers.pdf_manager import PDFManager
from controllers.dashboard import DashboardManager
from tkinter import Menu

class AdminView:
    def __init__(self, root, show_login_screen_callback):
        self.root = root
        self.show_login_screen_callback = show_login_screen_callback
        self.root.title("Admin Dashboard")
        self.root.geometry("1150x675")
        self.current_frame = None

        self.create_admin_menu()  # Setup the menu
        self.create_admin_dashboard()  # Setup the dashboard with frames and buttons

    def create_admin_menu(self):
        # Create a style object for the menu
        style = ttk.Style()

        # Define a custom style for the Menu items (applied to the root window)
        style.configure("TMenu", background="#333", foreground="#FFF", font=("Helvetica", 10))
        style.map("TMenu", background=[('active', '#002bb2')])  # Active background color for Menu items

        # Create the menu bar
        menu_bar = tk.Menu(self.root, bg="#333", fg="#FFF", font=("Helvetica", 10))

        # Material Management menu
        material_menu = tk.Menu(menu_bar, tearoff=0, bg="#333", fg="#FFF", activebackground="#002bb2")
        material_menu.add_command(label="Upload Material", command=self.show_upload_material_frame)
        material_menu.add_command(label="Create & Update Material", command=self.show_create_material_frame)
        material_menu.add_command(label="View Material Report", command=self.show_view_material_report_frame)
        material_menu.add_command(label="Create Material type", command=self.show_create_material_type_frame)  # Fixed reference
        menu_bar.add_cascade(label="Material Management", menu=material_menu)

        # Vendor Management menu
        vendor_menu = tk.Menu(menu_bar, tearoff=0, bg="#333", fg="#FFF", activebackground="#002bb2")
        vendor_menu.add_command(label="Add & Update Vendor", command=self.show_add_vendor_frame)
        vendor_menu.add_command(label="Vendor Report", command=self.show_vendor_report_frame)
        menu_bar.add_cascade(label="Vendor Management", menu=vendor_menu)

        # Stock Management menu
        stock_menu = tk.Menu(menu_bar, tearoff=0, bg="#333", fg="#FFF", activebackground="#002bb2")
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
        user_menu.add_command(label="Add & Update User", command=self.show_add_user_frame)
        user_menu.add_command(label="View User List", command=self.show_user_list_frame)
        menu_bar.add_cascade(label="User Management", menu=user_menu)

        # Logout option in the menu
        logout_menu = tk.Menu(menu_bar, tearoff=0, bg="#333", fg="#FFF", activebackground="#002bb2")
        logout_menu.add_command(label="Logout", command=self.logout)
        menu_bar.add_cascade(label="Logout", menu=logout_menu)

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
        """Display a welcome message with a compact grid of count cards and visualizations.""" 
        welcome_frame = ttk.Frame(self.content_frame)
        welcome_frame.pack(fill="both", expand=True, padx=20, pady=2)

        # Display the welcome label at the top
        ttk.Label(welcome_frame, text=f"Welcome to {session.user_name}'s Dashboard", font=("Helvetica", 16)).pack(pady=2)

        # Create a DashboardManager instance to fetch data
        dashboard_manager = DashboardManager()

        # Fetch all necessary data
        data = dashboard_manager.get_order_counts()
        material_counts = dashboard_manager.get_material_counts()
        user_count = dashboard_manager.get_user_count()
        vendor_count = dashboard_manager.get_vendor_count()
        stock_products = dashboard_manager.get_stock_products()

        # ------------------- Row 1: Stats -------------------
        stats_frame = ttk.Frame(welcome_frame)
        stats_frame.pack(fill="both", expand=True)

        # Create a 2x4 grid for the first two rows (count cards)
        for i in range(4):
            stats_frame.grid_columnconfigure(i, weight=1, minsize=150)

        # ------------------- Row 1 Cards -------------------
        # Total Orders
        self.create_card(stats_frame, "Total Orders", data['total_orders'], 0, 0)

        # Approved Orders
        self.create_card(stats_frame, "Approved Orders", data['approved_orders'], 0, 1)

        # Pending Orders
        self.create_card(stats_frame, "Pending Orders", data['pending_orders'], 0, 2)

        # Total Materials
        self.create_card(stats_frame, "Total Materials", material_counts['total_materials'], 0, 3)

        # ------------------- Row 2: Material Stats -------------------
        material_frame = ttk.Frame(welcome_frame)
        material_frame.pack(fill="both", expand=True)

        for i in range(4):
            material_frame.grid_columnconfigure(i, weight=1, minsize=150)

        # ------------------- Row 2 Cards -------------------
        # Active Materials
        self.create_card(material_frame, "Active Materials", material_counts['active_materials'], 1, 0)

        # Inactive Materials
        self.create_card(material_frame, "Inactive Materials", material_counts['inactive_materials'], 1, 1)

        # Total Users
        self.create_card(material_frame, "Total Users", user_count['total_users'], 1, 2)

        # Total Vendors
        self.create_card(material_frame, "Total Vendors", vendor_count['total_vendors'], 1, 3)

        # ------------------- Row 3: Donut Charts -------------------
        chart_frame = ttk.Frame(welcome_frame)
        chart_frame.pack(fill="both", expand=True)

        chart_frame.grid_columnconfigure(0, weight=1)
        chart_frame.grid_columnconfigure(1, weight=1)
        chart_frame.grid_columnconfigure(2, weight=1)

        # Plot Donut Chart 1: Order Status Distribution
        dashboard_manager.plot_order_donut(chart_frame, data["approved_orders"], data["pending_orders"], data["total_orders"], 0)

        # Plot Donut Chart 2: Material Status Distribution
        dashboard_manager.plot_material_donut(chart_frame, material_counts["active_materials"], material_counts["inactive_materials"], material_counts["total_materials"], 1)

        # ------------------- Row 4: Bar Charts -------------------
        bar_chart_frame = ttk.Frame(welcome_frame)
        bar_chart_frame.pack(fill="both", expand=True)

        bar_chart_frame.grid_columnconfigure(0, weight=1)
        bar_chart_frame.grid_columnconfigure(1, weight=1)
        bar_chart_frame.grid_columnconfigure(2, weight=1)

        # Plot Bar Chart 1: Least Stock Products
        dashboard_manager.plot_least_stock_materials(bar_chart_frame, stock_products["least_stock_materials"], 0)

        # Plot Bar Chart 2: Max Stock Products
        dashboard_manager.plot_max_stock_materials(bar_chart_frame, stock_products["max_stock_materials"], 1)

        # Show the final welcome_frame
        self.show_frame(welcome_frame)


    def create_card(self, parent, title, count, row, column):
        # Create a style for the card
        style = ttk.Style()
        style.configure("Card.TFrame", 
                        relief="raised", 
                        background="#f9f9f9",  # Light background for card
                        padding=10)
        """Create a card-like effect for displaying counts."""
        card_frame = ttk.Frame(parent, style="Card.TFrame",padding=10)
        card_frame.grid(row=row, column=column, padx=10, pady=10, sticky="nsew")

        # Set a background color for the card (you can adjust the color as needed)
        card_frame.configure(style="Card.TFrame")

        # Add the title label
        ttk.Label(card_frame, text=title, font=("Helvetica", 10, "bold"), anchor="center").pack()

        # Add the count label with larger font size
        ttk.Label(card_frame, text=str(count), font=("Helvetica", 16, "bold"), anchor="center",foreground="#007bff").pack()

        return card_frame










#--------------------------------------------------------------------
# -------------------- Material Management Views --------------------
#--------------------------------------------------------------------

#..... Material Menu  Frame-1 .....

    def show_upload_material_frame(self):
        # Clear any existing content and create a new frame
        frame = ttk.Frame(self.content_frame)
        
        # Title for the upload section
        ttk.Label(frame, text="Upload Material", font=("Helvetica", 16)).pack(pady=20)
        
        # Entry field for the file path
        # Entry field for the file path
        self.file_path_entry = ttk.Entry(frame, width=40)
        self.file_path_entry.pack(pady=5, padx=10)

        # Button to select file and display the file path in the entry field
        def select_file():
            from tkinter import filedialog
            file_path = filedialog.askopenfilename(title="Select a File", filetypes=[("All Files", "*.*")])
            self.file_path_entry.delete(0, tk.END)
            self.file_path_entry.insert(0, file_path)

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


#..... Material Menu  Frame-2 .....


    def show_create_material_frame(self):
        # Create a main frame for the Add or Edit Material view
        frame = ttk.Frame(self.content_frame)
        frame.pack(fill="both", expand=True)
        
        # Title label
        ttk.Label(frame, text="Add or Edit Material", font=("Helvetica", 16)).pack(pady=20)
        
        # Frame for loading material
        load_material_frame = ttk.Frame(frame)
        load_material_frame.pack(fill="x", padx=10, pady=5)
        
        # Material ID field to load existing material data
        ttk.Label(load_material_frame, text="Material ID (Enter to Edit Existing Material):").pack(side="left")
        material_id_var = StringVar()
        ttk.Entry(load_material_frame, textvariable=material_id_var).pack(side="left", padx=5)
        ttk.Button(load_material_frame, text="Load Material", command=lambda: load_material(material_id_var)).pack(side="left", padx=5)
        

        
        # Material details frame for input fields
        material_details_frame = ttk.LabelFrame(frame, text="Material Details", padding=(10, 10))
        material_details_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Define variables for each material attribute
        material_id_var2 = StringVar()
        material_name_var = StringVar()
        material_type_var = StringVar()
        description_var = StringVar()
        current_stock_var = StringVar()
        status_var = StringVar(value="Inactive")
        created_date_var = StringVar(value=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        created_by_var = StringVar(value=session.user_id)
        vendorid_var = StringVar()

        # Initialize MaterialManager
        material_manager = MaterialManager()

        # Fetch material types for the dropdown menu
        material_types = material_manager.get_material_types()
        
        if material_types:
            material_types.insert(0, "Select Type")
            material_type_var.set(material_types[0])  # Set the first type as default if available

        vendorids = material_manager.get_vendor_ids()
        if vendorids:
            vendorids.insert(0, "Select VendorID")
            vendorid_var.set(vendorids[0])  # Set the first type as default if available

        # Material detail fields layout - adjust positions to avoid overlapping
        fields = [
            ("Material Id", material_id_var2),
            ("Material Name", material_name_var),
            ("Description", description_var),
            ("Current Stock", current_stock_var),
            ("Created Date", created_date_var),
            ("Created By", created_by_var),
        ]
                    # ("Status", status_var),

        # Populate the details section with labels and entry widgets
        for i, (label_text, var) in enumerate(fields):
            # Adjust row positions to skip the Material Type row
            row_position = i + 1 if i >= 1 else i
            ttk.Label(material_details_frame, text=label_text + ":").grid(row=row_position, column=0, sticky="e", padx=5, pady=2)
            entry_state = "readonly" if label_text in ["Created Date", "Created By"] else "normal"
            ttk.Entry(material_details_frame, textvariable=var, state=entry_state).grid(row=row_position, column=1, sticky="w", padx=5, pady=2)

        # Material Type - Dropdown field on its dedicated row
        ttk.Label(material_details_frame, text="Material Type:").grid(row=1, column=0, sticky="e", padx=5, pady=2)
        material_type_dropdown = ttk.OptionMenu(material_details_frame, material_type_var, *material_types)
        material_type_dropdown.grid(row=1, column=1, sticky="w", padx=5, pady=2)

        # Material Type - Dropdown field on its dedicated row
        ttk.Label(material_details_frame, text="Vendor:").grid(row=7, column=0, sticky="e", padx=5, pady=2)
        material_type_dropdown = ttk.OptionMenu(material_details_frame, vendorid_var, *vendorids)
        material_type_dropdown.grid(row=7, column=1, sticky="w", padx=5, pady=2)

        # Status - Dropdown field with 'Active' and 'Inactive' options, defaulting to 'Inactive'
        ttk.Label(material_details_frame, text="Status:").grid(row=8, column=0, sticky="e", padx=5, pady=2)
        # status_var.set("Inactive")  # Set default value to 'Inactive'
        status_dropdown = ttk.OptionMenu(material_details_frame, status_var, "Inactive", "Active", "Inactive")
        status_dropdown.grid(row=8, column=1, sticky="w", padx=5, pady=2)

        # Clear the entries
        def clear_material_fields():
            material_id_var2.set("")
            material_name_var.set("")
            material_type_var.set("")
            description_var.set("")
            current_stock_var.set("")
            status_var.set("Inactive")
            created_date_var.set(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            created_by_var.set(session.user_id)
            vendorid_var.set("")

        # Function to load existing material data
        def load_material(material_id_var):
            material_id = material_id_var.get()
            print(material_id)

            if material_id.isdigit():
                material_data = material_manager.load_material(material_id)
                print(material_data)
                if material_data:
                    material_id_var2.set(material_data["material_id"])
                    material_name_var.set(material_data["material_name"])
                    material_type_var.set(material_data["material_type"])
                    description_var.set(material_data["description"])
                    current_stock_var.set(material_data["current_stock"])
                    status_var.set(material_data["status"])
                    created_date_var.set(material_data["created_date"])
                    created_by_var.set(material_data["created_by"])
                    vendorid_var.set(material_data["vendor_id"])
                else:
                    messagebox.showinfo("Material Not Found", f"No material found with ID {material_id}")
            else:
                messagebox.showwarning("Invalid ID", "Please enter a valid material ID.")

        # Function to add a new material
        def add_material():
            new_material_data = {
                "material_id": material_id_var2.get(),  # Automatically generated in most cases
                "material_name": material_name_var.get(),
                "material_type": material_type_var.get(),
                "description": description_var.get(),
                "current_stock": current_stock_var.get(),
                "status": status_var.get(),
                "created_date": created_date_var.get(),
                "created_by": session.user_id,
                "vendor_id": vendorid_var.get()
            }
            material_manager.add_material(new_material_data)
            clear_material_fields()

        # Function to update existing material data
        def update_material():
            material_id = material_id_var.get()
            if material_id and material_id.isdigit():
                updated_material_data = {
                    "material_name": material_name_var.get(),
                    "material_type": material_type_var.get(),
                    "description": description_var.get(),
                    "current_stock": current_stock_var.get(),
                    "status": status_var.get(),
                    "created_date": created_date_var.get(),
                    "created_by": created_by_var.get(),
                    "vendor_id": vendorid_var.get(),
                }
                material_manager.update_material(material_id, updated_material_data)
                clear_material_fields()
            else:
                messagebox.showwarning("Update Error", "Please load a valid material to update.")

        # Action buttons for Add and Update Material
        actions_frame = ttk.Frame(frame)
        actions_frame.pack(pady=10)
        
        ttk.Button(actions_frame, text="Add Material", command=add_material).grid(row=0, column=0, padx=10)
        ttk.Button(actions_frame, text="Update Material", command=update_material).grid(row=0, column=1, padx=10)
        ttk.Button(actions_frame, text="Home", command=self.show_welcome_message).grid(row=0, column=2, padx=10)

        # Display this frame
        self.show_frame(frame)





#..... Material Menu  Frame-3 .....

    def fetch_material(self):
        material_manager = MaterialManager()
        material_data = material_manager.get_all_materials()

        if material_data["success"]:
            # print(material_data)
            return material_data["data"]
        else:
            return []

    def show_view_material_report_frame(self):
        # Create a new frame for the Material Report
        frame = ttk.Frame(self.content_frame)

        # Title for the report
        ttk.Label(frame, text="Material Report", font=("Helvetica", 16)).pack(pady=20)

        # Table frame for the report
        table_frame = ttk.Frame(frame)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Dummy data for material report (replace this with real data as needed)
        # material_data = [
        #     {"material_id": i, "material_name": f"Material {i}", "material_type": "Type A" if i % 2 == 0 else "Type B",
        #     "current_stock": 100 + i, "status": "Active" if i % 2 == 0 else "Inactive"}
        #     for i in range(1, 31)  # 30 sample records
        # ]
        
        material_data = self.fetch_material()
  


        # Convert dummy data to DataFrame for pagination and export purposes
        self.columns = ["material_id", "material_name", "material_type", "description", "current_stock", "status", "created_date", "created_by"]
        self.material_df = pd.DataFrame(material_data,columns=self.columns)

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
        ttk.Button(pagination_frame, text="Export", command=self.export_material_report).grid(row=0, column=2, padx=5)


        # Home button to return to the welcome frame
        ttk.Button(pagination_frame, text="Home", command=self.show_welcome_message).grid(row=0, column=3, padx=5)


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
        columns = ("material_id", "material_name", "material_type","description", "current_stock", "status","created_date","created_by")
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


#..... Material Menu  Frame-4 .....

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

        # # Created By entry
        # ttk.Label(form_frame, text="Created By:").grid(row=4, column=0, sticky="w", padx=5, pady=5)
        # self.created_by_entry = ttk.Entry(form_frame)
        # self.created_by_entry.grid(row=4, column=1, padx=5, pady=5)

        # "Create Material Type" button
        create_button = ttk.Button(frame, text="Create Material Type", command=self.create_material_type_handler)
        create_button.pack(pady=10)

        # Home button to return to the welcome frame
        home_button = ttk.Button(frame, text="Home", command=self.show_welcome_message)
        home_button.pack(pady=10)

        # Display this frame
        self.show_frame(frame)



# -------------------- Action Methods -------------------------------
#--------------------- Material Manager -----------------------------


    def upload_material(self):
        # Get the file path from the entry field
        file_path = self.file_path_entry.get()
        
        if not file_path:
            messagebox.showerror("Error", "Please select a file to upload.")
            return

        # Instantiate the UploadFileManager and upload the file
        manager = UploadFileManager()
        result = manager.upload_materials(file_path)
        
        # Show a success or error message based on the result
        if "successfully" in result:
            messagebox.showinfo("Success", result)
        else:
            messagebox.showerror("Error", result)

#------------------------------- Material create -----------------------------

    def clear_materials_fields(self):
        # Loop through each field and clear the entry values
        self.fields["Material Name"].delete(0, "end")
        self.fields["Material Type"].set("")  # Clear the dropdown selection
        self.fields["Description"].delete(0, "end")
        self.fields["Current Stock"].delete(0, "end")
        self.fields["Status"].set("Inactive")  # Reset to default status
        self.fields["Created Date"].config(state="normal")
        self.fields["Created Date"].delete(0, "end")
        self.fields["Created Date"].insert(0, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        self.fields["Created Date"].config(state="readonly")
        self.fields["Created By"].config(state="normal")
        self.fields["Created By"].delete(0, "end")
        self.fields["Created By"].insert(0, session.user_id)  # Reset to current user ID
        self.fields["Created By"].config(state="readonly")


    def create_material(self):
        material_data = {
        "material_name": self.fields["Material Name"].get(),
        "material_type": self.fields["Material Type"].get(),
        "description": self.fields["Description"].get(),
        "current_stock": self.fields["Current Stock"].get(),
        "status": self.fields["Status"].get(),
        "created_date": self.fields["Created Date"].get(),
        "created_by": self.fields["Created By"].get()}



        print(material_data)

        # Call signup manager to handle signup
        manager = MaterialManager()
        result = manager.create_material(material_data)
        
        # Display success or error message
        if result["success"]:
            messagebox.showinfo("Create Material", result["message"])
            # self.show_welcome_message()
            self.clear_materials_fields()
        else:
            messagebox.showerror("Error", result["message"])

#----------------------------- Export Materials to csv -----------------------------
    def export_material_report(self):
        # Get the current timestamp to append to the filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Define the file paths
        data_folder_path = os.path.join(os.path.expanduser("~"), "Desktop", "Data", f"material_report_{timestamp}.csv")

        try:
            # Ensure the Data folder exists, if not, create it
            os.makedirs(os.path.dirname(data_folder_path), exist_ok=True)

            # Export to both locations
            self.material_df.to_csv(data_folder_path, index=False)

            # Show a message box indicating success
            MessageBox.showinfo("Export Success", f"Location: {data_folder_path}")

        except Exception as e:
            # Show error message if something goes wrong
            MessageBox.showerror("Export Failed", f"An error occurred while exporting the material report: {str(e)}")




#----------------------------------------- Material Type creation Done ------------------------------

    def clear_material_type_fields(self):
        # Clear each entry field by deleting its content from the start to the end
        self.material_type_id_entry.delete(0, tk.END)
        self.material_type_entry.delete(0, tk.END)
        self.material_desc_entry.delete(0, tk.END)
        self.created_date_entry.delete(0, tk.END)


    def create_material_type_handler(self):

        materialtype_data = {
            "material_type_id": self.material_type_id_entry.get(),
            "material_type": self.material_type_entry.get(),
            "material_desc": self.material_desc_entry.get(),
            "created_date": self.created_date_entry.get(),
            "created_by": session.user_id}


        print(materialtype_data)

        # Call signup manager to handle signup
        manager = MaterialManager()
        result = manager.save_material_type(materialtype_data)
        
        # Display success or error message
        if result["success"]:
            messagebox.showinfo("Material Type", result["message"])
            # self.show_welcome_message()
            self.clear_material_type_fields()
        else:
            messagebox.showerror("Error", result["message"])

#--------------------------------------------------------------------
# -------------------- Vendor Management Views --------------------
#--------------------------------------------------------------------

#..... Vendor Menu  Frame-1 .....


    def show_add_vendor_frame(self):
        # Create a main frame for the Add or Edit Vendor view
        frame = ttk.Frame(self.content_frame)
        frame.pack(fill="both", expand=True)
        
        # Title label
        ttk.Label(frame, text="Add or Edit Vendor", font=("Helvetica", 16)).pack(pady=20)
        
        # Frame for loading vendor
        load_vendor_frame = ttk.Frame(frame)
        load_vendor_frame.pack(fill="x", padx=10, pady=5)
        
        # Vendor ID field to load existing vendor data
        ttk.Label(load_vendor_frame, text="Vendor ID (Enter to Edit Existing Vendor):").pack(side="left")
        vendor_id_var = StringVar()
        ttk.Entry(load_vendor_frame, textvariable=vendor_id_var).pack(side="left", padx=5)
        ttk.Button(load_vendor_frame, text="Load Vendor", command=lambda: load_vendor(vendor_id_var)).pack(side="left", padx=5)
        
        # Vendor details frame for input fields
        vendor_details_frame = ttk.LabelFrame(frame, text="Vendor Details", padding=(10, 10))
        vendor_details_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Define variables for each vendor attribute
        vendor_name_var = StringVar()
        contact_fname_var = StringVar()
        contact_lname_var = StringVar()
        contact_email_var = StringVar()
        contact_phone_var = StringVar()
        address_key_var = StringVar()
        is_active_var = tk.BooleanVar()
        created_by_var = StringVar()

        # Vendor detail fields layout
        fields = [
            ("Vendor Name", vendor_name_var),
            ("Contact First Name", contact_fname_var),
            ("Contact Last Name", contact_lname_var),
            ("Contact Email", contact_email_var),
            ("Contact Phone", contact_phone_var),
            ("Address Key", address_key_var),
            ("Created By", created_by_var),
        ]

        # Populate the details section with labels and entry widgets
        for i, (label_text, var) in enumerate(fields):
            ttk.Label(vendor_details_frame, text=label_text + ":").grid(row=i, column=0, sticky="e", padx=5, pady=2)
            ttk.Entry(vendor_details_frame, textvariable=var).grid(row=i, column=1, sticky="w", padx=5, pady=2)


        ttk.Entry(vendor_details_frame, textvariable=created_by_var, state="readonly").grid(row=i, column=1, sticky="w", padx=5, pady=2)


        # Is Active checkbox
        ttk.Checkbutton(vendor_details_frame, text="Is Active", variable=is_active_var).grid(row=len(fields), column=1, sticky="w", padx=5, pady=2)

        # Created Date field (read-only, auto-populated with current date)
        created_date_var = StringVar(value=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        ttk.Label(vendor_details_frame, text="Created Date:").grid(row=len(fields) + 1, column=0, sticky="e", padx=5, pady=2)
        ttk.Entry(vendor_details_frame, textvariable=created_date_var, state="readonly").grid(row=len(fields) + 1, column=1, sticky="w", padx=5, pady=2)

        # Action buttons for Add and Update Vendor
        actions_frame = ttk.Frame(frame)
        actions_frame.pack(pady=10)
        
        ttk.Button(actions_frame, text="Add Vendor", command=lambda: add_vendor()).grid(row=0, column=0, padx=10)
        ttk.Button(actions_frame, text="Update Vendor", command=lambda: update_vendor()).grid(row=0, column=1, padx=10)
        ttk.Button(actions_frame, text="Home", command=self.show_welcome_message).grid(row=0, column=2, padx=10)

        # Initialize VendorManager
        vendor_manager = VendorManager()

        # Clear the entrys
        def clear_vendor_fields():
            vendor_name_var.set("")
            contact_fname_var.set("")
            contact_lname_var.set("")
            contact_email_var.set("")
            contact_phone_var.set("")
            address_key_var.set("")
            is_active_var.set(False)
            created_by_var.set("")
            created_date_var.set(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        # Function to load existing vendor data
        def load_vendor(vendor_id_var):
            vendor_id = vendor_id_var.get()
            if vendor_id.isdigit():
                vendor_data = vendor_manager.load_vendor(vendor_id)
                if vendor_data:
                    vendor_name_var.set(vendor_data["vendor_name"])
                    contact_fname_var.set(vendor_data["contact_fname"])
                    contact_lname_var.set(vendor_data["contact_lname"])
                    contact_email_var.set(vendor_data["contact_email"])
                    contact_phone_var.set(vendor_data["contact_phone"])
                    address_key_var.set(vendor_data["address_key"])
                    is_active_var.set(vendor_data["is_active"])
                    created_by_var.set(vendor_data["created_by"])
                else:
                    messagebox.showinfo("Vendor Not Found", f"No vendor found with ID {vendor_id}")
            else:
                messagebox.showwarning("Invalid ID", "Please enter a valid vendor ID.")

        # Function to add a new vendor
        def add_vendor():
            new_vendor_data = {
                "vendor_id": None,  # Automatically generated in most cases
                "vendor_name": vendor_name_var.get(),
                "contact_fname": contact_fname_var.get(),
                "contact_lname": contact_lname_var.get(),
                "contact_email": contact_email_var.get(),
                "contact_phone": contact_phone_var.get(),
                "address_key": address_key_var.get(),
                "is_active": is_active_var.get(),
                "created_by": session.user_id,
            }
            vendor_manager.add_vendor(new_vendor_data)
            clear_vendor_fields()

        # Function to update existing vendor data
        def update_vendor():
            vendor_id = vendor_id_var.get()
            if vendor_id and vendor_id.isdigit():
                updated_vendor_data = {
                    "vendor_name": vendor_name_var.get(),
                    "contact_fname": contact_fname_var.get(),
                    "contact_lname": contact_lname_var.get(),
                    "contact_email": contact_email_var.get(),
                    "contact_phone": contact_phone_var.get(),
                    "address_key": address_key_var.get(),
                    "is_active": is_active_var.get(),
                    "created_by": created_by_var.get(),
                }
                vendor_manager.update_vendor(vendor_id, updated_vendor_data)
                clear_vendor_fields()
            else:
                messagebox.showwarning("Update Error", "Please load a valid vendor to update.")

        # Display this frame
        self.show_frame(frame)


#..... Vendor Menu  Frame-2 .....




    def show_vendor_report_frame(self):
        # Create a new frame for the Vendor Report
        frame = ttk.Frame(self.content_frame)

        # Title for the report
        ttk.Label(frame, text="Vendor Report", font=("Helvetica", 16)).pack(pady=20)

        # Table frame for the report
        table_frame = ttk.Frame(frame)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # # Dummy vendor data (replace this with real data as needed)
        # vendor_data = [
        #     {"vendor_id": 1, "vendor_name": "Vendor A", "contact_fname": "John", "contact_lname": "Doe",
        #      "contact_email": "john@example.com", "contact_phone": "1234567890", "is_active": True, "created_date": "2024-01-01"},
        #     {"vendor_id": 2, "vendor_name": "Vendor B", "contact_fname": "Jane", "contact_lname": "Doe",
        #      "contact_email": "jane@example.com", "contact_phone": "0987654321", "is_active": False, "created_date": "2024-01-02"},
        #     # Add more records as needed
        # ]
        
        vendor_data = self.fetch_vendors()

        
        self.columns = ["vendor_id","vendor_name","contact_fname","contact_lname","contact_email","contact_phone","address_key","is_active","created_date","created_by"]

        # Convert dummy data to DataFrame for pagination and export purposes
        self.vendor_df = pd.DataFrame(vendor_data,columns = self.columns)

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
        ttk.Button(pagination_frame, text="Export", command=self.export_vendor_report).grid(row=0, column=2, padx=5)


        # Home button to return to the welcome frame
        ttk.Button(pagination_frame, text="Home", command=self.show_welcome_message).grid(row=0, column=3, padx=5)


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
        columns = ("vendor_id","vendor_name","contact_fname","contact_lname","contact_email","contact_phone","address_key","is_active","created_date","created_by")
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

# -------------------- Action Methods -------------------------------
#--------------------- Vendor Manager -------------------------------


    def fetch_vendors(self):
        vendor_manager = VendorManager()
        vendor_data = vendor_manager.get_all_vendors()

        if vendor_data["success"]:
            # print(material_data)
            return vendor_data["data"]
        else:
            return []


    def export_vendor_report(self):
        # Get the current timestamp to append to the filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Define the file paths
        data_folder_path = os.path.join(os.path.expanduser("~"), "Desktop", "Data", f"Vendor_report_{timestamp}.csv")

        try:
            # Ensure the Data folder exists, if not, create it
            os.makedirs(os.path.dirname(data_folder_path), exist_ok=True)

            # Export to both locations
            self.vendor_df.to_csv(data_folder_path, index=False)

            # Show a message box indicating success
            MessageBox.showinfo("Export Success", f"Location: {data_folder_path}")

        except Exception as e:
            # Show error message if something goes wrong
            MessageBox.showerror("Export Failed", f"An error occurred while exporting the material report: {str(e)}")


#--------------------------------------------------------------------
# -------------------- Stock Management Views --------------------
#--------------------------------------------------------------------




#..... Stock Menu  Frame-1 .....

    def show_update_stock_frame(self):
        # Create a new frame for updating stock
        # Create a main frame for the Add or Edit Material view
        frame = ttk.Frame(self.content_frame)
        frame.pack(fill="both", expand=True)
        
        # Title label
        ttk.Label(frame, text="Update Stock", font=("Helvetica", 16)).pack(pady=20)
        
        # Frame for loading material
        load_material_frame = ttk.Frame(frame)
        load_material_frame.pack(fill="x", padx=10, pady=5)
        
        # Material ID field to load existing material data
        ttk.Label(load_material_frame, text="Material ID (Enter to Edit Existing Material):").pack(side="left")
        material_id_var = StringVar()
        ttk.Entry(load_material_frame, textvariable=material_id_var).pack(side="left", padx=5)
        ttk.Button(load_material_frame, text="Load Material", command=lambda: load_material(material_id_var)).pack(side="left", padx=5)
        

        
        # Material details frame for input fields
        material_details_frame = ttk.LabelFrame(frame, text="Stock Details", padding=(10, 10))
        material_details_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Define variables for each material attribute
        material_name_var = StringVar()
        description_var = StringVar()
        current_stock_var = StringVar()

        material_manager = MaterialManager()

        fields = [
            ("Material Name", material_name_var),
            ("Description", description_var),
            ("Current Stock", current_stock_var),
        ]

        # Populate the details section with labels and entry widgets
        for i, (label_text, var) in enumerate(fields):
            # Adjust row positions to skip the Material Type row
            row_position = i + 1 if i >= 1 else i
            ttk.Label(material_details_frame, text=label_text + ":").grid(row=row_position, column=0, sticky="e", padx=5, pady=2)
            entry_state = "readonly" if label_text in ["Material Name", "Description",] else "normal"
            ttk.Entry(material_details_frame, textvariable=var, state=entry_state).grid(row=row_position, column=1, sticky="w", padx=5, pady=2)

        # Clear the entries
        def clear_material_fields():
            material_id_var.set("")
            material_name_var.set("")
            description_var.set("")
            current_stock_var.set("")


        # Function to load existing material data
        def load_material(material_id_var):
            material_id = material_id_var.get()
            if material_id.isdigit():
                material_data = material_manager.load_material(material_id)
                print(material_data)
                if material_data:
                    material_name_var.set(material_data["material_name"])
                    description_var.set(material_data["description"])
                    current_stock_var.set(material_data["current_stock"])
                else:
                    messagebox.showinfo("Material Not Found", f"No material found with ID {material_id}")
            else:
                messagebox.showwarning("Invalid ID", "Please enter a valid material ID.")


        def update_material2():
            material_id = material_id_var.get()
            if material_id and material_id.isdigit():
                updated_material_data = {
                    "current_stock": current_stock_var.get()  # Ensure this is a valid numeric value
                }
                material_manager.update_stock(int(material_id), updated_material_data)
                clear_material_fields()
            else:
                messagebox.showwarning("Update Error", "Please load a valid material to update.")


        # Action buttons for Add and Update Material
        actions_frame = ttk.Frame(frame)
        actions_frame.pack(pady=10)
        
        ttk.Button(actions_frame, text="Update Stock", command=update_material2).grid(row=0, column=0, padx=10)
        ttk.Button(actions_frame, text="Home", command=self.show_welcome_message).grid(row=0, column=1, padx=10)

        # Display this frame
        self.show_frame(frame)





#..... Stock Menu  Frame-3 .....


    def show_stock_report_frame(self):
        # Create a new frame for the Stock Report
        frame = ttk.Frame(self.content_frame)

        # Title for the report
        ttk.Label(frame, text="Stock Report", font=("Helvetica", 16)).pack(pady=20)

        # Table frame for the report
        table_frame = ttk.Frame(frame)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        
        material_data = self.fetch_material()
        filtered_material_data = [tuple(row[i] for i in [0, 1, 2, 3, 4, 5]) for row in material_data]
  


        # Convert dummy data to DataFrame for pagination and export purposes
        self.columns = ["material_id", "material_name", "material_type", "description", "current_stock", "status",]
        self.stock_df = pd.DataFrame(filtered_material_data,columns=self.columns)

        # Display the first 15 rows initially
        self.current_page = 0
        self.page_size = 15
        self.display_stock_page2(table_frame)

        # Pagination controls
        pagination_frame = ttk.Frame(frame)
        pagination_frame.pack(pady=10)

        ttk.Button(pagination_frame, text="Previous", command=lambda: self.change_material_page2(-1)).grid(row=0, column=0, padx=5)
        ttk.Button(pagination_frame, text="Next", command=lambda: self.change_material_page2(1)).grid(row=0, column=1, padx=5)

        # Export button
        ttk.Button(pagination_frame, text="Export", command=self.export_stock_report).grid(row=0, column=2, padx=5)


        # Home button to return to the welcome frame
        ttk.Button(pagination_frame, text="Home", command=self.show_welcome_message).grid(row=0, column=3, padx=5)


        # Display this frame
        self.show_frame(frame)

    def display_stock_page2(self, parent):
        # Clear existing table if any
        for widget in parent.winfo_children():
            widget.destroy()

        # Frame to hold the Treeview and scrollbars
        tree_frame = ttk.Frame(parent)
        tree_frame.pack(fill="both", expand=True)

        # Define columns for the Treeview
        columns = ("material_id", "material_name", "material_type","description", "current_stock", "status")
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
        for _, row in self.stock_df.iloc[start_idx:end_idx].iterrows():
            self.material_tree.insert("", "end", values=list(row))

    def change_material_page2(self, direction):
        # Change page based on the direction (-1 for previous, +1 for next)
        max_page = len(self.material_df) // self.page_size
        self.current_page = min(max(0, self.current_page + direction), max_page)
        
        # Refresh the displayed page
        self.display_stock_page2(self.material_tree.master)


    def export_stock_report(self):
        # Get the current timestamp to append to the filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Define the file paths
        data_folder_path = os.path.join(os.path.expanduser("~"), "Desktop", "Data", f"Stock_report_{timestamp}.csv")

        try:
            # Ensure the Data folder exists, if not, create it
            os.makedirs(os.path.dirname(data_folder_path), exist_ok=True)

            # Export to both locations
            self.stock_df.to_csv(data_folder_path, index=False)

            # Show a message box indicating success
            MessageBox.showinfo("Export Success", f"Location: {data_folder_path}")

        except Exception as e:
            # Show error message if something goes wrong
            MessageBox.showerror("Export Failed", f"An error occurred while exporting the Stock report: {str(e)}")





#--------------------------------------------------------------------
# -------------------- Order Management Views --------------------
#--------------------------------------------------------------------

#..... Order Menu  Frame-1 .....

    def show_manage_order_frame(self):
            # Create a new frame for Order Report
            frame = ttk.Frame(self.content_frame)
            
            # Title for the report
            ttk.Label(frame, text="Manage Order", font=("Helvetica", 16)).pack(pady=20)
            
            # Create a frame for the date pickers (start and end dates)
            date_frame = ttk.Frame(frame)
            date_frame.pack(pady=10)
            
            # Label and Date Picker for Start Date
            ttk.Label(date_frame, text="Start Date:").grid(row=0, column=0, padx=5)
            start_date_picker = DateEntry(date_frame, width=12, background='darkblue', foreground='white', borderwidth=2)
            start_date_picker.grid(row=0, column=1, padx=5)
            
            # Set default to the first day of the current month
            today = datetime.today()
            first_day_of_month = today.replace(day=1)
            start_date_picker.set_date(first_day_of_month)

            # Label and Date Picker for End Date
            ttk.Label(date_frame, text="End Date:").grid(row=0, column=2, padx=5)
            end_date_picker = DateEntry(date_frame, width=12, background='darkblue', foreground='white', borderwidth=2)
            end_date_picker.grid(row=0, column=3, padx=5)
            
            # Set default to the last day of the current month
            last_day_of_month = (today.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)
            end_date_picker.set_date(last_day_of_month)

            # Fetch Data Button
            fetch_button = ttk.Button(date_frame, text="Fetch Data", command=lambda: self.fetch_order_data2(start_date_picker, end_date_picker))
            fetch_button.grid(row=0, column=4, padx=5)

            # Create a table frame for displaying the report
            table_frame = ttk.Frame(frame)
            table_frame.pack(fill="both", expand=True, padx=10, pady=10)

            self.current_order_page = 0
            self.order_page_size = 15

            # Treeview for displaying order data
            columns = ("order_id","order_status", "user_id", "order_date", "pickup_date" )

            self.order_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=self.order_page_size)
            
            # Bind an event when an order is selected
            self.order_tree.bind("<Double-1>", lambda event, tree=self.order_tree: self.view_order_details(event, tree))
            
            # Define column headings and set anchor to center
            for col in columns:
                self.order_tree.heading(col, text=col.replace("_", " ").title())
                self.order_tree.column(col, anchor="center")
            
            # Vertical scrollbar
            vert_scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.order_tree.yview)
            vert_scrollbar.pack(side="right", fill="y")
            
            # Horizontal scrollbar
            horiz_scrollbar = ttk.Scrollbar(table_frame, orient="horizontal", command=self.order_tree.xview)
            horiz_scrollbar.pack(side="bottom", fill="x")
            
            # Configure scrollbars for the Treeview
            self.order_tree.configure(yscrollcommand=vert_scrollbar.set, xscrollcommand=horiz_scrollbar.set)
            self.order_tree.pack(fill="both", expand=True)

            # Pagination controls
            pagination_frame = ttk.Frame(frame)
            pagination_frame.pack(pady=10)

            ttk.Button(pagination_frame, text="Previous", command=lambda: self.change_order_page(-1)).grid(row=0, column=0, padx=5)
            ttk.Button(pagination_frame, text="Next", command=lambda: self.change_order_page(1)).grid(row=0, column=1, padx=5)

            ttk.Button(pagination_frame, text="Approve", command=self.approve_selected_order).grid(row=0, column=2, padx=5)
            # ttk.Button(pagination_frame, text="View", command=self.view_selected_order).grid(row=0, column=3, padx=5)
            ttk.Button(pagination_frame, text="Print", command=self.print_selected_order).grid(row=0, column=4, padx=5)

            # Export button
            ttk.Button(pagination_frame, text="Export", command=self.export_order_report).grid(row=0, column=5, padx=5)

            # Home button to return to the welcome frame
            ttk.Button(pagination_frame, text="Home", command=self.show_welcome_message).grid(row=0, column=6, padx=5)

            # Display this frame
            self.show_frame(frame)

    def fetch_order_data2(self, start_date_picker, end_date_picker):
        """Fetch and update order data based on selected start and end date"""
        start_date = start_date_picker.get_date().strftime('%Y-%m-%d')
        end_date = end_date_picker.get_date().strftime('%Y-%m-%d')
        
        # Fetch data from the order manager using the selected date range
        order_manager = OrderManager()  # Replace with your actual manager class
        order_data = order_manager.get_orders_between_dates_p(start_date, end_date)

        self.columns = ["order_id","order_status", "user_id", "order_date", "pickup_date" ]

        # Convert the fetched order data to a DataFrame
        self.order_df = pd.DataFrame(order_data,columns=self.columns)

        # Load the first page of order data into the Treeview
        self.current_order_page = 0
        self.order_page_size = 15
        # self.display_order_page(table_frame)
        self.display_order_page()

    def display_order_page(self):
        # Clear existing rows in the Treeview
        for item in self.order_tree.get_children():
            self.order_tree.delete(item)

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

    def approve_selected_order(self):
        # Approve or unapprove the selected order
        selected_item = self.order_tree.selection()
        print(selected_item)
        if selected_item:
            order_id = self.order_tree.item(selected_item)["values"][0]
            ord_obj = OrderManager()
            result = ord_obj.process_existing_order(order_id)
            print(result)


    def view_order_details(self, event, tree):
        # Get selected order's order_id
        selected_item = tree.selection()[0]
        order_id = tree.item(selected_item)['values'][0]

        order_manager = OrderManager()
        order_details = order_manager.get_ordersdetails(order_id)
        print(order_details)

        if order_details:
            # Create a popup window to display order details
            self.show_order_popup(order_details)


    def show_order_popup(self, order_details):
        popup = tk.Toplevel(self.root)
        popup.title(f"Order Details (ID: {order_details[0][0]})")

        # Display basic order details first (Order ID, Pickup Date, Order Status, etc.)
        order_info = [
            ("Order ID", order_details[0][0]),
            ("Pickup Date", order_details[0][1]),
            ("Order Status", order_details[0][2]),
        ]

        row = 0
        for label, value in order_info:
            tk.Label(popup, text=f"{label}: {value}").grid(row=row, column=0, padx=10, pady=5)
            row += 1

        # Now display the material names and quantities
        tk.Label(popup, text="Materials and Quantities:").grid(row=row, column=0, padx=10, pady=5)
        row += 1

        # Loop through the rows and display material names and quantities
        for order_id, pickup_date, order_status, material_name, quantity in order_details:
            tk.Label(popup, text=f"Material: {material_name}, Quantity: {quantity}").grid(row=row, column=0, padx=10, pady=5)
            row += 1

        # Add a Close button
        close_button = tk.Button(popup, text="Close", command=popup.destroy)
        close_button.grid(row=row, column=0, pady=10)

    def print_selected_order(self):
        # Print the selected order
        selected_item = self.order_tree.selection()
        order_id = self.order_tree.item(selected_item)["values"][0]
        order_manager = OrderManager()
        order_details = order_manager.get_ordersdetails(order_id)
        pdf_obj = PDFManager()
        pdf_obj.generate_receipt(order_details,order_id)
        print("printed")


    def export_order_report(self):
        # Export the order data to a CSV file
                # Get the current timestamp to append to the filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Define the file paths
        data_folder_path = os.path.join(os.path.expanduser("~"), "Desktop", "Data", f"Order_report_{timestamp}.csv")

        try:
            # Ensure the Data folder exists, if not, create it
            os.makedirs(os.path.dirname(data_folder_path), exist_ok=True)

            # Export to both locations
            self.order_df.to_csv(data_folder_path, index=False)

            # Show a message box indicating success
            MessageBox.showinfo("Export Success", f"Location: {data_folder_path}")

        except Exception as e:
            # Show error message if something goes wrong
            MessageBox.showerror("Export Failed", f"An error occurred while exporting the Order report: {str(e)}")

    # def show_manage_order_frame(self):
    #     # Create a new frame for managing orders
    #     frame = ttk.Frame(self.content_frame)

    #     # Title for the frame
    #     title_label = ttk.Label(frame, text="Manage Orders", font=("Helvetica", 16))
    #     title_label.grid(row=0, column=0, columnspan=2, pady=20)

    #     # Filter options (Order ID, Pickup Date, User ID)
    #     filter_frame = ttk.Frame(frame)
    #     filter_frame.grid(row=1, column=0, columnspan=2, pady=10)

    #     ttk.Label(filter_frame, text="Order ID:").grid(row=0, column=0, padx=5)
    #     self.order_id_entry = ttk.Entry(filter_frame)
    #     self.order_id_entry.grid(row=0, column=1, padx=5)

    #     ttk.Label(filter_frame, text="Pickup Date:").grid(row=0, column=2, padx=5)
    #     self.pickup_date_entry = ttk.Entry(filter_frame)
    #     self.pickup_date_entry.grid(row=0, column=3, padx=5)

    #     ttk.Label(filter_frame, text="User ID:").grid(row=0, column=4, padx=5)
    #     self.user_id_entry = ttk.Entry(filter_frame)
    #     self.user_id_entry.grid(row=0, column=5, padx=5)

    #     # Filter button
    #     filter_button = ttk.Button(filter_frame, text="Filter", command=self.apply_filters)
    #     filter_button.grid(row=0, column=6, padx=10)

    #     # Tree view for displaying orders
    #     columns = ("Order ID", "User ID", "Pickup Date", "Order Date", "Status")
    #     self.order_tree = ttk.Treeview(frame, columns=columns, show="headings", height=11)
    #     for col in columns:
    #         self.order_tree.heading(col, text=col)
    #         self.order_tree.column(col, width=100)

    #     # Scrollbars for the tree view
    #     vscrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.order_tree.yview)
    #     vscrollbar.grid(row=2, column=1, sticky="ns")
    #     self.order_tree.configure(yscrollcommand=vscrollbar.set)

    #     hscrollbar = ttk.Scrollbar(frame, orient="horizontal", command=self.order_tree.xview)
    #     hscrollbar.grid(row=3, column=0, sticky="ew")
    #     self.order_tree.configure(xscrollcommand=hscrollbar.set)

    #     self.order_tree.grid(row=2, column=0, sticky="nsew")

    #     # Pagination controls
    #     pagination_frame = ttk.Frame(frame)
    #     pagination_frame.grid(row=4, column=0, pady=10)

    #     ttk.Button(pagination_frame, text="Previous", command=lambda: self.change_page(-1)).grid(row=0, column=0, padx=5)
    #     ttk.Button(pagination_frame, text="Next", command=lambda: self.change_page(1)).grid(row=0, column=1, padx=5)

    #     # Action buttons for the selected order
    #     action_frame = ttk.Frame(frame)
    #     action_frame.grid(row=2, column=2, padx=10, sticky="n")

    #     approve_button = ttk.Button(action_frame, text="Approve", command=self.approve_selected_order)
    #     approve_button.pack(pady=5)

    #     view_button = ttk.Button(action_frame, text="View", command=self.view_selected_order)
    #     view_button.pack(pady=5)

    #     print_button = ttk.Button(action_frame, text="Print", command=self.print_selected_order)
    #     print_button.pack(pady=5)

    #     # Home button to return to the welcome frame
    #     ttk.Button(pagination_frame, text="Home", command=self.show_welcome_message).grid(row=0, column=2, padx=5)
        

    #     # Display this frame
    #     self.show_frame(frame)

    #     # Load initial data and display first page
    #     self.orders = self.load_order_data()  # Load your data here
    #     self.filtered_orders = self.orders
    #     self.current_page = 0
    #     self.page_size = 10
    #     self.display_orders_list()

    # def display_orders_list(self):
    #     # Clear the tree view
    #     for row in self.order_tree.get_children():
    #         self.order_tree.delete(row)

    #     # Get the current page of orders
    #     start_idx = self.current_page * self.page_size
    #     end_idx = start_idx + self.page_size
    #     current_orders = self.filtered_orders[start_idx:end_idx]

    #     # Insert the orders into the tree view
    #     for order in current_orders:
    #         self.order_tree.insert("", "end", values=(order["order_id"], order["user_id"], order["pickup_date"], order["order_date"], order["order_status"]))

    # def apply_filters(self):
    #     # Apply filters based on the entries
    #     order_id = self.order_id_entry.get().strip()
    #     pickup_date = self.pickup_date_entry.get().strip()
    #     user_id = self.user_id_entry.get().strip()

    #     if not (order_id or pickup_date or user_id):
    #         # Reset to all orders if no filter is entered
    #         self.filtered_orders = self.orders
    #     else:
    #         # Filter orders based on input criteria
    #         self.filtered_orders = [
    #             order for order in self.orders
    #             if (not order_id or str(order["order_id"]) == order_id) and
    #             (not pickup_date or order["pickup_date"] == pickup_date) and
    #             (not user_id or str(order["user_id"]) == user_id)
    #         ]

    #     # Reset to the first page after filtering
    #     self.current_page = 0
    #     self.display_orders_list()

    # def change_page(self, direction):
    #     # Change page based on the direction (-1 for previous, +1 for next)
    #     if 0 <= self.current_page + direction < len(self.filtered_orders) // self.page_size + 1:
    #         self.current_page += direction
    #         self.display_orders_list()



    # def load_order_data(self):
    #     # Sample data loader function (replace this with actual data loading logic)
    #     return [
    #         {"order_id": i, "user_id": i % 5, "order_date": f"2024-11-{i:02}", "pickup_date": f"2024-11-{i+1:02}", "order_status": "Pending"}
    #         for i in range(1, 101)  # 100 sample orders
    #     ]

    # def show_order_details(self, order):
    #     # Function to display order details in a popup
    #     order_details = f"Order ID: {order['order_id']}\nUser ID: {order['user_id']}\nOrder Date: {order['order_date']}\nPickup Date: {order['pickup_date']}\nStatus: {order['order_status']}"
    #     messagebox.showinfo("Order Details", order_details)

    # def print_order(self, order):
    #     # Function to print order details (simulate)
    #     print(f"Printing Order ID: {order['order_id']}")



#..... Order Menu  Frame-2 .....


    def show_order_report_frame(self):
        # Create a new frame for Order Report
        frame = ttk.Frame(self.content_frame)
        
        # Title for the report
        ttk.Label(frame, text="Order Report", font=("Helvetica", 16)).pack(pady=20)
        
        # Create a frame for the date pickers (start and end dates)
        date_frame = ttk.Frame(frame)
        date_frame.pack(pady=10)
        
        # Label and Date Picker for Start Date
        ttk.Label(date_frame, text="Start Date:").grid(row=0, column=0, padx=5)
        start_date_picker = DateEntry(date_frame, width=12, background='darkblue', foreground='white', borderwidth=2)
        start_date_picker.grid(row=0, column=1, padx=5)
        
        # Set default to the first day of the current month
        today = datetime.today()
        first_day_of_month = today.replace(day=1)
        start_date_picker.set_date(first_day_of_month)

        # Label and Date Picker for End Date
        ttk.Label(date_frame, text="End Date:").grid(row=0, column=2, padx=5)
        end_date_picker = DateEntry(date_frame, width=12, background='darkblue', foreground='white', borderwidth=2)
        end_date_picker.grid(row=0, column=3, padx=5)
        
        # Set default to the last day of the current month
        last_day_of_month = (today.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)
        end_date_picker.set_date(last_day_of_month)

        # Fetch Data Button
        fetch_button = ttk.Button(date_frame, text="Fetch Data", command=lambda: self.fetch_order_data(start_date_picker, end_date_picker))
        fetch_button.grid(row=0, column=4, padx=5)

        # Create a table frame for displaying the report
        table_frame = ttk.Frame(frame)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.current_order_page = 0
        self.order_page_size = 15

        # Treeview for displaying order data
        columns = (
            "order_id", "user_id", "first_name", "last_name", "email_address",
            "order_date", "pickup_date", "order_status", "order_text",
            "material_id", "material_name", "quantity", "unit_price", "role_type"
        )

        self.order_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=self.order_page_size)
        
        # Define column headings and set anchor to center
        for col in columns:
            self.order_tree.heading(col, text=col.replace("_", " ").title())
            self.order_tree.column(col, anchor="center")
        
        # Vertical scrollbar
        vert_scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.order_tree.yview)
        vert_scrollbar.pack(side="right", fill="y")
        
        # Horizontal scrollbar
        horiz_scrollbar = ttk.Scrollbar(table_frame, orient="horizontal", command=self.order_tree.xview)
        horiz_scrollbar.pack(side="bottom", fill="x")
        
        # Configure scrollbars for the Treeview
        self.order_tree.configure(yscrollcommand=vert_scrollbar.set, xscrollcommand=horiz_scrollbar.set)
        self.order_tree.pack(fill="both", expand=True)

        # Pagination controls
        pagination_frame = ttk.Frame(frame)
        pagination_frame.pack(pady=10)

        ttk.Button(pagination_frame, text="Previous", command=lambda: self.change_order_page(-1)).grid(row=0, column=0, padx=5)
        ttk.Button(pagination_frame, text="Next", command=lambda: self.change_order_page(1)).grid(row=0, column=1, padx=5)

        # Export button
        ttk.Button(pagination_frame, text="Export", command=self.export_order_report).grid(row=0, column=2, padx=5)

        # Home button to return to the welcome frame
        ttk.Button(pagination_frame, text="Home", command=self.show_welcome_message).grid(row=0, column=3, padx=5)

        # Display this frame
        self.show_frame(frame)

    def fetch_order_data(self, start_date_picker, end_date_picker):
        """Fetch and update order data based on selected start and end date"""
        start_date = start_date_picker.get_date().strftime('%Y-%m-%d')
        end_date = end_date_picker.get_date().strftime('%Y-%m-%d')
        
        # Fetch data from the order manager using the selected date range
        order_manager = OrderManager()  # Replace with your actual manager class
        order_data = order_manager.get_orders_between_dates(start_date, end_date)

        self.columns = ["order_id", "user_id", "first_name", "last_name", "email_address",
            "order_date", "pickup_date", "order_status", "order_text",
            "material_id", "material_name", "quantity", "unit_price", "role_type"]

        # Convert the fetched order data to a DataFrame
        self.order_df = pd.DataFrame(order_data,columns=self.columns)

        # Load the first page of order data into the Treeview
        self.current_order_page = 0
        self.order_page_size = 15
        # self.display_order_page(table_frame)
        self.display_order_page()

    def display_order_page(self):
        # Clear existing rows in the Treeview
        for item in self.order_tree.get_children():
            self.order_tree.delete(item)

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
                # Get the current timestamp to append to the filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Define the file paths
        data_folder_path = os.path.join(os.path.expanduser("~"), "Desktop", "Data", f"Order_report_{timestamp}.csv")

        try:
            # Ensure the Data folder exists, if not, create it
            os.makedirs(os.path.dirname(data_folder_path), exist_ok=True)

            # Export to both locations
            self.order_df.to_csv(data_folder_path, index=False)

            # Show a message box indicating success
            MessageBox.showinfo("Export Success", f"Location: {data_folder_path}")

        except Exception as e:
            # Show error message if something goes wrong
            MessageBox.showerror("Export Failed", f"An error occurred while exporting the Order report: {str(e)}")


#--------------------------------------------------------------------
# -------------------- User Management Views --------------------
#--------------------------------------------------------------------

#..... User Menu  Frame-1 .....

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
        first_name_var = StringVar()
        last_name_var = StringVar()
        email_address_var = StringVar()
        password_var = StringVar()
        mobile_number_var = StringVar()
        fulltime_var = BooleanVar()
        parttime_var = BooleanVar()
        undergraduate_var = BooleanVar()
        graduate_var = BooleanVar()
        already_graduate_var = BooleanVar()
        work_per_week_var = IntVar()
        age_group_var = IntVar()
        is_active_var = BooleanVar()
        role_type_var = StringVar()

        # User detail fields layout (now with two columns)
        fields = [
            ("First Name", first_name_var),
            ("Last Name", last_name_var),
            ("Email Address", email_address_var),
            ("Password", password_var),
            ("Mobile Number", mobile_number_var),
            ("Full-Time", fulltime_var),
            ("Part-Time", parttime_var),
            ("Undergraduate", undergraduate_var),
            ("Graduate", graduate_var),
            ("Already Graduated", already_graduate_var),
            ("Work per Week", work_per_week_var),
            ("Age Group", age_group_var),
            ("Active", is_active_var),
            ("Role Type", role_type_var),
        ]

        # Populate the details section with labels and entry widgets, arranged in two columns
        for i, (label_text, var) in enumerate(fields):
            row = i // 2  # This determines the row number, dividing the fields into two columns
            column = 2 * (i % 2)  # This places the field in one of the two columns (0 or 2)
            
            # Create label and input field in the appropriate column
            ttk.Label(user_details_frame, text=label_text + ":").grid(row=row, column=column, sticky="e", padx=5, pady=5)
            
            if isinstance(var, BooleanVar):
                # If the variable is a BooleanVar, create a Checkbutton
                ttk.Checkbutton(user_details_frame, variable=var).grid(row=row, column=column + 1, sticky="w", padx=5, pady=5)
            elif isinstance(var, IntVar):
                # If the variable is an IntVar, create an Entry for numbers
                ttk.Entry(user_details_frame, textvariable=var).grid(row=row, column=column + 1, sticky="w", padx=5, pady=5)
            elif label_text == "Role Type":
                # For Role Type, create a Combobox for selection between User and Admin
                role_type_combobox = ttk.Combobox(user_details_frame, textvariable=var, values=["User", "Admin"], state="readonly")
                role_type_combobox.grid(row=row, column=column + 1, sticky="w", padx=5, pady=5)
                role_type_combobox.set("User")  # Default value can be 'User' or 'Admin'
            else:
                # Default case for all other fields, create a simple Entry widget
                ttk.Entry(user_details_frame, textvariable=var).grid(row=row, column=column + 1, sticky="w", padx=5, pady=5)

        # Action buttons for Add and Update User
        actions_frame = ttk.Frame(frame)
        actions_frame.pack(pady=10)
        
        ttk.Button(actions_frame, text="Add User", command=lambda: add_user()).grid(row=0, column=0, padx=10)
        ttk.Button(actions_frame, text="Update User", command=lambda: update_user()).grid(row=0, column=1, padx=10)

            

        def clear_user_details():
            """Clears the values of the user detail fields."""
            # Reset all the fields to their default values
            user_id_var.set("")
            first_name_var.set("")
            last_name_var.set("")
            email_address_var.set("")
            password_var.set("")
            mobile_number_var.set("")
            fulltime_var.set(False)
            parttime_var.set(False)
            undergraduate_var.set(False)
            graduate_var.set(False)
            already_graduate_var.set(False)
            work_per_week_var.set(0.0)
            age_group_var.set(0)
            is_active_var.set(False)
            role_type_var.set("")




        # Function to load existing user data
        def load_user(user_id_var):
            user_id = user_id_var.get()
            if user_id.isdigit():
                user_id = int(user_id)
                # Retrieve user data from the database (replace with actual data loading)
                # Here would be the call to UserManager to retrieve user data
                print(user_id)
                user_manager = UserManager()  # Create an instance of the class
                user_data = user_manager.load_user(user_id)  # Call load_user on the instance
                if user_data["work_per_week"]=="":
                    user_data["work_per_week"]=0
                
                if user_data["age_group"]=="":
                    user_data["age_group"]=18
                    
                # Populate data in the fields if found
                print(user_data)
                # user_data = dummy_data.get(user_id, None)
                if user_data:
                    first_name_var.set(user_data["first_name"])
                    last_name_var.set(user_data["last_name"])
                    email_address_var.set(user_data["email_address"])
                    password_var.set(user_data["password"])
                    mobile_number_var.set(user_data["mobile_number"])
                    fulltime_var.set(user_data["fulltime"])
                    parttime_var.set(user_data["parttime"])
                    undergraduate_var.set(user_data["undergraduate"])
                    graduate_var.set(user_data["graduate"])
                    already_graduate_var.set(user_data["already_graduate"])
                    work_per_week_var.set(user_data["work_per_week"])
                    age_group_var.set(user_data["age_group"])
                    is_active_var.set(user_data["is_active"])
                    role_type_var.set(user_data["role_type"])
                else:
                    messagebox.showinfo("User Not Found", f"No user found with ID {user_id}")
            else:
                messagebox.showwarning("Invalid ID", "Please enter a valid user ID.")

        # Function to add a new user
        def add_user():
            new_user_data = {
                "first_name": first_name_var.get(),
                "last_name": last_name_var.get(),
                "email_address": email_address_var.get(),
                "password": password_var.get(),
                "mobile_number": mobile_number_var.get(),
                "fulltime": fulltime_var.get(),
                "parttime": parttime_var.get(),
                "undergraduate": undergraduate_var.get(),
                "graduate": graduate_var.get(),
                "already_graduate": already_graduate_var.get(),
                "work_per_week": work_per_week_var.get(),
                "age_group": age_group_var.get(),
                "is_active": is_active_var.get(),
                "role_type": role_type_var.get(),
            }

            user_manager = UserManager()  # Create an instance of the class
            user_manager.add_user(new_user_data)  # Call load_user on the instance
            clear_user_details()

        # Function to update existing user data
        def update_user():
            user_id = user_id_var.get()
            if user_id.isdigit():
                updated_user_data = {
                    "first_name": first_name_var.get(),
                    "last_name": last_name_var.get(),
                    "email_address": email_address_var.get(),
                    "password": password_var.get(),
                    "mobile_number": mobile_number_var.get(),
                    "fulltime": fulltime_var.get(),
                    "parttime": parttime_var.get(),
                    "undergraduate": undergraduate_var.get(),
                    "graduate": graduate_var.get(),
                    "already_graduate": already_graduate_var.get(),
                    "work_per_week": work_per_week_var.get(),
                    "age_group": age_group_var.get(),
                    "is_active": is_active_var.get(),
                    "role_type": role_type_var.get(),
                }
                user_manager = UserManager()  # Create an instance of the class
                user_manager.update_user(user_id,updated_user_data)  # Call load_user on the instance
                clear_user_details()
            else:
                messagebox.showwarning("Update Error", "Please load a valid user to update.")


        # Display this frame
        self.show_frame(frame)



#..... User Menu  Frame-2 .....

    def show_user_list_frame(self):
        # Create a new frame for the User List
        frame = ttk.Frame(self.content_frame)

        # Title for the report
        ttk.Label(frame, text="User List", font=("Helvetica", 16)).pack(pady=20)

        # Table frame for the report
        table_frame = ttk.Frame(frame)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Fetch user data from database
        user_manger = UserManager()
        user_data = user_manger.get_all_users()

        print(user_data)
          # Replace with actual database fetch method

        # Convert fetched data to DataFrame for pagination and export purposes
        self.columns = [
            "user_id", "first_name", "last_name", "email_address",
            "mobile_number", "fulltime", "parttime", "undergraduate", "graduate",
            "already_graduate", "work_per_week", "age_group", "is_active", "role_type", "created_date"
        ]
        self.user2_df = pd.DataFrame(user_data["data"], columns=self.columns)

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
        ttk.Button(pagination_frame, text="Export", command=self.export_user_report).grid(row=0, column=2, padx=5)

        # Home button to return to the welcome frame
        ttk.Button(pagination_frame, text="Home", command=self.show_welcome_message).grid(row=0, column=3, padx=5)

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
        columns = ("user_id", "first_name", "last_name", "email_address",
            "mobile_number", "fulltime", "parttime", "undergraduate", "graduate",
            "already_graduate", "work_per_week", "age_group", "is_active", "role_type", "created_date")
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
        for _, row in self.user2_df.iloc[start_idx:end_idx].iterrows():
            self.user_tree.insert("", "end", values=list(row))

    def change_user_page(self, direction):
        # Change page based on the direction (-1 for previous, +1 for next)
        max_page = len(self.user_df) // self.page_size
        self.current_page = min(max(0, self.current_page + direction), max_page)
        
        # Refresh the displayed page
        self.display_user_page(self.user_tree.master)

    def export_user_report(self):
        # Export the user data to a CSV file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        data_folder_path = os.path.join(os.path.expanduser("~"), "Desktop", "Data", f"User_report_{timestamp}.csv")

        try:
            # Ensure the Data folder exists, if not, create it
            os.makedirs(os.path.dirname(data_folder_path), exist_ok=True)

            # Export the data to CSV
            self.user2_df.to_csv(data_folder_path, index=False)

            # Show a message box indicating success
            MessageBox.showinfo("Export Success", f"Location: {data_folder_path}")

        except Exception as e:
            # Show error message if something goes wrong
            MessageBox.showerror("Export Failed", f"An error occurred while exporting the User report: {str(e)}")








# -------------------- Action Methods -------------------------------
# (Action methods as defined in your initial code...)
#--------------------------------------------------------------------




  



#-------------------------------------- Pending -----------------------------------------------


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


    def logout(self):
        # Destroy any current frame and reset the window to the login view
        if self.current_frame:
            self.current_frame.destroy()

        # Call the return_to_login method to display the login form
        self.show_login_screen_callback()

if __name__ == "__main__":
    root = ThemedTk()
    admin_view = AdminView(root)
    root.mainloop()
