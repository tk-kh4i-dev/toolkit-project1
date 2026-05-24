"""
NAME: disk_clean.py
DESCRIPTION: For cleaning and purges temporary files in the disk drive
LICENSE: MIT License - See the LICENSE file in the root directory.
"""

import os
import shutil
import platform

def clean_temp_directories():
    current_os = platform.system()
    targets = []

    if current_os == "Windows":
        user_profile = os.environ.get("USERPROFILE", "")
        targets = [
            os.path.join(os.environ.get("WINDIR", "C:\\Windows"), "Temp"),
            os.path.join(user_profile, "AppData\\Local\\Temp")
        ]
    elif current_os in ["Linux", "Darwin"]: # Linux or macOS
        targets = ["/tmp", "/var/tmp"]

    print(f"[#] OS verified: {current_os}. Loading volatile directory targets...")
    
    total_purged = 0
    errors = 0

    for path in targets:
        if not os.path.exists(path):
            print(f"[x] Path omitted (does not exist): {path}")
            continue
            
        print(f"[!] Purging data from target zone: {path}")
        
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            try:
                if os.path.isfile(item_path) or os.path.islink(item_path):
                    file_size = os.path.getsize(item_path)
                    os.unlink(item_path)
                    total_purged += file_size
                elif os.path.isdir(item_path):
                    # Calculate directory size before wiping
                    dir_size = sum(os.path.getsize(os.path.join(r, f)) for r, _, files in os.walk(item_path) for f in files)
                    shutil.rmtree(item_path)
                    total_purged += dir_size
            except Exception:
                # Files often lock if system apps are currently utilizing them
                errors += 1
                continue

    purged_mb = total_purged / (1024 * 1024)
    print("\n" + "─"*40)
    print(f"[✓] Maintenance run complete.")
    print(f"[✓] Space recovered: {purged_mb:.2f} MB")
    print(f"[!] Active items skipped (currently locked by OS): {errors}")

if __name__ == "__main__":
    # Prompt confirmation before running a delete operations script
    confirm = input("Proceed with sweeping temporary cache locations? (y/N): ")
    if confirm.lower() == 'y':
        clean_temp_directories()
    else:
        print("Operation cancelled.")