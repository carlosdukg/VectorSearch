import pymongo
import embedding
import json
from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder

app = FastAPI()

class service_request_search(BaseModel):
    SR: str = ''
    Title: str = ''
    Customer: str = ''
    Description: str = ''
    Score: float = 0.0

@app.get("/")
def read_root():
    service_requests = []
    client = pymongo.MongoClient("mongodb+srv://carlosdaboin:ecqupQzely7A8E3A@clusteruscenmo.hmm9x2o.mongodb.net/?retryWrites=true&w=majority")
    db = client.CustomsServices
    collection = db.ServiceRequests

    query = "web"

    results = collection.aggregate([
        {
            "$vectorSearch": {
                "queryVector": embedding.generate_embedding(query),
                "path": "title_embedding",
                "numCandidates": 100,
                "limit": 10,
                "index": "vector_index",
            }
        },
        {
            "$project": {
                "SR": 1,
                "Title": 1,
                "Customer": 1,
                "Description": 1,
                "score": { "$meta": "vectorSearchScore" }
            }
        }
    ])

    for document in results:
         service_requests.append(
             service_request_search(
                 SR=document["SR"],
                 Title=document["Title"],
                 Customer=document["Customer"],
                 Description=document["Description"],
                 Score=document["score"]))

    return jsonable_encoder(service_requests)

@app.post("/service_request_search")
def update_item(query: str, limit: int, candidates: int):
    service_requests = []
    client = pymongo.MongoClient("mongodb+srv://carlosdaboin:ecqupQzely7A8E3A@clusteruscenmo.hmm9x2o.mongodb.net/?retryWrites=true&w=majority")
    db = client.CustomsServices
    collection = db.ServiceRequests

    results = collection.aggregate([
        {
            "$vectorSearch": {
                "queryVector": embedding.generate_embedding(query),
                "path": "title_embedding",
                "numCandidates": candidates,
                "limit": limit,
                "index": "vector_index",
            }
        },
        {
            "$project": {
                "SR": 1,
                "Title": 1,
                "Customer": 1,
                "Description": 1,
                "score": { "$meta": "vectorSearchScore" }
            }
        }
    ])

    for document in results:
         service_requests.append(
             service_request_search(
                 SR=document["SR"],
                 Title=document["Title"],
                 Customer=document["Customer"],
                 Description=document["Description"],
                 Score=document["score"]))
    
    return jsonable_encoder(service_requests)