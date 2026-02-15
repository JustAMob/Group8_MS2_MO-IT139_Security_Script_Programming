# Group8_MS2_MO-IT139_Security_Script_Programming
Security Script Programming 2026

## PASSECURIST - Network Security Tools

A basic network security toolkit featuring port scanning and traffic analysis capabilities.

---

## Features Overview

### Homepage
- Card-based navigation with hover glow effects
- Professional branding and tool descriptions
- Easy access to all security tools

### 1. Network Port Scanner
- Scans TCP ports on any IP address or hostname
- Real-time port status display (OPEN/CLOSED)
- Validates input with inline error feedback
- Port type presets for common services and games
- Service name mapping for known ports
- Comprehensive common ports reference table
- Stop/resume scanning functionality
- Results table with service identification

### 2. Network Traffic Analyzer
- Real-time packet capture using Scapy
- Protocol filtering (TCP, UDP, ICMP)
- Port-based filtering
- BPF filter syntax support
- Detailed packet information display
- Color-coded protocol identification
- Quick filter presets
- Administrator privilege checking

---

## How to Run

### Installation
```bash
# Required: Python 3.7+
python --version

# For Network Traffic Analyzer: Install Scapy
pip install scapy

# Note: Traffic Analyzer requires administrator/root privileges
# Windows: Run as Administrator
# Linux/Mac: Run with sudo
```

### Launch Application
```bash
python src/main.py
```

---

## Key Files

### Core Application
- **src/main.py** - Homepage with card-based tool selection

### Features (`src/features/`)
- **network_port_scanner.py** - Complete port scanning logic including:
  - Port scanning functions (`scan_port`, `scan_port_range`)
  - Validation functions (`validate_host`, `validate_port_range`)
  - Port constants (`COMMON_PORTS_BY_CATEGORY`, `PORT_PRESETS`, `PORT_SERVICE_MAP`)
  - Helper functions (`build_port_service_map`, `get_service_name`)

- **network_traffic_analyzer.py** - Complete traffic analysis logic including:
  - Packet capture (`start_packet_capture`)
  - Packet formatting (`format_packet_info`)
  - Filter validation (`validate_filter`)
  - Privilege checking (`check_privileges`, `get_scapy_status`)

### GUI (`src/gui/`)
- **network_portscanner_tab.py** - Port scanner interface
- **network_traffic_analyzer_tab.py** - Traffic analyzer interface with real-time display

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

## Traffic Analyzer Features

### Packet Capture
- **Real-time capture**: Live network packet monitoring
- **Protocol support**: TCP, UDP, ICMP
- **BPF filtering**: Berkeley Packet Filter syntax
- **Quick filters**: One-click presets (TCP, UDP, ICMP, HTTP, HTTPS, DNS)

### Display Information
- **Timestamp**: Millisecond precision capture time
- **Source/Destination**: IP addresses and ports
- **Protocol**: Color-coded identification
- **Summary**: Packet description and flags

### Requirements
- **Scapy library**: Install with `pip install scapy`
- **Admin privileges**: Required for packet capture
  - Windows: Open Command Prompt as Administrator, then run application
  - Linux/Mac: Run with `sudo python3 src/main.py`
---

## Dependencies

### Port Scanner
```
tkinter (built-in)
socket (built-in)
threading (built-in)
```

### Traffic Analyzer
```
scapy (install with: pip install scapy)
tkinter (built-in)
threading (built-in)
datetime (built-in)
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

**Code Structure**:
- Modular architecture (features, GUI, utilities)
- Threading for responsive scanning
- Input validation layer
- Error handling throughout

### Week 5 - Homework (Refactored) - February 15, 2026
**Architecture Refactoring**:
- Consolidated validation logic into features module
- Moved port constants from GUI to features module
- Improved separation of concerns (GUI vs business logic)
- Removed utils/validators.py (merged into features)
- Added helper function `get_service_name()` for cleaner code

### Week 6 - Homework - February 15, 2026
**Network Traffic Analyzer Implementation**:
- Real-time packet capture using Scapy library
- Protocol filtering (TCP, UDP, ICMP)
- BPF filter syntax support
- Detailed packet information display with timestamps
- Color-coded protocol identification
- Quick filter presets (TCP, UDP, ICMP, HTTP, HTTPS, DNS)
- Administrator privilege checking and user guidance
- Error handling for missing Scapy installation
- Thread-based capture for responsive GUI

**Homepage Implementation**:
- Card-based navigation system
- Hover glow effects on cards
- Tool descriptions and icons

**Code Structure**:
- Modular traffic analyzer feature module
- Separate GUI component for traffic analysis
- Scapy integration with privilege checking
- Real-time packet display with color coding

---

## Group's Project Plan
- Link: https://docs.google.com/spreadsheets/d/1oXL5hJg6MRoZwp_r84P0JkorvVMnKP5bkcYPTfBOUP0/edit?usp=sharing