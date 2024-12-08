import sqlite3
from tkinter import messagebox
from datetime import datetime

class VendorManager:
    def __init__(self, db_path="pantry_shop_crm.db"):
        self.db_path = db_path

    def connect(self):
        return sqlite3.connect(self.db_path)

    def add_vendor(self, vendor_data):
        """Adds a new vendors to the database."""
        try:
            conn = self.connect()
            cursor = conn.cursor()

            query = """
            INSERT INTO vendors (vendor_id, vendor_name, contact_fname, contact_lname, contact_email,
                                contact_phone, address_key, is_active, created_date, created_by)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            cursor.execute(query, (
                vendor_data['vendor_id'], vendor_data['vendor_name'], vendor_data['contact_fname'],
                vendor_data['contact_lname'], vendor_data['contact_email'], vendor_data['contact_phone'],
                vendor_data['address_key'], vendor_data['is_active'], datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                vendor_data['created_by']
            ))

            conn.commit()
            messagebox.showinfo("Vendor Added", "New vendor has been successfully added.")
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
        finally:
            conn.close()

    def load_vendor(self, vendor_id):
        """Loads an existing vendors from the database."""
        try:
            conn = self.connect()
            cursor = conn.cursor()

            query = "SELECT * FROM vendors WHERE vendor_id = ?"
            cursor.execute(query, (vendor_id,))
            vendor = cursor.fetchone()

            if vendor:
                vendor_data = {
                    "vendor_id": vendor[0],
                    "vendor_name": vendor[1],
                    "contact_fname": vendor[2],
                    "contact_lname": vendor[3],
                    "contact_email": vendor[4],
                    "contact_phone": vendor[5],
                    "address_key": vendor[6],
                    "is_active": vendor[7],
                    "created_date": vendor[8],
                    "created_by": vendor[9]
                }
                return vendor_data
            else:
                messagebox.showinfo("Vendor Not Found", f"No vendor found with ID {vendor_id}")
                return None
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
            return None
        finally:
            conn.close()

    def update_vendor(self, vendor_id, updated_data):
        """Updates an existing vendor's information in the database."""
        try:
            conn = self.connect()
            cursor = conn.cursor()

            query = """
            UPDATE vendors SET vendor_name = ?, contact_fname = ?, contact_lname = ?, contact_email = ?,
                              contact_phone = ?, address_key = ?, is_active = ?, created_by = ?
            WHERE vendor_id = ?
            """
            cursor.execute(query, (
                updated_data['vendor_name'], updated_data['contact_fname'], updated_data['contact_lname'],
                updated_data['contact_email'], updated_data['contact_phone'], updated_data['address_key'],
                updated_data['is_active'], updated_data['created_by'], vendor_id
            ))

            conn.commit()

            if cursor.rowcount == 0:
                messagebox.showinfo("Update Error", "No vendor found with the provided ID.")
            else:
                messagebox.showinfo("Vendor Updated", "Vendor information has been successfully updated.")
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
        finally:
            conn.close()





    def get_all_vendors(self):
        try:
            # Connect to the database using the Database class
            conn = self.connect()  # assuming you have a method in your Database class to connect
            cursor = conn.cursor()

            # SQL query to fetch all materials from the `materials` table
            cursor.execute('''
                SELECT vendor_id,vendor_name,contact_fname,contact_lname,
                contact_email,contact_phone,address_key,is_active,created_date,created_by
                FROM vendors
            ''')

            # Fetch all rows from the result
            vendors = cursor.fetchall()

            # Return the fetched materials
            return {"success": True, "data": vendors}

        except sqlite3.Error as e:
            # print(f"Database error: {e}")
            return {"success": False, "message": "An error occurred while fetching materials."}

        finally:
            # Ensure the connection is closed after the operation
            conn.close()