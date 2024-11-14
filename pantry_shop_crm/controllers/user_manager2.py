import sqlite3
from datetime import datetime
from tkinter import messagebox

class UserManager2:
    def __init__(self, db_path="pantry_shop_crm.db"):
        self.db_path = db_path

    def connect(self):
        """Establishes a connection to the database."""
        return sqlite3.connect(self.db_path)


    def load_user(self, user_id):
        """Loads user details from the database based on user_id."""
        try:
            conn = self.connect()
            cursor = conn.cursor()

            query = """
            SELECT user_id, first_name, last_name, email_address, password,mobile_number, 
                   fulltime, parttime, undergraduate, graduate, already_graduate, 
                   work_per_week, age_group, is_active, role_type, created_date
            FROM users
            WHERE user_id = ?
            """
            cursor.execute(query, (user_id,))
            user = cursor.fetchone()

            if user:
                user_data = {
                    "user_id": user[0],
                    "first_name": user[1],
                    "last_name": user[2],
                    "email_address": user[3],
                    "password":user[4],
                    "mobile_number": user[5],
                    "fulltime": user[6],
                    "parttime": user[7],
                    "undergraduate": user[8],
                    "graduate": user[9],
                    "already_graduate": user[10],
                    "work_per_week": user[11],
                    "age_group": user[12],
                    "is_active": user[13],
                    "role_type": user[14],
                    "created_date": user[15]
                }
                return user_data
            else:
                messagebox.showinfo("User Not Found", f"No user found with ID {user_id}")
                return None
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
            return None
        finally:
            conn.close()

    def update_user(self, user_id, updated_data):
        """Updates an existing user's information in the database."""
        try:
            conn = self.connect()
            cursor = conn.cursor()

            query = """
            UPDATE users SET first_name = ?, last_name = ?, email_address = ?, mobile_number = ?
            WHERE user_id = ?
            """
            cursor.execute(query, (
                updated_data['first_name'], updated_data['last_name'], updated_data['email_address'],
                updated_data['mobile_number'], user_id
            ))

            conn.commit()

            if cursor.rowcount == 0:
                messagebox.showinfo("Update Error", "No user found with the provided ID.")
                return {"success": False, "message": "User not found"}
            else:
                messagebox.showinfo("User Updated", "User information has been successfully updated.")
                return {"success": True, "message": "User updated successfully"}
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
            return {"success": False, "message": "An error occurred during User Update"}
        finally:
            conn.close()

    