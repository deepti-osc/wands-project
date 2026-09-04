from fastapi import FastAPI
from opensearchpy import OpenSearch

app = FastAPI()
client = OpenSearch(hosts=[{"host": "localhost", "port": 9200}])

@app.get("/search")
def search(q: str):
    response = client.search(
        index="wands-products",
        body={"query": {"match": {"product_name": q}}}
    )
    return [hit["_source"] for hit in response["hits"]["hits"]]
