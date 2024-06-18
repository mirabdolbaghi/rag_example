from pydantic import BaseModel, Field
from enum import Enum
from pydantic import BaseModel
from os import environ
from typing import List
class processTextRequest(BaseModel):
    collection_name: str
    text: str
    chunk_size: int = 100
    overlap: int = 20


class RAGquery(BaseModel):
    query: str
    collection_name: str
    max_token: int = 100
    temperature: float = Field(0.1, gt=0.0, lt=1.0)

class processTextResponse(BaseModel):
    status: str
    chunks_processed: int


class RAGresponse(BaseModel):
    response: str
class RetrieveRaw(BaseModel):
    text:str
    score:float
class RetrieveResponse(BaseModel):
    result:List[RetrieveRaw]
class RetrieveRequest(BaseModel):
    collection_name:str
    query:str
    page:int=1
    limit:int=1

class DistanceMetric(Enum):
    COSINE = "Cosine"
    EUCLID = "Euclid"
    DOT = "Dot"


class HnswConfig(BaseModel):
    m: int = Field(
        default=32,
        description="Number of edges per node in the index graph. Larger the value increases search accuracy but requires more space.",
    )
    ef_construct: int = Field(
        default=512,
        description="Number of neighbors to consider during index building. Larger the value increases search accuracy but takes longer to build.",
    )
    on_disk: bool = Field(
        default=True,
        description="Store the HNSW index on disk (True) or in RAM (False).",
    )
    full_scan_threshold: int = Field(
        default=1000,
        description="Minimal vector size (in KiloBytes) for additional payload-based indexing.",
    )

class CreateCollectionRequests(BaseModel):
    collection_name: str
    size: int = environ["EMBEDDING_SIZE"]
    distance: DistanceMetric
    hnsw_config: HnswConfig | None = HnswConfig()

class CreateCollectionResponse(BaseModel):
    status: str
