import pandas as pd
import sqlite3
from tkinter import messagebox

class UploadFileManager:
    def __init__(self, db_path="pantry_shop_crm.db"):
        self.db_path = db_path

# import sqlite3
# import pandas as pd
# from tkinter import messagebox

    def upload_materials(self, file_path):
        # Connect to the database
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        try:
            # Read Excel file
            df = pd.read_excel(file_path)

            # Print column names for debugging
            # print("Columns in the Excel file:", df.columns.tolist())

            # Normalize column names
            df.columns = df.columns.str.strip().str.lower()

            # Verify columns in the DataFrame
            required_columns = ["material_name", "material_type", "description", "current_stock", "status", "created_date", "created_by", "vendor_id", "namebyvendor"]
            if not all(column in df.columns for column in required_columns):
                raise ValueError("Excel file must contain the required columns: " + ", ".join(required_columns))

            # Ensure created_date is in string format
            if "created_date" in df.columns:
                df["created_date"] = pd.to_datetime(df["created_date"], errors='coerce').dt.strftime("%Y-%m-%d")

            skipped_rows = []

            for _, row in df.iterrows():
                try:
                    # Check if vendor_id exists in the 'vendors' table
                    cursor.execute("SELECT COUNT(*) FROM vendors WHERE vendor_id = ?", (row["vendor_id"],))
                    vendor_exists = cursor.fetchone()[0]

                    if not vendor_exists:
                        raise ValueError(f"Vendor ID {row['vendor_id']} does not exist in the 'vendors' table.")

                    # Check if material_type exists in the 'material_type' table
                    cursor.execute("SELECT COUNT(*) FROM material_type WHERE id = ?", (row["material_type"],))
                    material_type_exists = cursor.fetchone()[0]

                    if not material_type_exists:
                        raise ValueError(f"Material Type '{row['material_type']}' does not exist in the 'material_type' table.")

                    # Check if the same material_name already exists in the 'materials' table to get material_id
                    cursor.execute('''
                        SELECT material_id FROM materials WHERE material_name = ?
                    ''', (row["material_name"],))
                    material_id_result = cursor.fetchone()

                    if material_id_result:
                        material_id = material_id_result[0]
                        
                        # Check if the combination of material_id and vendor_id already exists in the 'vendor_material' table
                        cursor.execute('''
                            SELECT COUNT(*) FROM vendor_material
                            WHERE material_id = ? AND vendor_id = ?
                        ''', (material_id, row["vendor_id"]))
                        vendor_material_exists = cursor.fetchone()[0]

                        if vendor_material_exists:
                            raise ValueError(f"Material '{row['material_name']}' with Vendor ID {row['vendor_id']} already exists in vendor_material table.")
                                        
                    # Insert into 'materials' table
                    cursor.execute(''' 
                        INSERT INTO materials (material_name, material_type, description, current_stock, status, created_date, created_by)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        row["material_name"],
                        row["material_type"],
                        row["description"],
                        row["current_stock"],
                        row["status"],
                        row["created_date"],
                        row["created_by"]
                    ))

                    # Get the last inserted material ID
                    material_id = cursor.lastrowid

                    # Insert into 'vendor_material' table
                    cursor.execute('''
                        INSERT INTO vendor_material (material_id, vendor_id, namebyvendor)
                        VALUES (?, ?, ?)
                    ''', (
                        material_id,
                        row["vendor_id"],
                        row["namebyvendor"]
                    ))

                except Exception as e:
                    # Add skipped rows with error details
                    skipped_rows.append({"row": row.to_dict(), "error": str(e)})

            connection.commit()

            # Show result using messagebox
            if skipped_rows:
                skipped_message = "\n".join([f"Row: {row['row']}, Error: {row['error']}" for row in skipped_rows])
                messagebox.showinfo("Upload Completed", f"Upload completed with skipped rows:\n{skipped_message}")
            else:
                messagebox.showinfo("Upload Completed", "Upload completed successfully with no skipped rows.")

            return "Materials uploaded successfully."

        except Exception as e:
            # Show error message
            messagebox.showerror("Error", f"Error uploading materials: {e}")
            return f"Error uploading materials: {e}"

        finally:
            connection.close()
