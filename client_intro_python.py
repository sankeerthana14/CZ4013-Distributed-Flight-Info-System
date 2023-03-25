#CLIENT

#Import
import socket
import sys

UDP_IP_ADDRESS = "127.0.0.1"
UDP_PORT_NUM = 6789


# get client_message from command line
# Example: python3 client_intro_python.py "query_flight_details,2"
# Example: python3 client_intro_python.py "query_flight,Italy,Australia"
# Example: python3 client_intro_python.py "reserve_seats,2,3"
# Example: python3 client_intro_python.py "query_flight_from_source,Italy"
# Example: python3 client_intro_python.py "add_delay,2,5"
# Example: python3 client_intro_python.py "monitor_interval,1,2"

client_message = sys.argv[1]

encoded_client_message = str.encode(client_message)

#Create a UDP socket at a client side
UDP_client_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

#Send to server using created UDP socket
UDP_client_socket.sendto(encoded_client_message, (UDP_IP_ADDRESS, UDP_PORT_NUM))

#Listening from Server
print("INFO: Receiving message from server...")
message_from_server = UDP_client_socket.recvfrom(1024)

print(f"Message from Server:\n\n{message_from_server[0].decode()}")