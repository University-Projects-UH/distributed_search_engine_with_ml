from client import Client

client = Client()

try:
    client.start()
except KeyboardInterrupt:
    print("Interrupted by user!")