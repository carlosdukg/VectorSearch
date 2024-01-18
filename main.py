import pymongo
import embedding
from custom_spec_model import service_request
from embedded_model import embedded_request, request_search
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware

class custom_spec_model(BaseModel):
    SR: str
    Title: str
    Customer: str
    Description: str

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/search")
def search_request(query: str, limit: int, candidates: int):
    service_requests = []
    service_requests.extend(__get_search_result(query, limit, candidates, "title_embedding"))
    service_requests.extend(__get_search_result(query, limit, candidates, "description_embedding"))
    service_requests.extend(__get_search_result(query, limit, candidates, "sr_embedding"))
    service_requests.extend(__get_search_result(query, limit, candidates, "customer_embedding"))

    filtered_result = __remove_SR_Duplicates(service_requests)
    final_result = sorted(filtered_result, key=lambda x: x.Score, reverse=True)[:limit]
    
    return jsonable_encoder(final_result)

@app.post("/service_request/")
async def create_item(request: service_request):
    collection = __get_specs_collection()

    new_embedded_request = embedded_request(
        Customer = request.Customer,
        SR = request.SR,
        Description = request.Description,
        Title = request.Title,
        sr_embedding = embedding.generate_embedding(request.SR),
        title_embedding = embedding.generate_embedding(request.Title),
        customer_embedding = embedding.generate_embedding(request.Customer),
        description_embedding = embedding.generate_embedding(request.Description)
    )

    collection.insert_one(new_embedded_request.__dict__)

    return jsonable_encoder(request)

def __get_specs_collection():
    connection_string = "mongodb+srv://carlosdaboin:tg2yFWrEazgqve1V@clusterukgrapidsearch.v9zv1e4.mongodb.net/?retryWrites=true&w=majority"
    client = pymongo.MongoClient(connection_string)
    db = client.CustomsVectorSearch
    collection = db.CustomSpecs

    return collection

def __get_search_result(query: str, limit: int, candidates: int, field: str):
    service_requests = []
    collection = __get_specs_collection()
    results = collection.aggregate([
        {
            "$vectorSearch": {
                "queryVector": embedding.generate_embedding(query),
                "path": field,
                "numCandidates": candidates,
                "limit": limit,
                "index": "vector_index_search",
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
             request_search(
                 SR=document["SR"],
                 Title=document["Title"],
                 Customer=document["Customer"],
                 Description=document["Description"],
                 Score=document["score"]))

    return service_requests

def __remove_SR_Duplicates(service_requests: []):
    filtered_list = []
    unique_SR_list = []

    for obj in service_requests:
        if obj.SR in unique_SR_list:
            continue
        else:
           unique_SR_list.append(obj.SR)
           filtered_list.append(obj) 

    return filtered_list