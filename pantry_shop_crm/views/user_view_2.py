import tkinter as tk
from tkinter import ttk,simpledialog
from tkinter import messagebox,Tk, StringVar, IntVar,BooleanVar
from datetime import datetime
from controllers import session


# -------------import controllers ---------

from controllers import user_manager2

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

        # Show the initial user home with a welcome message
        self.show_user_home()

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
        manage_order_menu.add_command(label="View and Edit Order", command=self.show_manage_order)
        menu_bar.add_cascade(label="Manage Order", menu=manage_order_menu)

        # Logout option in the menu
        logout_menu = tk.Menu(menu_bar, tearoff=0, bg="#333", fg="#FFF", activebackground="#002bb2")
        logout_menu.add_command(label="Logout", command=self.logout)
        menu_bar.add_cascade(label="Logout", menu=logout_menu)

        # Configure the root window to display this menu
        self.root.config(menu=menu_bar)

    def show_frame(self, frame):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = frame
        self.current_frame.pack(fill="both", expand=True)

    def show_user_home(self):
        # Create the main frame with a welcome message
        frame = ttk.Frame(self.root)
        welcome_message = "Welcome, User!"  # Replace "User" with the actual user's name if available
        ttk.Label(frame, text=welcome_message, font=("Helvetica", 18, "bold")).pack(pady=20)
        ttk.Label(frame, text="Please use the menu to navigate.", font=("Helvetica", 12)).pack(pady=10)
        self.show_frame(frame)


#  show view Profile 

    def show_view_profile(self):
        frame = ttk.Frame(self.root)
        
        # Title label
        ttk.Label(frame, text="View Profile", font=("Helvetica", 16, "bold")).pack(pady=20)

        # Create a frame to contain the profile fields
        profile_frame = ttk.Frame(frame)
        profile_frame.pack(pady=10)

        user_manager = user_manager2.UserManager2()
        self.user_data = user_manager.load_user(session.user_id)
        # print(self.user_data)

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
        
        # Loop through the fields and display them in a vertical list
        for label_text, value in fields:
            field_frame = ttk.Frame(profile_frame)
            field_frame.pack(fill="x", pady=5)
            
            ttk.Label(field_frame, text=f"{label_text}:", font=("Helvetica", 12), anchor="w", width=15).pack(side="left", padx=10)
            ttk.Label(field_frame, text=value, font=("Helvetica", 12), relief="sunken", width=30).pack(side="left", padx=10)
        
        # Add a back button to return to home screen
        back_button = ttk.Button(frame, text="Back", command=self.show_user_home)
        back_button.pack(pady=20)

        self.show_frame(frame)




    def show_update_profile(self):
        frame = ttk.Frame(self.root)
   
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
        cancel_button = ttk.Button(frame, text="Home", command=self.show_user_home)
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
            self.show_user_home()







# ------------------------------------------- order Frames ----------------------------------------------



    def show_create_order(self):
        
        """Display the Create Order screen."""
        # self.clear_screen()  # Clear current screen
        self.current_view = "create_order"

        # Main frame with scrollable area
        frame = ttk.Frame(self.root)
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
        columns = ("name", "price")
        product_tree = ttk.Treeview(product_frame, columns=columns, show="headings")
        product_tree.heading("name", text="Product Name")
        product_tree.heading("price", text="Price ($)")
        product_tree.column("name", anchor="w", width=150)
        product_tree.column("price", anchor="center", width=50)

        product_scrollbar = ttk.Scrollbar(product_frame, orient="horizontal", command=product_tree.xview)
        product_tree.configure(xscrollcommand=product_scrollbar.set)
        product_tree.pack(fill="both", expand=True)
        product_scrollbar.pack(fill="x")

        # Sample list of products
        products = [
            {"name": "Product 1", "price": 10},
            {"name": "Product 2", "price": 15},
            {"name": "Product 3", "price": 20}
        ]

        for product in products:
            product_tree.insert("", "end", values=(product["name"], product["price"]))

        # Add button at the bottom of the product frame
        add_button = ttk.Button(product_frame, text="Add Selected Product", command=lambda: self.add_selected_to_cart(product_tree))
        add_button.pack(pady=10)

        # Order Frame with Border and Padding
        self.order_frame = ttk.Frame(frame, borderwidth=2, relief="groove", padding=10)
        self.order_frame.pack(side="right", fill="both", expand=True, padx=10)
        
        ttk.Label(self.order_frame, text="Order Summary", font=("Helvetica", 14)).grid(row=0, column=0, columnspan=3, pady=10)

        # Show initial order items in the order frame
        self.update_order_frame()

        # Fixed Order Details (Address and Note) and Submit Button
        self.address_var = tk.StringVar()
        self.note_var = tk.StringVar()

        # Frame for Address, Note, and Submit Button at the bottom of order_frame
        details_frame = ttk.Frame(self.order_frame, padding=10)
        details_frame.grid(row=20, column=0, columnspan=3, sticky="ew", pady=10)

        ttk.Label(details_frame, text="Address:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        address_entry = ttk.Entry(details_frame, textvariable=self.address_var, width=30)
        address_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(details_frame, text="Note:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        note_entry = ttk.Entry(details_frame, textvariable=self.note_var, width=30)
        note_entry.grid(row=1, column=1, padx=5, pady=5)

        # Submit Order Button at the bottom
        submit_button = ttk.Button(details_frame, text="Submit Order", command=self.submit_order)
        submit_button.grid(row=2, column=0, columnspan=2, pady=10)
        self.show_frame(frame)

    def update_order_frame(self):
        print("Updating Order Frame with Cart:", self.cart)

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

        # Calculate and display the total cost
        total_cost = sum(details["price"] * details["quantity"] for details in self.cart.values())
        ttk.Label(self.order_frame, text=f"Total: ${total_cost:.2f}", font=("Helvetica", 12, "bold")).grid(row=row, column=0, columnspan=3, pady=10)


    def show_manage_order(self):
        """Display the Manage Orders screen."""
        # self.clear_screen()  # Clear current screen
        self.current_view = "manage_order"

        # Main frame for managing orders
        frame = ttk.Frame(self.root)
        frame.pack(fill="both", expand=True)

        # Label for Orders Frame
        ttk.Label(frame, text="Manage Orders", font=("Helvetica", 14)).pack(pady=10)

        # Order Treeview with options to Edit, View, Delete
        columns = ("order_id", "address", "status")
        order_tree = ttk.Treeview(frame, columns=columns, show="headings")
        order_tree.heading("order_id", text="Order ID")
        order_tree.heading("address", text="Address")
        order_tree.heading("status", text="Status")
        order_tree.column("order_id", anchor="center", width=100)
        order_tree.column("address", anchor="w", width=200)
        order_tree.column("status", anchor="center", width=100)

        order_tree.pack(fill="both", expand=True)

        # Display orders
        for order_id, details in self.orders.items():
            order_tree.insert("", "end", values=(order_id, details["address"], details["status"]))

        # Buttons for manage orders
        manage_buttons_frame = ttk.Frame(frame)
        manage_buttons_frame.pack(fill="x", pady=10)

        # View, Edit, Delete buttons
        view_button = ttk.Button(manage_buttons_frame, text="View Order", command=lambda: self.view_order(order_tree))
        view_button.pack(side="left", padx=10)

        edit_button = ttk.Button(manage_buttons_frame, text="Edit Order", command=lambda: self.edit_order(order_tree))
        edit_button.pack(side="left", padx=10)

        delete_button = ttk.Button(manage_buttons_frame, text="Delete Order", command=lambda: self.delete_order(order_tree))
        delete_button.pack(side="left", padx=10)
        self.show_frame(frame)

    def clear_screen(self):
        """Clears the current screen to show a new view."""
        for widget in self.root.winfo_children():
            widget.destroy()

    def add_selected_to_cart(self, product_tree):
        selected_item = product_tree.selection()
        if selected_item:
            item = product_tree.item(selected_item, "values")
            product_name, product_price = item[0], float(item[1])
            
            # Add or update product in cart
            if product_name in self.cart:
                self.cart[product_name]["quantity"] += 1
            else:
                self.cart[product_name] = {"price": product_price, "quantity": 1}
                
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


    def show_create_or_edit_order(self, order_id=None):
        """Display the Create or Edit Order screen."""
        if order_id:
            order_details = self.orders.get(order_id)
            if order_details:
                print(f"Editing Order: {order_id}, Note: {order_details['note']}")  # Debugging line
                self.address_var.set(order_details["address"])
                self.note_var.set(order_details["note"])  # Make sure this is being set
                self.cart = order_details.get("line_items", {})


        """Display the Create or Edit Order screen."""
        self.current_view = "create_order"
        frame = ttk.Frame(self.root)
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
        columns = ("name", "price")
        product_tree = ttk.Treeview(product_frame, columns=columns, show="headings")
        product_tree.heading("name", text="Product Name")
        product_tree.heading("price", text="Price ($)")
        product_tree.column("name", anchor="w", width=150)
        product_tree.column("price", anchor="center", width=50)

        product_scrollbar = ttk.Scrollbar(product_frame, orient="horizontal", command=product_tree.xview)
        product_tree.configure(xscrollcommand=product_scrollbar.set)
        product_tree.pack(fill="both", expand=True)
        product_scrollbar.pack(fill="x")

        # Sample list of products
        products = [
            {"name": "Product 1", "price": 10},
            {"name": "Product 2", "price": 15},
            {"name": "Product 3", "price": 20}
        ]

        for product in products:
            product_tree.insert("", "end", values=(product["name"], product["price"]))

        # Add button at the bottom of the product frame
        add_button = ttk.Button(product_frame, text="Add Selected Product", command=lambda: self.add_selected_to_cart(product_tree))
        add_button.pack(pady=10)

        # Order Frame with Border and Padding
        self.order_frame = ttk.Frame(frame, borderwidth=2, relief="groove", padding=10)
        self.order_frame.pack(side="right", fill="both", expand=True, padx=10)
        
        ttk.Label(self.order_frame, text="Order Summary", font=("Helvetica", 14)).grid(row=0, column=0, columnspan=3, pady=10)

        # Initialize line_items_tree if not already done
        if not hasattr(self, 'line_items_tree'):
            self.line_items_tree = ttk.Treeview(self.order_frame, columns=("product", "quantity", "price"), show="headings")
            self.line_items_tree.heading("product", text="Product Name")
            self.line_items_tree.heading("quantity", text="Quantity")
            self.line_items_tree.heading("price", text="Price ($)")
            self.line_items_tree.grid(row=1, column=0, columnspan=3, sticky="nsew")

        # Load existing order details and items if editing
        self.address_var = tk.StringVar()
        self.note_var = tk.StringVar()
        if order_id:
            order_details = self.orders.get(order_id)
            if order_details:
                self.address_var.set(order_details["address"])
                self.note_var.set(order_details["note"])
                self.cart = order_details.get("line_items", {})  # Load line items into the cart
        else:
            self.cart = {}

        # Populate line items if editing
        self.update_order_frame()

        # # Add button to remove selected item from the line items
        # remove_item_button = ttk.Button(self.order_frame, text="Remove Selected Item", command=self.remove_selected_item)
        # remove_item_button.grid(row=2, column=0, columnspan=3, pady=10)

        # Fixed Order Details (Address and Note) and Submit Button
        details_frame = ttk.Frame(self.order_frame, padding=10)
        details_frame.grid(row=20, column=0, columnspan=3, sticky="ew", pady=10)

        ttk.Label(details_frame, text="Address:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        address_entry = ttk.Entry(details_frame, textvariable=self.address_var, width=30)
        address_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(details_frame, text="Note:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        note_entry = ttk.Entry(details_frame, textvariable=self.note_var, width=30)
        note_entry.grid(row=1, column=1, padx=5, pady=5)

        # Submit Order Button at the bottom
        submit_button = ttk.Button(details_frame, text="Submit Order", command=lambda: self.submit_order(order_id))
        submit_button.grid(row=2, column=0, columnspan=2, pady=10)
        self.show_frame(frame)


    def submit_order(self, order_id=None):
        """Submit the order and generate a new order or update an existing order."""
        address = self.address_var.get()
        note = self.note_var.get()

        if not address or not self.cart:
            messagebox.showerror("Error", "Please add products to the cart and provide an address.")
            return
        
        if order_id:  # If it's an existing order being edited, update it
            self.orders[order_id]["address"] = address
            self.orders[order_id]["note"] = note
            self.orders[order_id]["line_items"] = self.cart  # Update line items
            success_message = f"Order {order_id} updated successfully!"
        else:  # New order creation
            order_id = self.order_counter
            self.orders[order_id] = {
                "address": address,
                "note": note,
                "status": "Pending",
                "line_items": self.cart  # Add line items to the new order
            }
            self.order_counter += 1
            success_message = f"Order {order_id} submitted successfully!"

        # Clear cart
        # self.cart.clear()
        self.update_order_frame()

        # Clear the entry fields
        self.address_var.set("")  # Clear address field
        self.note_var.set("")     # Clear note field

        # Optionally, show a success message after saving
        success_label = ttk.Label(self.root, text=success_message, font=("Helvetica", 12), foreground="green")
        success_label.pack(pady=10)

        self.root.after(2000, success_label.destroy)  # 2000 milliseconds = 2 seconds
        self.show_user_home()





    def view_order(self, order_tree):
        """View selected order details with cart items in a larger frame."""
        selected_item = order_tree.selection()
        if selected_item:
            order_id = order_tree.item(selected_item, "values")[0]
            order_details = self.orders.get(int(order_id))
            
            if order_details:
                # Create a new Toplevel window for displaying order details
                order_window = tk.Toplevel()
                order_window.title(f"Order Details - ID: {order_id}")
                order_window.geometry("400x300")  # Adjust size as needed

                # Display order metadata at the top
                tk.Label(order_window, text=f"Order ID: {order_id}", font=("Arial", 14, "bold")).pack(pady=(10, 5))
                tk.Label(order_window, text=f"Address: {order_details['address']}", font=("Arial", 12)).pack(pady=2)
                tk.Label(order_window, text=f"Note: {order_details['note']}", font=("Arial", 12)).pack(pady=2)
                tk.Label(order_window, text=f"Status: {order_details['status']}", font=("Arial", 12)).pack(pady=(2, 10))

                # Frame for cart items
                cart_frame = ttk.Frame(order_window)
                cart_frame.pack(fill="both", expand=True, padx=10, pady=5)

                # Headers for the cart item list
                headers = ["Product Name", "Quantity", "Price"]
                for col_num, header in enumerate(headers):
                    ttk.Label(cart_frame, text=header, font=("Arial", 10, "bold")).grid(row=0, column=col_num, padx=5, pady=5)

                # List each item in the cart with quantity and price
                for row_num, (product_name, details) in enumerate(order_details["line_items"].items(), start=1):
                    ttk.Label(cart_frame, text=product_name).grid(row=row_num, column=0, padx=5, pady=5)
                    ttk.Label(cart_frame, text=str(details["quantity"])).grid(row=row_num, column=1, padx=5, pady=5)
                    ttk.Label(cart_frame, text=f"${details['price']:.2f}").grid(row=row_num, column=2, padx=5, pady=5)

                # Add a close button at the bottom
                ttk.Button(order_window, text="Close", command=order_window.destroy).pack(pady=10)

    
    def edit_order(self, order_tree):
        """Edit selected order details."""
        selected_item = order_tree.selection()
        if selected_item:
            order_id = order_tree.item(selected_item, "values")[0]
            print(f"Selected Order ID: {order_id}")  # Debugging line
            self.show_create_or_edit_order(order_id=int(order_id))


    def delete_order(self, order_tree):
        """Delete selected order."""
        selected_item = order_tree.selection()
        if selected_item:
            order_id = order_tree.item(selected_item, "values")[0]
            if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete Order ID {order_id}?"):
                del self.orders[int(order_id)]
                self.show_manage_order()


    def logout(self):
        # Destroy any current frame and reset the window to the login view
        if self.current_frame:
            self.current_frame.destroy()

        # Call the return_to_login method to display the login form
        self.return_to_login()

