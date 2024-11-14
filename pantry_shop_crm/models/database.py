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
                        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        first_name TEXT,
                        last_name TEXT,
                        email_address TEXT,
                        password TEXT,    
                        mobile_number TEXT,
                        fulltime BOOLEAN,
                        parttime BOOLEAN,
                        undergraduate BOOLEAN,
                        graduate BOOLEAN,
                        already_graduate BOOLEAN,
                        work_per_week INTEGER,
                        age_group INTEGER,
                        is_active BOOLEAN,
                        role_type TEXT,
                        created_date TEXT
                    );''')

        # Create Orders Table
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS orders (
                                order_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                user_id INTEGER,
                                order_date TEXT,
                                pickup_date TEXT,
                                order_status TEXT,
                                order_text TEXT,
                                created_date TEXT,
                                FOREIGN KEY (user_id) REFERENCES users(user_id)
                            );''')

        # Create OrderItem Table
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS order_item (
                                order_id INTEGER,
                                material_id INTEGER,
                                quantity TEXT,
                                unit_price TEXT,
                                PRIMARY KEY (order_id, material_id),
                                FOREIGN KEY (order_id) REFERENCES orders(order_id),
                                FOREIGN KEY (material_id) REFERENCES materials(material_id)
                            );''')

        # Create Vendors Table
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS vendors (
                                vendor_id INTEGER PRIMARY KEY,
                                vendor_name TEXT,
                                contact_fname TEXT,
                                contact_lname TEXT,
                                contact_email TEXT,
                                contact_phone TEXT,
                                address_key INTEGER,
                                is_active BOOLEAN,
                                created_date TEXT,
                                created_by INTEGER,
                                FOREIGN KEY (address_key) REFERENCES address(Addrnr)
                            );''')

        # Create Materials Table
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS materials (
                                material_id INTEGER PRIMARY KEY,
                                material_name TEXT,
                                material_type INTEGER,
                                description TEXT,
                                current_stock REAL,
                                status TEXT,
                                created_date TEXT,
                                created_by INTEGER,
                                FOREIGN KEY (material_type) REFERENCES material_type(id)
                            );''')

        # Create Address Table
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS address (
                                Addrnr INTEGER PRIMARY KEY,
                                St1 TEXT,
                                St2 TEXT,
                                Apt TEXT,
                                Postal_Code TEXT,
                                created_date TEXT,
                                created_by INTEGER
                            );''')

        # Create MaterialType Table
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS material_type (
                                id INTEGER PRIMARY KEY,
                                m_type TEXT,
                                material_desc TEXT,
                                created_date TEXT,
                                created_by INTEGER
                            );''')

        # Create VendorMaterial Table
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS vendor_material (
                                material_id INTEGER,
                                vendor_id INTEGER,
                                namebyvendor TEXT,
                                PRIMARY KEY (material_id, vendor_id),
                                FOREIGN KEY (material_id) REFERENCES materials(material_id),
                                FOREIGN KEY (vendor_id) REFERENCES vendors(vendor_id)
                            );''')

        # Commit changes and close
        self.connection.commit()
        print("Tables created successfully!")

    def close(self):
        if self.connection:
            self.connection.close()
            print("Database connection closed.")
