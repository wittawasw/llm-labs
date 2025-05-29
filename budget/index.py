import os
import pandas as pd
import math
from dotenv import load_dotenv
from opensearchpy import OpenSearch, helpers
from tqdm import tqdm

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

load_dotenv()

CSV_PATH = "data/thailand_budget_2025_utf8_bom.csv"
INDEX_NAME = "thailand_budget_2025"
OPENSEARCH_URL = os.getenv("OPENSEARCH_URL", "https://localhost:9200")
USERNAME = os.getenv("OPENSEARCH_USERNAME", "admin")
PASSWORD = os.getenv("OPENSEARCH_PASSWORD", "admin")

es = OpenSearch(
    OPENSEARCH_URL,
    http_auth=(USERNAME, PASSWORD),
    use_ssl=True,
    verify_certs=False
)

df = pd.read_csv(CSV_PATH, encoding="utf-8-sig", low_memory=False)
df.columns = [col.strip().lower().replace("?", "").replace(" ", "_") for col in df.columns]

if not es.indices.exists(index=INDEX_NAME):
    mappings = {
        "mappings": {
            "properties": {
                "ministry": {"type": "keyword"},
                "budgetary_unit": {"type": "keyword"},
                "budget_plan": {"type": "keyword"},
                "category_lv1": {"type": "keyword"},
                "category_lv2": {"type": "keyword"},
                "category_lv3": {"type": "keyword"},
                "item_description": {"type": "text"},
                "amount": {"type": "double"},
                "fiscal_year": {"type": "integer"},
                "cross_func": {"type": "boolean"},
                "obliged": {"type": "boolean"},
            }
        }
    }
    es.indices.create(index=INDEX_NAME, body=mappings)

def sanitize(value):
    if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
        return None
    return value

def format_row(row):
    return {
        "_index": INDEX_NAME,
        "_source": {
            "ministry": sanitize(row.get("ministry")),
            "budgetary_unit": sanitize(row.get("budgetary_unit")),
            "budget_plan": sanitize(row.get("budget_plan")),
            "category_lv1": sanitize(row.get("category_lv1")),
            "category_lv2": sanitize(row.get("category_lv2")),
            "category_lv3": sanitize(row.get("category_lv3")),
            "item_description": sanitize(row.get("item_description")),
            "amount": float(row["amount"]) if pd.notna(row.get("amount")) and not math.isinf(row["amount"]) else 0.0,
            "fiscal_year": int(row["fiscal_year"]) if pd.notna(row.get("fiscal_year")) else 0,
            "cross_func": bool(row.get("cross_func", False)),
            "obliged": bool(row.get("obliged", False)),
        }
    }

print(f"⏳ Indexing {len(df)} documents to OpenSearch...")

actions = (format_row(row) for _, row in df.iterrows())
helpers.bulk(es, tqdm(actions, total=len(df)))

print("✅ Indexing complete.")
