import zmq
import logging
from pymongo import MongoClient

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect ('tcp://localhost:5557')
socket.setsockopt(zmq.SUBSCRIBE, '')

client = MongoClient('localhost', 27017)
db = client.surf_data
coll = db.buoy

while True:
    surf_data = socket.recv_json()
    logging.info("Recieved data: %s" % surf_data)
    coll.insert(surf_data)

