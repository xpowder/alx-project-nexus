@echo off
REM Setup script for local development on Windows

echo ========================================
echo ALX Project Nexus - Local Setup
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

echo [1/5] Creating virtual environment...
if exist venv (
    echo Virtual environment already exists. Skipping...
) else (
    python -m venv venv
    echo Virtual environment created!
)

echo.
echo [2/5] Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo [3/5] Upgrading pip...
python -m pip install --upgrade pip

echo.
echo [4/5] Installing dependencies...
pip install -r requirements.txt

echo.
echo [5/5] Setting up environment file...
if exist .env (
    echo .env file already exists. Skipping...
) else (
    echo Creating .env file from template...
    copy env.example .env
    echo.
    echo Generating SECRET_KEY...
    python generate_secret_key.py
    echo.
    echo Please copy the generated SECRET_KEY above and update your .env file
)

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Update .env file with your SECRET_KEY
echo 2. Run: python manage.py migrate
echo 3. Run: python manage.py load_sample_data
echo 4. Run: python manage.py createsuperuser
echo 5. Run: python manage.py runserver
echo.
echo Then visit: http://localhost:8000/
echo.

pause

