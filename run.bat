@echo off
REM CS2 Skin Arbitrage - Robust Installer & Launcher
REM This script checks for Python, optionally downloads the repository (if files missing),
REM checks required Python packages, prompts to install if missing, and launches the Streamlit app.

chcp 65001 >nul 2>&1
setlocal enabledelayedexpansion

:: --- Configure your GitHub repository here ---
:: Replace these with your actual repository URLs before distributing the BAT file.
set "REPO_GIT=https://github.com/DQUKR/arbitrajwithcopilot.git"
set "REPO_ZIP=https://github.com/DQUKR/arbitrajwithcopilot/archive/refs/heads/master.zip"
:: ------------------------------------------------

echo.
echo ========================================
echo CS2 Skin Arbitrage - Installer ^& Launcher
echo ========================================
echo.

:: 1) Check Python availability
echo [1/5] Checking for Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo Python not found using "python". Trying "py -3"...
    py -3 --version >nul 2>&1
    if errorlevel 1 (
        echo.
        echo ERROR: Python 3 not found or not in PATH.
        echo Please install Python 3.8+ from https://www.python.org/downloads/ and ensure "Add Python to PATH" is checked.
        pause
        exit /b 1
    ) else (
        set "PY_CMD=py -3"
    )
) else (
    set "PY_CMD=python"
)
echo [OK] Using %PY_CMD% to run Python.

:: Create (or reuse) a virtual environment in .venv and use its python
set "VENV_DIR=.venv"
if not exist "%VENV_DIR%\Scripts\python.exe" (
    echo Creating virtual environment in %VENV_DIR%...
    %PY_CMD% -m venv "%VENV_DIR%"
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment.
        pause
        exit /b 1
    )
)
set "PY_CMD=%VENV_DIR%\Scripts\python.exe"
echo [OK] Using virtual environment python at %PY_CMD%.

:: 2) If repository files are missing, offer to download from GitHub
echo.
echo [2/5] Checking repository files...
if not exist app.py (
    echo app.py not found in current directory. Attempting automatic download from GitHub...
    echo Checking for git...
    git --version >nul 2>&1
    if errorlevel 0 (
        echo Git detected - cloning %REPO_GIT% ...
        git clone %REPO_GIT% temp_repo
        if errorlevel 0 (
            echo Moving files from temp_repo...
            robocopy temp_repo . /e >nul 2>&1
            rd /s /q temp_repo >nul 2>&1
        ) else (
            echo Git clone failed. Falling back to ZIP download.
            echo Downloading ZIP from %REPO_ZIP% ...
            powershell -Command "(New-Object System.Net.WebClient).DownloadFile('%REPO_ZIP%','repo.zip')"
            if exist repo.zip (
                echo Extracting repo.zip ...
                powershell -Command "Expand-Archive -Path 'repo.zip' -DestinationPath '.' -Force"
                del /f /q repo.zip >nul 2>&1
                for /d %%D in (*-master) do (
                    robocopy "%%D" . /e >nul 2>&1
                    rd /s /q "%%D" >nul 2>&1
                )
            ) else (
                echo ERROR: Failed to download repository zip. Please download manually from your GitHub repo.
                pause
                exit /b 1
            )
        )
    ) else (
        echo Git not available. Downloading ZIP from %REPO_ZIP% ...
        powershell -Command "(New-Object System.Net.WebClient).DownloadFile('%REPO_ZIP%','repo.zip')"
        if exist repo.zip (
            echo Extracting repo.zip ...
            powershell -Command "Expand-Archive -Path 'repo.zip' -DestinationPath '.' -Force"
            del /f /q repo.zip >nul 2>&1
            for /d %%D in (*-master) do (
                robocopy "%%D" . /e >nul 2>&1
                rd /s /q "%%D" >nul 2>&1
            )
        ) else (
            echo ERROR: Failed to download repository zip. Please download manually from your GitHub repo.
            pause
            exit /b 1
        )
    )
) else (
    echo app.py found - using current directory as project root.
)

:: 3) Verify required files exist now
echo.
echo [3/5] Verifying required files...
set "MISSING_FILES=0"
for %%F in (app.py requirements.txt) do (
    if not exist "%%F" (
        echo Missing file: %%F
        set /a MISSING_FILES+=1
    )
)
if %MISSING_FILES% gtr 0 (
    echo One or more required files are missing. Please ensure the repository is downloaded correctly.
    pause
    exit /b 1
)
echo [OK] Required files present.

:: 4) Check pip availability
echo.
echo [4/5] Checking pip availability...
%PY_CMD% -m pip --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: pip not found for %PY_CMD%.
    echo Please ensure pip is installed and accessible.
    pause
    exit /b 1
)
echo [OK] pip available.

echo.
echo Installing/upgrading required Python packages (this runs non-interactively)...
%PY_CMD% -m pip install --upgrade pip
%PY_CMD% -m pip install -r requirements.txt
if errorlevel 1 (
    echo WARNING: Some packages may have failed to install. Continuing anyway.
) else (
    echo Packages installed successfully.
)

:: 6) Launch the Streamlit app and open browser
echo.
echo Launching Streamlit application...
rem Open default browser to Streamlit URL after a short delay so server has time to start
start "" powershell -NoProfile -Command "Start-Sleep -Seconds 2; Start-Process 'http://localhost:8501'" >nul 2>&1
rem Run Streamlit in the current console so the batch waits until the app exits
%PY_CMD% -m streamlit run app.py

echo Application exited. Press any key to close.
pause >nul
exit /b 0
