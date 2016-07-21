import os
import zmq
import json
import logging

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

buoy_data_folder = '/buoy'
if not os.path.exists(buoy_data_folder):
    logging.info("creating buoy folder")
    os.makedirs(buoy_data_folder)

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect ('tcp://broker:5557')
socket.setsockopt(zmq.SUBSCRIBE, '')

logging.info("Waiting for data")
while True:
    surf_data = socket.recv_json()
    logging.info("Recieved data: %s" % surf_data)
    buoy_file_name = "%s.json" % str(surf_data['id'])
    with open(os.path.join(buoy_data_folder, buoy_file_name), 'wb') as f:
        json.dump(surf_data, f, sort_keys=True, indent=4)

