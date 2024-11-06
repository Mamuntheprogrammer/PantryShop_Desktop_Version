# Pantry Shop CRM Project Structure

## pantry_shop_crm/
Main project directory containing all necessary files for the application.

### ├── main.py
Main entry point to start the application.

### ├── controllers/
Contains all business logic and handles communication between models and views.

- **pantry_shop_crm.py**: Main application logic, GUI controller (handles app initialization).
- **login_system.py**: Handles user authentication logic (Sign In, Sign Up, Password Reset).
- **user_manager.py**: Manages user data and updates (CRUD operations for user info).
- **order_manager.py**: Manages order creation, order history, and approval (Order flow logic).
- **vendor_manager.py**: Vendor management logic (Excel upload, update, reports).
- **material_manager.py**: Material management logic (Excel upload, update, reports).
- **stock_manager.py**: Stock quantity management and reporting logic (Stock update, stock report).
- **dashboard.py**: Dashboard logic for displaying statistics (total orders, vendors, etc.).

### ├── models/
Data models to represent the structure of the data and handle database operations.

- **user.py**: User model (stores user-related data and validates user details).
- **order.py**: Order model (stores order details, manages order validation).
- **vendor.py**: Vendor model (stores vendor details, handles vendor data).
- **material.py**: Material model (stores material details, handles material data).
- **stock.py**: Stock model (stores stock details, stock updates).
- **database.py**: Database interaction (connects to the DB, handles data persistence).

### ├── views/
GUI views (screens, layouts) implemented with tkinter.

- **login_view.py**: Login screen (Sign In, Sign Up, Password Reset).
- **user_view.py**: User information view (View, Update User Info).
- **order_view.py**: Order creation and order history view (User-specific order report).
- **vendor_view.py**: Vendor management view (Upload, Update, Report).
- **material_view.py**: Material management view (Upload, Update, Report).
- **stock_view.py**: Stock management view (Stock updates, Reports).
- **dashboard_view.py**: Dashboard screen (Shows statistics, popular items, top vendors).

### ├── utils/
Utility functions and helpers to manage specific tasks across the application.

- **excel_utils.py**: Handles Excel file reading/writing for vendor/material uploads.
- **alv_table.py**: Generates ALV (Advanced List View) reports for various data.
- **data_validation.py**: Validates data inputs (e.g., Excel data, user input).

### ├── assets/
Contains any assets like images, icons, etc.

- **icons/**: Icons for GUI buttons, status indicators, etc.
  - **logo.png**: Example CRM logo for the top of the application.

### └── requirements.txt
List of dependencies for the project (GUI framework, etc.).
