import signal
import zmq
from argparse import ArgumentParser
from udplib import UDP
import settings

parser = ArgumentParser()

parser.add_argument(
    '--ip', type=str, required=True,
    help='Interface IP address'
)

args = parser.parse_args()

ctx = zmq.Context()

# Socket input
input = ctx.socket(zmq.REP)
input.bind("tcp://%s:%d" % (args.ip, settings.CLI_SERV_PORT_NUMBER))

# ping port
udp = UDP(settings.PING_PORT_NUMBER,args.ip)

# poll sockets
poller = zmq.Poller()
poller.register(udp.handle, zmq.POLLIN)
poller.register(input,zmq.POLLIN)

while True:
    try:
        events = dict(poller.poll())
    except KeyboardInterrupt or signal.SIGTERM:
        print("interrupted")
        break
    
    # ping response
    if udp.handle.fileno() in events:
        rec,address = udp.recv(settings.PING_MSG_SIZE)
        if(settings.DEBUG_MODE):
            print("Server %s Received ping message: %s"  % (args.ip,str(rec)))
        udp.handle.sendto(b's',address)
    # client-server communication
    elif events.get(input) == zmq.POLLIN:
        input.send(b'OK')
        if(settings.DEBUG_MODE):
            print("Recieved message by port: %d", settings.COM_PORT_NUMBER)
