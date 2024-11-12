import sqlite3
import datetime

class SignupManager:
    def __init__(self, db_path="pantry_shop_crm.db"):
        self.db_path = db_path

    def connect(self):
        return sqlite3.connect(self.db_path)

    def save_user(self, user_data):
        """
        Saves user data into the 'users' table.
        `user_data` should be a dictionary containing the user's information.
        """
        try:
            conn = self.connect()
            cursor = conn.cursor()
            
            # Insert user data into the database
            cursor.execute('''
                INSERT INTO users (
                    first_name, last_name, email_address,password, mobile_number, 
                    fulltime, parttime, undergraduate, graduate, 
                    already_graduate, work_per_week, age_group, 
                    is_active, role_type, created_date
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                user_data["first_name"], user_data["last_name"], 
                user_data["email_address"], user_data["password"], user_data["mobile_number"], 
                user_data["fulltime"], user_data["parttime"], 
                user_data["undergraduate"], user_data["graduate"], 
                user_data["already_graduate"], user_data["work_per_week"], 
                user_data["age_group"], user_data["is_active"], 
                user_data["role_type"], datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ))

            conn.commit()
            print("User saved successfully!")
            return {"success": True, "message": "Signup successful!"}

        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return {"success": False, "message": "An error occurred during signup."}

        finally:
            if conn:
                conn.close()

    def validate_user_data(self, user_data):
        """
        Validates user data before saving.
        Returns True if valid, otherwise returns False with an error message.
        """
        # Example validation checks
        if not user_data.get("email_address"):
            return {"success": False, "message": "Email is required."}
        if not user_data.get("password"):
            return {"success": False, "message": "Password is required."}
        # Add more validation as needed
        return {"success": True}

    def handle_signup(self, user_data):
        """
        Handles the signup process: validates data and saves it to the database.
        """
        validation_result = self.validate_user_data(user_data)
        if not validation_result["success"]:
            return validation_result

        return self.save_user(user_data)
