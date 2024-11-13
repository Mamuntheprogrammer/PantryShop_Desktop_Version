import sqlite3
from datetime import datetime

class MaterialManager:
    def __init__(self, db_path="pantry_shop_crm.db"):
        self.db_path = db_path

    def connect(self):
        return sqlite3.connect(self.db_path)

    def save_material_type(self, materialtype_data):
        # Connect to the database


        try:
            conn = self.connect()
            cursor = conn.cursor()
            # Insert data into the `material_type` table
            cursor.execute('''
                INSERT INTO material_type (id, material_type, material_desc, created_date, created_by)
                VALUES (?, ?, ?, ?, ?)
            ''', (materialtype_data["material_type_id"], materialtype_data["material_type"], materialtype_data["material_desc"], 
                  materialtype_data["created_date"], materialtype_data["created_by"]))

            # Commit changes and close the connection
            conn.commit()
            return {"success": True, "message": "Material type created successfully"}
            

        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return {"success": False, "message": "An error occurred during Material Creation."}

        finally:
            conn.close()
 


#  -------------------------------Create meterial logics--------------------

    def get_material_types(self):
        # Fetch material types from the database and return as a list
        try:
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute("SELECT material_type FROM material_type")
            material_types = [row[0] for row in cursor.fetchall()]
            conn.close()
            return material_types
        except Exception as e:
            print("Error fetching material types:", e)
            return []
        
    def create_material(self, material_data):
        # Connect to the database
        try:
            conn = self.connect()  # assuming you have a connect method
            cursor = conn.cursor()
            
            # Insert data into the `materials` table
            cursor.execute('''
                INSERT INTO materials (
                    material_name,
                    material_type,
                    description,
                    current_stock,
                    status,
                    created_date,
                    created_by
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                material_data["material_name"],
                material_data["material_type"],
                material_data["description"],
                material_data["current_stock"],
                material_data["status"],
                material_data["created_date"],
                material_data["created_by"]
            ))

            # Commit changes and close the connection
            conn.commit()
            return {"success": True, "message": "Material created successfully"}

        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return {"success": False, "message": "An error occurred during Material creation."}

        finally:
            conn.close()