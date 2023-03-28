# CZ4013-Distributed-Flight-Info-System

Steps to run:

First start the server.

    python3 server.py
 Then run the client with any one of the request message.
 

    python3 client.py query_flight,Canada,France

    python3 client.py query_flight_details,2
    
    python3 client.py reserve_seats,2,3
    
    python3 client.py add_delay,2,10
    
    python3 client.py query_flight_from_source,Canada
    
    python3 client.py monitor_interval,60,2

