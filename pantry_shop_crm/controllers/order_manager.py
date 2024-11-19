import sqlite3
from datetime import datetime
from tkinter import messagebox

class OrderManager:
    def __init__(self, db_path="pantry_shop_crm.db"):
        self.db_path = db_path

    def connect(self):
        return sqlite3.connect(self.db_path)

# -------------------------------- Get Meterials Data -------------------------------


    def get_all_materials(self):
        try:
            # Connect to the database using the Database class
            conn = self.connect()  # assuming you have a method in your Database class to connect
            cursor = conn.cursor()

            # SQL query to fetch all materials from the `materials` table
            cursor.execute('''
                SELECT material_name, current_stock
                FROM materials where current_stock>0
            ''')

            # Fetch all rows from the result
            materials = cursor.fetchall()

            # Return the fetched materials
            return {"data": materials}

        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return {"success": False, "message": "An error occurred while fetching materials."}

        finally:
            # Ensure the connection is closed after the operation
            conn.close()





# 
# -------------------------------------------------------------------------------
# 




    def insert_order(self, cart, orderdetails):
        try:
            # Connect to the database
            conn = self.connect()
            cursor = conn.cursor()

            # Insert the order into the 'orders' table
            user_id = orderdetails['user_id']
            pickup_date = orderdetails['pickup']
            order_text = orderdetails['note']
            order_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Current timestamp
            created_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Current timestamp

            cursor.execute("""
                INSERT INTO orders (user_id, order_date, pickup_date, order_status, order_text, created_date)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (user_id, order_date, pickup_date, "Pending", order_text, created_date))

            # Get the generated order_id
            order_id = cursor.lastrowid

            # Insert the items from the cart into the 'order_item' table
            for item_name, item_details in cart.items():
                material_id = self.get_material_id(item_name)  # Get material ID from the material name
                quantity = item_details['quantity']
                unit_price = 0  # Get unit price for the material (set to 0 if no price is available)

                cursor.execute("""
                    INSERT INTO order_item (order_id, material_id, quantity, unit_price)
                    VALUES (?, ?, ?, ?)
                """, (order_id, material_id, quantity, unit_price))

            # Commit the changes and close the connection
            conn.commit()
            return {"success": True, "message": "Order created successfully"}

        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return {"success": False, "message": "An error occurred during order creation."}

        finally:
            conn.close()



    def get_material_id(self, material_name):
        """Get the material ID based on the material name."""
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("SELECT material_id FROM materials WHERE material_name = ?", (material_name,))
        result = cursor.fetchone()

        conn.close()

        if result:
            return result[0]
        else:
            raise ValueError(f"Material {material_name} not found in materials table.")

    # def get_material_price(self, material_id):
    #     """Get the price of a material based on its ID."""
    #     conn = self.connect()
    #     cursor = conn.cursor()

    #     cursor.execute("SELECT price FROM materials WHERE material_id = ?", (material_id,))
    #     result = cursor.fetchone()

    #     conn.close()

    #     if result:
    #         return result[0]
    #     else:
    #         raise ValueError(f"Material with ID {material_id} not found in materials table.")



    def get_orders(self, user_id):
        """Get the orders for a specific user."""
        conn = self.connect()
        cursor = conn.cursor()

        # Correct the query execution syntax
        cursor.execute("""
            SELECT order_id, user_id, order_date, pickup_date, order_status 
            FROM orders 
            WHERE user_id = ?
        """, (user_id,))  # Ensure parameters are passed as a tuple

        result = cursor.fetchall()  # Use fetchall() to get all orders for the user

        conn.close()

        if result:
            return result  # Return all the orders for the user
        else:
            raise ValueError("Orders not found")

        

    def get_ordersdetails(self, order_id):
        try:
            conn = self.connect()
            cursor = conn.cursor()
            # Execute the query to fetch order details
            cursor.execute('''SELECT 
                                    o.order_id, 
                                    o.pickup_date, 
                                    o.order_status, 
                                    m.material_name, 
                                    oi.quantity
                                FROM 
                                    orders o
                                JOIN 
                                    order_item oi ON o.order_id = oi.order_id
                                JOIN 
                                    materials m ON oi.material_id = m.material_id
                                WHERE 
                                    o.order_id = ?;''', (order_id,))

            # Fetch all rows from the query result
            result = cursor.fetchall()
            conn.close()


            # Check if any records were found
            if result:
                return result
            else:
                return None

        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return None
        
#  ---------------- For Order - Admin ------------

    def get_all_orders(self):
        """Get the orders for a specific user."""
        conn = self.connect()
        cursor = conn.cursor()

        # Correct the query execution syntax
        cursor.execute("""
            SELECT order_id, user_id, order_date, pickup_date, order_status 
            FROM orders 
            
        """)  # Ensure parameters are passed as a tuple

        result = cursor.fetchall()  # Use fetchall() to get all orders for the user

        conn.close()

        if result:
            return result  # Return all the orders for the user
        else:
            raise ValueError("Orders not found")
        
    def get_orders_between_dates(self, start_date, end_date):
        """Get all order details between a specific date range."""
        conn = self.connect()  # Assuming you have a method to establish the DB connection
        cursor = conn.cursor()

        # SQL query to get the order details within the specified date range
        cursor.execute("""
            SELECT
                o.order_id,
                o.user_id,
                u.first_name,
                u.last_name,
                u.email_address,
                o.order_date,
                o.pickup_date,
                o.order_status,
                o.order_text,
                oi.material_id,
                m.material_name,
                oi.quantity,
                oi.unit_price,
                u.role_type
            FROM
                orders o
            INNER JOIN
                users u ON o.user_id = u.user_id
            INNER JOIN
                order_item oi ON o.order_id = oi.order_id
            INNER JOIN
                materials m ON oi.material_id = m.material_id
            WHERE
                o.pickup_date BETWEEN ? AND ?
            ORDER BY
                o.pickup_date;
        """, (start_date, end_date))  # Use the tuple (start_date, end_date) for parameterized query

        result = cursor.fetchall()  # Fetch all matching records

        conn.close()

        if result:
            return result  # Return all orders within the specified date range
        else:
            raise ValueError("No orders found in the specified date range")


# ------------------------------------
    def get_orders_between_dates_p(self, start_date, end_date):
        """Get all order details between a specific date range."""
        conn = self.connect()  # Assuming you have a method to establish the DB connection
        cursor = conn.cursor()

        # SQL query to get the order details within the specified date range
        cursor.execute("""
            SELECT
                DISTINCT o.order_id,
                o.order_status,
                o.user_id,
                o.order_date,
                o.pickup_date
                
            FROM
                orders o
            INNER JOIN
                users u ON o.user_id = u.user_id
            INNER JOIN
                order_item oi ON o.order_id = oi.order_id
            INNER JOIN
                materials m ON oi.material_id = m.material_id
            WHERE
                o.pickup_date BETWEEN ? AND ?
            ORDER BY
                o.order_status;
        """, (start_date, end_date))  # Use the tuple (start_date, end_date) for parameterized query

        result = cursor.fetchall()  # Fetch all matching records

        conn.close()

        if result:
            return result  # Return all orders within the specified date range
        else:
            raise ValueError("No orders found in the specified date range")
        



#  ---------------- update the stock , change the order status ---------


    def process_existing_order(self, order_id):
        try:
            # Connect to the database
            conn = self.connect()
            cursor = conn.cursor()

            # Check if the order exists and is in "Pending" status
            cursor.execute("SELECT order_status FROM orders WHERE order_id = ?", (order_id,))
            order = cursor.fetchone()

            if not order:
                return {"success": False, "message": "Order not found."}
            
            order_status = order[0]

            if order_status != "Pending":
                return {"success": False, "message": "Order is already approved or processed."}

            # Track whether any items are removed (insufficient stock)
            all_items_approved = True

            # Get all items in the order
            cursor.execute("""
                SELECT oi.material_id, oi.quantity
                FROM order_item oi
                WHERE oi.order_id = ?
            """, (order_id,))
            items = cursor.fetchall()

            for material_id, quantity in items:
                # Check available stock for the material
                cursor.execute("SELECT current_stock FROM materials WHERE material_id = ?", (material_id,))
                stock = cursor.fetchone()

                if stock:
                    stock = stock[0]  # stock is returned as a tuple, so access the first element
                    if float(stock) >= float(quantity):  # Convert both to float before comparison
                        # Update the material stock
                        cursor.execute("""
                            UPDATE materials
                            SET current_stock = current_stock - ?
                            WHERE material_id = ?
                        """, (quantity, material_id))
                    else:
                        # Insufficient stock, delete the order item
                        cursor.execute("""
                            DELETE FROM order_item
                            WHERE order_id = ? AND material_id = ?
                        """, (order_id, material_id))
                        all_items_approved = False
                else:
                    # If no stock information, consider the item as failed
                    cursor.execute("""
                        DELETE FROM order_item
                        WHERE order_id = ? AND material_id = ?
                    """, (order_id, material_id))
                    all_items_approved = False

            # Update the order status based on stock availability
            if all_items_approved:
                cursor.execute("""
                    UPDATE orders
                    SET order_status = 'Approved'
                    WHERE order_id = ?
                """, (order_id,))
            else:
                cursor.execute("""
                    UPDATE orders
                    SET order_status = 'Pending'
                    WHERE order_id = ?
                """, (order_id,))

            # Commit the changes and close the connection
            conn.commit()
            return {"success": True, "message": "Order processed successfully"}

        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return {"success": False, "message": "An error occurred during order processing."}
        
        finally:
            conn.close()