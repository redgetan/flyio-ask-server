from dotenv import load_dotenv

import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from search_engine import SearchEngine
from indexer import Indexer

from pymilvus import MilvusClient


load_dotenv()

milvus_client = MilvusClient(
    uri=os.getenv("MILVUS_ENDPOINT"),
    token=os.getenv("MILVUS_API_KEY")
)

#milvus_collection_name = 'flyio_ada'
milvus_collection_name = 'test'

indexer = Indexer(milvus_client, milvus_collection_name)
searchEngine = SearchEngine(milvus_client, milvus_collection_name)


### API for indexing & AI search

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],  # Include OPTIONS method
    allow_headers=["*"],
)

class Msg(BaseModel):
    msg: str

@app.get("/")
async def root():
    return {"message": "/search, /create_index"}

@app.post("/search")
async def search(inp: Msg):
    result = searchEngine.search(inp.msg)
    return result

@app.post("/create_index")
async def create_index(inp: Msg):
    result = indexer.index_website(inp.msg)
    return { "message": "Indexing complete" }