# Recommendation Service

The Recommendation Service is the API that is requesting the ArXiv Copilot extension to get recommended papers from a text. It's running with FastAPI.

## User Guide

### Installation

## Getting Started

To run the recommendation service you should have the vector service running.
In this part we are going to explain how to set-up your environment and run the Recommendation Service.

### Prerequisites

* import the project
  ```sh
  git clone git@github.com:artefactory/redisventures-hackunamadata.git
  ```

* Go to the project's folder and then to the recommendation service's folder
  ```sh
  cd recommendation_service
  ```
  
* Create virtual env and install packages with pip
  ```sh
  python -m pip install -r requirements.txt
  ```


### Usage

You will need to export several confidential environment variables to make the API work.

 ```sh
 export VECTOR_SERVICE_HOST=<vector service private url on Saturn Cloud>
 export SATURN_TOKEN=<Saturn Cloud user token to access vector service>
 ```

Then, you can run the API:

 ```sh
 python main.py
 ```

From another window of your vs-code terminal you should be able to run the following command to check that the API is working:

 ```sh
 curl -i -H "Accept: application/json" -H "Content-Type: application/json" -X GET localhost:8080/docs
 ```

## Endpoints
| Endpoint                | Method | Description | Request Body | Response Body                                                                                                                                                                    |
|-------------------------| --- | --- | --- |----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| /api/v1/recommendations | POST | Get the recommendations for the given text and optional parameters | `{"text": "string", "categories": ["cond-mat.dis-nn"], "years": ["2007", "2010"], "number_of_results": 5}` | `{"papers": [{"id": "123", "title": "title", "authors": "authors", "abstract": "abstract", "categories": "categories", "journal_ref": "journal_ref", "similarity_score": 0.5}]}` |


## Developer Guide

### Architecture

See [here](../README.md) for more details.