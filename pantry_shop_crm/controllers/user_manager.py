import sqlite3
from datetime import datetime
from tkinter import messagebox
import re

class UserManager:
    def __init__(self, db_path="pantry_shop_crm.db"):
        self.db_path = db_path

    def connect(self):
        """Establishes a connection to the database."""
        return sqlite3.connect(self.db_path)

    def add_user(self, user_data):
        """Adds a new user to the database."""
        try:
            conn = self.connect()
            cursor = conn.cursor()

            query = """
            INSERT INTO users (first_name, last_name, email_address, password, mobile_number, 
                              fulltime, parttime, undergraduate, graduate, 
                              work_per_week, age_group, is_active, role_type, created_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            cursor.execute(query, (
                user_data['first_name'], user_data['last_name'], user_data['email_address'],
                user_data['password'], user_data['mobile_number'], user_data['fulltime'],
                user_data['parttime'], user_data['undergraduate'], user_data['graduate'],
                user_data['work_per_week'], user_data['age_group'],
                user_data['is_active'], user_data['role_type'],
                datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            ))

            conn.commit()
            messagebox.showinfo("User Added", "New user has been successfully added.")
            return {"success": True, "message": "User created successfully"}
        except sqlite3.IntegrityError:
            messagebox.showerror("Integrity Error", "Email already exists. Please use a unique email.")
            return {"success": False, "message": "Email already exists"}
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
            return {"success": False, "message": "An error occurred during User Creation"}
        finally:
            conn.close()

    

    def load_user(self, user_input):
        """Loads user details from the database based on user_id or email_address."""
        try:
            conn = self.connect()
            cursor = conn.cursor()
            user_input = str(user_input)

            # Check if user_input is a valid digit (user_id) or a valid email
            if user_input.isdigit():  # User ID is a valid digit
                user_id = int(user_input)
                query = """
                SELECT user_id, first_name, last_name, email_address, password, mobile_number, 
                    fulltime, parttime, undergraduate, graduate, 
                    work_per_week, age_group, is_active, role_type, created_date
                FROM users
                WHERE user_id = ?
                """
                cursor.execute(query, (user_id,))
            elif self.is_valid_email(user_input):  # Check if it's a valid email address
                email_address = user_input
                query = """
                SELECT user_id, first_name, last_name, email_address, password, mobile_number, 
                    fulltime, parttime, undergraduate, graduate, 
                    work_per_week, age_group, is_active, role_type, created_date
                FROM users
                WHERE email_address = ?
                """
                cursor.execute(query, (email_address,))
            else:
                messagebox.showerror("Invalid Input", "Please provide a valid user ID or email address.")
                return None

            user = cursor.fetchone()

            if user:
                user_data = {
                    "user_id": user[0],
                    "first_name": user[1],
                    "last_name": user[2],
                    "email_address": user[3],
                    "password": user[4],
                    "mobile_number": user[5],
                    "fulltime": user[6],
                    "parttime": user[7],
                    "undergraduate": user[8],
                    "graduate": user[9],
                    "work_per_week": user[10],
                    "age_group": user[11],
                    "is_active": user[12],
                    "role_type": user[13],
                    "created_date": user[14]
                }
                return user_data
            else:
                if user_input.isdigit():
                    messagebox.showinfo("User Not Found", f"No user found with ID {user_input}")
                else:
                    messagebox.showinfo("User Not Found", f"No user found with email address {user_input}")
                return None
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
            return None
        finally:
            conn.close()

    def is_valid_email(self, email):
        """Helper function to validate email format."""
        email_pattern = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        return re.match(email_pattern, email) is not None


    def update_user(self, user_input, updated_data):
        """Updates an existing user's information in the database based on user_id or email_address."""
        try:
            conn = self.connect()
            cursor = conn.cursor()

            # Ensure user_input is treated as a string
            user_input = str(user_input)  # Convert user_input to a string

            # Check if user_input is a valid digit (user_id) or a valid email
            if user_input.isdigit():  # User ID is a valid digit
                user_id = int(user_input)
                query = """
                UPDATE users SET first_name = ?, last_name = ?, email_address = ?, mobile_number = ?,
                                fulltime = ?, parttime = ?, undergraduate = ?, graduate = ?, 
                                work_per_week = ?, age_group = ?, is_active = ?, 
                                role_type = ?
                WHERE user_id = ?
                """
                cursor.execute(query, (
                    updated_data['first_name'], updated_data['last_name'], updated_data['email_address'],
                    updated_data['mobile_number'], updated_data['fulltime'], updated_data['parttime'],
                    updated_data['undergraduate'], updated_data['graduate'],
                    updated_data['work_per_week'], updated_data['age_group'], updated_data['is_active'],
                    updated_data['role_type'], user_id
                ))

            elif self.is_valid_email(user_input):  # Check if it's a valid email address
                email_address = user_input
                query = """
                UPDATE users SET first_name = ?, last_name = ?, email_address = ?, mobile_number = ?,
                                fulltime = ?, parttime = ?, undergraduate = ?, graduate = ?, 
                                work_per_week = ?, age_group = ?, is_active = ?, 
                                role_type = ?
                WHERE email_address = ?
                """
                cursor.execute(query, (
                    updated_data['first_name'], updated_data['last_name'], updated_data['email_address'],
                    updated_data['mobile_number'], updated_data['fulltime'], updated_data['parttime'],
                    updated_data['undergraduate'], updated_data['graduate'],
                    updated_data['work_per_week'], updated_data['age_group'], updated_data['is_active'],
                    updated_data['role_type'], email_address
                ))

            else:
                messagebox.showerror("Invalid Input", "Please provide a valid user ID or email address.")
                return {"success": False, "message": "Invalid user ID or email"}

            conn.commit()

            if cursor.rowcount == 0:
                messagebox.showinfo("Update Error", "No user found with the provided ID or email address.")
                return {"success": False, "message": "User not found"}
            else:
                messagebox.showinfo("User Updated", "User information has been successfully updated.")
                return {"success": True, "message": "User updated successfully"}

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
            return {"success": False, "message": "An error occurred during User Update"}
        finally:
            conn.close()

    def update_user_role(self, user_id, role_type):
        """Updates a user's role type in the database."""
        try:
            conn = self.connect()
            cursor = conn.cursor()

            query = """
            UPDATE users SET role_type = ?
            WHERE user_id = ?
            """
            cursor.execute(query, (role_type, user_id))

            conn.commit()

            if cursor.rowcount == 0:
                messagebox.showinfo("Update Error", "No user found with the provided ID.")
                return {"success": False, "message": "User not found"}
            else:
                messagebox.showinfo("Role Updated", "User role has been successfully updated.")
                return {"success": True, "message": "Role updated successfully"}
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
            return {"success": False, "message": "An error occurred during Role Update"}
        finally:
            conn.close()


    def get_all_users(self):
        try:
            # Connect to the database using the Database class
            conn = self.connect()  # assuming you have a method in your Database class to connect
            cursor = conn.cursor()

            # SQL query to fetch all users from the `user` table
            cursor.execute('''
                SELECT user_id, first_name, last_name, email_address, mobile_number, fulltime, parttime, 
                    undergraduate, graduate, work_per_week, age_group, is_active, 
                    role_type, created_date
                FROM users
            ''')

            # Fetch all rows from the result
            users = cursor.fetchall()

            # Return the fetched users
            return {"success": True, "data": users}

        except sqlite3.Error as e:
            # print(f"Database error: {e}")
            return {"success": False, "message": "An error occurred while fetching users."}

        finally:

            # Ensure the connection is closed after the operation
            conn.close()

