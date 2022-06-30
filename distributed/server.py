import signal
import zmq

import settings
from utils.udplib import UDP
from utils.ip import give_ip

class Server:

    def __init__(self):
        self.address = give_ip()

    def start(self):
        ctx = zmq.Context()

        # Socket input
        input = ctx.socket(zmq.REP)
        input.bind("tcp://%s:%d" % (self.address, settings.CLI_SERV_PORT_NUMBER))

        # ping port
        udp = UDP(settings.PING_PORT_NUMBER,self.address)

        # poll sockets
        poller = zmq.Poller()
        poller.register(udp.handle, zmq.POLLIN)
        poller.register(input,zmq.POLLIN)

        while True:
            events = dict(poller.poll())
            
            # ping response
            if udp.handle.fileno() in events:
                rec,address = udp.recv(settings.PING_MSG_SIZE)
                if(settings.DEBUG_MODE):
                    print("Server %s Received ping message: %s"  % (self.address, rec))
                udp.handle.sendto(b's',address)
            # client-server communication
            elif events.get(input) == zmq.POLLIN:
                input.send(b'OK')
                if(settings.DEBUG_MODE):
                    print("Recieved message by port: %d", settings.COM_PORT_NUMBER)
