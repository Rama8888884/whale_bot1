#!/bin/bash

echo "=== System and Environment Check for Solana Whale Bot Setup ==="
echo ""

# Function to check command existence and version
check_command() {
  local cmd=$1
  local version_flag=$2
  local friendly_name=$3
  if command -v "$cmd" >/dev/null 2>&1; then
    version=$($cmd $version_flag 2>&1 | head -n 1)
    echo "[OK] $friendly_name found: $version"
  else
    echo "[MISSING] $friendly_name is NOT installed or NOT in PATH."
  fi
}

# Check OS
echo "Operating System Info:"
uname -a
echo ""

# Check architecture
arch=$(uname -m)
echo "System Architecture: $arch"
echo ""

# Check Docker
check_command "docker" "--version" "Docker"

# Check Python 3 (ensure version >= 3.8)
if command -v python3 >/dev/null 2>&1; then
  python_version=$(python3 --version 2>&1 | awk '{print $2}')
  echo "[OK] Python3 found: $python_version"
  required="3.8"
  if [[ $(echo -e "$python_version\n$required" | sort -V | head -n1) == "$required" ]]; then
    echo "Python3 version is sufficient (>= $required)."
  else
    echo "[WARNING] Python3 version is lower than $required."
  fi
else
  echo "[MISSING] Python3 is NOT installed or NOT in PATH."
fi

# Check pip
check_command "pip3" "--version" "pip3"

# Check virtualenv (optional but recommended)
check_command "virtualenv" "--version" "virtualenv"

# Check Git
check_command "git" "--version" "Git"

# Check curl
check_command "curl" "--version" "curl"

# Check Node.js (optional, depending on your bot)
check_command "node" "--version" "Node.js"

# Check npm
check_command "npm" "--version" "npm"

# Check solana CLI (optional, if used in your workflow)
check_command "solana" "--version" "Solana CLI"

# Check if requirements.txt exists in current directory
if [ -f requirements.txt ]; then
  echo "[OK] requirements.txt found."
else
  echo "[MISSING] requirements.txt NOT found in current directory."
fi

# Check if main.py exists in current directory
if [ -f main.py ]; then
  echo "[OK] main.py found."
else
  echo "[MISSING] main.py NOT found in current directory."
fi

# Final advice message
echo ""
echo "=== Summary ==="
echo "Please install any missing tools or upgrade those marked with WARNING."
echo "If Docker is missing, download and install Docker Desktop for Windows (AMD64 for your machine)."
echo "Python3 version 3.8 or higher is recommended."
echo "Git is necessary for version control and cloning repos."
echo "curl is useful for network requests and downloading."
echo "Node.js and npm are optional depending on your bot's dependencies."
echo "virtualenv helps isolate Python environments."
echo ""
echo "Run this script again after installations to verify."
