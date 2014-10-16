import os
import json

def application(env, start_response):
    with open('buoy.json') as f:
        config = json.load(f)

    start_response('200 OK', [('Content-Type','application/json')])

    buoy_dir = config['buoy_dir'] 
    buoy_collection = []
    for buoy_file_name in os.listdir(buoy_dir):
        with open(os.path.join(buoy_dir, buoy_file_name)) as f:
            buoy_collection.append(json.load(f))

    return json.dumps(buoy_collection, sort_keys=True, indent=4) 
