import signal
from sys import flags
import zmq

import distributed.settings as settings
from distributed.utils.udplib import UDP
from distributed.utils.ip import give_ip

from ir_model.model.vectorial_model import VectorialModel
from ir_model.file_tools import DocsCollection

class Server:

    def __init__(self, document_set : str):
        self.dc = DocsCollection(document_set)
        self.vm = VectorialModel(self.dc.docs)
        self.address = give_ip()

    def query_docs(self, value: str = ""):
        documents = self.vm.query(value)
        return self.prepare_output(documents)

    def prepare_output(self, documents):
        body = []
        for doc in documents:
            body.append({
                "ranking": doc[0],
                "text": doc[1].text[:min(len(doc[1].text), 400)] + ("(...)" if len(doc[1].text) > 400 else ""),
                "id": doc[2]

            })
        return body

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
                recive = input.recv_multipart()

                docs = self.query_docs(recive)

                input.send_pyobj(docs)

                #input.send(b'', flags = zmq.SNDMORE)
                #input.send(b'OK')
                if(settings.DEBUG_MODE):
                    print("Recieved message: \"%s\" by port: %d" % (recive, settings.CLI_SERV_PORT_NUMBER) )
