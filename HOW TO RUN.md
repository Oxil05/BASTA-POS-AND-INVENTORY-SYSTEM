# 🍔 BASTA POS & INVENTORY MANAGEMENT SYSTEM - HOW TO RUN

A comprehensive guide to setting up, running, and navigating the BASTA Point of Sale (POS) and Restaurant Inventory System.

---

## 📋 System Prerequisites

Before running the application, make sure you have:
1. **Python 3.10 or higher** installed on your system.
2. **XAMPP** installed (for MySQL database management).
3. The project virtual environment with the required dependencies:
   - `customtkinter` (Modern UI framework)
   - `Pillow` (Image manipulation & rendering)
   - `mysql-connector-python` (MySQL database client)

---

## ⚙️ Step 1: Activate Virtual Environment

Open **PowerShell** or **Command Prompt** in the project root directory:

```powershell
# Navigate to the project root directory
cd d:\Projects\BASTA-POS-AND-INVENTORY-SYSTEM

# Activate the virtual environment
.venv\Scripts\activate
```

*(If you ever need to install or update dependencies manually:)*
```powershell
pip install customtkinter pillow mysql-connector-python
```

---

## 🗄️ Step 2: Set Up the XAMPP Database

### 1. Start XAMPP Services
1. Open the **XAMPP Control Panel**.
2. Click **Start** for **Apache**.
3. Click **Start** for **MySQL** (both should turn green).

### 2. Initialize the Database (`basta_pos`)
You can initialize the database using either of the two methods below:

#### Method A: Automatic Python Script (Recommended - 1 Command)
In your terminal, run:
```powershell
python ProjectMain/database.py
```
This script will automatically:
- Connect to your local MySQL server (`localhost:3306`).
- Create the database `basta_pos`.
- Create all 6 relational tables (`users`, `categories`, `products`, `inventory_items`, `sales_transactions`, `transaction_items`).
- Seed sample products, stock items, and default login accounts.

#### Method B: Visual Import via phpMyAdmin (Web Browser)
1. Open your browser and go to `http://localhost/phpmyadmin`.
2. Click **New** on the left panel, type database name `basta_pos`, and click **Create**.
3. Click the **Import** tab at the top.
4. Click **Choose File** and select `ProjectMain/schema.sql`.
5. Scroll down and click **Import** (or **Go**).

---

## 🚀 Step 3: Run the System

You can launch the system in different modes depending on what you want to test:

### 1. Launch the Complete System (Starting at Login Screen)
```powershell
python ProjectMain/login.py
```
- Enter credentials to log in:
  - **Username:** `admin` | **Password:** `admin123` *(Administrator)*
  - **Username:** `cashier1` | **Password:** `cashier123` *(Cashier)*
- Upon successful login, you are automatically redirected into the unified POS application.

---

### 2. Launch Directly into the Unified POS & Management System
```powershell
python ProjectMain/POS.py
```
- Opens the full application directly.
- The persistent left sidebar lets you switch between all modules instantly within the same window.

---

### 3. Direct Module Launchers (Quick Access)
If you want to open directly into a specific module, you can run:

| Module | Command | Features |
|---|---|---|
| **Product Management** | `python ProjectMain/product_management.py` | Add, edit, delete menu items, pricing & availability toggles |
| **Inventory Overview** | `python ProjectMain/inventory_overview.py` | Ingredient levels, par thresholds, low-stock alerts, receive stock |
| **Sales Reports** | `python ProjectMain/reports.py` | Daily, Weekly, Monthly, Yearly filters, bar chart, sales audit log |
| **Account Settings** | `python ProjectMain/account_settings.py` | Staff & administrator management, add user, edit roles |

> [!NOTE]
> Regardless of which module launcher you run, the sidebar remains active, allowing you to switch between any screen seamlessly without closing the window.

---

## 🧭 Step 4: Navigating the Unified Application

The application uses an integrated single-window layout:

```
+-----------------------------------------------------------------------------------+
|  SIDEBAR (110px)  |  UNIFIED CONTENT CONTAINER (Dynamically Switched)             |
|  [Logo] BASTA POS |                                                               |
|                   |  - POS Register: (Catalog Grid + Right Checkout Panel)        |
|  [ ⊞ POS ]        |  - Product Management: (Product Table + Right Editor Drawer)  |
|  [ 📦 Products ]  |  - Stock / Inventory: (Metrics + Alerts + Inventory Table)    |
|  [ 📋 Stock ]     |  - Reports: (Period Filter + Bar Chart + Audit Log Table)     |
|  [ 📊 Reports ]   |  - Settings: (Staff Metrics + User Accounts Table + Modals)   |
|  [ ⚙ Settings ]   |                                                               |
|                   |                                                               |
|  [ ➔ Logout ]     |                                                               |
+-----------------------------------------------------------------------------------+
```

- **Instant Switching (0ms delay)**: Click any sidebar button to switch views instantly.
- **Cart Preservation**: Adding items to your POS cart is never lost if you temporarily switch to **Stock** or **Products** to check inventory.
- **Receipt Modal**: Click **`🧾 Receipt`** or **`➔ Charge`** on the POS screen to open the digital tablet receipt and payment confirmation popup.
- **Logout**: Click **`➔ Logout`** at the bottom of the sidebar to return to the login screen.

---

## 📁 Project Directory Structure

```text
BASTA-POS-AND-INVENTORY-SYSTEM/
├── Designs/                       # Original Figma/Mockup UI designs and brand logo
│   ├── ADMIN_ACCOUNT SETTINGS.png
│   ├── ADMIN_INVENTORY.png
│   ├── ADMIN_PRODUCTMANAGEMENT.png
│   ├── ADMIN_REPORTS.png
│   ├── BASTA_RECEIPT.png
│   ├── LOG-IN PAGE.png
│   └── basta_LOGO.png
│
├── ProjectMain/                   # Python application modules
│   ├── POS.py                     # Master POS system & unified view manager
│   ├── login.py                   # Split-screen employee login page
│   ├── receipt.py                 # Payment confirmation & tablet receipt popup
│   ├── product_management.py      # Product catalog & side drawer editor
│   ├── inventory_overview.py      # Real-time ingredient tracking & restock dialogs
│   ├── reports.py                 # Analytics, period switcher & visual bar charts
│   ├── account_settings.py        # Staff accounts table & permission management
│   ├── database.py                # MySQL connection manager & auto-initializer
│   └── schema.sql                 # Standalone SQL schema for phpMyAdmin import
│
├── .venv/                         # Python virtual environment
├── HOW TO RUN.md                  # This run guide
└── README.md                      # Project documentation
```

---

## 🛠️ Common Troubleshooting

| Issue | Solution |
|---|---|
| **Can't connect to MySQL server on `localhost:3306`** | Ensure the **XAMPP Control Panel** is open and **MySQL** has been started (green indicator). |
| **Port 3306 Conflict in XAMPP** | If another service is using port 3306, change the port in XAMPP (`Config` -> `my.ini` -> change to `3307`), then update `"port": 3307` in `ProjectMain/database.py`. |
| **`ModuleNotFoundError: No module named 'customtkinter'`** | Make sure your virtual environment is active: `.venv\Scripts\activate`, then run `pip install -r requirements.txt` or `pip install customtkinter pillow mysql-connector-python`. |
| **Window scaling looks small or large** | The system uses responsive grid sizing and automatically adapts to your screen resolution and window resize events. |
