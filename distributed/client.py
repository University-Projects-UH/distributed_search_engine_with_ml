import time
import zmq
import settings
from utils.ip import give_ip
from udplib import UDP

class Client:

    def __init__(self):
        # Server actually listens
        self.active_servers = {}
        self.address = give_ip()

    def start(self):
        udp = UDP(settings.PING_PORT_NUMBER)

        poller = zmq.Poller()
        poller.register(udp.handle, zmq.POLLIN)

        # Send first ping right away
        ping_at = time.time()

        while True:
            timeout = ping_at - time.time()
            if timeout < 0:
                timeout = 0

            events = dict(poller.poll(1000* timeout))

            # Someone answered our ping
            if udp.handle.fileno() in events:
                resp, addrinfo = udp.recv(settings.PING_MSG_SIZE)
                if addrinfo[0] != self.address:
                    peer_type = 'peer'
                    if(resp == 's'):
                        peer_type = 'server'
                        self.active_servers[addrinfo[0]] = time.time()

                    if(settings.DEBUG_MODE):
                        print("Found %s %s:%d" % (peer_type, addrinfo[0], addrinfo[1]))

            if time.time() >= ping_at:
                # Broadcast our beacon
                if(settings.DEBUG_MODE):
                    print ("Pinging peers...")
                udp.send(b'!')
                ping_at = time.time() + settings.PING_INTERVAL
                self.check_servers()

    def check_servers(self):
        list_servers = []
        for server,last_time in self.active_servers.items():
            if(time.time() - last_time > settings.PEER_EXPIRY):
                list_servers.append(server)

        for server in list_servers:
            self.active_servers.remove(server)
