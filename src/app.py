from fastapi import FastAPI, HTTPException
from db import add_to_qdrant, retieve_from_qdrant, create_collection, get_collection_names
from services import chunk_text
from typing import List
import uvicorn
import numpy as np
from llm import generate_response
from logger import unhandled_exception_handler
from schemas import processTextRequest, processTextResponse, \
    RAGquery, RAGresponse, CreateCollectionRequests, CreateCollectionResponse, \
    RetrieveResponse,RetrieveRequest
app = FastAPI()
app.add_exception_handler(Exception, unhandled_exception_handler)

@app.get("/collections")
def get_collections_list() -> List[str]:
    return get_collection_names()

@app.put("/collections")
def make_collection(reuest:CreateCollectionRequests) -> CreateCollectionResponse:
    create_collection(request=reuest)
    return {"status":"success"}

@app.post("/collections")
def process_text_store_in_collection(request: processTextRequest)-> processTextResponse:
    text_chunks = list(chunk_text(request.text, request.chunk_size, request.overlap))
    
    if not text_chunks:
        raise HTTPException(status_code=400, detail="Text is too short to create chunks with given parameters.")
    
    add_to_qdrant(request.collection_name, text_chunks)
    return {"status": "success", "chunks_processed": len(text_chunks)}


@app.get("/retrieve")
def retrieve_from_collection(request:RetrieveRequest)-> RetrieveResponse:
    return {
        "result":retieve_from_qdrant(request.collection_name,
                               request.query,
                               request.limit,
                               (request.page-1)*request.limit) 
    }

@app.get("/rag/")
def retrieval_augmented_generation(query:RAGquery) -> RAGresponse:
    
    qdrant_resonse = retieve_from_qdrant(query.collection_name,query.query) 
    context =""
    for resp in qdrant_resonse:
        context += resp["text"]
    return {"response":generate_response(query.query,context,query.temperature,query.max_token)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)