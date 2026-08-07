@echo off
echo ========================================
echo   Douala Vehicle Dealership
echo   Flask Application Starter
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

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
    echo Virtual environment created successfully!
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo.
echo Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
REM Check if database exists
if not exist "database.db" (
    echo ========================================
    echo   Setting up database...
    echo ========================================
    echo.
    python setup_database.py
    if errorlevel 1 (
        echo ERROR: Failed to setup database
        pause
        exit /b 1
    )
    echo.
)

echo.
echo ========================================
echo   Starting Flask Application...
echo ========================================
echo.
echo The application will run at: http://127.0.0.1:5000
echo Admin panel at: http://127.0.0.1:5000/admin/login
echo.
echo Default admin credentials:
echo   Username: admin
echo   Password: admin123
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

REM Run the Flask application
python app.py

pause
