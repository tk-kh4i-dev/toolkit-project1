"""
NAME: sys_info.py
DESCRIPTION: Can be used for displaying the current system's information
LICENSE: MIT License - See the LICENSE file in the root directory.
"""

import cpuinfo
import ctypes
import platform
import psutil
import sys
import time
import winreg

UI_WIDTH = 58
BAR_LENGTH = 20
CPU_NAME = cpuinfo.get_cpu_info()['brand_raw']

def get_os_full_name():
    try:
        # Access the registry
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion")
        
        # Read the values
        product_name, _ = winreg.QueryValueEx(key, "ProductName")
        build, _ = winreg.QueryValueEx(key, "CurrentBuildNumber")
        ubr, _ = winreg.QueryValueEx(key, "UBR")
        winreg.CloseKey(key)

        # Fix Windows 10 -> 11 label
        if int(build) >= 22000 and "Windows 10" in product_name:
            product_name = product_name.replace("Windows 10", "Windows 11")
        
        # Explicitly return the formatted string
        return f"{product_name} (Build {build}.{ubr})"
    except Exception:
        # Fallback to the generic version if anything goes wrong
        uname = platform.uname()
        return f"{uname.system} {uname.release}"
    
def get_size(bytes, suffix="B"):
    """Scale bytes to proper format (KB, MB, GB, etc.)"""
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

def draw_header(title):
    print("┌" + "─" * UI_WIDTH + "┐")
    print(f"│ {title.center(56)} │")
    print("├" + "─" * UI_WIDTH + "┤")

def draw_footer():
    print("└" + "─" * UI_WIDTH + "┘")

def display_specs():
    # Clear terminal screen
    print("\033[H", end="")
    
    draw_header("CORE SYSTEM DIAGNOSTICS v1.18 [FINAL UPDATE]")
    
    # OS Info
    uname = platform.uname()
    full_os = get_os_full_name()
    print(f"│ [SYS] OS: {full_os} ({platform.machine()})".ljust(59) + "│")
    print(f"│ [SYS] Hostname: {uname.node}".ljust(59) + "│")
    
    # CPU Info
    print("├" + "─" * UI_WIDTH + "┤")
    cpufreq = psutil.cpu_freq()
    if cpufreq:
        print(f"│ [CPU] Base Clock: {cpufreq.max:.2f}Mhz".ljust(59) + "│")

    print(f"│ [CPU] Model: {CPU_NAME[:40]}".ljust(59) + "│")
    print(f"│ [CPU] Cores: {psutil.cpu_count(logical=False)} Physical | {psutil.cpu_count(logical=True)} Logical".ljust(59) + "│")
    
    # CPU Usage Bar
    cpu_usage = psutil.cpu_percent(interval=0)
    bar_length = BAR_LENGTH
    filled_length = int(round(bar_length * cpu_usage / 100))
    bar = '█' * filled_length + '░' * (bar_length - filled_length)
    print(f"│ [CPU] Load: [{bar}] {cpu_usage}%".ljust(59) + "│")
    
    # Memory Info
    print("├" + "─" * UI_WIDTH + "┤")
    svmem = psutil.virtual_memory()
    print(f"│ [RAM] Total: {get_size(svmem.total)} | Available: {get_size(svmem.available)}".ljust(59) + "│")
    ram_filled = int(round(bar_length * svmem.percent / 100))
    ram_bar = '█' * ram_filled + '░' * (bar_length - ram_filled)
    print(f"│ [RAM] Usage: [{ram_bar}] {svmem.percent}%".ljust(59) + "│")
    
    # Disk Info
    print("├" + "─" * UI_WIDTH + "┤")
    print("│ [DSK] Mountpoint     Total      Used       Usage         │")
    partitions = psutil.disk_partitions()
    
    for partition in partitions:
        if 'loop' in partition.device or not partition.fstype:
            continue
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

def main():
    if platform.system() == "Windows":
        kernel32 = ctypes.windll.kernel32
        # Enable ENABLE_VIRTUAL_TERMINAL_PROCESSING (0x0004)
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
    try:
        # The infinite loop lives here, inside 'main'
        while True:
            display_specs()
            time.sleep(2.5)
    except KeyboardInterrupt:
        print("\n[!] Stopping ...")
        sys.exit(0)

if __name__ == "__main__":
    main()
