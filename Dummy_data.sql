-- Insert into User
INSERT INTO Users (user_id, first_name, last_name, email_address,password, mobile_number, fulltime, parttime, undergraduate, graduate, already_graduate, work_per_week, age_group, is_active, role_type, created_date) 
VALUES 
(1, 'John', 'Doe', 'one', 'one', '123',1, 0, 1, 0, 0, 40, 2, 1, 'Admin', datetime('now')),
(2, 'Jane', 'Smith', 'two', 'two','123', 0, 1, 0, 1, 1, 20, 1, 1, 'User', datetime('now'));

-- Insert into Address
INSERT INTO Address (Addrnr, St1, St2, Apt, Postal_Code, created_date, created_by) 
VALUES 
(1, '123 Elm St', 'Suite A', '1A', '54321', datetime('now'), 1),
(2, '456 Oak St', '', '2B', '12345', datetime('now'), 2);

-- Insert into Vendor
INSERT INTO Vendors (vendor_id, vendor_name, contact_fname, contact_lname, contact_email, contact_phone, address_key, is_active, created_date, created_by)
VALUES 
(1, 'Acme Supplies', 'Alice', 'Johnson', 'alice.johnson@acme.com', '5551234567', 1, 1, datetime('now'), 1),
(2, 'Best Goods', 'Bob', 'Williams', 'bob.williams@bestgoods.com', '5559876543', 2, 1, datetime('now'), 1);

-- Insert into MaterialType
INSERT INTO Material_Type (id, m_type, material_desc, created_date, created_by) 
VALUES 
(1, 'Food', 'Perishable food items', datetime('now'), 1),
(2, 'Non-Food', 'Non-perishable items', datetime('now'), 1);

-- Insert into Material
INSERT INTO Materials (material_id, material_name, material_type, description, current_stock, status, created_date, created_by)
VALUES 
(1, 'Rice', 1, 'Basmati rice', 100, 'Active', datetime('now'), 1),
(2, 'Flour', 1, 'All-purpose flour', 200, 'Active', datetime('now'), 1),
(3, 'Soap', 2, 'Hand soap', 50, 'Active', datetime('now'), 1);

-- Insert into Vendormaterial
INSERT INTO Vendor_material (material_id, vendor_id, namebyvendor)
VALUES 
(1, 1, 'Acme Supplies'),
(2, 1, 'Acme Supplies'),
(3, 2, 'Best Goods');

-- Insert into Order
INSERT INTO Orders (order_id, user_id, order_date, pickup_date, order_status, order_text, created_date) 
VALUES 
(1, 2, '2024-11-01', '2024-11-02', 'Pending', 'Order for pantry items', datetime('now')),
(2, 2, '2024-11-10', '2024-11-11', 'Delivered', 'Weekly groceries', datetime('now'));

-- Insert into OrderItem
INSERT INTO Order_Item (order_id, material_id, quantity, unit_price) 
VALUES 
(1, 1, '2', '50.00'),
(1, 2, '1', '20.00'),
(2, 3, '3', '10.00');
