@echo off
title BASTA POS & INVENTORY MANAGEMENT SYSTEM
echo ========================================================
echo    BASTA BURGER - POS & INVENTORY MANAGEMENT SYSTEM
echo ========================================================
echo.

:: 1. Check if Python or the Windows py launcher is available
where python >nul 2>&1
if %errorlevel% neq 0 (
    where py >nul 2>&1
    if %errorlevel% neq 0 (
        echo [ERROR] Python is not detected on your system.
        echo Please install Python 3.10+ from https://www.python.org/
        echo Make sure to check "Add Python to PATH" during installation!
        echo.
        pause
        exit /b 1
    ) else (
        set "PY_EXEC=py -3"
    )
) else (
    set "PY_EXEC=python"
)

:: 2. Create virtual environment if it does not already exist
if not exist ".venv\Scripts\activate.bat" (
    echo [*] Virtual environment not found. Creating .venv...
    %PY_EXEC% -m venv .venv
    if %errorlevel% neq 0 (
        echo [ERROR] Could not create virtual environment.
        pause
        exit /b 1
    )
    echo [OK] Virtual environment created.
)

:: 3. Activate the virtual environment
call .venv\Scripts\activate.bat

:: 4. Install/Update required libraries
echo [*] Verifying required libraries (customtkinter, pillow, mysql-connector-python)...
python -m pip install -r requirements.txt --quiet
if %errorlevel% neq 0 (
    echo [WARNING] Pip install had issues. Attempting direct installation...
    python -m pip install customtkinter pillow mysql-connector-python
)

:: 5. Initialize MySQL database
echo [*] Checking database connection to XAMPP MySQL...
python ProjectMain\database.py

:: 6. Launch the application
echo.
echo ========================================================
echo    Starting BASTA Login Screen...
echo ========================================================
python ProjectMain\login.py

pause
