# redisventures-hackunamadata
https:/hackathon.redisventures.com/


```mermaid
sequenceDiagram
    title "High level flow - synchronous"

    Team ->> Vector Service: Send all data in arXiv dataset
    Vector Service ->> Vector Service: Compute all vectors
    Vector Service ->> Redis: Cache all vectors

    User ->> Browser Extension: Sets the recommendation trigger actions

    loop while user is writing
        User ->> Browser Extension: Write text casually
        opt user's text is a trigger action
            Browser Extension ->> Recommendation Service: Send last paraghraph
            Recommendation Service ->> Vector Service: Send text
            Vector Service ->> Vector Service : Compute vector for given text input
            Vector Service -->> Recommendation Service: return vector
            Recommendation Service ->> Redis: search vector's nearest articles
            Redis -->> Recommendation Service: return nearest articles
            Recommendation Service -->> Browser Extension: Return recommendations
            Browser Extension -->> User: Display recommendations
        end
    end
```

# Components specification
## Vector Service
### Endpoints

| Endpoint | Method | Description | Request Body | Response Body |
| --- | --- | --- | --- | --- |
| /api/v1/arxiv/articles | POST | Compute the vectors for the given list of arxiv articles json | `{"articles": [{"id": "123", "title": "title", "abstract": "abstract"}]}` | `{"status": "ok"}` |
| /api/v1/arxiv/articles/:id | GET | Get the vector for the given arxiv article id | - | `{"vector": [0.1, 0.2, 0.3]}` |
| /api/v1/text | POST | Compute the vector for the given text | `{"text": "text"}` | `{"status": "ok"}` |
| /api/v1/text/:text | GET | Get the vector for the given text | - | `{"vector": [0.1, 0.2, 0.3]}` |
| /api/v1/text/:text/nearest?k=10 | GET | Get the k nearest articles for the given text | - | `{"articles": [{"id": "123", "title": "title", "abstract": "abstract"}]}` |


## Recommendation Service
### Endpoints
| Endpoint | Method | Description | Request Body | Response Body |
| --- | --- | --- | --- | --- |
| /api/v1/recommendations/:text | GET | Get the recommendations for the given text | - | `{"articles": [{"id": "123", "title": "title", "abstract": "abstract"}]}` |