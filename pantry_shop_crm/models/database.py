 
import sqlite3
import os

class Database:
    def __init__(self, db_name="pantry_shop_crm.db"):
        self.db_name = db_name
        self.connection = None
        self.cursor = None
        self._create_connection()

    def _create_connection(self):
        # If the database does not exist, it will be created
        if not os.path.exists(self.db_name):
            self.connection = sqlite3.connect(self.db_name)
            self.cursor = self.connection.cursor()
            print(f"Database {self.db_name} created successfully.")
            self._initialize_tables()
        else:
            self.connection = sqlite3.connect(self.db_name)
            self.cursor = self.connection.cursor()
            print(f"Connected to the existing database: {self.db_name}")

    def _initialize_tables(self):
        # Create Users Table
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        first_name TEXT,
                        last_name TEXT,
                        email TEXT,
                        password TEXT NOT NULL,
                        user_type TEXT DEFAULT NULL,
                        departname TEXT DEFAULT NULL,
                        phone TEXT DEFAULT NULL,
                        age INTEGER DEFAULT NULL,
                        max_hour INTEGER DEFAULT NULL,
                        reference TEXT DEFAULT NULL,
                        student_status TEXT DEFAULT NULL,
                        auth_otp TEXT DEFAULT NULL
                    );''')

        # Create Orders Table
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS orders (
                                id INTEGER PRIMARY KEY,
                                user_id INTEGER,
                                order_date TEXT,
                                status TEXT,
                                FOREIGN KEY (user_id) REFERENCES users(id)
                            );''')

        # Create Vendors Table
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS vendors (
                                id INTEGER PRIMARY KEY,
                                name TEXT NOT NULL,
                                contact_info TEXT
                            );''')

        # Create Materials Table
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS materials (
                                id INTEGER PRIMARY KEY,
                                name TEXT NOT NULL,
                                description TEXT,
                                price REAL
                            );''')

        # Create Stock Table
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS stock (
                                id INTEGER PRIMARY KEY,
                                material_id INTEGER,
                                quantity INTEGER,
                                FOREIGN KEY (material_id) REFERENCES materials(id)
                            );''')

        # Commit changes and close
        self.connection.commit()
        print("Tables created successfully!")

    def close(self):
        if self.connection:
            self.connection.close()
            print("Database connection closed.")
