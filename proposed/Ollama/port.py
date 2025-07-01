import socket

# Scan ports 49152 to 65536 (ephemeral ports)
def find_first_available_port(start=49152, end=65535):
    for port in range(start, end + 1):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.1)
            
            if s.connect_ex(('127.0.0.1', port)) != 0:
                return port
            
    # No available port found
    return None 

port = find_first_available_port()
if port:
    print(f"First available ephemeral port: {port}")
else:
    print("No available ports found in the ephemeral port range.")

