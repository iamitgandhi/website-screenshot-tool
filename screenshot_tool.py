#!/usr/bin/env python3
"""
Local Website Screenshot Tool
A Flask-based web application for taking screenshots of websites
across multiple device resolutions.
"""

from flask import Flask, render_template, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from PIL import Image
from io import BytesIO
import os
import shutil
import time
import random
import urllib.parse
import concurrent.futures
import threading

app = Flask(__name__)

# Configuration
DEVICE_FOLDERS = {
    "Desktop": (1920, 1080),
    "Laptop": (1366, 768),
    "Tablet": (768, 1024),
    "Mobile": (390, 844),
}

BASE_SAVE_PATH = "screenshots"
DOWNLOAD_PATH = "/home/iamitgandhi/Downloads"

# Ensure directories exist
os.makedirs(BASE_SAVE_PATH, exist_ok=True)
os.makedirs(DOWNLOAD_PATH, exist_ok=True)

# Global variables for progress tracking and stop functionality
screenshot_count = 0
screenshot_total = 0
current_status = "Ready"
progress_messages = []
stop_event = threading.Event()
current_thread = None

def init_driver():
    """Initialize Chrome WebDriver with headless options"""
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")

    # Try to use system Chrome/Chromium
    try:
        driver = webdriver.Chrome(options=chrome_options)
    except Exception as e:
        # Fallback to chromium-browser if available
        chrome_options.binary_location = "/usr/bin/chromium-browser"
        driver = webdriver.Chrome(options=chrome_options)

    driver.set_page_load_timeout(60)
    return driver

def capture_screenshot(url, device_name, resolution, save_dir):
    """Capture screenshot for a specific URL and device resolution"""
    global screenshot_count, progress_messages, stop_event

    # Check if stop was requested
    if stop_event.is_set():
        return

    try:
        driver = init_driver()
        width, _ = resolution
        clean_url = url.rstrip('/') + f"/?cache={int(time.time())}"
        driver.set_window_size(width, 1000)
        driver.get(clean_url)

        # Check for stop during page load
        if stop_event.is_set():
            driver.quit()
            return

        time.sleep(random.randint(3, 5))

        # Scroll main page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        # Check for stop during scrolling
        if stop_event.is_set():
            driver.quit()
            return

        # Scroll iframes
        try:
            iframes = driver.find_elements(By.TAG_NAME, "iframe")
            for iframe in iframes:
                if stop_event.is_set():
                    break
                try:
                    driver.switch_to.frame(iframe)
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(1)
                    driver.switch_to.default_content()
                except:
                    driver.switch_to.default_content()
        except:
            pass

        # Final check before screenshot
        if stop_event.is_set():
            driver.quit()
            return

        # Get full page height and resize
        total_height = driver.execute_script("return document.body.scrollHeight")
        driver.set_window_size(width, min(total_height + 200, 10000))
        time.sleep(1)

        # Take screenshot
        png = driver.get_screenshot_as_png()
        image = Image.open(BytesIO(png))

        # Generate filename
        page_slug = urllib.parse.urlparse(url).path.replace("/", "_").strip("_") or "home"
        filename = f"{page_slug}_{width}px.png"
        filepath = os.path.join(save_dir, device_name, filename)

        # Save image
        image.save(filepath)
        driver.quit()

        screenshot_count += 1
        message = f"✅ {url} [{device_name}] captured. ({screenshot_count}/{screenshot_total})"
        progress_messages.append(message)
        print(message)

    except Exception as e:
        message = f"❌ {url} [{device_name}] failed. Reason: {str(e)}"
        progress_messages.append(message)
        print(message)

def get_internal_links(base_url):
    """Get all internal links from a website"""
    if stop_event.is_set():
        return []

    try:
        driver = init_driver()
        driver.get(base_url)
        time.sleep(4)

        # Check for stop during link discovery
        if stop_event.is_set():
            driver.quit()
            return []

        links = set()
        link_elements = driver.find_elements(By.TAG_NAME, "a")

        for elem in link_elements:
            if stop_event.is_set():
                break
            href = elem.get_attribute("href")
            if href and href.startswith(base_url):
                clean_link = href.split('#')[0]  # Remove anchors
                links.add(clean_link)

        driver.quit()
        return list(links)
    except Exception as e:
        print(f"Error getting internal links: {e}")
        return []

def process_screenshots(urls):
    """Process screenshots for multiple URLs"""
    global screenshot_count, screenshot_total, current_status, progress_messages, stop_event

    current_status = "Processing"
    progress_messages = []
    stop_event.clear()  # Clear any previous stop signal

    # Clean up previous screenshots
    shutil.rmtree(BASE_SAVE_PATH, ignore_errors=True)
    os.makedirs(BASE_SAVE_PATH, exist_ok=True)

    all_tasks = []

    for url in urls:
        if stop_event.is_set():
            current_status = "Stopped"
            progress_messages.append("🛑 Process stopped by user.")
            return

        try:
            domain = urllib.parse.urlparse(url).netloc.replace(".", "_")
            save_dir = os.path.join(BASE_SAVE_PATH, domain)
            os.makedirs(save_dir, exist_ok=True)

            # Create device folders
            for device in DEVICE_FOLDERS:
                os.makedirs(os.path.join(save_dir, device), exist_ok=True)

            # Get internal links
            progress_messages.append(f"🔍 Scanning {url} for internal links...")
            internal_links = get_internal_links(url)

            if stop_event.is_set():
                current_status = "Stopped"
                progress_messages.append("🛑 Process stopped by user.")
                return

            internal_links.append(url)  # Include the main URL

            progress_messages.append(f"📄 Found {len(internal_links)} pages to screenshot")

            # Create tasks for each page and device
            for page in internal_links:
                if stop_event.is_set():
                    break
                for device_name, resolution in DEVICE_FOLDERS.items():
                    all_tasks.append((page, device_name, resolution, save_dir))

        except Exception as e:
            progress_messages.append(f"❌ Error processing {url}: {str(e)}")

    if stop_event.is_set():
        current_status = "Stopped"
        progress_messages.append("🛑 Process stopped by user.")
        return

    screenshot_count = 0
    screenshot_total = len(all_tasks)

    progress_messages.append(f"🚀 Starting {screenshot_total} screenshot tasks...")

    # Execute screenshots with thread pool
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        # Submit all tasks
        future_to_task = {executor.submit(capture_screenshot, *task): task for task in all_tasks}

        # Process completed tasks and check for stop
        for future in concurrent.futures.as_completed(future_to_task):
            if stop_event.is_set():
                # Cancel remaining futures
                for f in future_to_task:
                    f.cancel()
                current_status = "Stopped"
                progress_messages.append("🛑 Process stopped by user.")
                return

            try:
                future.result()  # This will raise any exception that occurred
            except Exception as e:
                print(f"Task failed: {e}")

    # Check one final time before saving
    if stop_event.is_set():
        current_status = "Stopped"
        progress_messages.append("🛑 Process stopped by user.")
        return

    # Move website folders directly to Downloads (no parent timestamp folder)
    for item in os.listdir(BASE_SAVE_PATH):
        source_path = os.path.join(BASE_SAVE_PATH, item)
        if os.path.isdir(source_path):
            dest_path = os.path.join(DOWNLOAD_PATH, item)
            # Remove existing folder if it exists
            if os.path.exists(dest_path):
                shutil.rmtree(dest_path)
            shutil.move(source_path, dest_path)
            progress_messages.append(f"📂 {item} saved to {dest_path}")

    current_status = "Completed"
    progress_messages.append(f"✅ All screenshots saved to {DOWNLOAD_PATH}")

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/start_screenshots', methods=['POST'])
def start_screenshots():
    """Start screenshot process"""
    global current_status, current_thread

    data = request.get_json()
    urls_text = data.get('urls', '')

    if not urls_text.strip():
        return jsonify({'error': 'Please enter at least one URL'}), 400

    urls = [url.strip() for url in urls_text.split(',') if url.strip()]

    if current_status == "Processing":
        return jsonify({'error': 'Screenshot process is already running'}), 400

    # Start processing in background thread
    current_thread = threading.Thread(target=process_screenshots, args=(urls,))
    current_thread.daemon = True
    current_thread.start()

    return jsonify({'message': 'Screenshot process started'})

@app.route('/stop', methods=['POST'])
def stop_screenshots():
    """Stop the current screenshot process"""
    global current_status, stop_event

    if current_status != "Processing":
        return jsonify({'error': 'No process is currently running'}), 400

    stop_event.set()
    progress_messages.append("🛑 Stop requested by user...")

    return jsonify({'message': 'Stop signal sent'})

@app.route('/status')
def get_status():
    """Get current status and progress"""
    return jsonify({
        'status': current_status,
        'progress': f"{screenshot_count}/{screenshot_total}",
        'messages': progress_messages[-10:]  # Last 10 messages
    })

if __name__ == '__main__':
    print("🚀 Starting Local Screenshot Tool...")
    print("📱 Access the tool at: http://localhost:5000")
    print(f"📂 Screenshots will be saved to: {DOWNLOAD_PATH}")
    app.run(debug=False, host='0.0.0.0', port=5000)
