import tkinter as tk
from tkinter import ttk,simpledialog
from tkinter import messagebox,Tk, StringVar, IntVar,BooleanVar
from datetime import datetime
from controllers import session
from tkcalendar import DateEntry


# -------------import controllers ---------

from controllers import user_manager2
from controllers.order_manager import OrderManager
from controllers.udashboard import UDashboardManager

class UserView:
    
    def __init__(self, root, return_to_login):
        self.root = root
        self.return_to_login = return_to_login
        self.current_frame = None

        self.cart = {}
        # Placeholder for orders (order ID, order details)
        self.orders = {}
        self.order_counter = 1
        self.line_items_tree = None
        self.root.title("User Dashboard")

        # Show the initial user home with a welcome message
        self.create_user_dashboard()

        # Create the user menu bar
        self.create_user_menu()



    def create_user_menu(self):
        # Create the menu bar
        menu_bar = tk.Menu(self.root, bg="#333", fg="#FFF", font=("Helvetica", 10))

        # Profile menu
        profile_menu = tk.Menu(menu_bar, tearoff=0, bg="#333", fg="#FFF", activebackground="#002bb2")
        profile_menu.add_command(label="View Profile", command=self.show_view_profile)
        profile_menu.add_command(label="Update Profile", command=self.show_update_profile)
        menu_bar.add_cascade(label="Profile", menu=profile_menu)

        # Manage Order menu
        manage_order_menu = tk.Menu(menu_bar, tearoff=0, bg="#333", fg="#FFF", activebackground="#002bb2")
        manage_order_menu.add_command(label="Create Order", command=self.show_create_order)
        manage_order_menu.add_command(label="View Orders", command=self.show_orders)
        menu_bar.add_cascade(label="Manage Order", menu=manage_order_menu)

        # Logout option in the menu
        logout_menu = tk.Menu(menu_bar, tearoff=0, bg="#333", fg="#FFF", activebackground="#002bb2")
        logout_menu.add_command(label="Logout", command=self.logout)
        menu_bar.add_cascade(label="Logout", menu=logout_menu)

        # Configure the root window to display this menu
        self.root.config(menu=menu_bar)
    
    def create_user_dashboard(self):
        # Main dashboard frame
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
        # Create the welcome frame
        welcome_frame = ttk.Frame(self.content_frame)  # Ensure correct parent
        welcome_frame.pack(fill="both", expand=True, padx=20, pady=2)
        # Display the welcome label
        ttk.Label(welcome_frame, text=f"Welcome to the {session.user_name}'s Dashboard", font=("Helvetica", 16)).pack(pady=10)

        # Fetch and display statistics
        dashboard_manager = UDashboardManager()

        data = dashboard_manager.get_user_dashboard_data(session.user_id)


        stats_frame = ttk.Frame(welcome_frame)
        stats_frame.pack(fill="both", expand=True)

        for i in range(4):
            stats_frame.grid_columnconfigure(i, weight=1)



        def create_card(parent, title, count):
            """
            Creates a styled rectangular card with title and large count in two sections.

            :param parent: The parent frame where the card will be placed.
            :param title: The title of the card (e.g., "Total Orders").
            :param count: The count to be displayed in large font (e.g., number of orders).
            """
            # Create a style for the card
            style = ttk.Style()
            style.configure("Card.TFrame", 
                            relief="raised", 
                            background="#f9f9f9",  # Light background for card
                            padding=10)

            # Create the shadow frame (light background with no border)
            shadow_frame = ttk.Frame(parent, style="Card.TFrame", padding=5)
            shadow_frame.grid_propagate(False)  # Prevent resizing based on content

            # Define font styles
            title_font = ("Helvetica", 10, "bold")  # Small font for the title
            count_font = ("Helvetica", 18, "bold")  # Large font for the count

            # Create and pack the title label (small font at the top)
            title_label = ttk.Label(shadow_frame, text=title, font=title_font, anchor="center", foreground="#333")
            title_label.pack(expand=False, fill="both", padx=5, pady=5)

            # Create and pack the count label (large font at the bottom)
            count_label = ttk.Label(shadow_frame, text=str(count), font=count_font, anchor="center", foreground="#007bff")
            count_label.pack(expand=True, fill="both", padx=5, pady=5)

            # Place the shadow frame in the grid
            shadow_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

            return shadow_frame



        # Assuming 'stats_frame' is the frame where you want to display the cards
        create_card(stats_frame, "Total Orders", data['total_orders']).grid(row=0, column=0, padx=10, pady=10)
        create_card(stats_frame, "Approved Orders", data['approved_orders']).grid(row=0, column=1, padx=10, pady=10)
        create_card(stats_frame, "Pending Orders", data['pending_orders']).grid(row=0, column=2, padx=10, pady=10)
        create_card(stats_frame, "Last Order ID", data['last_order_id']).grid(row=0, column=3, padx=10, pady=10)
        create_card(stats_frame, "Last Order Date", data['last_order_date']).grid(row=1, column=0, padx=10, pady=10, columnspan=4)

        # Show the frame
        self.show_frame(welcome_frame)






    def show_view_profile(self):
        frame = ttk.Frame(self.content_frame)
        
        # Title label
        ttk.Label(frame, text="View Profile", font=("Helvetica", 16, "bold")).pack(pady=20)

        # Create a LabelFrame to contain the profile fields in two columns
        profile_frame = ttk.LabelFrame(frame, text="User Profile", padding=(10, 10))
        profile_frame.pack(pady=10, padx=20, fill="both", expand=True)

        user_manager = user_manager2.UserManager2()
        self.user_data = user_manager.load_user(session.user_id)

        # Define the user fields and map them to user data keys from the loaded dictionary
        fields = [
            ("User ID", self.user_data["user_id"]),
            ("First Name", self.user_data["first_name"]),
            ("Last Name", self.user_data["last_name"]),
            ("Email Address", self.user_data["email_address"]),
            ("Password", self.user_data["password"]),
            ("Mobile Number", self.user_data["mobile_number"]),
            ("Fulltime", self.user_data["fulltime"]),
            ("Parttime", self.user_data["parttime"]),
            ("Undergraduate", self.user_data["undergraduate"]),
            ("Graduate", self.user_data["graduate"]),
            ("Already Graduate", self.user_data["already_graduate"]),
            ("Work Per Week", self.user_data["work_per_week"]),
            ("Age Group", self.user_data["age_group"]),
            ("Is Active", self.user_data["is_active"]),
            ("Role Type", self.user_data["role_type"]),
            ("Created Date", self.user_data["created_date"]),
        ]
        
        # Loop through the fields and display them in two columns inside the LabelFrame
        for idx, (label_text, value) in enumerate(fields):
            row = idx // 2  # For two columns, this will alternate the rows
            col = idx % 2   # Alternate between column 0 and 1
            
            # Label for the field name
            ttk.Label(profile_frame, text=f"{label_text}:", font=("Helvetica", 12), anchor="w", width=20).grid(row=row, column=col*2, padx=10, pady=5, sticky="w")
            
            # Value for the field
            ttk.Label(profile_frame, text=value, font=("Helvetica", 12), relief="sunken", width=30).grid(row=row, column=col*2+1, padx=10, pady=5, sticky="w")
        
        # Add a back button to return to home screen
        back_button = ttk.Button(frame, text="Back", command=self.show_welcome_message)
        back_button.pack(pady=20)

        self.show_frame(frame)







    def show_update_profile(self):
        frame = ttk.Frame(self.content_frame)
   
        # Title label
        ttk.Label(frame, text="Update Profile", font=("Helvetica", 16, "bold")).pack(pady=20)
        
        # Create a frame to hold the update profile fields
        update_frame = ttk.Frame(frame)
        update_frame.pack(pady=10)

        user_manager = user_manager2.UserManager2()
        self.user_data = user_manager.load_user(session.user_id)
        if self.user_data:
            # Initializing StringVar with the existing user data
            self.first_name_var = StringVar(value=self.user_data["first_name"])
            self.last_name_var = StringVar(value=self.user_data["last_name"])
            self.email_address_var = StringVar(value=self.user_data["email_address"])
            self.password_var = StringVar(value=self.user_data["password"])
            self.mobile_number_var = StringVar(value=self.user_data["mobile_number"])

        # Define the fields to be updated
        fields = [
            ("First Name", self.first_name_var),
            ("Last Name", self.last_name_var),
            ("Email Address", self.email_address_var),
            ("Password", self.password_var),
            ("Mobile Number", self.mobile_number_var),
        ]

        # Loop through the fields and create entry widgets for each field
        for label_text, var in fields:
            field_frame = ttk.Frame(update_frame)
            field_frame.pack(fill="x", pady=5)
            
            ttk.Label(field_frame, text=f"{label_text}:", font=("Helvetica", 12), anchor="w", width=15).pack(side="left", padx=10)
            entry = ttk.Entry(field_frame, textvariable=var, font=("Helvetica", 12), width=30)
            entry.pack(side="left", padx=10)

        # Button to save the updated profile information
        save_button = ttk.Button(frame, text="Update Profile", command=self.save_profile_changes)
        save_button.pack(pady=20)

        # Button to cancel and go back to the profile view
        cancel_button = ttk.Button(frame, text="Home", command=self.show_welcome_message)
        cancel_button.pack(pady=10)

        self.show_frame(frame)

    def save_profile_changes(self):
        updated_user_data = {
            "first_name": self.first_name_var.get(),
            "last_name": self.last_name_var.get(),
            "email_address": self.email_address_var.get(),
            "password": self.password_var.get(),
            "mobile_number": self.mobile_number_var.get(),
        }
        
        user_manager = user_manager2.UserManager2()  # Create an instance of the class
        update_result = user_manager.update_user(session.user_id, updated_user_data)  # Call the update_user method

        if update_result["success"]:
            # Optionally, show a success message after saving
            success_message = "Profile updated successfully!"
            success_label = ttk.Label(self.root, text=success_message, font=("Helvetica", 12), foreground="green")
            success_label.pack(pady=10)

            # Remove the success message after 2 seconds
            self.root.after(2000, success_label.destroy)  # 2000 milliseconds = 2 seconds
            
            # Redirect back to view profile after saving changes
            self.show_welcome_message()







# ------------------------------------------- order Frames ----------------------------------------------



    def show_create_order(self):
        
        """Display the Create Order screen."""
        # self.clear_screen()  # Clear current screen
        self.current_view = "create_order"

        # Main frame with scrollable area
        frame = ttk.Frame(self.content_frame)
        frame.pack(fill="both", expand=True)
        
        # Horizontal scrollbar for the main frame
        h_scrollbar = ttk.Scrollbar(frame, orient="horizontal")
        h_scrollbar.pack(side="bottom", fill="x")

        # Product Selection Frame with Treeview and Scrollbar
        product_frame = ttk.Frame(frame, borderwidth=1, relief="solid", padding=10)
        product_frame.pack(side="left", fill="both", expand=True, padx=10)

        # Label for Product Frame
        ttk.Label(product_frame, text="Products", font=("Helvetica", 14)).pack(pady=10)

        # Product Treeview with Horizontal Scrollbar
        columns = ("name", "stock")
        product_tree = ttk.Treeview(product_frame, columns=columns, show="headings")
        product_tree.heading("name", text="Product Name")
        product_tree.heading("stock", text="Stock")
        product_tree.column("name", anchor="w", width=150)
        product_tree.column("stock", anchor="center", width=50)

        product_scrollbar = ttk.Scrollbar(product_frame, orient="horizontal", command=product_tree.xview)
        product_tree.configure(xscrollcommand=product_scrollbar.set)
        product_tree.pack(fill="both", expand=True)
        product_scrollbar.pack(fill="x")

        order_manager = OrderManager()

        data = order_manager.get_all_materials()
        products = data["data"]

    

        for product in products:
            product_tree.insert("", "end", values=(product[0], product[1]))

        # Add button at the bottom of the product frame
        add_button = ttk.Button(product_frame, text="Add Selected Product", command=lambda: self.add_selected_to_cart(product_tree))
        add_button.pack(side="left",pady=10)
        # Add a back button to return to home screen
        back_button = ttk.Button(product_frame, text="Home", command=self.show_welcome_message)
        back_button.pack(side="left",padx=10)

        # Order Frame with Border and Padding
        self.order_frame = ttk.Frame(frame, borderwidth=2, relief="groove", padding=10)
        self.order_frame.pack(side="right", fill="both", expand=True, padx=10)
        
        ttk.Label(self.order_frame, text="Order Summary", font=("Helvetica", 14)).grid(row=0, column=0, columnspan=3, pady=10)

        # Show initial order items in the order frame
        self.update_order_frame()

        # Fixed Order Details (Address and Note) and Submit Button
        self.pickup_var = tk.StringVar()
        self.note_var = tk.StringVar()

        # Frame for Address, Note, and Submit Button at the bottom of order_frame
        details_frame = ttk.Frame(self.order_frame, padding=10)
        details_frame.grid(row=20, column=0, columnspan=3, sticky="ew", pady=10)

         # DateEntry (date picker)
        ttk.Label(details_frame, text="PickUp Date:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        pickup_entry = DateEntry(details_frame, textvariable=self.pickup_var, width=30, date_pattern='yyyy-mm-dd')
        pickup_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(details_frame, text="Note:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        note_entry = ttk.Entry(details_frame, textvariable=self.note_var, width=30)
        note_entry.grid(row=1, column=1, padx=5, pady=5)

        # Submit Order Button at the bottom
        submit_button = ttk.Button(details_frame, text="Submit Order", command=self.submit_order)
        submit_button.grid(row=2, column=0, columnspan=2, pady=10)
        self.show_frame(frame)

    def update_order_frame(self):
        pass
        # print("Updating Order Frame with Cart:", self.cart)

        """Update the order summary frame."""
        # Clear all widgets in the order frame except the header and footer.
        for widget in self.order_frame.grid_slaves():
            if int(widget.grid_info()["row"]) > 1 and int(widget.grid_info()["row"]) < 20:
                widget.grid_forget()

        # Header Labels
        ttk.Label(self.order_frame, text="Product", font=("Helvetica", 12, "bold")).grid(row=1, column=0, padx=5, pady=5)
        ttk.Label(self.order_frame, text="Quantity", font=("Helvetica", 12, "bold")).grid(row=1, column=1, padx=5, pady=5)
        ttk.Label(self.order_frame, text="Actions", font=("Helvetica", 12, "bold")).grid(row=1, column=2, padx=5, pady=5)

        # Dynamically add each item from the cart to the order frame
        row = 2
        for product_name, details in self.cart.items():
            # Display product name and quantity
            ttk.Label(self.order_frame, text=product_name).grid(row=row, column=0, padx=5, pady=5)
            ttk.Label(self.order_frame, text=str(details["quantity"])).grid(row=row, column=1, padx=5, pady=5)

            # Action frame with increment, decrement, and remove buttons
            action_frame = ttk.Frame(self.order_frame)
            action_frame.grid(row=row, column=2, padx=5, pady=5)

            increment_button = ttk.Button(action_frame, text="+", command=lambda p=product_name: self.increment_quantity(p))
            increment_button.grid(row=0, column=0, padx=2)
            
            decrement_button = ttk.Button(action_frame, text="-", command=lambda p=product_name: self.decrement_quantity(p))
            decrement_button.grid(row=0, column=1, padx=2)

            remove_button = ttk.Button(action_frame, text="X", command=lambda p=product_name: self.remove_from_cart(p))
            remove_button.grid(row=0, column=2, padx=2)

            row += 1

        # # Calculate and display the total cost
        # total_cost = sum(details["stock"] * details["quantity"] for details in self.cart.values())
        # ttk.Label(self.order_frame, text=f"Total: ${total_cost:.2f}", font=("Helvetica", 12, "bold")).grid(row=row, column=0, columnspan=3, pady=10)


    def clear_screen(self):
        """Clears the current screen to show a new view."""
        for widget in self.root.winfo_children():
            widget.destroy()

    def add_selected_to_cart(self, product_tree):
        selected_item = product_tree.selection()
        if selected_item:
            item = product_tree.item(selected_item, "values")
            product_name= item[0]
            
            # Add or update product in cart
            if product_name in self.cart:
                self.cart[product_name]["quantity"] += 1
            else:
                self.cart[product_name] = {"quantity": 1}
                
            self.update_order_frame()



    def increment_quantity(self, product_name):
        """Increment quantity of a product in the cart."""
        if product_name in self.cart:
            self.cart[product_name]["quantity"] += 1
            self.update_order_frame()

    def decrement_quantity(self, product_name):
        """Decrement quantity of a product in the cart."""
        if product_name in self.cart and self.cart[product_name]["quantity"] > 1:
            self.cart[product_name]["quantity"] -= 1
            self.update_order_frame()

    def remove_from_cart(self, product_name):
        """Remove a product from the cart."""
        if product_name in self.cart:
            del self.cart[product_name]
        self.update_order_frame()



    def submit_order(self, order_id=None):
        user_id = session.user_id
        """Submit the order and generate a new order or update an existing order."""
        pickup = self.pickup_var.get()
        note = self.note_var.get()

        if not pickup or not self.cart:
            messagebox.showerror("Error", "Please add products to the cart and provide an address.")
            return
        

        # order_details = {
        #     "user_id": 1,
        #     "pickup_date": "2024-11-30",
        #     "order_text": "Please deliver during business hours"
        # }

        order_details = {}
        order_details["user_id"]=user_id
        order_details["pickup"] = pickup
        order_details["note"] = note

        # print(order_details)

        order_manager = OrderManager()
        result = order_manager.insert_order(self.cart,order_details)

        

               # Display success or error message
        if result["success"]:
            messagebox.showinfo("Order Status", result["message"])
            # Clear cart
            # self.cart.clear()
            self.update_order_frame()

            # Clear the entry fields
            self.pickup_var.set("")  # Clear address field
            self.note_var.set("")     # Clear note field
        else:
            messagebox.showerror("Error", result["message"])



        self.show_welcome_message()



# -------------------------- View Orders  frame ------------------------------------


    def show_orders(self):
        """Display the Manage Orders screen."""
        self.current_view = "manage_order"

        # Main frame for managing orders
        frame = ttk.Frame(self.content_frame)
        frame.pack(fill="both", expand=True)

        # Label for Orders Frame
        ttk.Label(frame, text="Manage Orders", font=("Helvetica", 14)).pack(pady=10)

        # Frame to hold the Treeview and scrollbars
        tree_frame = ttk.Frame(frame)
        tree_frame.pack(padx=20, pady=10, fill="both", expand=True) 

        # Define columns for the Treeview
        columns = ("order_id", "user_id", "order_date", "pickup_date", "order_status")
        order_tree = ttk.Treeview(tree_frame, columns=columns, show="headings")

        # Define column headings and set anchor to center
        for col in columns:
            order_tree.heading(col, text=col.replace("_", " ").title())
            order_tree.column(col, anchor="center")

        # Add the Treeview widget to the frame
        order_tree.pack(fill="both", expand=True)

        # Horizontal scrollbar
        horiz_scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal", command=order_tree.xview)
        horiz_scrollbar.pack(side="bottom", fill="x")

        # Configure scrollbars for the Treeview
        order_tree.configure(xscrollcommand=horiz_scrollbar.set)

        # Fetch orders from the database and insert them into the Treeview
        order_manager = OrderManager()
        orders = order_manager.get_orders(session.user_id)

        for order in orders:
            order_tree.insert("", "end", values=(order[0], order[1], order[2], order[3], order[4]))

        # Bind an event when an order is selected
        order_tree.bind("<Double-1>", lambda event, tree=order_tree: self.view_order_details(event, tree))

        # Buttons for managing orders (View, Edit, Delete)
        manage_buttons_frame = ttk.Frame(frame)
        manage_buttons_frame.pack(fill="x", pady=10)

        # Add a back button to return to home screen
        back_button = ttk.Button(manage_buttons_frame, text="Back", command=self.show_welcome_message)
        back_button.pack(pady=20)

        # Show the frame
        self.show_frame(frame)





    def view_order_details(self, event, tree):
        # Get selected order's order_id
        selected_item = tree.selection()[0]
        order_id = tree.item(selected_item)['values'][0]

        order_manager = OrderManager()
        order_details = order_manager.get_ordersdetails(order_id)
        # print(order_details)

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








    def logout(self):
        # Destroy any current frame and reset the window to the login view
        if self.current_frame:
            self.current_frame.destroy()

        # Call the return_to_login method to display the login form
        self.return_to_login()

