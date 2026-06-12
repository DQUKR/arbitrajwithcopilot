#!/usr/bin/env bash

# CS2 Skin Arbitrage Application Installer & Launcher (Linux/Mac)
# This script will:
# - ensure Python 3 is available
# - optionally download the repository if app.py is missing
# - create a virtual environment in .venv
# - install requirements into the venv
# - launch Streamlit and open the browser

set -e

REPO_GIT="https://github.com/YOUR_USERNAME/cs2-arbitrage.git"
REPO_ZIP="https://github.com/YOUR_USERNAME/cs2-arbitrage/archive/refs/heads/main.zip"

echo
echo "========================================"
echo "CS2 Skin Arbitrage - Installer & Launcher"
echo "========================================"
echo

echo "[1/6] Checking for Python 3..."
if command -v python3 >/dev/null 2>&1; then
    SYS_PY=python3
elif command -v python >/dev/null 2>&1; then
    # some systems have python pointing to python3
    SYS_PY=python
else
    echo "ERROR: Python 3 not found. Install it and retry."
    exit 1
fi

PYVER=$($SYS_PY --version 2>&1 || true)
echo "[OK] Found $PYVER"
echo

echo "[2/6] Checking repository files..."
if [ ! -f "app.py" ]; then
    echo "app.py not found in current directory."
    read -p "Do you want to download the repository from GitHub now? (y/N) : " -r
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        if command -v git >/dev/null 2>&1; then
            echo "Cloning repository via git..."
            git clone "$REPO_GIT" temp_repo
            echo "Moving files into current directory..."
            shopt -s dotglob || true
            mv temp_repo/* . || true
            rm -rf temp_repo
        else
            echo "Git not found, attempting ZIP download..."
            $SYS_PY - <<'PY'
import urllib.request, zipfile, io, sys
url = sys.argv[1]
print('Downloading', url)
data = urllib.request.urlopen(url).read()
zf = zipfile.ZipFile(io.BytesIO(data))
zf.extractall()
print('Extracted')
PY "$REPO_ZIP"
            # move contents of *-main into current dir
            for d in ./*-main/; do
                if [ -d "$d" ]; then
                    echo "Moving contents of $d to current directory..."
                    shopt -s dotglob || true
                    mv "$d"* . || true
                    rm -rf "$d"
                    break
                fi
            done
        fi
    else
        echo "Skipping repository download. Ensure you're running this from the project folder." 
    fi
else
    echo "app.py found - using current directory as project root."
fi
echo

echo "[3/6] Verifying required files..."
if [ ! -f "app.py" ] || [ ! -f "requirements.txt" ]; then
    echo "ERROR: Required files missing (app.py or requirements.txt)."
    exit 1
fi
echo "[OK] Required files present"
echo

echo "[4/6] Setting up virtual environment (.venv)..."
VENV_DIR=".venv"
if [ ! -x "$VENV_DIR/bin/python" ]; then
    $SYS_PY -m venv "$VENV_DIR"
fi
PY="$PWD/$VENV_DIR/bin/python"
echo "Using virtual environment python: $PY"
echo

echo "[5/6] Installing Python packages (this can take a while)..."
"$PY" -m pip install --upgrade pip setuptools wheel
"$PY" -m pip install -r requirements.txt || {
    echo "WARNING: Some packages failed to install."
    read -p "Continue anyway? (y/N) : " -r
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Aborting."
        exit 1
    fi
}
echo "[OK] Packages installed or user chose to continue"
echo

echo "[6/6] Launching Streamlit application..."
echo "Opening browser to http://localhost:8501 after short delay..."
(
    sleep 2
    if [[ "$OSTYPE" == "darwin"* ]]; then
        open "http://localhost:8501"
    else
        xdg-open "http://localhost:8501" 2>/dev/null || true
    fi
) &

"$PY" -m streamlit run app.py
