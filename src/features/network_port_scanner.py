import socket
from typing import List, Tuple, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed


def probe_port(host: str, port: int, timeout: float = 1.2) -> Tuple[int, bool]:
    """
    Returns (port, is_open)
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))
            return port, result == 0
    except (socket.gaierror, socket.error, OverflowError, ValueError):
        return port, False


def scan_ports(
    host: str,
    ports: List[int],
    timeout: float = 1.2,
    max_workers: int = 50
) -> List[Tuple[int, bool]]:
    """
    Returns list of (port, is_open) sorted by port number
    """
    results = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_port = {
            executor.submit(probe_port, host, port, timeout): port
            for port in ports
        }

        for future in as_completed(future_to_port):
            try:
                port, opened = future.result()
                results.append((port, opened))
            except Exception:
                # shouldn't normally happen, but safety
                port = future_to_port[future]
                results.append((port, False))

    return sorted(results)


def get_common_ports() -> List[int]:
    """Example helper — can be extended / loaded from file later"""
    return [21, 22, 23, 25, 53, 80, 110, 135, 139, 143, 443, 445,
            1433, 3306, 3389, 5432, 5900, 8080, 8443]


def resolve_host(host: str) -> Optional[str]:
    """Try to resolve hostname → IP (for display)"""
    try:
        return socket.gethostbyname(host)
    except socket.gaierror:
        return None