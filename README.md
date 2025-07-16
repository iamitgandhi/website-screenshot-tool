# Local Website Screenshot Tool

A simple, fast, and fully local web app to capture full-page screenshots of any website across multiple device resolutions.  
**Screenshots are saved directly to your Downloads folder, organized by website and device.**

---

## 🚀 Features

- **Multi-Device Screenshots:**  
  Captures each website in Desktop (1920×1080), Laptop (1366×768), Tablet (768×1024), and Mobile (390×844) resolutions.

- **Automatic Internal Link Discovery:**  
  Finds and screenshots all internal pages of the provided websites.

- **Organized Output:**  
  Each website gets its own folder in `/home/iamitgandhi/Downloads/`, with subfolders for each device type.

- **Simple Web UI:**  
  - Enter one or more URLs (comma-separated)
  - Start and Stop buttons for process control
  - Real-time progress and status updates

- **24/7 Operation:**  
  Runs as a systemd service, auto-starts on boot, and restarts on failure.

- **No Download/ZIP Management:**  
  All screenshots are saved directly to your Downloads folder for easy access.

---

## 📦 Folder Structure Example



/home/iamitgandhi/Downloads/ ├── example_com/ │ ├── Desktop/ │ ├── Laptop/ │ ├── Tablet/ │ └── Mobile/ └── anotherdomain_com/ ├── Desktop/ ├── Laptop/ ├── Tablet/ └── Mobile/


---

## 🛠️ Requirements

- Ubuntu 24.04 LTS
- Python 3.x
- Chrome or Chromium browser installed
- ChromeDriver installed and in PATH
- Python packages: Flask, Selenium, Pillow

---

## ⚡ Installation & Setup

1. **Clone or copy the tool to your machine.**

2. **Set up a Python virtual environment and install requirements:**
   ```bash
   python3 -m venv screenshot_env
   source screenshot_env/bin/activate
   pip install flask selenium pillow


Ensure Chrome/Chromium and ChromeDriver are installed.

Copy the provided screenshot_tool.py and templates/index.html to your project directory.

Set up the systemd service:

Create /etc/systemd/system/screenshot-tool.service with:

[Unit]
Description=Local Screenshot Tool
After=network.target

[Service]
Type=simple
User=iamitgandhi
Group=iamitgandhi
WorkingDirectory=/home/iamitgandhi/WebsiteScreenshotTool
Environment=PATH=/home/iamitgandhi/WebsiteScreenshotTool/screenshot_env/bin
ExecStart=/home/iamitgandhi/WebsiteScreenshotTool/screenshot_env/bin/python3 /home/iamitgandhi/WebsiteScreenshotTool/screenshot_tool.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal
SyslogIdentifier=screenshot-tool

[Install]
WantedBy=multi-user.target


Reload and start the service:

sudo systemctl daemon-reload
sudo systemctl enable screenshot-tool.service
sudo systemctl start screenshot-tool.service

🌐 Usage

Access the web UI:
Open http://localhost:5000 in your browser.

Input URLs:
Enter one or more website URLs, separated by commas.

Start Screenshots:
Click Start Screenshots. Progress and status will be shown live.

Stop Process:
Click Stop Process at any time to cancel the current job.

Access Results:
Open your file manager and go to /home/iamitgandhi/Downloads/.
Each website will have its own folder (e.g., example_com/), with device-specific subfolders.

🛑 Systemd Service Management
Check status:
sudo systemctl status screenshot-tool.service
View logs:
sudo journalctl -u screenshot-tool.service -f
Restart:
sudo systemctl restart screenshot-tool.service
Stop:
sudo systemctl stop screenshot-tool.service
📝 Changelog
Initial public release
Clean, minimal UI
Direct folder output to Downloads
Stop/cancel functionality
No ZIP/download management (files are always local)
📬 Support & Customization

For feature requests, bug reports, or customizations, contact the maintainer.

Enjoy fast, organized, and reliable website screenshots — right from your own machine!


---
