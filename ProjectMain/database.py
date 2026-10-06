"""
BASTA BURGER - POS and Inventory Management System
Database Connection and Initialization Module (XAMPP MySQL)
All variables and functions strictly use snake_case.
"""

import sys
import mysql.connector
from mysql.connector import Error

# Default XAMPP MySQL Configuration
DEFAULT_DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "port": 3306,
    "database": "basta_pos"
}


def get_db_connection(use_database=True):
    """
    Establishes and returns a connection to the MySQL server (XAMPP).
    If use_database is False, connects to the server without selecting a database.
    """
    config = DEFAULT_DB_CONFIG.copy()
    if not use_database:
        config.pop("database", None)

    try:
        connection = mysql.connector.connect(**config)
        return connection
    except Error as err:
        print(f"[BASTA DB] Connection error: {err}")
        return None


def initialize_database():
    """
    Connects to XAMPP MySQL, creates the 'basta_pos' database if missing,
    creates required tables, and seeds initial sample records.
    """
    print("\n" + "=" * 60)
    print(" BASTA POS - Initializing MySQL Database (XAMPP)")
    print("=" * 60)

    # 1. Connect to MySQL server (without database)
    conn = get_db_connection(use_database=False)
    if not conn:
        print("\n[FAILED] Could not connect to MySQL server.")
        print("Please ensure XAMPP Control Panel is open and MySQL is started (Green status).")
        return False

    cursor = conn.cursor()

    try:
        # Create database
        db_name = DEFAULT_DB_CONFIG["database"]
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
        print(f"[OK] Database '{db_name}' ready.")
        cursor.close()
        conn.close()

        # 2. Connect to the 'basta_pos' database
        conn = get_db_connection(use_database=True)
        if not conn:
            return False
        cursor = conn.cursor()

        # Users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS `users` (
                `id` INT AUTO_INCREMENT PRIMARY KEY,
                `username` VARCHAR(50) NOT NULL UNIQUE,
                `password_hash` VARCHAR(255) NOT NULL,
                `full_name` VARCHAR(100) NOT NULL,
                `email` VARCHAR(120),
                `role` ENUM('Administrator', 'Shift Supervisor', 'Cashier', 'Inventory Manager') NOT NULL DEFAULT 'Cashier',
                `status` ENUM('Active', 'Disabled') NOT NULL DEFAULT 'Active',
                `last_login` DATETIME NULL,
                `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """)
        print("[OK] Table 'users' verified.")

        # Categories table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS `categories` (
                `id` INT AUTO_INCREMENT PRIMARY KEY,
                `name` VARCHAR(50) NOT NULL UNIQUE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """)
        print("[OK] Table 'categories' verified.")

        # Products table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS `products` (
                `id` INT AUTO_INCREMENT PRIMARY KEY,
                `sku` VARCHAR(50) NOT NULL UNIQUE,
                `name` VARCHAR(100) NOT NULL,
                `category` VARCHAR(50) NOT NULL,
                `price` DECIMAL(10, 2) NOT NULL,
                `cost_price` DECIMAL(10, 2) DEFAULT 0.00,
                `stock_quantity` INT NOT NULL DEFAULT 0,
                `low_stock_threshold` INT NOT NULL DEFAULT 10,
                `in_store` BOOLEAN NOT NULL DEFAULT TRUE,
                `online_ordering` BOOLEAN NOT NULL DEFAULT TRUE,
                `grabfood` BOOLEAN NOT NULL DEFAULT FALSE,
                `status` ENUM('Active', 'Draft', 'Archived') NOT NULL DEFAULT 'Active',
                `image_filename` VARCHAR(255) DEFAULT 'basta_LOGO.png',
                `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """)
        print("[OK] Table 'products' verified.")

        # Inventory Items table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS `inventory_items` (
                `id` INT AUTO_INCREMENT PRIMARY KEY,
                `sku` VARCHAR(50) NOT NULL UNIQUE,
                `item_name` VARCHAR(120) NOT NULL,
                `category` VARCHAR(50) NOT NULL,
                `on_hand` DECIMAL(10, 2) NOT NULL DEFAULT 0.0,
                `par_level` DECIMAL(10, 2) NOT NULL DEFAULT 0.0,
                `unit` VARCHAR(20) NOT NULL DEFAULT 'units',
                `unit_cost` DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
                `status` ENUM('Healthy', 'Low stock', 'Critical') NOT NULL DEFAULT 'Healthy',
                `last_updated` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """)
        print("[OK] Table 'inventory_items' verified.")

        # Sales Transactions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS `sales_transactions` (
                `id` INT AUTO_INCREMENT PRIMARY KEY,
                `transaction_id` VARCHAR(50) NOT NULL UNIQUE,
                `order_id` VARCHAR(50) NOT NULL,
                `table_num` VARCHAR(50) DEFAULT 'Takeout',
                `cashier_name` VARCHAR(100) DEFAULT 'Cashier',
                `payment_method` ENUM('Cash', 'GCash', 'Card', 'Maya') NOT NULL DEFAULT 'Cash',
                `subtotal` DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
                `vat` DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
                `service_charge` DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
                `total` DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
                `cash_received` DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
                `change_due` DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
                `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """)
        print("[OK] Table 'sales_transactions' verified.")

        # Transaction Line Items table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS `transaction_items` (
                `id` INT AUTO_INCREMENT PRIMARY KEY,
                `transaction_id` VARCHAR(50) NOT NULL,
                `product_name` VARCHAR(100) NOT NULL,
                `quantity` INT NOT NULL DEFAULT 1,
                `unit_price` DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
                `line_total` DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
                FOREIGN KEY (`transaction_id`) REFERENCES `sales_transactions`(`transaction_id`) ON DELETE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """)
        print("[OK] Table 'transaction_items' verified.")

        # Seed initial data
        _seed_sample_data(cursor)
        conn.commit()

        print("\n[SUCCESS] All tables and sample data initialized successfully!")
        print("Database 'basta_pos' is ready for use with XAMPP MySQL.")
        print("=" * 60 + "\n")
        return True

    except Error as err:
        print(f"\n[ERROR] SQL Execution Error: {err}")
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def _seed_sample_data(cursor):
    """Inserts initial users, products, and inventory items if tables are empty."""
    # Check users
    cursor.execute("SELECT COUNT(*) FROM `users`;")
    user_count = cursor.fetchone()[0]
    if user_count == 0:
        cursor.execute("""
            INSERT INTO `users` (`username`, `password_hash`, `full_name`, `email`, `role`, `status`) VALUES
            ('admin', 'admin123', 'Chef Marco S.', 'admin@bastaburger.com', 'Administrator', 'Active'),
            ('cashier1', 'cashier123', 'Bea M.', 'bea@bastaburger.com', 'Cashier', 'Active'),
            ('supervisor', 'super123', 'Danilo R.', 'danilo@bastaburger.com', 'Shift Supervisor', 'Active'),
            ('inventory1', 'inv123', 'Aris P.', 'aris@bastaburger.com', 'Inventory Manager', 'Active');
        """)
        print("  -> Seeded 4 default user accounts.")

    # Check products
    cursor.execute("SELECT COUNT(*) FROM `products`;")
    prod_count = cursor.fetchone()[0]
    if prod_count == 0:
        cursor.execute("""
            INSERT INTO `products` (`sku`, `name`, `category`, `price`, `cost_price`, `stock_quantity`, `low_stock_threshold`, `in_store`, `online_ordering`, `grabfood`, `status`) VALUES
            ('BGR-001', 'Classic Basta Smash Burger', 'Burgers', 189.00, 85.00, 32, 12, TRUE, TRUE, TRUE, 'Active'),
            ('BGR-002', 'Truffle Mushroom Cheeseburger', 'Burgers', 249.00, 110.00, 18, 8, TRUE, TRUE, FALSE, 'Active'),
            ('BGR-003', 'Spicy BBQ Bacon Deluxe', 'Burgers', 229.00, 95.00, 24, 10, TRUE, TRUE, TRUE, 'Active'),
            ('DRK-001', 'Ube Shake Special', 'Beverages', 120.00, 45.00, 45, 15, TRUE, TRUE, FALSE, 'Active'),
            ('DRK-002', 'Calamansi Cold Brew Fizz', 'Beverages', 95.00, 30.00, 50, 15, TRUE, TRUE, TRUE, 'Active'),
            ('SDE-001', 'Crispy Golden Fries', 'Sides', 79.00, 25.00, 60, 20, TRUE, TRUE, TRUE, 'Active'),
            ('SDE-002', 'Garlic Parmesan Wedges', 'Sides', 99.00, 35.00, 22, 10, TRUE, TRUE, FALSE, 'Active'),
            ('DES-001', 'Warm Brioche Ice Cream Bun', 'Desserts', 119.00, 40.00, 8, 10, TRUE, FALSE, FALSE, 'Active');
        """)
        print("  -> Seeded 8 default menu products.")

    # Check inventory
    cursor.execute("SELECT COUNT(*) FROM `inventory_items`;")
    inv_count = cursor.fetchone()[0]
    if inv_count == 0:
        cursor.execute("""
            INSERT INTO `inventory_items` (`sku`, `item_name`, `category`, `on_hand`, `par_level`, `unit`, `unit_cost`, `status`) VALUES
            ('ING-0018', 'USDA ground beef 80/20', 'Proteins', 18.5, 14.0, 'kg', 410.00, 'Healthy'),
            ('ING-0031', 'Brioche burger buns', 'Bakery', 4.0, 12.0, 'packs', 185.00, 'Critical'),
            ('ING-0064', 'Frozen ube ice cream', 'Desserts', 2.4, 6.0, 'L', 320.00, 'Low stock'),
            ('ING-0085', 'Russet potatoes', 'Produce', 31.0, 20.0, 'kg', 86.00, 'Healthy'),
            ('ING-0102', 'Calamansi glaze', 'Sauces', 3.0, 8.0, 'bottles', 145.00, 'Low stock');
        """)
        print("  -> Seeded 5 inventory ingredient items.")


# Helper functions to query data
def fetch_all_products():
    """Fetches list of active products from database or returns empty list."""
    conn = get_db_connection()
    if not conn:
        return []
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM `products` ORDER BY `category`, `name`;")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows
    except Exception:
        return []


def fetch_all_inventory():
    """Fetches list of inventory ingredients from database."""
    conn = get_db_connection()
    if not conn:
        return []
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM `inventory_items` ORDER BY `sku`;")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows
    except Exception:
        return []


def fetch_all_users():
    """Fetches list of user accounts from database."""
    conn = get_db_connection()
    if not conn:
        return []
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, username, full_name, email, role, status, last_login FROM `users` ORDER BY `id`;")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows
    except Exception:
        return []


def verify_user_login(username, password):
    """
    Validates user credentials against the MySQL database.
    Returns (True, user_dict) or (False, None).
    """
    conn = get_db_connection()
    if not conn:
        return False, None
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM `users` WHERE `username` = %s AND `password_hash` = %s AND `status` = 'Active' LIMIT 1;",
            (username, password)
        )
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        if user:
            return True, user
        return False, None
    except Exception:
        return False, None


if __name__ == "__main__":
    success = initialize_database()
    if not success:
        sys.exit(1)
