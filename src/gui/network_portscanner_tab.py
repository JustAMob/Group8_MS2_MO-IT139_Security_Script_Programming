import tkinter as tk
from tkinter import Scrollbar, Text, END
import threading

# ===== IMPORT YOUR SCANNER LOGIC =====
from features.network_port_scanner import (
    scan_ports,
    get_common_ports,
    resolve_host
)

# ================= THEME =================
BG_COLOR = "#0f172a"
CARD_COLOR = "#1e293b"
TEXT_MAIN = "#e2e8f0"
ACCENT_COLOR = "#38bdf8"
BTN_HOVER = "#0ea5e9"
INPUT_BG = "#334155"
SUCCESS_COLOR = "#22c55e"
ERROR_COLOR = "#ef4444"
DETAIL_COLOR = "#94a3b8"


class NetworkPortScannerTab(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=BG_COLOR)
        self.pack(fill="both", expand=True, padx=20, pady=20)

        # ================= HEADER =================
        tk.Label(
            self,
            text="PASSECURIST",
            font=("Segoe UI", 22, "bold"),
            fg=ACCENT_COLOR,
            bg=BG_COLOR
        ).pack(pady=(10, 4))

        tk.Label(
            self,
            text="Network Scanner & Port Analyzer",
            font=("Segoe UI", 11),
            fg=TEXT_MAIN,
            bg=BG_COLOR
        ).pack(pady=(0, 15))

        # ================= MAIN CARD =================
        main_card = tk.Frame(self, bg=CARD_COLOR, padx=25, pady=20)
        main_card.pack(fill="both", expand=True)

        tk.Label(
            main_card,
            text="Scan Configuration",
            font=("Segoe UI", 14, "bold"),
            fg=ACCENT_COLOR,
            bg=CARD_COLOR
        ).pack(anchor="w", pady=(0, 15))

        # ================= TARGET =================
        tk.Label(
            main_card,
            text="Target IP / Hostname",
            font=("Segoe UI", 11),
            fg=TEXT_MAIN,
            bg=CARD_COLOR
        ).pack(anchor="w")

        self.entry_target = tk.Entry(
            main_card,
            font=("Consolas", 12),
            bg=INPUT_BG,
            fg=TEXT_MAIN,
            insertbackground="white",
            relief="flat"
        )
        self.entry_target.pack(fill="x", pady=(5, 12), ipady=6)

        # ================= PORT RANGE =================
        port_frame = tk.Frame(main_card, bg=CARD_COLOR)
        port_frame.pack(fill="x", pady=(0, 15))

        tk.Label(
            port_frame,
            text="Port Range",
            font=("Segoe UI", 11),
            fg=TEXT_MAIN,
            bg=CARD_COLOR
        ).pack(side="left")

        self.entry_ports = tk.Entry(
            port_frame,
            font=("Consolas", 12),
            bg=INPUT_BG,
            fg=TEXT_MAIN,
            insertbackground="white",
            relief="flat"
        )
        self.entry_ports.pack(
            side="left", fill="x", expand=True, padx=(10, 0), ipady=6
        )
        self.entry_ports.insert(0, "1-1024")

        # ================= BUTTONS =================
        btn_frame = tk.Frame(main_card, bg=CARD_COLOR)
        btn_frame.pack(fill="x", pady=(10, 20))

        tk.Button(
            btn_frame,
            text="START SCAN",
            bg=ACCENT_COLOR,
            fg="#0f172a",
            font=("Segoe UI", 11, "bold"),
            relief="flat",
            activebackground=BTN_HOVER,
            cursor="hand2",
            command=self.start_scan
        ).pack(side="left", fill="x", expand=True, padx=(0, 10))

        tk.Button(
            btn_frame,
            text="COMMON PORTS",
            bg="#475569",
            fg=TEXT_MAIN,
            font=("Segoe UI", 11, "bold"),
            relief="flat",
            cursor="hand2",
            command=self.use_common_ports
        ).pack(side="left", padx=(0, 10))

        tk.Button(
            btn_frame,
            text="CLEAR RESULTS",
            bg="#334155",
            fg=TEXT_MAIN,
            font=("Segoe UI", 11, "bold"),
            relief="flat",
            cursor="hand2",
            command=self.clear_results
        ).pack(side="left")

        # ================= RESULTS =================
        tk.Label(
            main_card,
            text="Scan Results",
            font=("Segoe UI", 13, "bold"),
            fg=ACCENT_COLOR,
            bg=CARD_COLOR
        ).pack(anchor="w", pady=(10, 8))

        result_container = tk.Frame(main_card, bg=CARD_COLOR)
        result_container.pack(fill="both", expand=True)

        self.result_scroll = Scrollbar(result_container)
        self.result_scroll.pack(side="right", fill="y")

        self.result_text = Text(
            result_container,
            font=("Consolas", 11),
            bg=INPUT_BG,
            fg=TEXT_MAIN,
            insertbackground="white",
            wrap="word",
            relief="flat",
            yscrollcommand=self.result_scroll.set
        )
        self.result_text.pack(side="left", fill="both", expand=True)

        self.result_scroll.config(command=self.result_text.yview)

        self.log("Ready. Enter a target and start scanning.")

    # ================= UTIL =================
    def log(self, message):
        self.result_text.insert(END, message + "\n")
        self.result_text.see(END)

    def clear_results(self):
        self.result_text.delete("1.0", END)
        self.log("Results cleared.")

    def use_common_ports(self):
        ports = get_common_ports()
        self.entry_ports.delete(0, END)
        self.entry_ports.insert(0, ",".join(map(str, ports)))

    def parse_ports(self, port_input: str):
        ports = set()
        try:
            if "-" in port_input:
                start, end = port_input.split("-", 1)
                ports.update(range(int(start), int(end) + 1))
            else:
                for p in port_input.split(","):
                    ports.add(int(p.strip()))
        except ValueError:
            return None

        return sorted(p for p in ports if 0 < p < 65536)

    # ================= SCAN CONTROL =================
    def start_scan(self):
        target = self.entry_target.get().strip()
        port_input = self.entry_ports.get().strip()

        if not target:
            self.log("[ERROR] Target is required.")
            return

        ports = self.parse_ports(port_input)
        if not ports:
            self.log("[ERROR] Invalid port format.")
            return

        self.clear_results()
        self.log("[INFO] Resolving host...")

        threading.Thread(
            target=self._scan_worker,
            args=(target, ports),
            daemon=True
        ).start()

    def _scan_worker(self, target, ports):
        ip = resolve_host(target)

        if not ip:
            self.after(0, self.log, "[ERROR] Unable to resolve host.")
            return

        self.after(0, self.log, f"[INFO] Target IP: {ip}")
        self.after(0, self.log, f"[INFO] Scanning {len(ports)} ports...")
        self.after(0, self.log, "-" * 55)

        results = scan_ports(target, ports)

        open_count = 0
        for port, is_open in results:
            if is_open:
                open_count += 1
                self.after(0, self.log, f"[OPEN]   {port}/tcp")
            else:
                self.after(0, self.log, f"[CLOSED] {port}/tcp")

        self.after(0, self.log, "-" * 55)
        self.after(
            0,
            self.log,
            f"[DONE] Scan complete — {open_count} open / {len(results)} total"
        )
