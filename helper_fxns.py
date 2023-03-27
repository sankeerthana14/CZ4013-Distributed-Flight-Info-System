#\HELPER FUNCTIONS

from datetime import datetime
from marshalling.marshalling_logic import marshall

"""
Function to handle 24 hour time with delays - NEED TO WORK ON THIS!!
"""
def handle_time(delayed_time):
    # Parse the time string into a datetime object
    t = datetime.strptime(delayed_time, '%I')
    # Format the datetime object into a 24-hour time string2
    return t.strftime('%H')

"""
Function to acknowledge received message by sending ACK,timestamp
"""
def acknowledge_request(request):
    request_id = request.split(",")[-1]
    byte_message, request_id = marshall(f"ACK", request_id)
    return byte_message

        

