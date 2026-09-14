import pandas as pd
from opensearchpy import OpenSearch, helpers

client = OpenSearch(hosts=[{"host": "localhost", "port": 9200}])

# name index
index_name = "wands-products"

mapping = {
    "settings": {
        "analysis": {
            "filter": {
                "plural_stemmer": {
                    "type": "stemmer",
                    "language": "minimal_english"
                }
            },
            "analyzer": {
                "my_analyzer": {
                    "type": "custom",
                    "tokenizer": "standard",
                    "filter": ["lowercase", "stop", "plural_stemmer"]
                }
            }
        }
    },
    "mappings": {
        "properties": {
            "product_name": {"type": "text", "analyzer": "my_analyzer"},
            "product_description": {"type": "text", "analyzer": "my_analyzer"},
            "product_class": {
                "type": "text",
                "analyzer": "my_analyzer",
                "fields": {"keyword": {"type": "keyword"}}
            },
            "category_hierarchy": {
                "type": "text",
                "analyzer": "my_analyzer",
                "fields": {"keyword": {"type": "keyword"}}
            },
            "rating_count": {"type": "integer"},
            "review_count": {"type": "integer"},
            "average_rating": {"type": "float"},
        }
    }
}

# deletes index if it already exists and creates a new one with the specified mapping
if client.indices.exists(index=index_name):
    client.indices.delete(index=index_name)

client.indices.create(index=index_name, body=mapping)

# read dataset
df = pd.read_csv("WANDS/dataset/product.csv", sep="\t")

#Fill missing values for text columns with empty string and for numeric columns with None
text_cols = ['product_class', 'category hierarchy', 'product_description']
num_cols = ['rating_count', 'average_rating', 'review_count']

df[text_cols] = df[text_cols].fillna("")
df[num_cols] = df[num_cols].where(df[num_cols].notnull(), None)

df['category_hierarchy'] = df['category hierarchy'].apply(
    lambda x: [level.strip() for level in x.split('/')] if x else []
)

def clean_num(value):
    return None if pd.isna(value) else value

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
                #"product_features": row["product_features"],
                "rating_count": clean_num(row["rating_count"]),
                "average_rating": clean_num(row["average_rating"]),
                "review_count": clean_num(row["review_count"]),
            },
        }

helpers.bulk(client, generate_docs())
print(f"Loaded {len(df)} products")