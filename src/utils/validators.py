# src/utils/validators.py

def validate_port_range(start_str, end_str):
    """
    Validate port range input
    
    Requirements:
    - Both values must be integers
    - Starting port < Ending port
    - Range must be within 1-65535
    - No letters or special symbols
    
    """
    try:
        # Check if both are numeric (no letters or special symbols)
        if not start_str.isdigit():
            return False, None, None, "Start port must be a number (no letters or symbols)"
        
        if not end_str.isdigit():
            return False, None, None, "End port must be a number (no letters or symbols)"
        
        start_port = int(start_str)
        end_port = int(end_str)
        
        # Validate port range (1-65535)
        if start_port < 1:
            return False, None, None, "Start port must be at least 1"
        
        if start_port > 65535:
            return False, None, None, "Start port must not exceed 65535"
        
        if end_port < 1:
            return False, None, None, "End port must be at least 1"
        
        if end_port > 65535:
            return False, None, None, "End port must not exceed 65535"
        
        # Validate start < end
        if start_port > end_port:
            return False, None, None, "Start port must be less than end port"
        
        # Validate start == end is acceptable (scanning single port)
        if start_port == end_port:
            return True, start_port, end_port, None
        
        # Warn about very large ranges (but still allow them)
        if (end_port - start_port) > 10000:
            return False, None, None, "Port range too large (max 10,000 ports for performance)"
        
        return True, start_port, end_port, None
    
    except ValueError:
        return False, None, None, "Invalid port number format"
    except Exception as e:
        return False, None, None, f"Validation error: {str(e)}"