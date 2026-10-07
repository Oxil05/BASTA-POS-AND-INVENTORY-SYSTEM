# 🍔 BASTA POS & INVENTORY MANAGEMENT SYSTEM - HOW TO RUN

A comprehensive guide for developers and team members to set up, run, and troubleshoot the BASTA Point of Sale (POS) and Restaurant Inventory System after cloning or pulling from GitHub.

---

## ⚡ The 1-Click Fast Track (`run.bat`)

If you are on Windows, an automated launcher script is included in the project root:

1. Open **XAMPP Control Panel** and click **Start** for **MySQL** (and **Apache**).
2. Double-click **`run.bat`** (or open terminal and run `.\run.bat`).

The script will automatically:
- Detect your Python installation (`python` or Windows `py` launcher).
- Create a clean local `.venv` virtual environment if you don't have one.
- Install all required libraries from `requirements.txt`.
- Verify/initialize the MySQL database tables.
- Launch the application login screen.

---

## 📋 Prerequisites

Before running manually, make sure your machine has:
1. **Python 3.10 or higher** installed from [python.org](https://www.python.org/).
   > [!IMPORTANT]
   > During Python installation on Windows, **check the box: "Add python.exe to PATH"**.
2. **XAMPP** installed (to run Apache and MySQL).

---

## 🛠️ Step-by-Step Setup Guide (Manual)

If you prefer setting up manually or need to run specific commands:

### Step 1: Start XAMPP Services
1. Open the **XAMPP Control Panel**.
2. Click **Start** for **Apache**.
3. Click **Start** for **MySQL** (both should turn green with Port 3306 active).

---

### Step 2: Open Terminal in Project Root
Navigate to the cloned repository directory:
```powershell
cd path\to\BASTA-POS-AND-INVENTORY-SYSTEM
```

---

### Step 3: Create & Activate a Local Virtual Environment

> [!WARNING]
> **Why you must create your own `.venv`:**
> Python virtual environments are **machine-specific**. They contain absolute file paths hardcoded to the original creator's computer. Never copy someone else's `.venv` folder. Always generate your own local virtual environment!

#### 1. Create a fresh virtual environment:
```powershell
python -m venv .venv
```
*(If `python` is not recognized, use: `py -3 -m venv .venv`)*

#### 2. Activate the virtual environment:
- **In PowerShell:**
  ```powershell
  .venv\Scripts\Activate.ps1
  ```
  > [!TIP]
  > **If PowerShell blocks the script** with error:
  > `File ... Activate.ps1 cannot be loaded because running scripts is disabled on this system`
  > Run this command in your PowerShell window to allow activation:
  > ```powershell
  > Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
  > ```
  > Then run `.venv\Scripts\Activate.ps1` again.

- **In Command Prompt (CMD):**
  ```cmd
  .venv\Scripts\activate.bat
  ```

Once activated, your terminal prompt will show `(.venv)`.

---

### Step 4: Install Required Libraries

With `(.venv)` activated, install all dependencies from `requirements.txt`:
```powershell
pip install -r requirements.txt
```

This installs:
- `customtkinter` (Modern UI framework)
- `pillow` (Image rendering & manipulation)
- `mysql-connector-python` (Official MySQL client driver)

---

### Step 5: Initialize the MySQL Database

Run the database setup script:
```powershell
python ProjectMain/database.py
```

This script will automatically:
- Connect to your local MySQL server (`localhost:3306`).
- Create the database `basta_pos` if it doesn't exist yet.
- Create all 6 relational tables (`users`, `categories`, `products`, `inventory_items`, `sales_transactions`, `transaction_items`).
- Seed initial sample products, stock items, and default login accounts.

*(Alternative: You can also import `ProjectMain/schema.sql` visually via phpMyAdmin at `http://localhost/phpmyadmin`)*.

---

### Step 6: Launch the Application

#### A. Full Application (Login Screen)
```powershell
python ProjectMain/login.py
```
Default accounts stored in the database:
- **Administrator:** `admin` / `admin123` *(Chef Marco S.)*
- **Cashier:** `cashier1` / `cashier123` *(Bea M.)*
- Or log in with **any user account** created via **Account Settings** or **phpMyAdmin**. All accounts are verified dynamically against MySQL.

#### B. Direct POS & Navigation Launcher
```powershell
python ProjectMain/POS.py
```

#### C. Direct Module Launchers (Quick Access)
| Module | Command | Features |
|---|---|---|
| **Product Management** | `python ProjectMain/product_management.py` | Add, edit, delete menu items, pricing & availability toggles |
| **Inventory Overview** | `python ProjectMain/inventory_overview.py` | Ingredient levels, par thresholds, low-stock alerts, receive stock |
| **Sales Reports** | `python ProjectMain/reports.py` | Daily, Weekly, Monthly, Yearly filters, bar chart, sales audit log |
| **Account Settings** | `python ProjectMain/account_settings.py` | Staff & administrator management, add user, edit roles |

---

## 🧭 System Navigation Overview

The application features a single-window layout with a persistent sidebar:

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

- **Instant Switching**: Click any sidebar button to switch views instantly without closing the window.
- **Cart Preservation**: Adding items to your POS cart is preserved when switching to **Stock** or **Products**.
- **Receipt Modal**: Click **`🧾 Receipt`** or **`➔ Charge`** on the POS screen to open the digital tablet receipt and payment confirmation popup.
- **Logout**: Click **`➔ Logout`** in the sidebar to return cleanly to the login screen.

---

## 🛠️ Complete Troubleshooting Guide for Colleague Errors

Here are the most common errors colleagues encounter when pulling from GitHub and how to fix them:

### 1. `ModuleNotFoundError: No module named 'customtkinter'` (or `'PIL'`, `'mysql'`)
- **Cause:** Python is running globally instead of inside the virtual environment, or dependencies were not installed.
- **Solution:**
  1. Make sure your virtual environment is active (your prompt should show `(.venv)`).
  2. If not active, run `.venv\Scripts\activate`.
  3. Run `pip install -r requirements.txt`.

---

### 2. `Activate.ps1 cannot be loaded because running scripts is disabled on this system`
- **Cause:** Windows PowerShell default security policy prevents running unsigned `.ps1` scripts.
- **Solution:**
  In your current PowerShell window, run:
  ```powershell
  Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
  ```
  Then re-run `.venv\Scripts\Activate.ps1`.
  *(Alternatively, use Command Prompt (CMD) and run `.venv\Scripts\activate.bat`)*.

---

### 3. `Fatal error in launcher: Unable to create process using '...'`
- **Cause:** Attempting to use a `.venv` directory that was copied from another colleague's computer. The virtual environment's internal scripts point to file paths on the original PC that do not exist on your PC.
- **Solution:**
  1. Delete the existing `.venv` folder:
     ```powershell
     Remove-Item -Recurse -Force .venv
     ```
  2. Re-create a fresh virtual environment:
     ```powershell
     python -m venv .venv
     .venv\Scripts\activate
     pip install -r requirements.txt
     ```

---

### 4. `2003 (HY000): Can't connect to MySQL server on 'localhost:3306'`
- **Cause:** The MySQL server in XAMPP is stopped or not running.
- **Solution:**
  1. Open **XAMPP Control Panel**.
  2. Click the **Start** button next to **MySQL**.
  3. Ensure the text turns green with port `3306`.

---

### 5. `1045 (28000): Access denied for user 'root'@'localhost' (using password: NO/YES)`
- **Cause:** The colleague's local MySQL server has a password set on the `root` account (e.g. `root`, `admin`, or a custom password from a previous MySQL / Workbench installation), whereas default XAMPP uses an empty password (`""`).
- **Solution:**
  Open `ProjectMain/database.py` and update line 15 with your MySQL password:
  ```python
  DEFAULT_DB_CONFIG = {
      "host": "localhost",
      "user": "root",
      "password": "YOUR_MYSQL_PASSWORD_HERE",  # <-- Put your MySQL root password here
      "port": 3306,
      "database": "basta_pos"
  }
  ```
  *(Or set an environment variable before running: `$env:BASTA_DB_PASSWORD="YOUR_PASSWORD"`)*.

---

### 6. `1049 (42000): Unknown database 'basta_pos'`
- **Cause:** The database has not been initialized in MySQL yet.
- **Solution:**
  Run the initialization script:
  ```powershell
  python ProjectMain/database.py
  ```
  *(Note: The system now also includes auto-initialization that will automatically create the database on the fly if it is missing)*.

---

### 7. `python : The term 'python' is not recognized as the name of a cmdlet...`
- **Cause:** Python is installed, but `python.exe` was not added to the Windows system PATH environment variable.
- **Solution:**
  - Try using `py` instead:
    ```powershell
    py -3 -m venv .venv
    py -3 ProjectMain/login.py
    ```
  - Or add Python to your PATH: In Windows Search, open "Edit the system environment variables" -> Environment Variables -> Path -> Add the path to your Python installation (e.g. `C:\Users\<User>\AppData\Local\Programs\Python\Python313\`).

---

### 8. `Port 3306 conflict in XAMPP`
- **Cause:** Another service on the colleague's PC (e.g., MySQL Workbench, MariaDB service, or Docker) is already using port 3306.
- **Solution:**
  1. In XAMPP Control Panel, click **Config** next to MySQL -> `my.ini`.
  2. Change `port=3306` to `port=3307`.
  3. Save and start MySQL.
  4. In `ProjectMain/database.py`, update `"port": 3307`.

---

## 📁 Repository File Structure

```text
BASTA-POS-AND-INVENTORY-SYSTEM/
├── run.bat                        # Automated 1-click Windows setup & launcher
├── requirements.txt               # Python package dependencies
├── .gitignore                     # Git ignore rules (.venv, __pycache__, etc.)
├── HOW TO RUN.md                  # Complete setup and troubleshooting guide
├── README.md                      # Project documentation
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
└── Designs/                       # Original Figma/Mockup UI designs and brand logo
    ├── ADMIN_ACCOUNT SETTINGS.png
    ├── ADMIN_INVENTORY.png
    ├── ADMIN_PRODUCTMANAGEMENT.png
    ├── ADMIN_REPORTS.png
    ├── BASTA_RECEIPT.png
    ├── LOG-IN PAGE.png
    └── basta_LOGO.png
```
