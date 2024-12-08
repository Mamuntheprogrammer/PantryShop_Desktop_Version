import sqlite3
from datetime import datetime
from tkinter import messagebox

class MaterialManager:
    def __init__(self, db_path="pantry_shop_crm.db"):
        self.db_path = db_path

    def connect(self):
        return sqlite3.connect(self.db_path)
    

#  ------------------------------- Material Types logics--------------------

    def save_material_type(self, materialtype_data):
        # Connect to the database
        try:
            conn = self.connect()
            cursor = conn.cursor()
            # Insert data into the `material_type` table
            cursor.execute('''
                INSERT INTO material_type (id, m_type, material_desc, created_date, created_by)
                VALUES (?, ?, ?, ?, ?)
            ''', (materialtype_data["material_type_id"], materialtype_data["m_type"], materialtype_data["material_desc"], 
                  materialtype_data["created_date"], materialtype_data["created_by"]))

            # Commit changes and close the connection
            conn.commit()
            return {"success": True, "message": "Material type created successfully"}
        except sqlite3.Error as e:
            # print(f"Database error: {e}")
            return {"success": False, "message": "An error occurred during Material Creation."}
        finally:
            conn.close()
 


    def get_material_types(self):
        # Fetch material types from the database and return as a list
        try:
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM material_type")
            material_types = [row[0] for row in cursor.fetchall()]
            conn.close()
            return material_types
        except Exception as e:
            # print("Error fetching material types:", e)
            return []
        


    def get_vendor_ids(self):
        # Fetch material types from the database and return as a list
        try:
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute("SELECT vendor_id FROM vendors")
            vendorids = [row[0] for row in cursor.fetchall()]
            # print("from get vendors id ",vendorids)
            conn.close()
            return vendorids
        except Exception as e:
            # print("Error fetching vendors:", e)
            return []
    
#  -------------------------------Create meterial logics--------------------

    def add_material(self, material_data):
        """Adds a new material to the database."""
        try:
            conn = self.connect()
            cursor = conn.cursor()

            query = """
            INSERT INTO materials (material_id, material_name, material_type, description, current_stock,
                                   status, created_date, created_by)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """
            cursor.execute(query, (
                material_data['material_id'], material_data['material_name'], material_data['material_type'],
                material_data['description'], material_data['current_stock'], material_data['status'],
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'), material_data['created_by']
            ))

                    # Fetch vendor_name for namebyvendor
            cursor.execute("SELECT vendor_name FROM Vendors WHERE vendor_id = ?", (material_data['vendor_id']))
            
            vendor_name = cursor.fetchone()
            # print(vendor_name)
            if vendor_name:
                vendor_name = vendor_name[0]  # Extract the name from the tuple
                # print(vendor_name)

                # Insert into Vendormaterial
                cursor.execute(
                    "INSERT INTO Vendor_material (material_id, vendor_id, namebyvendor) VALUES (?, ?, ?)",
                    (material_data['material_id'], material_data['vendor_id'], vendor_name)
                )

            conn.commit()
            # print("Material and VendorMaterial records added successfully!")

            conn.commit()
            messagebox.showinfo("Material Added", "New material has been successfully added.")
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
        finally:
            conn.close()

    def load_material(self, material_id):
        """Loads an existing material from the database, including the material type name."""
        try:
            conn = self.connect()
            cursor = conn.cursor()

            # Update the query to join materials with material_types to get the type name
            query = """
                        SELECT 
                            materials.material_id, 
                            materials.material_name, 
                            material_type.id, 
                            materials.description, 
                            materials.current_stock, 
                            materials.status, 
                            materials.created_date, 
                            materials.created_by, 
                            vendor_material.vendor_id
                        FROM 
                            materials
                        JOIN 
                            material_type ON materials.material_type = material_type.id
                        LEFT JOIN 
                            vendor_material ON materials.material_id = vendor_material.material_id
                        WHERE 
                            materials.material_id = ?;
            """
            cursor.execute(query, (material_id,))
            material = cursor.fetchone()


            if material:
                material_data = {
                    "material_id": material[0],
                    "material_name": material[1],
                    "material_type": material[2],  # This will now be the type name, not the ID
                    "description": material[3],
                    "current_stock": material[4],
                    "status": material[5],
                    "created_date": material[6],
                    "created_by": material[7],
                    "vendor_id": material[8]
                }
                return material_data
            else:
                messagebox.showinfo("Material Not Found", f"No material found with ID {material_id}")
                return None
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
            return None
        finally:
            conn.close()


    def update_material(self, material_id, updated_data):
        """Updates an existing material's information in the database."""
        try:
            # print("from updat:",updated_data)
            conn = self.connect()
            cursor = conn.cursor()

            query = """
            UPDATE materials SET material_name = ?, material_type = ?, description = ?, current_stock = ?,
                                status = ?, created_by = ?
            WHERE material_id = ?
            """
            cursor.execute(query, (
                updated_data['material_name'], updated_data['material_type'], updated_data['description'],
                updated_data['current_stock'], updated_data['status'], updated_data['created_by'], material_id
            ))

            cursor.execute(
                """UPDATE Vendor_material 
                SET vendor_id = ?, 
                    namebyvendor = (SELECT vendor_name FROM Vendors WHERE vendor_id = ?)
                WHERE material_id = ?""",
                (updated_data['vendor_id'], updated_data['vendor_id'], material_id
                 ))


            conn.commit()

            if cursor.rowcount == 0:
                messagebox.showinfo("Update Error", "No material found with the provided ID.")
            else:
                messagebox.showinfo("Material Updated", "Material information has been successfully updated.")
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
        finally:
            conn.close()




    def update_stock(self, material_id, updated_data):
        """Updates an existing material's stock information in the database."""
        try:
            conn = self.connect()
            cursor = conn.cursor()

            query = """
            UPDATE materials SET current_stock = ?
            WHERE material_id = ?
            """
            cursor.execute(query, (
                updated_data['current_stock'],  # Use the current stock value
                material_id  # Use the material ID to locate the correct record
            ))

            conn.commit()

            if cursor.rowcount == 0:
                messagebox.showinfo("Update Error", "No material found with the provided ID.")
            else:
                messagebox.showinfo("Material Updated", "Material stock has been successfully updated.")
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
        finally:
            conn.close()


# -------------------------------- Get Meterials Data -------------------------------


    def get_all_materials(self):
        try:
            # Connect to the database using the Database class
            conn = self.connect()  # assuming you have a method in your Database class to connect
            cursor = conn.cursor()

            # SQL query to fetch all materials along with vendor details
            cursor.execute(''' 
                SELECT m.material_id, m.material_name, m.material_type, m.description, m.current_stock, 
                    m.status, m.created_date, m.created_by, v.vendor_id, v.vendor_name
                FROM materials m
                LEFT JOIN vendor_material vm ON m.material_id = vm.material_id
                LEFT JOIN vendors v ON vm.vendor_id = v.vendor_id
            ''')

            # Fetch all rows from the result
            materials = cursor.fetchall()

            # Return the fetched materials along with vendor details
            return {"success": True, "data": materials}

        except sqlite3.Error as e:
            # print(f"Database error: {e}")
            return {"success": False, "message": "An error occurred while fetching materials."}

        finally:
            # Ensure the connection is closed after the operation
            conn.close()



