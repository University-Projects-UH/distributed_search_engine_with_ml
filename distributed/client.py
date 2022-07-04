from audioop import add, reverse
from ipaddress import ip_address
import time
import zmq
from threading import Thread
from typing import List

import distributed.settings as settings
from distributed.utils.ip import give_ip
from distributed.utils.udplib import UDP

class Client:

    def __init__(self, address):
        # Server actually listens
        self.active_servers = {}
        self.address = address

        self.docs_save = None

        self.ctx = None
        # self.request = None
        
    def start(self):
        # ping socket
        udp = UDP(settings.PING_PORT_NUMBER)

        # connect to servers
        self.ctx = zmq.Context()
        
        poller = zmq.Poller()
        poller.register(udp.handle, zmq.POLLIN)

        while True:

            events = dict(poller.poll())

            # Someone answered our ping
            if udp.handle.fileno() in events:
                rec,address_port = udp.recv(settings.PING_MSG_SIZE)
                if rec == 's':
                    self.active_servers[address_port[0]] = time.time()
                    if(settings.DEBUG_MODE):
                        print("Client %s Received ping message: %s"  % (self.address, rec))


    # Check if some server was disconnected
    def check_servers(self):
        list_servers = []
        for server,last_time in self.active_servers.items():
            if(time.time() - last_time > settings.PEER_EXPIRY):
                list_servers.append(server)

        for server in list_servers:
            if(settings.DEBUG_MODE == True):
                print("Disconect server %s" % server)
            self.active_servers.pop(server)

    # Recive query and return docs results from the query
    def send_request(self, query = 'CUBA'):
        self.check_servers()

        count_servers = len(self.active_servers)

        thread = [None] * count_servers
        results = [None] * count_servers
        # save server ip
        ip_server = [None] * count_servers

        # server communication within threading
        idx = 0
        for server in self.active_servers:
            thread[idx] = Thread(target=self.communicate_server, args = (server, 'query1:' + query, results, idx))
            thread[idx].start()
            
            ip_server[idx] = server

            idx += 1

        # wait response from servers
        time.sleep(settings.WAIT_TIME_FOR_REQUEST)

        # if no one server is available wait a bit longer
        if( not any(x != None for x in results)):
            time.sleep(settings.WAIT_TIME_FOR_REQUEST / 2)

        # TO-DO: kill bugs process

        if( not any(x != None for x in results)):
            if(settings.DEBUG_MODE):
                print("No one server is available")
            return None

        # delete None results
        new_results = [results[i] for i in range(len(results)) if results[i] != None]
        news_ip_address  = [ip_server[i] for i in range(len(results)) if results[i] != None]

        self.docs_save = self.handle_response(new_results,news_ip_address)

        # create a new copy of docs for response
        docs_copy = []
        for i in range(len(self.docs_save)):
            docs_copy.append({
                'text' : self.docs_save[i]['text'],
                'ranking' : self.docs_save[i]['ranking'],
                'id' : i
            })

        return docs_copy

    def handle_response(self, response : List, ip_address : List):
        """
        Given a List servers' results
        Return a list with most important documents 
        result of merge
        """

        results = []
        for i in range(len(response)):
            for doc in response[i]:
                doc['ip'] = ip_address[i]
                results.append(doc)

        results.sort(key=lambda dic: dic['ranking'],reverse=True)

        hash_map = {}

        final_results = []
        for i in results:
            #calculate hash to document's text
            h = hash(i['text'])

            # if hash no exist actually is a new document
            if hash_map.get(h) is None:
                hash_map[h] = True

                final_results.append(i)

                if len(hash_map) == settings.AMOUNT_DOCS_IN_RESPONSE:
                    break

        # results = results[:settings.AMOUNT_DOCS_IN_RESPONSE]

        return final_results

    def communicate_server(self, server, query, results, index):
        """
        Request to a server docs for a given query
        """

        context = zmq.Context.instance()

        socket = context.socket(zmq.REQ)
        socket.connect("tcp://%s:%d" % (server, settings.CLI_SERV_PORT_NUMBER))

        # convert to buffer format and send query
        socket.send(query.encode('ascii'))

        resp = socket.recv_pyobj()

        if(settings.DEBUG_MODE):
            print("Received response from server: %s" % server)

        # TO-DO: some work to format response

        results[index] = resp

        socket.close()

    def query_docs(self, id : int):
        doc = [None]
        # print(self.docs_save)
        query = str(self.docs_save[id]['id'])
        query = 'query2:' + query
        ip_server = self.docs_save[id]['ip']
 
        thread = Thread(target=self.communicate_server, args = (ip_server, query, doc, 0))
        thread.start()

        # wait response from servers
        time.sleep(settings.WAIT_TIME_FOR_REQUEST)

        # TO-DO: kill bugs process

        if doc[0] is None:
            if(settings.DEBUG_MODE):
                print("Document is not available now")
            return None

        return doc[0]

# # self.request.send_multipart([b'',b'request'])
# self.request.send(b'',flags=zmq.SNDMORE)
# self.request.send(b'request %d' %cnt)

# self.request.recv_multipart()
#input.send(b'', flags = zmq.SNDMORE)
#input.send(b'OK')
