from fastapi import FastAPI
from opensearchpy import OpenSearch

app = FastAPI()
client = OpenSearch(hosts=[{"host": "localhost", "port": 9200}])

@app.get("/search")
def search(q: str):
    response = client.search(
        index="wands-products",
        body={
            "query": {
                "multi_match": {
                    "query": q,
                    "fields": ["product_name^3", "product_description"]
                }
            }
        }
    )
    return [hit["_source"] for hit in response["hits"]["hits"]]
