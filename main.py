import os
import sys
import subprocess
import platform

# --- CONFIGURATION ---
# This dictionary maps your menu choices to the actual file paths
TOOLS = {
    "1": {"name": "Disk Cleaner", "path": os.path.join("src", "maintenance", "disk_clean.py")},
    "2": {"name": "File Scanner", "path": os.path.join("src", "diagnostics", "file_scan.py")},
    "3": {"name": "Network Check", "path": os.path.join("src", "diagnostics", "netcheck.ps1")},
    "4": {"name": "System Info", "path": os.path.join("src", "diagnostics", "sys_info.py")}
}

def clear_screen():
    # Detects OS and runs the correct clear command
    subprocess.run('cls' if platform.system() == "Windows" else 'clear')

def run_tool(path):
    # Check if file exists before trying to run it
    if not os.path.exists(path):
        print(f"\n[!] ERROR: Could not find {path}")
        return

    # Execute based on file type
    try:
        if path.endswith('.py'):
            # Run Python using the current interpreter
            subprocess.run([sys.executable, path])
        elif path.endswith('.ps1'):
            # Run PowerShell
            subprocess.run(["powershell", "-File", path])
    except Exception as e:
        print(f"\n[!] An error occurred: {e}")

def main():
    while True:
        clear_screen()
        print(f"\n--- {platform.node()} System Toolkit ---")
        for key, tool in TOOLS.items():
            print(f"{key}. {tool['name']}")
        print("q. Quit")
        
        choice = input("\nSelect an option: ").lower()
        
        if choice == 'q':
            print("Exiting Toolkit ...")
            break
        elif choice in TOOLS:
            run_tool(TOOLS[choice]['path'])
            input("\nPress Enter to return to the menu...")
        else:
            print("Invalid choice!")
            input("Press Enter to continue...")

if __name__ == "__main__":
    main()