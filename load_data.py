import pandas as pd
from opensearchpy import OpenSearch, helpers

client = OpenSearch(hosts=[{"host": "localhost", "port": 9200}])
df = pd.read_csv("WANDS/dataset/product.csv", sep="\t")
df = df.fillna("")  # replace blank cells with empty strings instead of NaN

def generate_docs():
    for _, row in df.iterrows():
        yield {
            "_index": "wands-products",
            "_id": row["product_id"],
            "_source": {
                "product_name": row["product_name"],
                "product_class": row["product_class"],
                "category_hierarchy": row["category hierarchy"],
                "product_description": row["product_description"],
            },
        }

helpers.bulk(client, generate_docs())
print(f"Loaded {len(df)} products")