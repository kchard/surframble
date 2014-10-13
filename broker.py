import zmq

xsub_url = 'tcp://*:5556'
xpub_url = 'tcp://*:5557'

ctx = zmq.Context()

xsub = ctx.socket(zmq.XSUB)
xsub.bind(xsub_url)

xpub = ctx.socket(zmq.XPUB)
xpub.bind(xpub_url)

zmq.proxy(xpub, xsub)
