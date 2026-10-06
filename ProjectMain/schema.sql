-- ====================================================================
-- BASTA POS & INVENTORY MANAGEMENT SYSTEM - DATABASE SCHEMA (XAMPP MySQL)
-- Database Name: basta_pos
-- ====================================================================

CREATE DATABASE IF NOT EXISTS `basta_pos` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `basta_pos`;

-- --------------------------------------------------------------------
-- 1. Table: users
-- --------------------------------------------------------------------
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

-- Seed default user accounts
INSERT INTO `users` (`username`, `password_hash`, `full_name`, `email`, `role`, `status`) VALUES
('admin', 'admin123', 'Chef Marco S.', 'admin@bastaburger.com', 'Administrator', 'Active'),
('cashier1', 'cashier123', 'Bea M.', 'bea@bastaburger.com', 'Cashier', 'Active'),
('supervisor', 'super123', 'Danilo R.', 'danilo@bastaburger.com', 'Shift Supervisor', 'Active'),
('inventory1', 'inv123', 'Aris P.', 'aris@bastaburger.com', 'Inventory Manager', 'Active')
ON DUPLICATE KEY UPDATE `username`=`username`;

-- --------------------------------------------------------------------
-- 2. Table: categories
-- --------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS `categories` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(50) NOT NULL UNIQUE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO `categories` (`name`) VALUES
('All items'), ('Burgers'), ('Sides'), ('Beverages'), ('Desserts')
ON DUPLICATE KEY UPDATE `name`=`name`;

-- --------------------------------------------------------------------
-- 3. Table: products
-- --------------------------------------------------------------------
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

INSERT INTO `products` (`sku`, `name`, `category`, `price`, `cost_price`, `stock_quantity`, `low_stock_threshold`, `in_store`, `online_ordering`, `grabfood`, `status`) VALUES
('BGR-001', 'Classic Basta Smash Burger', 'Burgers', 189.00, 85.00, 32, 12, TRUE, TRUE, TRUE, 'Active'),
('BGR-002', 'Truffle Mushroom Cheeseburger', 'Burgers', 249.00, 110.00, 18, 8, TRUE, TRUE, FALSE, 'Active'),
('BGR-003', 'Spicy BBQ Bacon Deluxe', 'Burgers', 229.00, 95.00, 24, 10, TRUE, TRUE, TRUE, 'Active'),
('DRK-001', 'Ube Shake Special', 'Beverages', 120.00, 45.00, 45, 15, TRUE, TRUE, FALSE, 'Active'),
('DRK-002', 'Calamansi Cold Brew Fizz', 'Beverages', 95.00, 30.00, 50, 15, TRUE, TRUE, TRUE, 'Active'),
('SDE-001', 'Crispy Golden Fries', 'Sides', 79.00, 25.00, 60, 20, TRUE, TRUE, TRUE, 'Active'),
('SDE-002', 'Garlic Parmesan Wedges', 'Sides', 99.00, 35.00, 22, 10, TRUE, TRUE, FALSE, 'Active'),
('DES-001', 'Warm Brioche Ice Cream Bun', 'Desserts', 119.00, 40.00, 8, 10, TRUE, FALSE, FALSE, 'Active')
ON DUPLICATE KEY UPDATE `sku`=`sku`;

-- --------------------------------------------------------------------
-- 4. Table: inventory_items
-- --------------------------------------------------------------------
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

INSERT INTO `inventory_items` (`sku`, `item_name`, `category`, `on_hand`, `par_level`, `unit`, `unit_cost`, `status`) VALUES
('ING-0018', 'USDA ground beef 80/20', 'Proteins', 18.5, 14.0, 'kg', 410.00, 'Healthy'),
('ING-0031', 'Brioche burger buns', 'Bakery', 4.0, 12.0, 'packs', 185.00, 'Critical'),
('ING-0064', 'Frozen ube ice cream', 'Desserts', 2.4, 6.0, 'L', 320.00, 'Low stock'),
('ING-0085', 'Russet potatoes', 'Produce', 31.0, 20.0, 'kg', 86.00, 'Healthy'),
('ING-0102', 'Calamansi glaze', 'Sauces', 3.0, 8.0, 'bottles', 145.00, 'Low stock')
ON DUPLICATE KEY UPDATE `sku`=`sku`;

-- --------------------------------------------------------------------
-- 5. Table: sales_transactions
-- --------------------------------------------------------------------
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

-- --------------------------------------------------------------------
-- 6. Table: transaction_items
-- --------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS `transaction_items` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `transaction_id` VARCHAR(50) NOT NULL,
    `product_name` VARCHAR(100) NOT NULL,
    `quantity` INT NOT NULL DEFAULT 1,
    `unit_price` DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    `line_total` DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    FOREIGN KEY (`transaction_id`) REFERENCES `sales_transactions`(`transaction_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
