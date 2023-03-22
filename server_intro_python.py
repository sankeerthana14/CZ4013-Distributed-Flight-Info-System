#SOCKET PROGRAMMING

#Imports
import socket

#initialising the IP address, port number and buffer size
UDP_IP_ADDRESS = "127.0.0.1"
UDP_PORT_NUM = 6789

flights = {
    1: {
        "source": "USA",
        "destination": "Japan",
        "departure_time": {
            "hour": 8,
            "minute": 30
        },
        "airfare": 1200.00,
        "seats_available": 50
    },
    2: {
        "source": "Canada",
        "destination": "France",
        "departure_time": {
            "hour": 12,
            "minute": 45
        },
        "airfare": 950.00,
        "seats_available": 30
    },
    3: {
        "source": "Brazil",
        "destination": "Spain",
        "departure_time": {
            "hour": 10,
            "minute": 15
        },
        "airfare": 750.00,
        "seats_available": 20
    },
    4: {
        "source": "Australia",
        "destination": "Mexico",
        "departure_time": {
            "hour": 14,
            "minute": 0
        },
        "airfare": 1100.00,
        "seats_available": 40
    },
    5: {
        "source": "Germany",
        "destination": "China",
        "departure_time": {
            "hour": 11,
            "minute": 30
        },
        "airfare": 900.00,
        "seats_available": 25
    },
    6: {
        "source": "Italy",
        "destination": "Australia",
        "departure_time": {
            "hour": 9,
            "minute": 0
        },
        "airfare": 1300.00,
        "seats_available": 35
    },
    7: {
        "source": "Mexico",
        "destination": "South Korea",
        "departure_time": {
            "hour": 13,
            "minute": 45
        },
        "airfare": 850.00,
        "seats_available": 10
    },
    8: {
        "source": "Spain",
        "destination": "USA",
        "departure_time": {
            "hour": 16,
            "minute": 30
        },
        "airfare": 1200.00,
        "seats_available": 45
    },
    9: {
        "source": "China",
        "destination": "Canada",
        "departure_time": {
            "hour": 17,
            "minute": 15
        },
        "airfare": 1100.00,
        "seats_available": 30
    },
    10: {
        "source": "France",
        "destination": "Brazil",
        "departure_time": {
            "hour": 18,
            "minute": 0
        },
        "airfare": 750.00,
        "seats_available": 20
    }
}

# query flight identifier given source and destination by client and return flight id(s)
def query_flight(source, destination):
    print(f"INFO: Querying flight from {source} to {destination}...")
    flight_id = []
    for flight in flights:
        if flights[flight]["source"] == source and flights[flight]["destination"] == destination:
            flight_id.append(flight)
    return flight_id

# query the departure time, airfare and seatavailability by specifying the flight identifier, else error
def query_flight_details(flight_id):
    print(f"INFO: Querying flight details for flight {flight_id}...")
    if flight_id in flights:
        return flights[flight_id]
    else:
        return "Flight does not exist"

# reserve seats for a flight by specifying the flight identifier and number of seats to reserve, else error
def reserve_seats(flight_id, seats):
    print(f"INFO: Reserving {seats} seats for flight {flight_id}...")
    if flight_id in flights:
        if flights[flight_id]["seats_available"] >= seats:
            flights[flight_id]["seats_available"] -= seats
            print(f"INFO: Seats available for flight {flight_id}: {flights[flight_id]['seats_available']}")
            return "Seats reserved"
        else:
            return "Not enough seats available"
    else:
        return "Flight does not exist"
    
def add_delay(flight_id, delay):
    print(f"INFO: Adding {delay} hours delay to flight {flight_id}...")
    if flight_id in flights:
        flights[flight_id]["departure_time"]["hour"] += delay
        print(f"INFO: Flight {flight_id} delayed by {delay} hours")
        return "Flight delayed"
    else:
        return "Flight does not exist"
    

def query_flight_from_source(source):
    print(f"INFO: Querying flights from {source}...")
    flight_id = []
    for flight in flights:
        if flights[flight]["source"] == source:
            flight_id.append(flight)
    return flight_id


#data to send to client
server_message = "Hello UDP Client!"

#encoded data to send to the client
encoded_server_message = str.encode(server_message)

#Create a datagram socket
UDP_server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

#Binding to the address and IP
UDP_server_socket.bind((UDP_IP_ADDRESS, UDP_PORT_NUM))

print("INFO: UDP Server up and listening...")

#Listen for incoming datagrams
while True:
    byte_address_pair = UDP_server_socket.recvfrom(1024)
    print("INFO: Received from client!")

    message, address = byte_address_pair[0], byte_address_pair[1]

    print("{}: {}".format(address,message))

    message = message.decode().split(",")
    if message[0] == "query_flight":
        encoded_server_message = str.encode(str(query_flight(message[1], message[2])))
    elif message[0] == "query_flight_details":
        encoded_server_message = str.encode(str(query_flight_details(int(message[1]))))
    elif message[0] == "reserve_seats":
        encoded_server_message = str.encode(str(reserve_seats(int(message[1]), int(message[2]))))
    elif message[0] == "add_delay":
        encoded_server_message = str.encode(str(add_delay(int(message[1]), int(message[2]))))
    elif message[0] == "query_flight_from_source":
        encoded_server_message = str.encode(str(query_flight_from_source(message[1])))
    else:
        encoded_server_message = str.encode("Invalid request")

    #sending a reply to the client
    UDP_server_socket.sendto(encoded_server_message, address)