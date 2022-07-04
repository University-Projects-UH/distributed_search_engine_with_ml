import zmq
import time

import distributed.settings as settings
from distributed.utils.udplib import UDP
from distributed.utils.ip import give_ip

from ir_model.model.vectorial_model import VectorialModel
from ir_model.file_tools import DocsCollection

class Server:

    def __init__(self, address, document_set : str):
        self.dc = DocsCollection(document_set)
        self.vm = VectorialModel(self.dc.docs)
        self.address = address

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
        udp = UDP(settings.PING_PORT_NUMBER)

        # poll sockets
        poller = zmq.Poller()
        # poller.register(udp.handle, zmq.POLLIN)
        poller.register(input,zmq.POLLIN)

        # Send first ping right away
        ping_at = time.time()

        while True:
            timeout = ping_at - time.time()
            if timeout < 0:
                timeout = 0

            events = dict(poller.poll(1000* timeout))
                               
            # client-server communication
            if events.get(input) == zmq.POLLIN:
                recive = input.recv().decode('utf-8')

                response = self.handle_request(recive)

                input.send_pyobj(response)

                if(settings.DEBUG_MODE):
                    print("Recieved message: \"%s\" by port: %d" % (recive, settings.CLI_SERV_PORT_NUMBER) )

            # Is time to send broadcast ping
            if time.time() >= ping_at:
                # Broadcast our beacon
                if(settings.DEBUG_MODE):
                    print ("Pinging peers...")
                udp.send(b's')
                ping_at = time.time() + settings.PING_INTERVAL

    def handle_request(self, request):
        # request for docs match with a query

        if 'query1:' in request:
            request = request.replace('query1:', '', 1)

            # return docs
            return self.query_docs(request)
        if 'query2:' in request:
            request = request.replace('query2:', '', 1)

            id = int(request)

            # return doc
            return {"text" : self.vm.docs[id].text}
        
