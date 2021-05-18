#!/usr/bin/env python

from pymavlink import mavutil
import time
import sys

# Start a connection listening to a UDP port
the_connection = mavutil.mavlink_connection('tcp:localhost:5763')

# Wait for the first heartbeat
#   This sets the system and component ID of remote system for the link
the_connection.wait_heartbeat()
print("Heartbeat from system (system %u component %u)" % (the_connection.target_system, the_connection.target_system))

# Wait for the vehicle data
time.sleep(1)

# Request all parameters
the_connection.mav.param_request_list_send(
    the_connection.target_system, the_connection.target_component
)
while True:
    time.sleep(0.05)
    try:
        message = the_connection.recv_match(type='PARAM_VALUE', blocking=True).to_dict()
        print('PARAM: %s\tvalue: %d' % (message['param_id'],
                                       message['param_value']))
    except Exception as error:
        print(error)
        sys.exit(0)
