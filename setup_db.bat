@echo off
echo ========================================
echo   Database Setup Script
echo   Douala Vehicle Dealership
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from https://www.python.org/
    pause
    exit /b 1
)

echo Python found!
echo.

REM Check if database already exists
if exist "database.db" (
    echo WARNING: database.db already exists!
    echo.
    set /p confirm="Do you want to delete and recreate it? (yes/no): "
    if /i not "%confirm%"=="yes" (
        echo Database setup cancelled.
        pause
        exit /b 0
    )
    echo.
    echo Deleting existing database...
    del database.db
    echo Existing database deleted.
    echo.
)

REM Check if virtual environment exists and activate it
if exist "venv" (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo No virtual environment found. Installing dependencies globally...
    pip install -r requirements.txt >nul 2>&1
)

echo.
echo ========================================
echo   Creating Database...
echo ========================================
echo.

REM Run the setup script
python setup_database.py

if errorlevel 1 (
    echo.
    echo ERROR: Database setup failed!
    echo Make sure you have installed all requirements:
    echo   pip install -r requirements.txt
    pause
    exit /b 1
)

echo.
echo ========================================
echo   SUCCESS!
echo ========================================
echo.
echo Database has been created: database.db
echo.
echo You can now:
echo   1. Run 'start.bat' to start the application
echo   2. Or run 'python app.py' directly
echo.
echo Access the website at: http://127.0.0.1:5000
echo Access admin at: http://127.0.0.1:5000/admin/login
echo.
echo Login with:
echo   Username: admin
echo   Password: admin123
echo.
pause
