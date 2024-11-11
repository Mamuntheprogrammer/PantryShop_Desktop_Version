 
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime

class PantryShopApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pantry Shop CRM")
        self.root.geometry("900x600")
        
        # Placeholder for cart items
        self.cart = {}

    def show_create_order(self):
        # Main frame with scrollable area
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill="both", expand=True)
        
        # Horizontal scrollbar for the main frame
        h_scrollbar = ttk.Scrollbar(main_frame, orient="horizontal")
        h_scrollbar.pack(side="bottom", fill="x")

        # Product Selection Frame with Treeview and Scrollbar
        product_frame = ttk.Frame(main_frame, borderwidth=1, relief="solid", padding=10)
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
        self.order_frame = ttk.Frame(main_frame, borderwidth=2, relief="groove", padding=10)
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

    def update_order_frame(self):
        # Clear the order frame's product section
        for widget in self.order_frame.grid_slaves():
            if int(widget.grid_info()["row"]) > 1 and int(widget.grid_info()["row"]) < 20:
                widget.grid_forget()

        # Header for Order Frame
        ttk.Label(self.order_frame, text="Product", font=("Helvetica", 12, "bold")).grid(row=1, column=0, padx=5, pady=5)
        ttk.Label(self.order_frame, text="Quantity", font=("Helvetica", 12, "bold")).grid(row=1, column=1, padx=5, pady=5)
        ttk.Label(self.order_frame, text="Actions", font=("Helvetica", 12, "bold")).grid(row=1, column=2, padx=5, pady=5)

        # Display each product in cart with quantity and action buttons
        row = 2
        for product_name, details in self.cart.items():
            ttk.Label(self.order_frame, text=product_name).grid(row=row, column=0, padx=5, pady=5)
            ttk.Label(self.order_frame, text=str(details["quantity"])).grid(row=row, column=1, padx=5, pady=5)

            # Action buttons: Add, Remove, and X for deleting the product
            action_frame = ttk.Frame(self.order_frame)
            action_frame.grid(row=row, column=2, padx=5, pady=5)

            # Increment quantity button
            increment_button = ttk.Button(action_frame, text="+", command=lambda p=product_name: self.increment_quantity(p))
            increment_button.grid(row=0, column=0, padx=2)
            
            # Decrement quantity button
            decrement_button = ttk.Button(action_frame, text="-", command=lambda p=product_name: self.decrement_quantity(p))
            decrement_button.grid(row=0, column=1, padx=2)

            # X button for removing item from cart
            remove_button = ttk.Button(action_frame, text="X", command=lambda p=product_name: self.remove_from_cart(p))
            remove_button.grid(row=0, column=2, padx=2)

            row += 1

    def increment_quantity(self, product_name):
        if product_name in self.cart:
            self.cart[product_name]["quantity"] += 1
        self.update_order_frame()

    def decrement_quantity(self, product_name):
        if product_name in self.cart and self.cart[product_name]["quantity"] > 1:
            self.cart[product_name]["quantity"] -= 1
        else:
            del self.cart[product_name]  # Remove item if quantity goes to 0
        self.update_order_frame()

    def remove_from_cart(self, product_name):
        if product_name in self.cart:
            del self.cart[product_name]
        self.update_order_frame()

    def submit_order(self):
        if not self.cart:
            messagebox.showinfo("Empty Cart", "Cannot submit an order with an empty cart.")
            return

        # Gather order details
        order_date = datetime.now().strftime("%Y-%m-%d")  # Automatic order date
        address = self.address_var.get()  # User-entered address
        note = self.note_var.get()        # User-entered note
        created_date = datetime.now().strftime("%Y-%m-%d")  # Automatic created date

        print("Order submitted with the following items:")
        for product, details in self.cart.items():
            print(f"{product}: {details['quantity']} x ${details['price']}")
        print(f"Order Date: {order_date}, Address: {address}, Note: {note}, Created Date: {created_date}")

        # Clear cart and fields after submission
        self.cart.clear()
        self.address_var.set("")
        self.note_var.set("")
        self.update_order_frame()

    

if __name__ == "__main__":
    root = tk.Tk()
    app = PantryShopApp(root)
    app.show_create_order()
    root.mainloop()
