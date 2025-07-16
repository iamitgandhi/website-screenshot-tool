# 📸 Local Website Screenshot Tool

A simple, fast, and fully local web app to capture full-page screenshots of any website across multiple device resolutions.  
**Screenshots are saved directly to your Downloads folder, organized by website and device.**

---

## 🚀 Features

- **Multi-Device Screenshots**  
  Captures each website in:
  - Desktop (1920×1080)
  - Laptop (1366×768)
  - Tablet (768×1024)
  - Mobile (390×844)

- **Automatic Internal Link Discovery**  
  Finds and screenshots all internal pages of the provided websites.

- **Organized Output**  
  Each website gets its own folder in `/home/iamitgandhi/Downloads/`, with subfolders for each device type.

- **Simple Web UI**  
  - Enter one or more URLs (comma-separated)
  - Start and Stop buttons for control
  - Real-time progress and status updates

- **24/7 Operation via systemd**  
  - Auto-starts on boot
  - Restarts on failure

- **No ZIP or Download Hassles**  
  All screenshots are saved directly to your Downloads folder for instant access.

---

## 📂 Folder Structure Example

```
/home/iamitgandhi/Downloads/
├── example_com/
│   ├── Desktop/
│   ├── Laptop/
│   ├── Tablet/
│   └── Mobile/
└── anotherdomain_com/
    ├── Desktop/
    ├── Laptop/
    ├── Tablet/
    └── Mobile/
```

---

## 🛠️ Requirements

- Ubuntu 24.04 LTS
- Python 3.x
- Chrome or Chromium browser
- ChromeDriver (installed and in `PATH`)
- Python packages:
  - Flask
  - Selenium
  - Pillow

---

## ⚙️ Installation & Setup

1. **Clone or copy the tool to your machine**

2. **Set up a Python virtual environment and install requirements**

```bash
python3 -m venv screenshot_env
source screenshot_env/bin/activate
pip install flask selenium pillow
```

3. **Ensure Chrome/Chromium and ChromeDriver are installed**

4. **Copy files to your working directory**

Make sure `screenshot_tool.py` and `templates/index.html` are in the project root.

---

## 🔧 Run as a systemd Service

### Create the service file

```bash
sudo nano /etc/systemd/system/screenshot-tool.service
```

Paste the following content:

```ini
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
```

### Reload and start the service

```bash
sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl enable screenshot-tool.service
sudo systemctl start screenshot-tool.service
```

---

## 🌐 Usage

- **Access the web UI:**  
  Open [http://localhost:5000](http://localhost:5000) in your browser.

- **Input URLs:**  
  Enter one or more website URLs (comma-separated).

- **Start Screenshots:**  
  Click **Start Screenshots**. Progress and status updates appear in real-time.

- **Stop Process:**  
  Click **Stop Process** to cancel the running task.

- **Access Results:**  
  Navigate to `/home/iamitgandhi/Downloads/` in your file manager.

---

## 🧭 Systemd Management Commands

```bash
# Check service status
sudo systemctl status screenshot-tool.service

# View live logs
sudo journalctl -u screenshot-tool.service -f

# Restart service
sudo systemctl restart screenshot-tool.service

# Stop service
sudo systemctl stop screenshot-tool.service
```

---

## 📝 Changelog

- Initial public release
- Clean, minimal UI
- Direct folder output to Downloads
- Stop/cancel functionality
- No ZIP/download management (everything stays local)

---

## 📬 Support & Customization

For feature requests, bug reports, or custom development/customization — contact the maintainer.

> Enjoy fast, organized, and reliable website screenshots — right from your own machine!