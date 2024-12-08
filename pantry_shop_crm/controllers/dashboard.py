import sqlite3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk

class DashboardManager:
    def __init__(self, db_path="pantry_shop_crm.db"):
        self.db_path = db_path

    def connect(self):
        """Establish a database connection."""
        return sqlite3.connect(self.db_path)

    # ------------------------- Get Orders Data -------------------------

    def get_order_counts(self):
        try:
            conn = self.connect()
            cursor = conn.cursor()

            # Fetch total orders count
            cursor.execute("SELECT COUNT(*) FROM orders;")
            total_orders = cursor.fetchone()[0]

            # Fetch approved orders count
            cursor.execute("SELECT COUNT(*) FROM orders WHERE order_status = 'Approved';")
            approved_orders = cursor.fetchone()[0]

            # Fetch pending orders count
            cursor.execute("SELECT COUNT(*) FROM orders WHERE order_status = 'Pending';")
            pending_orders = cursor.fetchone()[0]

            return {
                "total_orders": total_orders,
                "approved_orders": approved_orders,
                "pending_orders": pending_orders
            }

        except sqlite3.Error as e:
            # print(f"Database error: {e}")
            return {"success": False, "message": "An error occurred while fetching orders."}

        finally:
            conn.close()

    # ------------------------- Get Materials Data -------------------------

    def get_material_counts(self):
        try:
            conn = self.connect()
            cursor = conn.cursor()

            # Fetch total materials count
            cursor.execute("SELECT COUNT(*) FROM materials;")
            total_materials = cursor.fetchone()[0]

            # Fetch active materials count
            cursor.execute("SELECT COUNT(*) FROM materials WHERE status = 'Active';")
            active_materials = cursor.fetchone()[0]

            # Fetch inactive materials count
            cursor.execute("SELECT COUNT(*) FROM materials WHERE status = 'Inactive';")
            inactive_materials = cursor.fetchone()[0]

            return {
                "total_materials": total_materials,
                "active_materials": active_materials,
                "inactive_materials": inactive_materials
            }

        except sqlite3.Error as e:
            # print(f"Database error: {e}")
            return {"success": False, "message": "An error occurred while fetching materials."}

        finally:
            conn.close()

    # ------------------------- Get User Counts -------------------------

    def get_user_count(self):
        try:
            conn = self.connect()
            cursor = conn.cursor()

            # Fetch total users count
            cursor.execute("SELECT COUNT(*) FROM users;")
            total_users = cursor.fetchone()[0]

            return {"total_users": total_users}

        except sqlite3.Error as e:
            # print(f"Database error: {e}")
            return {"success": False, "message": "An error occurred while fetching user count."}

        finally:
            conn.close()

    # ------------------------- Get Vendor Counts -------------------------

    def get_vendor_count(self):
        try:
            conn = self.connect()
            cursor = conn.cursor()

            # Fetch total vendors count
            cursor.execute("SELECT COUNT(*) FROM vendors;")
            total_vendors = cursor.fetchone()[0]

            return {"total_vendors": total_vendors}

        except sqlite3.Error as e:
            # print(f"Database error: {e}")
            return {"success": False, "message": "An error occurred while fetching vendor count."}

        finally:
            conn.close()

    # ------------------------- Get Least and Max Stock Products -------------------------

    def get_stock_products(self):
        try:
            conn = self.connect()
            cursor = conn.cursor()

            # Fetch 5 products with the least stock
            cursor.execute("SELECT material_name, current_stock FROM materials ORDER BY current_stock ASC LIMIT 5;")
            least_stock_materials = cursor.fetchall()

            # Fetch 5 products with the most stock
            cursor.execute("SELECT material_name, current_stock FROM materials ORDER BY current_stock DESC LIMIT 5;")
            max_stock_materials = cursor.fetchall()

            return {
                "least_stock_materials": least_stock_materials,
                "max_stock_materials": max_stock_materials
            }

        except sqlite3.Error as e:
            # print(f"Database error: {e}")
            return {"success": False, "message": "An error occurred while fetching stock products."}

        finally:
            conn.close()

    # ------------------------- Generate Pie Charts -------------------------

    def show_welcome_message(self):
        """Display a welcome message with a 3x3 grid of cards."""
        welcome_frame = ttk.Frame(self.content_frame)
        welcome_frame.pack(fill="both", expand=True)

        # Display the welcome label at the top
        ttk.Label(welcome_frame, text="Welcome to the Admin Dashboard", font=("Helvetica", 16)).grid(row=0, column=0, columnspan=3, pady=20)

        # Create a DashboardManager instance to fetch data
        dashboard_manager = DashboardManager()

        # Fetch all necessary data
        order_counts = dashboard_manager.get_order_counts()
        material_counts = dashboard_manager.get_material_counts()
        user_count = dashboard_manager.get_user_count()
        vendor_count = dashboard_manager.get_vendor_count()
        stock_products = dashboard_manager.get_stock_products()

        # ------------------- Row 1: Stats -------------------
        # Card for Total Orders
        ttk.Label(welcome_frame, text=f"Total Orders: {order_counts['total_orders']}", font=("Helvetica", 12)).grid(row=1, column=0, padx=10, pady=10)

        # Card for Approved Orders
        ttk.Label(welcome_frame, text=f"Approved Orders: {order_counts['approved_orders']}", font=("Helvetica", 12)).grid(row=1, column=1, padx=10, pady=10)

        # Card for Pending Orders
        ttk.Label(welcome_frame, text=f"Pending Orders: {order_counts['pending_orders']}", font=("Helvetica", 12)).grid(row=1, column=2, padx=10, pady=10)

        # ------------------- Row 2: Material Stats -------------------
        # Card for Total Materials
        ttk.Label(welcome_frame, text=f"Total Materials: {material_counts['total_materials']}", font=("Helvetica", 12)).grid(row=2, column=0, padx=10, pady=10)

        # Card for Active Materials
        ttk.Label(welcome_frame, text=f"Active Materials: {material_counts['active_materials']}", font=("Helvetica", 12)).grid(row=2, column=1, padx=10, pady=10)

        # Card for Inactive Materials
        ttk.Label(welcome_frame, text=f"Inactive Materials: {material_counts['inactive_materials']}", font=("Helvetica", 12)).grid(row=2, column=2, padx=10, pady=10)

        # ------------------- Row 3: Users and Vendors -------------------
        # Card for Total Users
        ttk.Label(welcome_frame, text=f"Total Users: {user_count['total_users']}", font=("Helvetica", 12)).grid(row=3, column=0, padx=10, pady=10)

        # Card for Total Vendors
        ttk.Label(welcome_frame, text=f"Total Vendors: {vendor_count['total_vendors']}", font=("Helvetica", 12)).grid(row=3, column=1, padx=10, pady=10)

        # Empty card space (can be used for future information or additional cards)
        ttk.Label(welcome_frame, text="Additional Info", font=("Helvetica", 12)).grid(row=3, column=2, padx=10, pady=10)

        # ------------------- Row 4: Donut Charts -------------------
        chart_frame = ttk.Frame(welcome_frame)
        chart_frame.grid(row=4, column=0, columnspan=3, pady=5, padx=5, sticky="nsew")

        # Configure the grid for donut chart row (3 columns)
        chart_frame.grid_columnconfigure(0, weight=1)
        chart_frame.grid_columnconfigure(1, weight=1)
        chart_frame.grid_columnconfigure(2, weight=1)

        # Plot Donut Chart 1: Order Status Distribution
        dashboard_manager.plot_order_donut(chart_frame, order_counts["approved_orders"], order_counts["pending_orders"], order_counts["total_orders"], 0)

        # Plot Donut Chart 2: Material Status Distribution
        dashboard_manager.plot_material_donut(chart_frame, material_counts["active_materials"], material_counts["inactive_materials"], material_counts["total_materials"], 1)

        # ------------------- Row 5: Bar Charts -------------------
        bar_chart_frame = ttk.Frame(welcome_frame)
        bar_chart_frame.grid(row=5, column=0, columnspan=3, pady=5, padx=5, sticky="nsew")

        # Configure the grid for bar chart row (1 column for least stock, 1 column for max stock)
        bar_chart_frame.grid_columnconfigure(0, weight=1)
        bar_chart_frame.grid_columnconfigure(1, weight=1)

        # Plot Bar Chart 1: Least Stock Products
        dashboard_manager.plot_least_stock_materials(bar_chart_frame, stock_products["least_stock_materials"], 0)

        # Plot Bar Chart 2: Max Stock Products
        dashboard_manager.plot_max_stock_materials(bar_chart_frame, stock_products["max_stock_materials"], 1)

        # Show the final welcome_frame
        self.show_frame(welcome_frame)

    # Donut Chart for Order Status
    def plot_order_donut(self, parent_frame, approved_orders, pending_orders, total_orders, column):
        if total_orders == 0 or (approved_orders == 0 and pending_orders == 0):
            return  # If no data, don't plot
        
        sizes = [approved_orders, pending_orders]
        labels = ['Approved', 'Pending']

        # Create Donut chart
        fig, ax = plt.subplots(figsize=(4, 1.7))
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, wedgeprops={'width': 0.3})
        ax.set_title("Order Status")
        ax.axis('equal')

        # Adjust the margins of the plot to make more efficient use of space
        plt.subplots_adjust(left=0.1, right=0.9, top=0.8, bottom=0.1) 

        # Embed Donut chart in Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=parent_frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=column, padx=0, pady=5)


    # Donut Chart for Material Status
    def plot_material_donut(self, parent_frame, active_materials, inactive_materials, total_materials, column):
        if total_materials == 0 or (active_materials == 0 and inactive_materials == 0):
            return  # If no data, don't plot
        
        sizes = [active_materials, inactive_materials]
        labels = ['Active', 'Inactive']

        # Create Donut chart
        fig, ax = plt.subplots(figsize=(4, 1.7))
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, wedgeprops={'width': 0.3})
        ax.set_title("Material Status")
        ax.axis('equal')

        # Adjust the margins of the plot to make more efficient use of space
        plt.subplots_adjust(left=0.1, right=0.9, top=0.8, bottom=0.1)  

        # Embed Donut chart in Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=parent_frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=column, padx=0, pady=5)


    # Bar Chart for Least Stock Materials
    def plot_least_stock_materials(self, parent_frame, least_stock_materials, column):
        if not least_stock_materials:
            return  # If no data, don't plot
        
        materials = [material[0] for material in least_stock_materials]
        stock = [material[1] for material in least_stock_materials]

        # Create bar chart
        fig, ax = plt.subplots(figsize=(4, 2))  # Adjusted size for better view
        bars = ax.bar(materials, stock, color='orange')
        ax.set_ylabel("Stock")
        ax.set_title("Least Stock Products")
        plt.xticks(rotation=45)

        # Display material names inside each bar
        for bar, material in zip(bars, stock):
            yval = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2, yval / 2,  # Position inside the bar (middle)
                    material, ha='center', va='center', fontweight='bold', color='white')  # Material names inside the bar

        # Adjust the margins of the plot to make more efficient use of space
        plt.subplots_adjust(left=0.2, right=0.9, top=0.8, bottom=0.4) 

        # Embed bar chart in Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=parent_frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=column, padx=0, pady=0)


    # Bar Chart for Max Stock Materials
    def plot_max_stock_materials(self, parent_frame, max_stock_materials, column):
        if not max_stock_materials:
            return  # If no data, don't plot
        
        materials = [material[0] for material in max_stock_materials]
        stock = [material[1] for material in max_stock_materials]

        # Create bar chart
        fig, ax = plt.subplots(figsize=(4, 2))  # Adjusted size for better view
        bars = ax.bar(materials, stock, color='green')
        ax.set_ylabel("Stock")
        ax.set_title("Max Stock Products")
        plt.xticks(rotation=45)

        # Display material names inside each bar
        for bar, material in zip(bars, stock):
            yval = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2, yval / 2,  # Position inside the bar (middle)
                    material, ha='center', va='center', fontweight='bold', color='white')  # Material names inside the bar

        # Adjust the margins of the plot to make more efficient use of space
        plt.subplots_adjust(left=0.2, right=0.9, top=0.8, bottom=0.4) 

        # Embed bar chart in Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=parent_frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=column, padx=0, pady=0)

