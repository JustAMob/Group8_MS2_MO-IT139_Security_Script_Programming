# Documentation 

## Network Port Scanner

### scan_port(host, port, timeout=0.5)
**Purpose**: Scan a single TCP port on the specified host.

**Parameters**:
- `host` (str): IP address or hostname to scan
- `port` (int): Port number to check
- `timeout` (float, default=0.5): Connection timeout in seconds

**Returns**: 
- `bool`: True if port is open, False if closed

**Details**:
- Creates a TCP socket using `socket.socket(socket.AF_INET, socket.SOCK_STREAM)`
- Uses `connect_ex()` which returns 0 if connection successful
- Automatically closes socket after attempt
- Returns False on any socket error

**Example**:
```python
is_open = scan_port("127.0.0.1", 80, timeout=1.0)
if is_open:
    print("Port 80 is OPEN")
else:
    print("Port 80 is CLOSED")
```

---

### scan_port_range(host, start_port, end_port, timeout=0.5, callback=None)
**Purpose**: Scan a range of ports on the specified host.

**Parameters**:
- `host` (str): IP address or hostname
- `start_port` (int): First port in range
- `end_port` (int): Last port in range (inclusive)
- `timeout` (float, default=0.5): Connection timeout
- `callback` (function, optional): Function called for each port result

**Returns**: 
- `dict`: Dictionary with 'open' and 'closed' lists
  ```python
  {
      'open': [80, 443],
      'closed': [22, 23, 25, ...]
  }
  ```

**Details**:
- Iterates through port range calling `scan_port()` for each
- Callback signature: `callback(port, is_open)`
- Used for batch scanning operations

---

### validate_host(host)
**Purpose**: Validate if the host is reachable and properly formatted.

**Parameters**:
- `host` (str): IP address or hostname to validate

**Returns**: 
- `tuple`: (is_valid, error_message)
  - `is_valid` (bool): True if host is valid
  - `error_message` (str or None): Error description if invalid

**Details**:
- Checks for empty/whitespace-only input
- Uses `socket.gethostbyname()` for DNS resolution
- Returns specific error messages:
  - "Please enter a valid IP address or hostname." (empty input)
  - "Host unreachable or invalid hostname." (DNS failure)
  - Custom error for unexpected exceptions

**Example**:
```python
valid, error = validate_host("google.com")
if valid:
    print("Host is reachable")
else:
    print(f"Error: {error}")
```

---

## Validators Module

### validate_port_range(start_str, end_str)
**Purpose**: Validate port range input with comprehensive checks.

**Parameters**:
- `start_str` (str): Starting port as string
- `end_str` (str): Ending port as string

**Returns**: 
- `tuple`: (is_valid, start_port, end_port, error_message)
  - `is_valid` (bool): True if range is valid
  - `start_port` (int or None): Validated starting port
  - `end_port` (int or None): Validated ending port
  - `error_message` (str or None): Error description if invalid

**Validation Rules**:
1. **Numeric Check**: Both values must be digits only (no letters/symbols)
2. **Range Bounds**: Ports must be within 1-65535
3. **Logical Order**: Start port ≤ end port
4. **Performance Limit**: Maximum 10,000 ports per scan

**Error Messages**:
- "Start port must be a number (no letters or symbols)"
- "End port must be a number (no letters or symbols)"
- "Start port must be at least 1"
- "Start port must not exceed 65535"
- "End port must be at least 1"
- "End port must not exceed 65535"
- "Start port must be less than end port"
- "Port range too large (max 10,000 ports for performance)"

**Example**:
```python
valid, start, end, error = validate_port_range("80", "443")
if valid:
    print(f"Scanning ports {start} to {end}")
else:
    print(f"Validation error: {error}")
```

---

## GUI Module

### NetworkPortScannerTab Class

#### \_\_init\_\_(self, parent)
**Purpose**: Initialize the port scanner GUI.

**Parameters**:
- `parent`: Parent Tkinter window

**Details**:
- Creates scrollable canvas for entire interface
- Sets up mousewheel scrolling
- Calls `setup_ui()` to build interface
- Configures canvas scroll region

---

#### setup_ui(self)
**Purpose**: Build all GUI elements.

**Components Created**:

1. **Header Section**:
   - Title: "NETWORK PORT SCANNER"
   - Subtitle: "Scan ports with real-time validation..."

2. **Scan Configuration Panel** (Left):
   - Host/IP input field
   - Port Type dropdown (12 presets)
   - Port range inputs (start/end)
   - Real-time validation indicators
   - START SCAN, STOP, CLEAR RESULTS buttons

3. **Common Ports Reference** (Right):
   - Grid-based table with 25+ entries
   - Categories: Web, Mail, Remote Access, etc.
   - Scrollable with fixed width (500px)
   - Center-aligned columns

4. **Results Section** (Bottom):
   - Treeview table with 3 columns:
     - Port Name (service)
     - Port # (number)
     - Result (OPEN/CLOSED)
   - Color-coded results (green=OPEN, gray=CLOSED)

---

#### validate_host_realtime(self, event=None)
**Purpose**: Real-time host validation on keystroke.

**Behavior**:
- Calls `validate_host()` from features module
- Updates `host_status` label with ✓ or ⚠ indicator
- Returns boolean for button enable/disable logic

---

#### validate_ports_realtime(self, event=None)
**Purpose**: Real-time port range validation on keystroke.

**Behavior**:
- Calls `validate_port_range()` from validators module
- Displays port count (e.g., "✓ Valid range (364 ports)")
- Shows specific error messages
- Returns boolean for button enable/disable logic

---

#### start_scan(self)
**Purpose**: Initiate port scanning process.

**Process**:
1. Check if already scanning → show warning if true
2. Validate host and port range → show error if invalid
3. Clear previous results
4. Disable START button, enable STOP button
5. Set flags: `is_scanning = True`, `scan_cancelled = False`
6. Launch `perform_scan()` in separate thread (daemon mode)

**Threading**:
- Uses `threading.Thread(target=self.perform_scan, daemon=True)`
- Keeps UI responsive during scan
- Daemon thread exits when main thread exits

---

#### perform_scan(self, host, start_port, end_port)
**Purpose**: Execute the actual port scanning operation.

**Process**:
1. Print "Scanning host: X" to console
2. Loop through port range:
   - Check if `scan_cancelled` → break if true
   - Call `scan_port(host, port, timeout=0.5)`
   - Determine status (OPEN/CLOSED)
   - Get service name from `PORT_SERVICE_MAP`
   - Print "Port X: OPEN/CLOSED" to console
   - Insert result into Treeview table with appropriate tag
3. Show completion message if not cancelled
4. Handle exceptions with error dialog
5. Finally block: Re-enable START button, disable STOP button

**Output Format**:
```
Scanning host: 127.0.0.1
Port 20: CLOSED
Port 21: CLOSED
Port 22: OPEN
...
Scan complete.
```

---

#### stop_scan(self)
**Purpose**: Stop ongoing scan gracefully.

**Behavior**:
- Sets `scan_cancelled = True`
- Disables STOP button
- `perform_scan()` checks this flag and breaks loop

---

#### clear_results(self)
**Purpose**: Remove all entries from results table.

**Implementation**:
```python
for item in self.results_tree.get_children():
    self.results_tree.delete(item)
```

---

#### on_preset_change(self, event=None)
**Purpose**: Handle port type dropdown selection.

**Behavior**:
- Gets selected preset from `PORT_PRESETS` dictionary
- Updates start/end port entries with preset values
- Triggers `validate_ports_realtime()` to update validation

**Presets Available**:
- Select (20-100)
- Web Services (80-443)
- Mail Services (25-143)
- Remote Access & Management (22-3389)
- Directory/Authentication (88-636)
- File Transfer & Sharing (20-445)
- Network Core (53-123)
- Network Management (161)
- Communication/VoIP (194-5061)
- Legacy/Testing (7-23)
- Steam (80-27100)
- Valorant (80-8400)

---

## Global Constants

### COMMON_PORTS_BY_CATEGORY
Dictionary mapping service categories to port-service pairs.

**Structure**:
```python
{
    "Web Services": [
        ("80", "HTTP"),
        ("443", "HTTPS")
    ],
    "Mail Services": [
        ("25", "SMTP"),
        ("110", "POP3"),
        ("143", "IMAP")
    ],
    # ... more categories
}
```

**Usage**: Displayed in reference table on right side of GUI

---

### PORT_PRESETS
Dictionary of pre-configured port ranges for quick selection.

**Structure**:
```python
{
    "Web Services": {
        "ports": ["80", "443"],
        "start": "80",
        "end": "443",
        "description": "HTTP and HTTPS ports"
    },
    # ... more presets
}
```

**Usage**: Populates Port Type dropdown and fills port range inputs

---

### PORT_SERVICE_MAP
Dictionary mapping port numbers to service names.

**Generation**:
- Built automatically from `COMMON_PORTS_BY_CATEGORY`
- Handles compound ports (e.g., "20/21" → maps both 20 and 21)
- Handles port ranges (e.g., "67, 68" → maps both)

**Usage**: Display service name in results table

**Example**:
```python
PORT_SERVICE_MAP[80]    # "HTTP"
PORT_SERVICE_MAP[443]   # "HTTPS"
PORT_SERVICE_MAP[22]    # "SSH/SCP"
PORT_SERVICE_MAP[9999]  # KeyError (unknown port)
```

---

### Theme Colors
```python
BG_COLOR = "#0f172a"        # Dark slate background
CARD_COLOR = "#1e293b"      # Card/panel background
TEXT_MAIN = "#e2e8f0"       # Main text color
ACCENT_COLOR = "#38bdf8"    # Sky blue accent
INPUT_BG = "#334155"        # Input field background
SUCCESS_COLOR = "#22c55e"   # Green for valid/open
ERROR_COLOR = "#ef4444"     # Red for errors
DETAIL_COLOR = "#94a3b8"    # Gray for closed ports
```

---

## Technical Implementation Notes

### Socket Connection Process
1. Create TCP socket: `socket.socket(socket.AF_INET, socket.SOCK_STREAM)`
2. Set timeout: `sock.settimeout(0.5)`
3. Attempt connection: `result = sock.connect_ex((host, port))`
4. Check result: `result == 0` means port is OPEN
5. Close socket: `sock.close()`

### Threading Architecture
- **Main Thread**: Handles GUI updates and user interaction
- **Daemon Thread**: Executes `perform_scan()` for non-blocking operation
- **Communication**: Uses instance variables (`is_scanning`, `scan_cancelled`)
- **UI Updates**: Treeview insertions are thread-safe in Tkinter

### Grid Layout for Table
- Uses `grid()` instead of `pack()` for precise column alignment
- Column weights control proportional widths:
  ```python
  table_frame.grid_columnconfigure(0, weight=2)  # Category
  table_frame.grid_columnconfigure(1, weight=1)  # Port
  table_frame.grid_columnconfigure(2, weight=6)  # Service
  ```
- `sticky="ew"` makes cells expand to fill column width
- Enables perfect center alignment

### Real-Time Validation
- **Event**: `<KeyRelease>` binding on Entry widgets
- **Trigger**: Fires validation function on every keystroke
- **Feedback**: Updates status labels immediately
- **Colors**: Green (✓) for valid, Red (⚠) for invalid

---

## Error Handling

### Network Errors
- `socket.gaierror`: DNS resolution failure → "Host unreachable"
- `socket.timeout`: Connection timeout → Port marked CLOSED
- `socket.error`: General socket error → Port marked CLOSED

### Validation Errors
- Empty input → "Host/Port required"
- Non-numeric ports → "Must be a number"
- Out of range → "Must be within 1-65535"
- Reversed range → "Start must be less than end"
- Large range → "Too many ports (max 10,000)"

### GUI Error Handling
- Exceptions in scan thread → Caught and displayed in error dialog
- Invalid state transitions → Prevented by button state management
- Multiple scan attempts → Blocked with warning message

---

## Performance Considerations

### Timeout Configuration
- Default: 0.5 seconds per port
- Trade-off: Lower timeout = faster scans, higher false negatives
- For reliable results: Use 1.0 second timeout
- For quick surveys: Use 0.3 second timeout

### Port Range Limits
- Maximum 10,000 ports per scan enforced
- Example: Scanning 1-65535 would take ~9 hours at 0.5s/port
- Recommended: Use port presets for targeted scanning

### Memory Usage
- Results stored in Treeview widget (in-memory)
- Each result: ~100 bytes (service name + port + status)
- 10,000 results ≈ 1 MB memory usage

---

## Version History

### Version 1.0 - February 9, 2026
**Initial Release**:
- Socket-based TCP port scanning
- Real-time input validation
- 12 port type presets
- Common ports reference table (25+ entries)
- Grid-based results display
- Threading for responsive UI
- Stop/clear/resume functionality
- Service name mapping
- Professional dark theme

---

## Future Enhancements

**Potential Improvements**:
- UDP port scanning support
- Port scan history/logging
- Export results to CSV/JSON
- Web-host scanning
- Scan templates (save custom port ranges)
