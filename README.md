# redisventures-hackunamadata
https:/hackathon.redisventures.com/


```mermaid
sequenceDiagram
    title "High level flow - synchronous"

    Team ->> Vector Service: Send all papers in arXiv dataset
    Note over Team, Vector Service: POST vector_service/v1/arxiv/papers/
    Vector Service ->> Redis: Send papers in a queue and add papers as hashes with prefix /arxiv/papers/

    opt jupyter server and dask cluster are running:
        Redis -->> Jupyter Server: Consume messages in queue
        Note over Redis, Jupyter Server: user redis client to consume messages from queue
        Jupyter Server ->> Dask Cluster: Compute embeding for message
        Note over Jupyter Server, Dask Cluster: use dask client to push jobs to cluster
        Dask Cluster -->> Jupyter Server: Get message's embedding
        Jupyter Server ->> Redis: Store embeddings in papers hashes
    end

    User ->> Browser Extension: Sets the recommendation trigger actions

    loop while user is writing
        User ->> Browser Extension: Write text casually
        opt user's text is a trigger action
            Browser Extension ->> Recommendation Service: Send last paraghraph
            Recommendation Service ->> Vector Service: Send text
            Vector Service ->> Vector Service : Compute vector for given text input
            Vector Service ->> Redis : Find nearest papers in index
            Redis ->> Vector Service: Return nearest papers
            Vector Service -->> Recommendation Service: return nearest papers
            Recommendation Service -->> Browser Extension: Return recommendations
            Browser Extension -->> User: Display recommendations
        end
    end
```

# Components specification
## Redis
### Data structure
```json
{
    "id": "1801.00001",
    "title": "Title of the paper",
    "abstract": "Abstract of the paper",
    "categories": "cs.AI cs.CL cs.LG",
    "authors": "Author 1, Author 2, Author 3",
    "journal-ref": "Phys. Rev. B 76, 174425 (2007)"
}
```

## Vector Service
### Endpoints

| Endpoint | Method | Description | Request Body | Response Body |
| --- | --- | --- | --- | --- |
| /vector_service/v1/arxiv/papers | POST | Add the papers metadata in Redis hashes and put id in a Redis queue for future processing | `{"papers": [{"id": "123", "title": "title", "abstract": "abstract", ...}]}` | `{"status": "ok"}` |
| /vector_service/v1/arxiv/papers/{id} | GET | Get the metadata stored in Redis ahsh for the given arxiv paper id | - | `{"id": "123", "title": "title", "abstract": "abstract", ...}` |
| /vector_service/v1/text/nearest| POST | Get the nearest papers for the given text | `{"text": "string", "categories": ["cond-mat.dis-nn"], "years": ["2007", "2010"], "number_of_results": 5,"search_type": "KNN"}` | `{"papers": [{"id": "123", "title": "title", "abstract": "abstract"}, ...]}` |


## Recommendation Service
### Endpoints
| Endpoint | Method | Description | Request Body | Response Body |
| --- | --- | --- | --- | --- |
| /recommandation_service/v1/recommendations | POST | Get the recommendations for the given text and optional parameters | `{"text": "string", "categories": ["cond-mat.dis-nn"], "years": ["2007", "2010"], "number_of_results": 5}` | `{"papers": [{"id": "123", "title": "title", "abstract": "abstract"}]}` |

## Browser Extension
TBC