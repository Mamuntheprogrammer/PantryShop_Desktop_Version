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