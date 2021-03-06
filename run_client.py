from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from threading import Thread
import uvicorn
import sys
from argparse import ArgumentParser

from distributed.client import Client
import distributed.settings as settings

parser = ArgumentParser()

parser.add_argument(
    '--ip', type=str, required=True,
    help='IP address'
)

args = parser.parse_args()

app_client = FastAPI()

client = Client(args.ip)

app_client.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ORIGINS_API_CLIENT,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app_client.get("/query")
def query_docs(value: str = ""):
    return client.send_request(value)

@app_client.get("/document/{doc_id}")
def read_document(doc_id: int):
    return client.query_docs(doc_id)

client_thread = Thread(target=client.start,daemon=True)
client_thread.start()

if __name__ == "__main__":
    try:
        uvicorn.run("run_client:app_client", reload=True, port=8000)
    except KeyboardInterrupt:
        sys.exit()

# curl http://127.0.0.1:8000/query?value=cuba
# curl http://127.0.0.1:8000/document/1