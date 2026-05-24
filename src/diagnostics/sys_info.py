"""
NAME: sys_info.py
DESCRIPTION: Can be used for displaying the current system's information
LICENSE: MIT License - See the LICENSE file in the root directory.
"""

import cpuinfo
import os
import platform
import psutil
import subprocess
import sys
import time


def get_size(bytes, suffix="B"):
    """Scale bytes to proper format (KB, MB, GB, etc.)"""
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

def draw_header(title):
    print("┌" + "─" * 58 + "┐")
    print(f"│ {title.center(56)} │")
    print("├" + "─" * 58 + "┤")

def draw_footer():
    print("└" + "─" * 58 + "┘")

def display_specs():
    # Clear terminal screen
    subprocess.run('cls' if os.name == 'nt' else 'clear', shell=True)
    
    draw_header("CORE SYSTEM DIAGNOSTICS v1.16.5")
    
    # OS Info
    uname = platform.uname()
    print(f"│ [SYS] OS: {uname.system} {uname.release} ({uname.machine})".ljust(59) + "│")
    print(f"│ [SYS] Hostname: {uname.node}".ljust(59) + "│")
    
    # CPU Info
    print("├" + "─" * 58 + "┤")
    cpufreq = psutil.cpu_freq()
    if cpufreq:
        print(f"│ [CPU] Base Clock: {cpufreq.max:.2f}Mhz".ljust(59) + "│")
    cpu_name = cpuinfo.get_cpu_info()['brand_raw']
    print(f"│ [CPU] Model: {cpu_name[:40]}".ljust(59) + "│")
    print(f"│ [CPU] Cores: {psutil.cpu_count(logical=False)} Physical | {psutil.cpu_count(logical=True)} Logical".ljust(59) + "│")
    
    # CPU Usage Bar
    cpu_usage = psutil.cpu_percent(interval=0.5)
    bar_length = 20
    filled_length = int(round(bar_length * cpu_usage / 100))
    bar = '█' * filled_length + '░' * (bar_length - filled_length)
    print(f"│ [CPU] Load: [{bar}] {cpu_usage}%".ljust(59) + "│")
    
    # Memory Info
    print("├" + "─" * 58 + "┤")
    svmem = psutil.virtual_memory()
    print(f"│ [RAM] Total: {get_size(svmem.total)} | Available: {get_size(svmem.available)}".ljust(59) + "│")
    ram_filled = int(round(bar_length * svmem.percent / 100))
    ram_bar = '█' * ram_filled + '░' * (bar_length - ram_filled)
    print(f"│ [RAM] Usage: [{ram_bar}] {svmem.percent}%".ljust(59) + "│")
    
    # Disk Info
    print("├" + "─" * 58 + "┤")
    print("│ [DSK] Mountpoint     Total      Used       Usage         │")
    partitions = psutil.disk_partitions()
    
    for partition in partitions[:3]: # Limit to first 3 partitions to keep layout clean
        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
            color_code = "\033[91m" if partition_usage.percent > 90 else "\033[92m"
            reset_color = "\033[0m"

            p_str = f"│  ├─ {partition.mountpoint:<12} " \
                    f"{get_size(partition_usage.total):<10} " \
                    f"{get_size(partition_usage.used):<10} " \
                    f"{partition_usage.percent}%"
            print(p_str.ljust(59) + "│")
        except PermissionError:
            continue
            
    draw_footer()

if __name__ == "__main__":
    display_specs()