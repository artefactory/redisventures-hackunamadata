# Vector Service

The vector service is an api that aims to collect raw papers metadata and push it to the redis database. It computes afterwards the corresponding vectorized form of each paper of the list.

## Getting Started

In order to run this service, the "papers_embeddor" server and the "vector_service" must be running.
Note that the working details of this system is completely obfuscated to the end user by the recommendation service.

### Prerequisites

- import the project

  ```sh
  git clone git@github.com:artefactory/redisventures-hackunamadata.git
  ```

- Go to the project's folder and then to the recommendation service's folder
  ```sh
  cd vector_service
  ```
- Create virtual env and install packages with pip
  ```sh
  python -m pip install -r requirements.txt
  ```

### Usage

You will need to export several confidential environment variables to make the API work.

```sh
 export REDIS_HOST=...
 export REDIS_PORT=...
 export REDIS_DB=...
 export REDIS_USERNAME=...
 export REDIS_PASSWORD=...
 export QUEUE_NAME=...
 export INDEX_NAME=...
 export INDEX_TYPE=...
```

### Endpoints

| Endpoint                             | Method | Description                                                                               | Request Body                                                                                                                    | Response Body                                                                |
| ------------------------------------ | ------ | ----------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| /vector_service/v1/arxiv/papers      | POST   | Add the papers metadata in Redis hashes and put id in a Redis queue for future processing | `{"papers": [{"id": "123", "title": "title", "abstract": "abstract", ...}]}`                                                    | `{"status": "ok"}`                                                           |
| /vector_service/v1/arxiv/papers/{id} | GET    | Get the metadata stored in Redis ahsh for the given arxiv paper id                        | -                                                                                                                               | `{"id": "123", "title": "title", "abstract": "abstract", ...}`               |
| /vector_service/v1/text/nearest      | POST   | Get the nearest papers for the given text                                                 | `{"text": "string", "categories": ["cond-mat.dis-nn"], "years": ["2007", "2010"], "number_of_results": 5,"search_type": "KNN"}` | `{"papers": [{"id": "123", "title": "title", "abstract": "abstract"}, ...]}` |

### Architecture

See [here](../README.md) for more details.
