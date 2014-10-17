import os
import json

def application(env, start_response):
    with open('buoy.json') as f:
        config = json.load(f)

    is_xml = False
    is_json = False

    path = env['PATH_INFO']
    if path.endswith('.json'):
        is_json = True
        start_response('200 OK', [('Content-Type','application/json')])
    elif path.endswith('.xml'):
        is_xml = True
        start_response('200 OK', [('Content-Type','application/xml')])
    else:
        start_response('404 NOT FOUND')


    buoy_dir = config['buoy_dir'] 

    if is_json:
        buoy_collection = []
        for buoy_file_name in os.listdir(buoy_dir):
            if buoy_file_name.endswith('.json'):
                with open(os.path.join(buoy_dir, buoy_file_name)) as f:
                    buoy_collection.append(json.load(f))

        return json.dumps(buoy_collection, sort_keys=True, indent=4) 
    elif is_xml:
        buoys = "" 
        
        for buoy_file_name in os.listdir(buoy_dir):
            if buoy_file_name.endswith('.xml'):
                with open(os.path.join(buoy_dir, buoy_file_name)) as f:
                    xml = f.read()
                    buoys += xml

        return "<buoys>%s</buoys>" % buoys 

