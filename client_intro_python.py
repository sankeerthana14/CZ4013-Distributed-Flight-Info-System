#CLIENT

#Import
import socket

client_message = "Hello UDP Server!"
encoded_client_message = str.encode(client_message)

SERVER_ADDRESS_PORT = ("127.0.0.1", 20001)
BUFFER_SIZE = 1024

#Create a UDP socket at a client side
UDP_client_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

#Send to server using created UDP socket
UDP_client_socket.sendto(encoded_client_message, SERVER_ADDRESS_PORT)

print("INFO: Receiving message from server...")
message_from_server = UDP_client_socket.recvfrom(BUFFER_SIZE)

print(f"Message from Server: {message_from_server}")