
from qdrant_client.models import Distance,VectorParams,HnswConfigDiff 
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.http.exceptions import UnexpectedResponse
from fastapi import  HTTPException
from schemas import CreateCollectionRequests
import grpc
from os import environ

qdrant_client = QdrantClient(host=environ["QDRANT_CNAME"], https=False, port=6333, grpc_port=6334, prefer_grpc=True, api_key=environ["QDRANT_API_KEY"])
model = SentenceTransformer(environ["EMBEDDING_MODEL"])

def exception_handler(function):
    def qdrant_exception_handler(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except grpc.RpcError as rpc_error:
          if rpc_error.code() == grpc.StatusCode.NOT_FOUND:
              raise HTTPException(status_code=404, detail=f"collection doesn't exist")
          elif rpc_error.code() == grpc.StatusCode.INVALID_ARGUMENT:
              raise HTTPException(status_code=400, detail=rpc_error.details())
          else:
              raise rpc_error
        except UnexpectedResponse as http_error:
          if http_error.status_code in [404,400]:
              raise HTTPException(status_code=http_error.status_code, detail=http_error.content)
          else:
              raise http_error
 
    return qdrant_exception_handler
@exception_handler
def add_to_qdrant(collection_name,text_lst):
    
    encoded_chunks = model.encode(text_lst)
    qdrant_client.upload_collection(
        collection_name=collection_name,
        vectors=encoded_chunks,
        payload=[{"text": text} for text in text_lst]
    )
@exception_handler
def retieve_from_qdrant(collection_name:str,qurey:str,limit:int=1,offset=0):
        encoded_query = model.encode(qurey)
        return clean_qdrant_response(qdrant_client.search(
            collection_name=collection_name,
            query_vector=encoded_query,
            with_vectors=False,
            with_payload=True,
            limit=limit,
            offset=offset,
        ))
def clean_qdrant_response(scored_point_list):
    return [{"text":point.payload["text"],"score":point.score} for point in scored_point_list]
def get_collection_names():
    collections = qdrant_client.get_collections().collections 
    return [col.name for col in collections]
@exception_handler
def create_collection(request:CreateCollectionRequests):
    hnsw_config = None
    match request.distance.value:
            case 'Cosine':
                distance = Distance.COSINE
            case 'Euclid':
                distance = Distance.EUCLID
            case 'Dot':
                distance = Distance.DOT
            case _:
                raise Exception("distance metric is not corrented")
    if request.hnsw_config != None:
        hnsw_config = HnswConfigDiff(
        m=request.hnsw_config.m,
        ef_construct=request.hnsw_config.ef_construct,
        on_disk=request.hnsw_config.on_disk,
        full_scan_threshold=request.hnsw_config.full_scan_threshold,
        
        )

  
    qdrant_client.create_collection(
        collection_name=request.collection_name,
        vectors_config=VectorParams(size=request.size, distance=distance,hnsw_config=hnsw_config),
    )
