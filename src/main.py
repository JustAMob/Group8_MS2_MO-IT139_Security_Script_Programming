import tkinter as tk
from tkinter import ttk

from gui.styles import AppTheme
from gui.network_portscanner_tab import NetworkPortScannerTab

def main():
    root = tk.Tk()
    root.title("PASSECURIST - Local Security Toolkit")
    root.geometry("720x920")         

    # Apply theme
    AppTheme.apply(root)

    # Notebook
    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True, padx=12, pady=(10, 12))

    # Tab 1 – Port Scanner (new
    tab1 = tk.Frame(notebook, bg=AppTheme.BG)
    notebook.add(tab1, text="  Port Scanner  ")
    NetworkPortScannerTab(tab1)



    # Bottom accent bar
    tk.Frame(root, height=2, bg=AppTheme.ACCENT).pack(fill="x", side="bottom")

    root.mainloop()


if __name__ == "__main__":
    main()