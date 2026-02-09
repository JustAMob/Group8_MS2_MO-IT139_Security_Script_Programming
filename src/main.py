# src/main.py

import tkinter as tk
import sys
import os

# Add src to path; for Python to find modules inside the src directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the GUI
from gui.network_portscanner_tab import NetworkPortScannerTab

root = tk.Tk()
root.title("🛡️ PASSECURIST - Network Port Scanner")
root.geometry("1600x900")
root.configure(bg="#0f172a")

# Passes root window to network port scanner gui tab so it can attach its design/widgets to the main app window
NetworkPortScannerTab(root)

# Starts app
root.mainloop()