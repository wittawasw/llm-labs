import faiss
import sqlite3
import numpy as np
from sentence_transformers import SentenceTransformer

embedding_model_name = "sentence-transformers/all-MiniLM-L6-v2"
# embedding_model_name = "sentence-transformers/multi-qa-MiniLM-L6-cos-v1"
embedding_model = SentenceTransformer(embedding_model_name)

def get_embedding(text):
    return embedding_model.encode(text, convert_to_numpy=True).astype(np.float32)

def retrieve_supplements(query):
    index = faiss.read_index("./db/recommender_rag/supplement_index.faiss")
    supplement_ids = np.load("./db/recommender_rag/supplement_ids.npy")

    query_embedding = get_embedding(query)
    distances, indices = index.search(np.array([query_embedding]), k=3)

    conn = sqlite3.connect("./db/recommender_rag.db")
    cursor = conn.cursor()

    retrieved_supplements = []
    for idx in indices[0]:
        if idx == -1:
            continue
        supplement_id = supplement_ids[idx]
        cursor.execute("SELECT name, description, benefits FROM supplements WHERE id=?", (supplement_id,))
        result = cursor.fetchone()

        if result:
            retrieved_supplements.append(result)

    conn.close()

    return retrieved_supplements if retrieved_supplements else []
