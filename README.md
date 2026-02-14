# Group8_MS2_MO-IT139_Security_Script_Programming
Security Script Programming 2026

## PASSECURIST - Network Port Scanner

A basic network port scanning tool with real-time validation and detailed results display.

---

## Features Overview

### 1. Network Port Scanner
- Scans TCP ports on any IP address or hostname
- Real-time port status display (OPEN/CLOSED)
- Validates input with inline error feedback
- Port type presets for common services and games
- Service name mapping for known ports
- Comprehensive common ports reference table
- Stop/resume scanning functionality
- Results table with service identification

---

## How to Run

### Installation
```bash
# No additional packages required - uses built-in Python libraries
python --version  # Requires Python 3.7+
```

### Launch Application
```bash
python src/main.py
```

---

## Key Files

### Core Application
- **src/main.py** - Main application entry point

### Features (`src/features/`)
- **network_port_scanner.py** - Port scanning logic using socket connections

### GUI (`src/gui/`)
- **network_port_scanner_tab.py** - Scanner interface with grid-based table layout

---

## Port Scanning Features

### Input Validation
- **Host/IP Address**: Validates both numerical IPs and domain names
- **Port Range**: Enforces 1-65535 range, numeric input only, start < end
- **Real-time Feedback**: Inline validation with ✓/⚠ indicators

### Scanning Capabilities
- **Socket-based scanning**: Uses `socket.connect_ex()` for connection testing
- **Configurable timeout**: 0.5 second default for responsive scanning
- **Real-time updates**: Results appear row-by-row during scan
- **Service mapping**: Identifies 25+ common services automatically

### Port Type Presets
Pre-configured port ranges for quick scanning:
- **Web Services** (80-443): HTTP, HTTPS
- **Mail Services** (25-143): SMTP, POP3, IMAP
- **Remote Access** (22-3389): SSH, Telnet, RDP
- **Directory/Auth** (88-636): Kerberos, LDAP
- **File Transfer** (20-445): FTP, TFTP, SMB
- **Network Core** (53-123): DNS, DHCP, NTP
- **Gaming**: Steam (80-27100), Valorant (80-8400)

---

## Dependencies
```
tkinter (built-in)
socket (built-in)
threading (built-in)
```

---

## Version History

### Week 5 - Homework (Initial Code) - February 9, 2026
**Network Port Scanner Implementation**:
- Socket-based TCP port scanning
- Real-time validation with inline feedback
- Port type presets for common services
- Comprehensive common ports reference table
- Grid-based results display with service mapping
- Stop/clear/resume functionality
- Professional dark theme UI

### Week 5 - Homework - February 15, 2026
**Network Port Scanner Implementation**:
- Removed validators.py and transferred the code to network_port_scanner.py


**Code Structure**:
- Modular architecture (features, GUI, utilities)
- Threading for responsive scanning
- Input validation layer
- Error handling throughout

---

## Group's Project Plan
- Link: https://docs.google.com/spreadsheets/d/1oXL5hJg6MRoZwp_r84P0JkorvVMnKP5bkcYPTfBOUP0/edit?usp=sharing

