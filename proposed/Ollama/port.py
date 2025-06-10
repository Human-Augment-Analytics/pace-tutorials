#This function looks for the first free port and prints its number
import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(('', 0))  # Bind to the first free port detected
    port = s.getsockname()[1]
    print(f"Available port: {port}")
