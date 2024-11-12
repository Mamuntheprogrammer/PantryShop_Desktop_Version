import pandas as pd
import sqlite3

class UploadFileManager:
    def __init__(self, db_path="pantry_shop_crm.db"):
        self.db_path = db_path

    def upload_materials(self, file_path):
        # Connect to the database
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        try:
            # Load the Excel file into a DataFrame
            df = pd.read_excel(file_path)

            # Verify columns in the DataFrame
            required_columns = ["material_name", "material_type", "description", "current_stock", "status", "created_date", "created_by"]
            if not all(column in df.columns for column in required_columns):
                raise ValueError("Excel file must contain the required columns: " + ", ".join(required_columns))

            # Ensure created_date is in string format
            if "created_date" in df.columns:
                df["created_date"] = pd.to_datetime(df["created_date"], errors='coerce').dt.strftime("%Y-%m-%d %H:%M:%S")

            # Insert data from DataFrame into the 'materials' table
            for _, row in df.iterrows():
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

            # Commit changes and close the connection
            connection.commit()
            print("Materials uploaded successfully.")
            return "Materials uploaded successfully."

        except Exception as e:
            print("Error uploading materials:", e)
            return f"Error uploading materials: {e}"

        finally:
            connection.close()
