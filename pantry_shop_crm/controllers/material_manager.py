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
 
