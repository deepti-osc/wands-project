# wands-project

Product search experiments using the [WANDS](https://github.com/wayfair/WANDS) dataset and OpenSearch.

## Dataset dependency

This repo does not include the WANDS dataset (it's a separate ~92MB clone with large CSV files). Fetch it yourself before running anything:

```
git clone https://github.com/wayfair/WANDS.git
```

Clone it into a `WANDS/` folder at the root of this project (already gitignored here) so the paths in `load_data.py` (e.g. `WANDS/dataset/product.csv`) resolve correctly.

## Setup

```
python -m venv .venv
source .venv/bin/activate
pip install pandas opensearch-py fastapi uvicorn
```

Start OpenSearch with Docker Compose:

```
docker compose up -d
```

This runs OpenSearch on `localhost:9200`.

## Usage

Load the product data into OpenSearch:

```
python load_data.py
```

Run the search API:

```
uvicorn main:app --reload
```

Then query it, e.g. `GET /search?q=chair`.
