"""
NAME: file_scan.py
DESCRIPTION: For scanning and counting files, to try and find duplicates of files
LICENSE: MIT License - See the LICENSE file in the root directory.
"""

import hashlib
import tempfile
import os
import sys
from collections import defaultdict

IGNORE_DIRS = {'$RECYCLE.BIN', 'System Volume Information', 'Windows'}
SIZE_THRESHOLD_MB = 100  # <--- Change this number here whenever you want

temp_dirs = [tempfile.gettempdir()]

def get_file_hash(path):
    """Calculates SHA256 hash for a file."""
    hasher = hashlib.sha256()
    with open(path, 'rb') as f:
        # Read in chunks to avoid memory issues with huge files
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()
    pass

def scan_directory(target_dir, threshold=SIZE_THRESHOLD_MB):
    threshold_bytes = threshold * 1024 * 1024
    large_files = []
    size_map = defaultdict(list)
    
    print(f"\n[!] Initializing scan target: {target_dir}")
    print(f"[!] Target threshold: > {threshold_bytes}MB\n")
    print("Scanning...")
    
    file_count = 0
    for root, _, files in os.walk(target_dir):
        for root, dirs, files in os.walk(target_dir):
            dirs[:] = [d for d in dirs if d not in IGNORE_DIRS] # Modifies 'dirs' in-place to skip them
        for filename in files:
            file_path = os.path.join(root, filename)
            try:
                stats = os.stat(file_path)
                file_size = stats.st_size
            except (PermissionError, FileNotFoundError, OSError):
                continue
    
    print("\n--- Verifying Duplicates with Hash ---")
    for size, paths in size_map.items():
        if len(paths) > 1 and size > 1024*1024:
            # Only if files have the same size, compare hashes
            hashes = {}
            for path in paths:
                try:
                    file_hash = get_file_hash(path)
                    if file_hash in hashes:
                        print(f"CONFIRMED DUPLICATE: {path} matches {hashes[file_hash]}")
                    else:
                        hashes[file_hash] = path
                except Exception:
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