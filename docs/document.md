# Documentation 

---

# Network Port Scanner

## Core Functions

### scan_port(host, port, timeout=0.5)
Scan a single TCP port on the specified host.

**Parameters**:
- `host` (str): IP address or hostname
- `port` (int): Port number to check
- `timeout` (float): Connection timeout in seconds

**Returns**: 
- `bool`: True if port is open, False if closed

**Example**:
```python
is_open = scan_port("127.0.0.1", 80)
if is_open:
    print("Port 80 is OPEN")
```

---

### validate_host(host)
Validate if the host is reachable.

**Parameters**:
- `host` (str): IP address or hostname

**Returns**: 
- `tuple`: (is_valid, error_message)

---

### validate_port_range(start_str, end_str)
Validate port range input.

**Parameters**:
- `start_str` (str): Starting port as string
- `end_str` (str): Ending port as string

**Returns**: 
- `tuple`: (is_valid, start_port, end_port, error_message)

**Validation Rules**:
- Both values must be numeric
- Ports within 1-65535
- Start port ≤ end port
- Maximum 10,000 ports per scan

---

# Network Traffic Analyzer

## Core Functions

### start_packet_capture(filter_string="", packet_callback=None, stop_callback=None, count=0)
Start capturing packets with optional BPF filter.

**Parameters**:
- `filter_string` (str): BPF filter (e.g., "tcp and port 80")
- `packet_callback` (function): Called for each packet
- `stop_callback` (function): Check if capture should stop
- `count` (int): Number of packets (0 = infinite)

**Raises**:
- `ImportError`: If Scapy not installed
- `PermissionError`: If no admin/root privileges
- `ValueError`: If invalid filter

**Example**:
```python
def handle_packet(packet_info):
    print(f"{packet_info['protocol']} packet captured")

start_packet_capture(
    filter_string="tcp and port 443",
    packet_callback=handle_packet
)
```

---

### format_packet_info(packet)
Extract packet details for display.

**Parameters**:
- `packet`: Scapy packet object

**Returns**: 
- `dict`: Packet information with keys:
  - `timestamp`: Capture time
  - `protocol`: TCP/UDP/ICMP/Other
  - `src_ip`: Source IP address
  - `dst_ip`: Destination IP address
  - `src_port`: Source port (or 'N/A')
  - `dst_port`: Destination port (or 'N/A')
  - `summary`: Packet description

---

### validate_filter(filter_string)
Validate BPF filter syntax.

**Parameters**:
- `filter_string` (str): BPF filter to validate

**Returns**: 
- `tuple`: (is_valid, error_message)

**Valid Protocols**: tcp, udp, icmp, ip, arp

---

### check_privileges()
Check if running with admin/root privileges.

**Returns**: 
- `bool`: True if has privileges

**Platform Detection**:
- Windows: Uses `ctypes.windll.shell32.IsUserAnAdmin()`
- Linux/Mac: Checks `os.geteuid() == 0`

---

### get_scapy_status()
Get Scapy installation and privilege status.

**Returns**: 
- `tuple`: (scapy_installed, has_privileges, message)

---

## BPF Filter Syntax

### Common Filters
```
tcp                       # All TCP traffic
udp                       # All UDP traffic
icmp                      # All ICMP packets
tcp and port 80           # HTTP traffic
tcp and port 443          # HTTPS traffic
udp and port 53           # DNS queries
host 192.168.1.1          # Specific host
src host 10.0.0.5         # From specific source
dst port 443              # To specific port
```

---

# Homepage & Navigation

## PassecuristApp Class

### Main Components

**ToolCard**:
- Interactive card with hover glow effect
- Icon, title, and description
- Click opens tool in new window

**Features**:
- Card-based navigation
- Hover glow effects
- Back button in tool windows
- Homepage hides when tool opens

---

# Common Components

## Theme Colors
```python
BG_COLOR = "#0f172a"        # Dark slate background
CARD_COLOR = "#1e293b"      # Card/panel background
TEXT_MAIN = "#e2e8f0"       # Main text color
ACCENT_COLOR = "#38bdf8"    # Sky blue accent
INPUT_BG = "#334155"        # Input field background
SUCCESS_COLOR = "#22c55e"   # Green for valid/open
ERROR_COLOR = "#ef4444"     # Red for errors
WARNING_COLOR = "#f59e0b"   # Orange for warnings
DETAIL_COLOR = "#94a3b8"    # Gray for details
```

---

## Port Scanner Constants

### PORT_SERVICE_MAP
Maps port numbers to service names.

**Example**:
```python
PORT_SERVICE_MAP[80]    # "HTTP"
PORT_SERVICE_MAP[443]   # "HTTPS"
PORT_SERVICE_MAP[22]    # "SSH/SCP"
```

### PORT_PRESETS
Pre-configured port ranges for quick selection.

**Available Presets**:
- Web Services (80-443)
- Mail Services (25-143)
- Remote Access (22-3389)
- Directory/Auth (88-636)
- File Transfer (20-445)
- Network Core (53-123)
- Steam (80-27100)
- Valorant (80-8400)

---

## Technical Implementation

### Threading Architecture

**Port Scanner**:
- Main thread: GUI updates
- Daemon thread: Port scanning
- Communication: `is_scanning`, `scan_cancelled` flags

**Traffic Analyzer**:
- Main thread: GUI updates
- Daemon thread: Packet capture with Scapy
- Communication: `is_capturing`, `capture_stopped` flags

### Error Handling

**Port Scanner**:
- DNS resolution failure
- Connection timeout
- Invalid port range
- Host unreachable

**Traffic Analyzer**:
- Missing Scapy
- No admin privileges
- Invalid BPF filter
- Capture errors

---

## Platform Support

### Windows
- Port Scanner: Works without admin
- Traffic Analyzer: Requires Administrator
- Run: Open Command Prompt as Admin → `python src/main.py`

### Linux
- Port Scanner: Works without root
- Traffic Analyzer: Requires root
- Run: `sudo python3 src/main.py`

### Mac
- Port Scanner: Works without root
- Traffic Analyzer: Requires root
- Run: `sudo python3 src/main.py`

---

## Performance Notes

### Port Scanner
- Default timeout: 0.5 seconds/port
- Maximum ports: 10,000 per scan
- Memory usage: ~1 MB per 10,000 results

### Traffic Analyzer
- Real-time packet display
- Memory efficient (doesn't store packets)
- Thread-safe GUI updates
- Auto-scroll to latest packets

---

## Security Considerations

### Port Scanner
- Uses standard socket connections
- No special privileges needed
- Safe for general use

### Traffic Analyzer
- Requires elevated privileges
- Captures ALL network traffic
- Use responsibly and legally
- Only monitor authorized networks

---

## Version History 

### Version 1.0 (Week 5) - February 9, 2026
- Network Port Scanner
- Socket-based TCP scanning
- Real-time validation
- Service identification

### Version 1.1 (Week 5 Refactored) - February 15, 2026
- Architecture refactoring
- Consolidated validation logic
- Moved constants to features module

### Version 2.0 (Week 6) - February 15, 2026
- Network Traffic Analyzer
- Packet capture with Scapy
- BPF filter support
- Homepage with card navigation
- Back button functionality
- Platform-specific instructions