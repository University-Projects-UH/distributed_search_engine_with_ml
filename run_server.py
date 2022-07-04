from distributed.server import Server
from argparse import ArgumentParser

parser = ArgumentParser()

parser.add_argument(
    '--collection', type=str, required=True,
    help='The collection of the document that the server goes to process'
)
parser.add_argument(
    '--ip', type=str, required=True,
    help='IP address'
)

args = parser.parse_args()

server = Server(args.ip, args.collection)

try:
    server.start()
except KeyboardInterrupt:
    print("Interrupted by user!")