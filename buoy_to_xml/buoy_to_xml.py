import os
import zmq
import json
import logging
import xml.etree.ElementTree as ET

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

def dict_to_xml(d, root):

    for key in d:
        node = ET.Element(key)
        val = d[key]
        if isinstance(val, dict):
            root.append(dict_to_xml(val, node))
        else:
            node.text = str(val)
            root.append(node) 

    return root

buoy_data_folder = os.path.join(os.environ['RESOURCE_DIR'], 'buoy')

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect ('tcp://broker:5557')
socket.setsockopt(zmq.SUBSCRIBE, '')

while True:
    surf_data = socket.recv_json()
    logging.info("Recieved data: %s" % surf_data)
    buoy_file_name = "%s.xml" % str(surf_data['id'])
    with open(os.path.join(buoy_data_folder, buoy_file_name), 'wb') as f:
        xml = dict_to_xml(surf_data, ET.Element('buoy'))
        f.write(ET.tostring(xml))
