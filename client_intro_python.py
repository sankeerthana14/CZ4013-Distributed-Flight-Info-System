#CLIENT

#Import
import socket
import sys
import marshalling.marshalling_logic as MARSHALLING

UDP_IP_ADDRESS = "127.0.0.1"
UDP_PORT_NUM = 6789

encoded_client_message = MARSHALLING.marshall(sys.argv[1])

#Create a UDP socket at a client side
UDP_client_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

#Send to server using created UDP socket
UDP_client_socket.sendto(encoded_client_message, (UDP_IP_ADDRESS, UDP_PORT_NUM))

#Listening from Server
print("INFO: Receiving message from server...")
message_from_server = UDP_client_socket.recvfrom(1024)

print(f"Message from Server:\n{MARSHALLING.unmarshall(message_from_server[0])}")