import signal
import zmq
from argparse import ArgumentParser
from udplib import UDP

PING_PORT_NUMBER = 2525
PING_MSG_SIZE    = 1

COM_PORT_NUMBER = 2526

parser = ArgumentParser()

parser.add_argument(
    '--ip', type=str, required=True,
    help='Interface IP address'
)

args = parser.parse_args()

ctx = zmq.Context()

# Socket input
input = ctx.socket(zmq.REP)
input.bind("tcp://"+args.ip+":2526")

# ping port
udp = UDP(PING_PORT_NUMBER,args.ip)

poller = zmq.Poller()
poller.register(udp.handle, zmq.POLLIN)
poller.register(input,zmq.POLLIN)

while True:
    try:
        events = dict(poller.poll())
    except KeyboardInterrupt or signal.SIGTERM:
        print("interrupted")
        break
    
    if udp.handle.fileno() in events:
        rec,address = udp.recv(PING_MSG_SIZE)
        print("Server %s Received ping message: %s"  % (args.ip,str(rec)))
        udp.handle.sendto(b's',address)
    elif events.get(input) == zmq.POLLIN:
        input.send(b'OK')
        print("Recieved message by port: %d", COM_PORT_NUMBER)
