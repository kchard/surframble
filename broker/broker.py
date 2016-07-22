import zmq
import logging

xsub_url = 'tcp://*:5556'
xpub_url = 'tcp://*:5557'

ctx = zmq.Context()

xsub = ctx.socket(zmq.XSUB)
xsub.bind(xsub_url)

xpub = ctx.socket(zmq.XPUB)
xpub.bind(xpub_url)

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
logging.info("Starting broker")
try:
    zmq.proxy(xpub, xsub) #zmq 3.X 
except: 
    zmq.device(zmq.FORWARDER, xpub, xsub) #xmq 2.X
