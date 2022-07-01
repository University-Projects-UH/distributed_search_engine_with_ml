import time
import zmq
from threading import Thread
from typing import List

import settings
from utils.ip import give_ip
from utils.udplib import UDP

class Client:

    def __init__(self):
        # Server actually listens
        self.active_servers = {}
        self.address = give_ip()

        self.ctx = None
        # self.request = None
        
    def start(self):
        # ping socket
        udp = UDP(settings.PING_PORT_NUMBER)

        # connect to servers
        self.ctx = zmq.Context()
        
        poller = zmq.Poller()
        poller.register(udp.handle, zmq.POLLIN)

        # Send first ping right away
        ping_at = time.time()

        while True:
            timeout = ping_at - time.time()
            if timeout < 0:
                timeout = 0

            events = dict(poller.poll(1000* timeout))

            # recive a query from standard input
            query = input()
            if query != '':
                self.send_request(query)

            # Someone answered our ping
            if udp.handle.fileno() in events:
                resp, addrinfo = udp.recv(settings.PING_MSG_SIZE)
                if(resp == 's'):
                    if(settings.DEBUG_MODE and self.active_servers.get(addrinfo[0]) == None):
                        print("Found server %s:%d" % addrinfo)

                    self.active_servers[addrinfo[0]] = time.time()

            # Is time to send broadcast ping
            if time.time() >= ping_at:
                # Broadcast our beacon
                if(settings.DEBUG_MODE):
                    print ("Pinging peers...")
                udp.send(b'!')
                ping_at = time.time() + settings.PING_INTERVAL

    def check_servers(self):
        list_servers = []
        for server,last_time in self.active_servers.items():
            if(time.time() - last_time > settings.PEER_EXPIRY):
                list_servers.append(server)

        for server in list_servers:
            self.active_servers.pop(server)

    def send_request(self, query = 'CUBA'):
        # self.check_servers()

        count_servers = len(self.active_servers)

        thread = [None] * count_servers
        results = [None] * count_servers

        # server communication within threading
        idx = 0
        for server in self.active_servers:
            thread[idx] = Thread(target=self.communicate_server, args = (server, query, results, idx))
            thread[idx].start()

            idx += 1

        # wait response from servers
        time.sleep(settings.WAIT_TIME_FOR_REQUEST)

        # if no one server is available wait a bit longer
        if( not any(x != None for x in results)):
            time.sleep(settings.WAIT_TIME_FOR_REQUEST / 2)

        # TO-DO: kill bugs process

        if( not any(x != None for x in results)):
            print("No one server is available")
            return None

        # delete None results
        new_results = [i for i in results if i != None]

        self.handle_response(new_results)

    def handle_response(self, response : List):
        """
        Given a List servers' results
        Return a list with results merged
        """

        results = []
        for i in response:
            results.extend(i)

        return results[:settings.AMOUNT_DOCS_IN_RESPONSE]

    def communicate_server(self, server, query, results, index):
        """
        Request to a server docs for a given query
        """

        context = zmq.Context.instance()

        socket = context.socket(zmq.REQ)
        socket.connect("tcp://%s:%d" % (server, settings.CLI_SERV_PORT_NUMBER))

        # convert to buffer format and send query
        socket.send(query.encode('ascii'))

        resp = socket.recv()

        if(settings.DEBUG_MODE):
            print("Received response from server: %s" % server)

        # TO-DO: some work to format response

        results[index] = resp

        socket.close()





# # self.request.send_multipart([b'',b'request'])
# self.request.send(b'',flags=zmq.SNDMORE)
# self.request.send(b'request %d' %cnt)

# self.request.recv_multipart()