from client import Client
import signal

client = Client()

try:
    client.start()
except KeyboardInterrupt or signal.SIGTERM:
    print("Interrupted by user!")