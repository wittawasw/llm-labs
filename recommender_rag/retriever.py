import faiss
import sqlite3
import numpy as np
from sentence_transformers import SentenceTransformer

# embedding_model_name = "sentence-transformers/all-MiniLM-L6-v2"
# embedding_model_name = "sentence-transformers/multi-qa-MiniLM-L6-cos-v1"
embedding_model_name = "alifaheem94/bge-m3_medical_ur_ru"

embedding_model = SentenceTransformer(embedding_model_name)

def get_embedding(text):
    return embedding_model.encode(text, convert_to_numpy=True).astype(np.float32)

def retrieve_supplements(query):
    index = faiss.read_index("./db/recommender_rag/supplement_index.faiss")
    supplement_data = np.load("./db/recommender_rag/supplement_data.npy", allow_pickle=True)

    query_embedding = get_embedding(query)
    _, indices = index.search(np.array([query_embedding]), k=3)

    retrieved_supplements = []
    for idx in indices[0]:
        if idx == -1:
            continue
        retrieved_supplements.append(supplement_data[idx])

    return retrieved_supplements
