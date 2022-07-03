from distributed.server import Server
from argparse import ArgumentParser

parser = ArgumentParser()

parser.add_argument(
    '--collection', type=str, required=True,
    help='The collection of the document that the server goes to process'
)

args = parser.parse_args()

server = Server(args.collection)

try:
    server.start()
except KeyboardInterrupt:
    print("Interrupted by user!")