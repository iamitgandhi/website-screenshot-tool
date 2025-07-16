#!/bin/bash

# Local Screenshot Tool Installation Script for Ubuntu 24.04 LTS
# This script installs all dependencies and sets up the screenshot tool

echo "🚀 Installing Local Screenshot Tool for Ubuntu 24.04 LTS"
echo "=================================================="

# Update system packages
echo "📦 Updating system packages..."
sudo apt update

# Install Python3 and pip if not already installed
echo "🐍 Installing Python3 and pip..."
sudo apt install -y python3 python3-pip python3-venv

# Install Chrome/Chromium browser
echo "🌐 Installing Chrome browser..."
if ! command -v google-chrome &> /dev/null; then
    if ! command -v chromium-browser &> /dev/null; then
        echo "Installing Chromium browser..."
        sudo apt install -y chromium-browser
    else
        echo "Chromium browser already installed"
    fi
else
    echo "Google Chrome already installed"
fi

# Install ChromeDriver
echo "🚗 Installing ChromeDriver..."
sudo apt install -y chromium-chromedriver

# Create virtual environment
echo "🔧 Creating Python virtual environment..."
python3 -m venv screenshot_env
source screenshot_env/bin/activate

# Install Python dependencies
echo "📚 Installing Python dependencies..."
pip install --upgrade pip
pip install flask selenium pillow

# Create project directory structure
echo "📁 Setting up project structure..."
mkdir -p screenshots downloads templates

# Set permissions
chmod +x screenshot_tool.py

echo ""
echo "✅ Installation completed successfully!"
echo ""
echo "🎯 To run the screenshot tool:"
echo "1. Activate virtual environment: source screenshot_env/bin/activate"
echo "2. Run the application: python3 screenshot_tool.py"
echo "3. Open your browser and go to: http://localhost:5000"
echo ""
echo "📝 Note: Make sure you have the following files in your directory:"
echo "   - screenshot_tool.py (main application)"
echo "   - templates/index.html (web interface)"
echo ""
