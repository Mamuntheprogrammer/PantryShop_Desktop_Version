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
            print(f"Database error: {e}")
            return {"success": False, "message": "An error occurred during Material Creation."}

        finally:
            conn.close()
 


    def get_material_types(self):
        # Fetch material types from the database and return as a list
        try:
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute("SELECT m_type FROM material_type")
            material_types = [row[0] for row in cursor.fetchall()]
            conn.close()
            return material_types
        except Exception as e:
            print("Error fetching material types:", e)
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
                SELECT materials.material_id, materials.material_name, material_type.m_type, 
                    materials.description, materials.current_stock, materials.status, 
                    materials.created_date, materials.created_by
                FROM materials
                JOIN material_type ON materials.material_type = material_type.id
                WHERE materials.material_id = ?
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
                    "created_by": material[7]
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
            conn = self.connect()
            cursor = conn.cursor()

            query = """
            UPDATE materials SET material_name = ?, m_type = ?, description = ?, current_stock = ?,
                                status = ?, created_by = ?
            WHERE material_id = ?
            """
            cursor.execute(query, (
                updated_data['material_name'], updated_data['m_type'], updated_data['description'],
                updated_data['current_stock'], updated_data['status'], updated_data['created_by'], material_id
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

            # SQL query to fetch all materials from the `materials` table
            cursor.execute('''
                SELECT material_id, material_name, material_type,description,current_stock, status,created_date,created_by
                FROM materials
            ''')

            # Fetch all rows from the result
            materials = cursor.fetchall()

            # Return the fetched materials
            return {"success": True, "data": materials}

        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return {"success": False, "message": "An error occurred while fetching materials."}

        finally:
            # Ensure the connection is closed after the operation
            conn.close()


