simple RAGs Backend API
This document describes a simple backend API for implementing Retrieval-Augmented Generation (RAGs). RAGs combine retrieval and generation techniques to enhance the quality of text generation.

* Architecture
* installation
* api docs
  
## Architecture
## installation
- git clone
- env.example -> .env
    *  DEBUG=false // show errors
    * QDRANT_CNAME=qdrantt // qdrant container name
    * QDRANT_API_KEY=buyhgsdfuysef78reh 
    * EMBEDDING_MODEL=all-MiniLM-L6-v2 // model for embedding
    * EMBEDDING_SIZE=384 // size of output of model embedding
    * LLM_MODEL=microsoft/Phi-3-mini-4k-instruct // generative model
```
docker-compose up -d
```

## API Endpoints

## Create Collection:
Request:
```
Method: PUT
Endpoint: /collections
```
Body:JSON
```
{
  "collection_name": "string", // Name of the collection
  "distance": "Cosine", // Cosine/Dot/Euclid method similarity for vectors
}
```

Response:
Status code: 201 (Created) on success
```
{
  "status": "string"
}
```
## Get Collection Names:
```
Method: GET
Endpoint: /collections
```

Response:
Status code: 200 (OK)
```
["string", ...]  // Array of collection names stored in the database
```

## Retrieve from Database:

Method: POST
Endpoint: /retrieve
Body:JSON
```
{
  "collection_name": "string", // Name of the collection
  "prompt": "string",  // Prompt for generation
  "page": 1, // pagination
  "limit": 1 // perpage limits
}
```
Response:
Status code: 200 (OK).
```
{
  "result": [
    {
      "text": "string",
      "score": float
    }
  ]
}
```
## Chunk Text and Embed:
Request:
```
Method: POST
Endpoint: /collections/
Path Parameter:
collectionName: Name of the collection to process.
```
 Body:JSON
 ```
{
  "collection_name": "string", // Name of the collection
  "text": "string",  // Text to be chunked and embedded
  "chunk_size": integer (optional)  // Size of text chunks for embedding (default: 128)
  "overlap": integer (optional)  // ovelap charaters for chunking  (default: 20)
}
```
Response:
```
Status code: 200 (OK) on success, or an error code with an appropriate message on failure.
```
Body:
JSON
```
{
  "status": "string",
  "chunks_processed": int
}
```

## Retrieval-Augmented Generation (RAG):
```
Method: POST
Endpoint: /generate
```

Request Body:
JSON
```
{
  "prompt": "string",  // Prompt for generation
  "collection_name": "string",  // Name of the collection to retrieve from
  "k": integer (optional)  // Number of top retrieved documents (default: 10)
  "temperature": float (optional)  // Temperature for controlling randomness in generation (default: 1.0)
}
```
Use code with caution.
content_copy
Response:
Status code: 200 (OK) 
```
{
  "generated_text": "string"  // Generated text based on the prompt and retrieved documents
}
```
