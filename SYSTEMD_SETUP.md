# Systemd Service Setup Instructions

## Step-by-Step Setup

### 1. Replace your current screenshot_tool.py
Replace your current `screenshot_tool.py` with the updated version that saves to `$HOME/Downloads`

### 2. Copy the service file to systemd directory
```bash
sudo cp screenshot-tool.service /etc/systemd/system/
```

### 3. Reload systemd to recognize the new service
```bash
sudo systemctl daemon-reload
```

### 4. Enable the service (start on boot)
```bash
sudo systemctl enable screenshot-tool.service
```

### 5. Start the service
```bash
sudo systemctl start screenshot-tool.service
```

### 6. Check service status
```bash
sudo systemctl status screenshot-tool.service
```

## Service Management Commands

### Check if service is running
```bash
sudo systemctl status screenshot-tool.service
```

### Start the service
```bash
sudo systemctl start screenshot-tool.service
```

### Stop the service
```bash
sudo systemctl stop screenshot-tool.service
```

### Restart the service
```bash
sudo systemctl restart screenshot-tool.service
```

### View logs (real-time)
```bash
sudo journalctl -u screenshot-tool.service -f
```

### View recent logs
```bash
sudo journalctl -u screenshot-tool.service --since "1 hour ago"
```

### Disable service (won't start on boot)
```bash
sudo systemctl disable screenshot-tool.service
```

## Troubleshooting

### If service fails to start:
1. Check the logs:
   ```bash
   sudo journalctl -u screenshot-tool.service -n 50
   ```

2. Verify file paths in the service file are correct

3. Make sure the virtual environment exists and has all dependencies

### If you need to update the service file:
1. Edit the service file
2. Reload systemd: `sudo systemctl daemon-reload`
3. Restart the service: `sudo systemctl restart screenshot-tool.service`

## What This Setup Provides

✅ **Auto-start on boot** - Service starts automatically when your system boots
✅ **Auto-restart on crash** - If the app crashes, systemd will restart it after 10 seconds
✅ **Runs in background** - No need to keep a terminal open
✅ **System logging** - All output goes to system logs (viewable with journalctl)
✅ **User isolation** - Runs as your user, not root
✅ **Network dependency** - Waits for network to be available before starting

## Access Your Tool

Once the service is running, you can access your screenshot tool at:
- http://localhost:5000 (from your machine)
- http://192.168.1.10:5000 (from other devices on your network)

The tool will now be available 24/7!
