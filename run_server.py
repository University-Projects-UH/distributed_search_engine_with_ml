from distributed.server import Server

server = Server('docs-lisa')

try:
    server.start()
except KeyboardInterrupt:
    print("Interrupted by user!")