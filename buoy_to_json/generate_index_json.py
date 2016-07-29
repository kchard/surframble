import os
import json

buoy_data_folder = os.path.join(os.environ['RESOURCE_DIR'], 'buoy')
buoy_file_name =  os.path.join(os.environ['RESOURCE_DIR'], 'buoy.json')
web_host = os.environ['WEB_HOST']

def generate_entry(buoy_id):
    return { 'id': buoy_id, 'link': 'http://' + web_host + '/api/buoy/' + buoy_id + '.json' }

buoy_ids = [f.split('.')[0] for f in os.listdir(buoy_data_folder) if f.endswith('.json')]
buoys = map(generate_entry, buoy_ids)

with open(buoy_file_name, 'wb') as f:
    json.dump(buoys, f, sort_keys=True, indent=4)
