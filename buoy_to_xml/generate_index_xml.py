import os
import xml.etree.ElementTree as ET

buoy_data_folder = os.path.join(os.environ['RESOURCE_DIR'], 'buoy')
buoy_file_name =  os.path.join(os.environ['RESOURCE_DIR'], 'buoy.xml')
web_host = os.environ['WEB_HOST']

def generate_entry(buoy_id):
    return { 'id': buoy_id, 'link': 'http://' + web_host + '/api/buoy/' + buoy_id + '.json' }

def dict_to_xml(d):
    
    root = ET.Element('buoy')
    for key in d:
        node = ET.Element(key)
        val = d[key]
        if isinstance(val, dict):
            root.append(dict_to_xml(val, node))
        else:
            node.text = str(val)
            root.append(node) 

    return root

def final_xml(buoys_xml):
    root = ET.Element('buoys')
    for b in buoys_xml:
        root.append(b)

    return root

buoy_ids = [f.split('.')[0] for f in os.listdir(buoy_data_folder) if f.endswith('.json')]
buoys = map(generate_entry, buoy_ids)
buoys_xml = [dict_to_xml(b) for b in buoys]


with open(buoy_file_name, 'wb') as f:
    f.write(ET.tostring(final_xml(buoys_xml)))
