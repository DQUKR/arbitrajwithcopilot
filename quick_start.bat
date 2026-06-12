@echo off
REM Quick check and install script

setlocal enabledelayedexpansion
chcp 65001 >nul 2>&1

echo Checking dependencies...
python --version >nul 2>&1
if errorlevel 1 (
    echo Python not found! Download from https://www.python.org
    pause
    exit /b 1
)

echo Installing packages...
python -m pip install -r requirements.txt --quiet

echo.
echo All done! The app will start now...
echo.
timeout /t 2 >nul

start "" http://localhost:8501
python -m streamlit run app.py
