@echo off
echo === Environment Check for Solana Whale Bot ===
echo.

REM Check Solana CLI
echo Checking Solana CLI...
solana --version
if %errorlevel% neq 0 (
    echo [ERROR] Solana CLI not found or not working.
) else (
    echo [OK] Solana CLI detected.
)
echo.

REM Check Docker
echo Checking Docker...
docker --version
if %errorlevel% neq 0 (
    echo [ERROR] Docker not found or not working.
) else (
    echo [OK] Docker detected.
)

docker run --rm hello-world >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Docker hello-world test failed.
) else (
    echo [OK] Docker hello-world test passed.
)
echo.

REM Check Python
echo Checking Python...
python --version
if %errorlevel% neq 0 (
    echo [ERROR] Python not found or not working.
) else (
    echo [OK] Python detected.
)
echo.

REM Check pip
echo Checking pip...
pip --version
if %errorlevel% neq 0 (
    echo [ERROR] pip not found or not working.
) else (
    echo [OK] pip detected.
)
echo.

REM Check Node.js and npm
echo Checking Node.js...
node --version
if %errorlevel% neq 0 (
    echo [ERROR] Node.js not found or not working.
) else (
    echo [OK] Node.js detected.
)

echo Checking npm...
npm --version
if %errorlevel% neq 0 (
    echo [ERROR] npm not found or not working.
) else (
    echo [OK] npm detected.
)
echo.

REM Check Python dependencies installed (optional: you need requirements.txt in folder)
echo Checking Python dependencies installation...
pip install -r requirements.txt --quiet
if %errorlevel% neq 0 (
    echo [WARNING] Some Python dependencies may not have installed correctly.
) else (
    echo [OK] Python dependencies installed.
)
echo.

REM Test Python import (create test file and run)
echo Creating and running a quick Python import test...
echo import solana_functions > test_import.py
echo print("Python import test passed.") >> test_import.py

python test_import.py
if %errorlevel% neq 0 (
    echo [ERROR] Python import test failed.
) else (
    echo [OK] Python import test passed.
)

del test_import.py
echo.

echo === Environment Check Complete ===
pause