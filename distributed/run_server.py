from server import Server

server = Server()

try:
    server.start()
except KeyboardInterrupt:
    print("Interrupted by user!")