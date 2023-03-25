#\HELPER FUNCTIONS

from datetime import datetime

#Function Legend for Printing Results
"""
Function name and ID mapping:
    • 1 - query_flight(source, destination)
    • 2 - query_flight_details(flight_id)
    • 3 - add_delay(flight_id, delay)
    • 4 - query_flight_from_source(source)
"""

"""
Function 1 : query_flight(source, destination)
    • Input: a list of flight_ids that match the source and destination
    • Output: Text
"""
def function_1(flight_id, source, destination):
    text = f"Flights available from {source} to {destination}:\n-----------------------------\n"

    for flight in flight_id:
        text += f'Flight ID: {flight}\n'

    return text

"""
Function 2 : query_flight_details(flight_id)
    • Input: dictionary with details - flight_id
    • Output: Text
"""
def function_2(dict_flights, flight_id):
    text = f"Flight details are as follows:\n-------------------------------\n"
    
    details = f"Flight ID: {flight_id}\nFrom: {dict_flights['source']}\nTo: {dict_flights['destination']}\nDeparture Time: {str(dict_flights['departure_time']['hour'])+str(dict_flights['departure_time']['minute'])}\nAirfare: {dict_flights['airfare']}\nSeats Availability: {dict_flights['seats_available']}"
    text += details

    return text

"""
Function to handle 24 hour time with delays - NEED TO WORK ON THIS!!
"""
def handle_time(delayed_time):
    # Parse the time string into a datetime object
    t = datetime.strptime(delayed_time, '%I')
    # Format the datetime object into a 24-hour time string
    return t.strftime('%H')

        

