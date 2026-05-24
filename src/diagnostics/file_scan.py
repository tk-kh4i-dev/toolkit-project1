"""
NAME: file_scan.py
DESCRIPTION: For scanning and counting files, to try and find duplicates of files
LICENSE: MIT License - See the LICENSE file in the root directory.
"""

import os
import sys
from collections import defaultdict

def scan_directory(target_dir, size_threshold_mb=100):
    threshold_bytes = size_threshold_mb * 1024 * 1024
    large_files = []
    size_map = defaultdict(list)
    
    print(f"\n[!] Initializing scan target: {target_dir}")
    print(f"[!] Target threshold: > {size_threshold_mb}MB\n")
    print("Scanning...")
    
    file_count = 0
    for root, _, files in os.walk(target_dir):
        for filename in files:
            file_path = os.path.join(root, filename)
            try:
                # Get file size safely without breaking on broken symlinks
                if os.path.exists(file_path):
                    file_size = os.path.getsize(file_path)
                    file_count += 1
                    
                    # Track large files
                    if file_size > threshold_bytes:
                        large_files.append((file_path, file_size))
                    
                    # Track sizes for duplicate tracking
                    size_map[file_size].append(file_path)
            except (PermissionError, FileNotFoundError):
                continue

    # Print Large Files
    print("\n" + "="*30 + " LARGE FILES " + "="*30)
    if not large_files:
        print(" No files found exceeding threshold.")
    else:
        # Sort by largest first
        large_files.sort(key=lambda x: x[1], reverse=True)
        for path, size in large_files[:20]: # Show top 20
            size_mb = size / (1024 * 1024)
            print(f"[{size_mb:.1f} MB] {path}")

    # Print Potential Duplicates (Matching sizes)
    print("\n" + "="*27 + " SUSPECTED DUPLICATES " + "="*27)
    duplicate_groups = {k: v for k, v in size_map.items() if len(v) > 1 and k > 1024*1024} # Only files > 1MB
    
    if not duplicate_groups:
        print(" No duplicate size footprints detected.")
    else:
        for size, paths in sorted(duplicate_groups.items(), reverse=True)[:10]: # Show top 10 groups
            print(f"\nSize Footprint: {size / (1024*1024):.2f} MB")
            for path in paths:
                print(f"  ├─ {path}")
                
    print(f"\n[✓] Scan complete. Total items indexed: {file_count}")

if __name__ == "__main__":
    # Use current working directory if no path passed
    target = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    scan_directory(target)