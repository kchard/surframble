import feedparser
from HTMLParser import HTMLParser
import time
import json
import zmq
import logging

def iso_date_str(date):
    return time.strftime('%Y-%m-%dT%H:%M:%S %Z', date)

class NdbcHtmlParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.surf_data = {}
        self.in_strong = False
        self.found_val = False
        self.curr_key = None
    
    def handle_starttag(self, tag, attrs):
        if "strong" == tag:
            self.in_strong = True
            self.found_val = False

    def handle_endtag(self, tag):
        if "strong" == tag:
            self.in_strong = False 

    def handle_data(self, data):
        if self.in_strong:
            try:
                date = time.strptime(data, '%B %d, %Y %I:%M %p %Z')
                self.surf_data['time'] = iso_date_str(date)
                return
            except Exception as e: 
                pass

            self.curr_key = data.lower().replace(' ', '_').replace(':', '') 
        else:
            if not self.found_val:
                if self.curr_key == 'dominant_wave_period':
                    self.surf_data['period'] = float(data.strip().split()[0])
                elif self.curr_key == 'significant_wave_height':
                    self.surf_data['height'] = float(data.strip().split()[0])
                elif self.curr_key == 'location':
                    location = data.strip().split()
                    self.surf_data['location'] = { 'latitude': location[0], 'longitude': location[1] } 
                elif self.curr_key == "mean_wave_direction":
                    self.surf_data['direction'] = int(data.split()[1].replace('(', ''))
                self.found_val = True

def html_from_rss(buoy_id):
    url = 'http://www.ndbc.noaa.gov/data/latest_obs/%s.rss' % buoy_id
    feed = feedparser.parse(url)
    return feed['items'][0]['summary_detail']['value']

def surf_data_from_html(html):
    parser = NdbcHtmlParser()
    parser.feed(html)
    return parser.surf_data

def load_buoys():
    with open('buoys.json') as f:
        buoys = json.load(f)
    return buoys

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

context = zmq.Context()
publisher = context.socket(zmq.PUB)
publisher.connect('tcp://localhost:5556')

buoys = load_buoys()
for buoy_id in buoys:
    surf_data = surf_data_from_html(html_from_rss(buoy_id))
    surf_data['id'] = buoy_id
    surf_data['location']['city'] = buoys[buoy_id]['city']
    surf_data['location']['state'] = buoys[buoy_id]['state']

    logging.info("Sending data: %s" % surf_data)
    publisher.send_json(surf_data)
