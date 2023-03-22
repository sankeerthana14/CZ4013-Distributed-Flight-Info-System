#SOCKET PROGRAMMING

#Imports
import socket

#initialising the IP address, port number and buffer size
LOCAL_IP = "127.0.0.1"
LOCAL_PORT = 20001
BUFFER_SIZE = 1024

#data to send to client
server_message = "Hello UDP Client!"

#encoded data to send to the client
encoded_server_message = str.encode(server_message)

#Create a datagram socket
UDP_server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

#Binding to the address and IP
UDP_server_socket.bind((LOCAL_IP, LOCAL_PORT))

print("INFO: UDP Server up and listening...")

#Listen for incoming datagrams
while True:
    byte_address_pair = UDP_server_socket.recvfrom(BUFFER_SIZE)
    print("INFO: Received from client!")

    message, address = byte_address_pair[0], byte_address_pair[1]

    message_from_client = "Message from Client: {}".format(message)
    client_IP = "Client IP Address: {}".format(address)

    print(message_from_client)
    print(client_IP)

    #sending a reply to the client
    UDP_server_socket.sendto(encoded_server_message, address)

    break