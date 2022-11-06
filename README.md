<div align="center">
<img src="https://dwglogo.com/wp-content/uploads/2017/12/1100px_Redis_Logo_01.png" height="200" align="middle"/>
</div>

# ArXiv Copilot </br> Redisventures - Hackunamadata team

## :bookmark_tabs: Menu

* [Overview](#overview)
* [How to install ArXiv Copilot](#how-to-install-arxiv-copilot)
* [Sequence Diagram](#sequence-diagram)
* [Developer Guide](#developer-guide)
  * [Redis - Data structure](#redis---data-structure)
  * [Vector Service](#vector-service)
  * [Recommendation Service](#recommendation-service)
  * [ArXiv Copilot](#arxiv-copilot)
* [License](#license)
* [Authors](#authors)

## Overview

ArXiv Copilot is a Chrome extension that is giving you live suggestions of scientific papers that could interest you when you're writing an article, course notes, ...
</br>It is a system created using the Vector Search technology on the [arXiv scholarly papers dataset](https://arxiv.org/).
This was developed during the [Vector Search Engineering Lab (Hackathon)](https:/hackathon.redisventures.com/), in collaboration with Saturn Cloud and Redis, by three data engineers and one data scientist from Artefact Paris.
</br>If you want to understand more how the tool was thought and made, you can read our article [here](https://docs.google.com/document/d/14p3btpmbXqG21guGo1Bf6Wf9mrt3gc6wc-CJ0aMpUWQ/edit?usp=sharing).

## How to install ArXiv Copilot

See [here](./browser_extension/README.md) to know how to install the browser extension and enjoy the use of ArXiv Copilot.

## Sequence Diagram
```mermaid
sequenceDiagram
    title "High level flow - synchronous"

        opt team wants to upload articles
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
    end

    opt User wants custom exention setting
        User ->> ArXiv Copilot: Setup the exention's options
    end

    loop while user is writing
        User ->> ArXiv Copilot: Write text casually
        opt ArXiv Copilot has registered `text_trigger_depth` words
            ArXiv Copilot ->> Recommendation Service: Send `text_send_depth` words.
            activate Recommendation Service
            Note over ArXiv Copilot, Recommendation Service: GET /api/v1/text/:text/nearest?k=10
            Recommendation Service ->> Vector Service: Send text
            Vector Service ->> Vector Service : Compute vector for given text input
            Vector Service ->> Redis : Find nearest papers in index
            Redis -->> Vector Service: Return nearest papers
            Vector Service -->> Recommendation Service: return nearest papers
            Recommendation Service -->> ArXiv Copilot: Return recommendations
            deactivate Recommendation Service
            ArXiv Copilot -->> User: Return recommendations as chrome notifications
            opt user clicks on notificaiton
                ArXiv Copilot ->> User: Open article in new tab
            end
        end
    end
```

# Developer Guide
## Redis - Data structure
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

For more details, see [here](./vector_service).

## Recommendation Service
### Endpoints
| Endpoint | Method | Description | Request Body | Response Body |
| --- | --- | --- | --- | --- |
| /recommandation_service/v1/recommendations | POST | Get the recommendations for the given text and optional parameters | `{"text": "string", "categories": ["cond-mat.dis-nn"], "years": ["2007", "2010"], "number_of_results": 5}` | `{"papers": [{"id": "123", "title": "title", "abstract": "abstract"}]}` |

For more details, see [here](./recommendation_service).

## ArXiv Copilot

### Extension configuration
| Field | Description | Example | Default |
| --- | --- | --- | --- |
| text_trigger_depth | Number of words to wait before asking for recommandations again | `10` | `10` |
| text_send_depth | Number of words to send to the recommendation service | `3000` | `3000` |
| recommendation_service_url | URL of the recommendation service | `https://recommendationservice.community.saturnenterprise.io/api/v1/recommendations/` | `https://recommendationservice.community.saturnenterprise.io/api/v1/recommendations/` |
| recommendation_service_token | Token for the recommendation service | `678GSA576SQ` | `undefined` |

For more details, see [here](./browser_extension).

## License

The [MIT License]() (MIT)

## Authors
- [@dauresh](https://github.com/dauresh)
- [@ali-artefact](https://github.com/ali-artefact)
- [@benoitbazouin](https://github.com/benoitbazouin)
- [@pol-defont-reaulx](https://github.com/pol-defont-reaulx)
