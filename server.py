#SOCKET PROGRAMMING

#Imports
import socket
import flights_db as FLIGHTS
import time
import marshalling.marshalling_logic as MARSHALLING
from helper_fxns import acknowledge_request
import threading
from datetime import datetime, timedelta
import sys

#FLAG
FILTER_DUPLICATES = sys.argv[1]

#initialising the IP address, port number and buffer size
UDP_IP_ADDRESS = "127.0.0.1"
UDP_PORT_NUM = 6789

# query flight identifier given source and destination by client and return flight id(s)
def query_flight(source, destination):
    print(f"INFO: Querying flight from {source} to {destination}...")
    #list of flight ids that match
    flight_id = []
    for flight in FLIGHTS.flights:
        if FLIGHTS.flights[flight]["source"] == source and FLIGHTS.flights[flight]["destination"] == destination:
            flight_id.append(flight)
    return flight_id

# query the departure time, airfare and seatavailability by specifying the flight identifier, else error
def query_flight_details(flight_id):
    flight_id = int(flight_id)
    print(f"INFO: Querying flight details for flight {flight_id}...")
    if flight_id in FLIGHTS.flights:
        return FLIGHTS.flights[flight_id]
    else:
        return "ERROR: Flight does not exist"

# reserve seats for a flight by specifying the flight identifier and number of seats to reserve, else error
def reserve_seats(flight_id, seats):
    print(f"INFO: Reserving {seats} seats for flight {flight_id}...")
    flight_id = int(flight_id)
    seats = int(seats)
    if flight_id in FLIGHTS.flights:
        if FLIGHTS.flights[flight_id]["seats_available"] >= seats:
            FLIGHTS.flights[flight_id]["seats_available"] -= seats
            print(f"INFO: Seats remaining for flight {flight_id}: {FLIGHTS.flights[flight_id]['seats_available']}")
            return f"{seats} Seats successfully reserved for Flight {flight_id}!"
        else:
            return "ERROR: Not enough seats available"
    else:
        return "ERROR: Flight does not exist"
    
#announcing delay of departure of flight
def add_delay(flight_id, delay):
    flight_id = int(flight_id)
    delay = int(delay)
    print(f"INFO: Adding {delay} hours delay to flight {flight_id}.")
    if flight_id in FLIGHTS.flights:
        str_time = f"{FLIGHTS.flights[flight_id]['departure_time']['hour']}:{FLIGHTS.flights[flight_id]['departure_time']['minute']}"
        dt_time = datetime.strptime(str_time, '%H:%M')
        delayed_time = (dt_time + timedelta(hours=delay)).strftime('%H:%M')
        list_time = str(delayed_time).split(":")

        FLIGHTS.flights[flight_id]['departure_time']['hour'] = list_time[0]
        FLIGHTS.flights[flight_id]['departure_time']['minute'] = list_time[-1]

        text = f"Flight {flight_id} delayed by {delay} hours, New Departure Time: {delayed_time}"
        return text
    else:
        return "ERROR: Flight does not exist"
    

def query_flight_from_source(source):
    print(f"INFO: Querying flights from {source}...")
    flight_ids = []
    for flight in FLIGHTS.flights:
        if FLIGHTS.flights[flight]["source"] == source:
            flight_ids.append(flight)
    return flight_ids

#track the seat availability
def monitor_interval(interval, flight_id):
    print(f"INFO: Monitoring flight {flight_id} for {interval} minutes...")
    interval = int(interval)
    flight_id = int(flight_id)

    org_seats = FLIGHTS.flights[flight_id]['seats_available']

    # Define a thread function to run the loop
    def thread_func():
        nonlocal interval
        nonlocal org_seats

        old_address = address

        while interval:
            # Displaying the time
            mins, secs = divmod(interval, 1)
            current_seats = FLIGHTS.flights[flight_id]['seats_available']

            # When there is a change in the seats
            print(f"{old_address} checking for change in seat availability...")
            if current_seats != org_seats:
                print("SEATS CHANGED!")
                text = f"INFO: Change in Seat Availability from {org_seats} to {current_seats}!"
                text, request_id = MARSHALLING.marshall(text)
                print("Notifying client: ", old_address)
                UDP_server_socket.sendto(text, old_address)
                org_seats = current_seats
            time.sleep(1)
            interval -= 1

        print(f"INFO: Final Seat Availability: {current_seats}")

    # Start a new thread to run the loop
    print("INFO: Starting thread...")
    thread = threading.Thread(target=thread_func)
    thread.start()



#Create a datagram socket
UDP_server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

#Binding to the address and IP
UDP_server_socket.bind((UDP_IP_ADDRESS, UDP_PORT_NUM))

print("INFO: UDP Server up and listening...")

#Dictionary to keep track of reuests
processed_requests = set()

#Listen for incoming datagrams
while True:
    byte_address_pair = UDP_server_socket.recvfrom(1024)
    message, address = byte_address_pair[0], byte_address_pair[1]  #message is in bytes
    
    print("START\nReceived message from {}".format(address))

    message = MARSHALLING.unmarshall(message) #unmarshall it to receive string


    # send acknowledgement to client
    ack = acknowledge_request(message)
    UDP_server_socket.sendto(ack, address)
    print("Sent acknowledgement to client {}".format(address))

    message = message.split(",")

    print(f"MESSAGE: {message}, ADDRESS: {address}")

    unique_code = message[-1]

    #checking for duplicate request
    if FILTER_DUPLICATES == "at-most-once":
        if unique_code not in processed_requests:
            processed_requests.add(unique_code)
        else:
            print(f"LOG: Duplicated Request {unique_code}")
            continue

    if message[0] == "query_flight":
        encoded_server_message, request_id = MARSHALLING.marshall(query_flight(message[1], message[2]))
    elif message[0] == "query_flight_details":
        encoded_server_message, request_id = MARSHALLING.marshall(query_flight_details(message[1]))
    elif message[0] == "reserve_seats":
        encoded_server_message, request_id = MARSHALLING.marshall(reserve_seats(message[1], message[2]))
    elif message[0] == "add_delay":
        encoded_server_message, request_id = MARSHALLING.marshall(add_delay(message[1], message[2]))
    elif message[0] == "query_flight_from_source":
        encoded_server_message, request_id = MARSHALLING.marshall(query_flight_from_source(message[1]))
    elif message[0] == "monitor_interval":
        monitor_interval(message[1], message[2])
        encoded_server_message, request_id = MARSHALLING.marshall("Monitoring started")
    else:
        encoded_server_message, request_id = MARSHALLING.marshall("ERROR: Invalid request")

    #sending a reply to the client
    print("Sending to {}: {}\nEND\n".format(address, encoded_server_message))
    UDP_server_socket.sendto(encoded_server_message, address)