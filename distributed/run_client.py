from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from threading import Thread

import uvicorn
from client import Client
import settings

app_client = FastAPI()

client = Client()

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
    pass


client_thread = Thread(target=client.start,daemon=True)
client_thread.start()


if __name__ == "__main__":
    uvicorn.run("run_client:app_client", reload=True)





#curl http://127.0.0.1:8000/query?value=cuba
