"""
BASTA BURGER - POS and Inventory Management System
Database Connection and Initialization Module (XAMPP MySQL)
All variables and functions strictly use snake_case.
"""

import os
import sys
import mysql.connector
from mysql.connector import Error

# Default XAMPP MySQL Configuration (can be overridden via environment variables or edited directly)
DEFAULT_DB_CONFIG = {
    "host": os.environ.get("BASTA_DB_HOST", "localhost"),
    "user": os.environ.get("BASTA_DB_USER", "root"),
    "password": os.environ.get("BASTA_DB_PASSWORD", ""),
    "port": int(os.environ.get("BASTA_DB_PORT", 3306)),
    "database": os.environ.get("BASTA_DB_NAME", "basta_pos")
}

_is_auto_initializing = False


def get_db_connection(use_database=True):
    """
    Establishes and returns a connection to the MySQL server (XAMPP).
    If use_database is False, connects to the server without selecting a database.
    If database 'basta_pos' doesn't exist yet (errno 1049), automatically initializes it.
    """
    global _is_auto_initializing
    config = DEFAULT_DB_CONFIG.copy()
    if not use_database:
        config.pop("database", None)

    try:
        connection = mysql.connector.connect(**config)
        return connection
    except Error as err:
        # Detect MySQL error 1049: Unknown database 'basta_pos'
        if use_database and not _is_auto_initializing and getattr(err, "errno", None) == 1049:
            print("\n[BASTA DB] Database 'basta_pos' does not exist yet.")
            print("[BASTA DB] Automatically initializing database and tables now...")
            _is_auto_initializing = True
            try:
                if initialize_database():
                    return mysql.connector.connect(**config)
            except Exception as auto_init_err:
                print(f"[BASTA DB] Auto-initialization encountered an error: {auto_init_err}")
            finally:
                _is_auto_initializing = False
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
                `role` ENUM('Administrator', 'Cashier') NOT NULL DEFAULT 'Cashier',
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


# Default menu products that have verified image files in Designs/
DEFAULT_SEED_PRODUCTS = [
    ("BUR-001", "Basta Smash Burger", "Burgers", 285.00, 110.00, 45, 10, True, True, True, "Active", "BASTA_SMASHBURGER.jpg"),
    ("BUR-002", "Crispy Chicken Sandwich", "Burgers", 220.00, 95.00, 35, 8, True, True, True, "Active", "BASTA_CRISPY CHICKEN SANDWICH.jpg"),
    ("SDE-001", "Truffle Parm Fries", "Sides", 145.00, 55.00, 60, 15, True, True, True, "Active", "BASTA_TRUFFLE FRIES.jpg"),
    ("MLS-001", "Calamansi Glazed Wings", "Meals", 249.00, 110.00, 30, 10, True, True, True, "Active", "BASTA_CALAMANSIWINGS.jpg"),
    ("PAS-001", "Slow-Braised Bolognese", "Pasta", 265.00, 115.00, 25, 8, True, True, False, "Active", "BASTA_BOLOGNESE.jpg"),
    ("SDE-002", "Charred Caesar Salad", "Sides", 185.00, 75.00, 25, 8, True, True, False, "Active", "BASTA_CHARRED CAESAR.jpg"),
    ("BEV-001", "Ube Milkshake", "Beverages", 165.00, 60.00, 50, 15, True, True, False, "Active", "BASTA_UBE MILKSHAKE.jpg"),
    ("DES-001", "Warm Sea Salt Choc Cookie", "Desserts", 95.00, 35.00, 40, 10, True, False, False, "Active", "BASTA_SEASALT COOKIE.jpg")
]


def _seed_sample_data(cursor):
    """Inserts initial users, products, and inventory items if tables are empty."""
    # Check users
    cursor.execute("SELECT COUNT(*) FROM `users`;")
    user_count = cursor.fetchone()[0]
    if user_count == 0:
        cursor.execute("""
            INSERT INTO `users` (`username`, `password_hash`, `full_name`, `email`, `role`, `status`) VALUES
            ('admin', 'admin123', 'Chef Marco S.', 'admin@bastaburger.com', 'Administrator', 'Active'),
            ('cashier1', 'cashier123', 'Bea M.', 'bea@bastaburger.com', 'Cashier', 'Active');
        """)
        print("  -> Seeded 2 default user accounts (Administrator, Cashier).")

    # 2. Check and seed categories
    cursor.execute("SELECT COUNT(*) FROM `categories`;")
    cat_count = cursor.fetchone()[0]
    if cat_count == 0:
        cursor.execute("""
            INSERT INTO `categories` (`name`) VALUES
            ('Burgers'), ('Sides'), ('Meals'), ('Pasta'), ('Beverages'), ('Desserts');
        """)
        print("  -> Seeded 6 default menu categories.")

    # 3. Check and seed products (Only products with verified images)
    cursor.execute("SELECT COUNT(*) FROM `products`;")
    prod_count = cursor.fetchone()[0]
    if prod_count == 0:
        insert_prod_sql = """
            INSERT INTO `products` 
            (`sku`, `name`, `category`, `price`, `cost_price`, `stock_quantity`, `low_stock_threshold`, `in_store`, `online_ordering`, `grabfood`, `status`, `image_filename`)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        for prod in DEFAULT_SEED_PRODUCTS:
            cursor.execute(insert_prod_sql, prod)
        print(f"  -> Seeded {len(DEFAULT_SEED_PRODUCTS)} default menu products with verified images.")

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


def reset_products_database():
    """
    Resets the products and categories tables in MySQL,
    and seeds only the 8 products that have verified image files in Designs/.
    """
    print("\n" + "=" * 60)
    print(" BASTA POS - Resetting Products Database (Pictured Products Only)")
    print("=" * 60)
    conn = get_db_connection(use_database=True)
    if not conn:
        print("[BASTA DB] Cannot reset products: No database connection.")
        return False
    try:
        cursor = conn.cursor()

        # 1. Reset categories
        cursor.execute("DELETE FROM `categories`;")
        categories = ["Burgers", "Sides", "Meals", "Pasta", "Beverages", "Desserts"]
        for cat in categories:
            cursor.execute("INSERT INTO `categories` (`name`) VALUES (%s);", (cat,))
        print("  -> Reset and updated 6 menu categories.")

        # 2. Reset products
        cursor.execute("DELETE FROM `products`;")
        cursor.execute("ALTER TABLE `products` AUTO_INCREMENT = 1;")

        insert_prod_sql = """
            INSERT INTO `products` 
            (`sku`, `name`, `category`, `price`, `cost_price`, `stock_quantity`, `low_stock_threshold`, `in_store`, `online_ordering`, `grabfood`, `status`, `image_filename`)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        for prod in DEFAULT_SEED_PRODUCTS:
            cursor.execute(insert_prod_sql, prod)

        conn.commit()
        cursor.close()
        conn.close()
        print(f"[SUCCESS] Reset products table with {len(DEFAULT_SEED_PRODUCTS)} pictured products!")
        print("=" * 60)
        return True
    except Exception as err:
        print(f"[BASTA DB] Error resetting products database: {err}")
        return False


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
    Validates user credentials directly against the MySQL database.
    Returns (True, user_dict) on success, or (False, error_reason).
    error_reason can be: 'DB_CONNECTION_ERROR', 'USER_NOT_FOUND', 'INVALID_PASSWORD', 'ACCOUNT_INACTIVE'
    """
    conn = get_db_connection()
    if not conn:
        return False, "DB_CONNECTION_ERROR"
    try:
        cursor = conn.cursor(dictionary=True)
        # Search by username or email
        cursor.execute(
            "SELECT * FROM `users` WHERE `username` = %s OR `email` = %s LIMIT 1;",
            (username, username)
        )
        user = cursor.fetchone()
        if not user:
            cursor.close()
            conn.close()
            return False, "USER_NOT_FOUND"

        if user.get("status") != "Active":
            cursor.close()
            conn.close()
            return False, "ACCOUNT_INACTIVE"

        if str(user.get("password_hash")) != str(password):
            cursor.close()
            conn.close()
            return False, "INVALID_PASSWORD"

        # Update last_login timestamp upon successful authentication
        try:
            update_cursor = conn.cursor()
            update_cursor.execute(
                "UPDATE `users` SET `last_login` = NOW() WHERE `id` = %s;",
                (user["id"],)
            )
            conn.commit()
            update_cursor.close()
        except Exception:
            pass

        cursor.close()
        conn.close()
        return True, user
    except Exception as err:
        print(f"[BASTA DB] Auth query error: {err}")
        return False, "QUERY_ERROR"


# --- PRODUCT DATA MANIPULATION (CRUD) ---

def add_product(name, sku, category, price, cost_price=0.0, stock_quantity=0, low_stock_threshold=10, in_store=True, online_ordering=True, grabfood=False, image_filename="basta_LOGO.png"):
    """Inserts a new product into MySQL database."""
    conn = get_db_connection()
    if not conn:
        return None
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO `products` (`name`, `sku`, `category`, `price`, `cost_price`, `stock_quantity`, `low_stock_threshold`, `in_store`, `online_ordering`, `grabfood`, `status`, `image_filename`)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'Active', %s);
        """, (name, sku, category, price, cost_price, stock_quantity, low_stock_threshold, in_store, online_ordering, grabfood, image_filename or "basta_LOGO.png"))
        conn.commit()
        new_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return new_id
    except Exception as err:
        print(f"[BASTA DB] Add product error: {err}")
        return None


def update_product(product_id, name, sku, category, price, cost_price, stock_quantity, low_stock_threshold, in_store, online_ordering, grabfood, image_filename=None):
    """Updates an existing product in MySQL database."""
    conn = get_db_connection()
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        if image_filename is not None:
            cursor.execute("""
                UPDATE `products`
                SET `name` = %s, `sku` = %s, `category` = %s, `price` = %s, `cost_price` = %s,
                    `stock_quantity` = %s, `low_stock_threshold` = %s, `in_store` = %s,
                    `online_ordering` = %s, `grabfood` = %s, `image_filename` = %s
                WHERE `id` = %s;
            """, (name, sku, category, price, cost_price, stock_quantity, low_stock_threshold, in_store, online_ordering, grabfood, image_filename, product_id))
        else:
            cursor.execute("""
                UPDATE `products`
                SET `name` = %s, `sku` = %s, `category` = %s, `price` = %s, `cost_price` = %s,
                    `stock_quantity` = %s, `low_stock_threshold` = %s, `in_store` = %s,
                    `online_ordering` = %s, `grabfood` = %s
                WHERE `id` = %s;
            """, (name, sku, category, price, cost_price, stock_quantity, low_stock_threshold, in_store, online_ordering, grabfood, product_id))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as err:
        print(f"[BASTA DB] Update product error: {err}")
        return False


def delete_product(product_id):
    """Deletes a product from MySQL database by ID."""
    conn = get_db_connection()
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM `products` WHERE `id` = %s;", (product_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as err:
        print(f"[BASTA DB] Delete product error: {err}")
        return False


def deduct_product_stock(product_name, quantity):
    """Decrements stock quantity of a product in MySQL."""
    conn = get_db_connection()
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE `products`
            SET `stock_quantity` = GREATEST(0, `stock_quantity` - %s)
            WHERE `name` = %s;
        """, (quantity, product_name))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as err:
        print(f"[BASTA DB] Deduct stock error: {err}")
        return False


# --- USER DATA MANIPULATION (CRUD) ---

def add_user(username, password_hash, full_name, email, role="Cashier", status="Active"):
    """Inserts a new user account into MySQL database."""
    conn = get_db_connection()
    if not conn:
        return None
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO `users` (`username`, `password_hash`, `full_name`, `email`, `role`, `status`)
            VALUES (%s, %s, %s, %s, %s, %s);
        """, (username, password_hash, full_name, email, role, status))
        conn.commit()
        new_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return new_id
    except Exception as err:
        print(f"[BASTA DB] Add user error: {err}")
        return None


def update_user(user_id, full_name, email, role, status="Active"):
    """Updates user information in MySQL database."""
    conn = get_db_connection()
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE `users`
            SET `full_name` = %s, `email` = %s, `role` = %s, `status` = %s
            WHERE `id` = %s;
        """, (full_name, email, role, status, user_id))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as err:
        print(f"[BASTA DB] Update user error: {err}")
        return False


def delete_user(user_id):
    """Deletes a user account from MySQL database."""
    conn = get_db_connection()
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM `users` WHERE `id` = %s;", (user_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as err:
        print(f"[BASTA DB] Delete user error: {err}")
        return False


# --- TRANSACTION RECORDING ---

def record_sale_transaction(transaction_id, order_id, table_num, cashier_name, payment_method, subtotal, vat, service_charge, total, cash_received, change_due, items):
    """Records completed order transaction and its line items in MySQL."""
    conn = get_db_connection()
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO `sales_transactions`
            (`transaction_id`, `order_id`, `table_num`, `cashier_name`, `payment_method`, `subtotal`, `vat`, `service_charge`, `total`, `cash_received`, `change_due`)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """, (transaction_id, order_id, table_num, cashier_name, payment_method, subtotal, vat, service_charge, total, cash_received, change_due))

        for itm in items:
            name = itm.get("name", "Item")
            qty = itm.get("qty", 1)
            price = itm.get("price", 0.0)
            line_tot = price * qty
            cursor.execute("""
                INSERT INTO `transaction_items` (`transaction_id`, `product_name`, `quantity`, `unit_price`, `line_total`)
                VALUES (%s, %s, %s, %s, %s);
            """, (transaction_id, name, qty, price, line_tot))

        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as err:
        print(f"[BASTA DB] Record sale error: {err}")
        return False


if __name__ == "__main__":
    if "--reset-products" in sys.argv:
        success = reset_products_database()
        if not success:
            sys.exit(1)
    else:
        success = initialize_database()
        if not success:
            sys.exit(1)
