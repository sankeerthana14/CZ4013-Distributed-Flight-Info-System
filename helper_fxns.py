#\HELPER FUNCTIONS

from datetime import datetime
from marshalling.marshalling_logic import marshall

"""
Function to acknowledge received message by sending ACK,timestamp
"""
def acknowledge_request(request):
    request_id = request.split(",")[-1]
    byte_message, request_id = marshall(f"ACK", request_id)
    return byte_message

        

