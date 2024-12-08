import tkinter as tk
from tkinter import ttk
import sqlite3

class UDashboardManager:
    def __init__(self, db_path="pantry_shop_crm.db"):
        self.db_path = db_path

    def connect(self):
        """Establish a database connection."""
        return sqlite3.connect(self.db_path)

    def get_user_dashboard_data(self, user_id):
        """Fetch order stats and last order details for a specific user."""
        try:
            conn = self.connect()
            cursor = conn.cursor()

            # Fetch total orders count for the user
            cursor.execute("SELECT COUNT(*) FROM orders WHERE user_id = ?;", (user_id,))
            total_orders = cursor.fetchone()[0]

            # Fetch pending orders count for the user
            cursor.execute("SELECT COUNT(*) FROM orders WHERE user_id = ? AND order_status = 'Pending';", (user_id,))
            pending_orders = cursor.fetchone()[0]

            # Fetch approved orders count for the user
            cursor.execute("SELECT COUNT(*) FROM orders WHERE user_id = ? AND order_status = 'Approved';", (user_id,)) 
            approved_orders = cursor.fetchone()[0]

            # Fetch the last order number and date for the user
            cursor.execute(
                "SELECT order_id, order_date FROM orders WHERE user_id = ? ORDER BY order_date DESC LIMIT 1;", 
                (user_id,)
            )
            last_order = cursor.fetchone()

            last_order_id = last_order[0] if last_order else None
            last_order_date = last_order[1] if last_order else None

            return {
                "total_orders": total_orders,
                "pending_orders": pending_orders,
                "approved_orders": approved_orders,
                "last_order_id": last_order_id,
                "last_order_date": last_order_date,
            }

        except sqlite3.Error as e:
            # print(f"Database error: {e}")
            return {"success": False, "message": "An error occurred while fetching dashboard data."}

        finally:
            conn.close()

    # def show_welcome_message(self, user_id):
    #     """Display a welcome message with a 3x3 grid of cards."""
    #     welcome_frame = ttk.Frame(self.content_frame)
    #     welcome_frame.pack(fill="both", expand=True)

    #     # Fetch the user dashboard data
    #     dashboard_data = self.get_user_dashboard_data(user_id)

    #     # Display the welcome label at the top
    #     ttk.Label(welcome_frame, text="Welcome to the User Dashboard", font=("Helvetica", 16)).grid(row=0, column=0, columnspan=3, pady=20)

    #     if dashboard_data.get("success", True):
    #         # ------------------- Row 1: Stats -------------------
    #         # Card for Total Orders
    #         ttk.Label(welcome_frame, text=f"Total Orders: {dashboard_data['total_orders']}", font=("Helvetica", 12)).grid(row=1, column=0, padx=10, pady=10)

    #         # Card for Approved Orders
    #         ttk.Label(welcome_frame, text=f"Approved Orders: {dashboard_data['approved_orders']}", font=("Helvetica", 12)).grid(row=1, column=1, padx=10, pady=10)

    #         # Card for Pending Orders
    #         ttk.Label(welcome_frame, text=f"Pending Orders: {dashboard_data['pending_orders']}", font=("Helvetica", 12)).grid(row=1, column=2, padx=10, pady=10)

    #         # ------------------- Row 2: Last Order Info -------------------
    #         # Card for Last Order Number
    #         ttk.Label(welcome_frame, text=f"Last Order ID: {dashboard_data['last_order_id'] or 'N/A'}", font=("Helvetica", 12)).grid(row=2, column=0, padx=10, pady=10)

    #         # Card for Last Order Date
    #         ttk.Label(welcome_frame, text=f"Last Order Date: {dashboard_data['last_order_date'] or 'N/A'}", font=("Helvetica", 12)).grid(row=2, column=1, padx=10, pady=10)

    #         # ------------------- Row 3: Empty Slot -------------------
    #         # Empty card space (can be used for future information or additional cards)
    #         ttk.Label(welcome_frame, text="Additional Info", font=("Helvetica", 12)).grid(row=3, column=2, padx=10, pady=10)

    #     else:
    #         # If there was an error fetching data, display a message
    #         ttk.Label(welcome_frame, text="Error fetching dashboard data", font=("Helvetica", 12), foreground="red").grid(row=1, column=0, columnspan=3, pady=20)
