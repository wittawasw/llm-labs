import faiss
import sqlite3
import numpy as np
from sentence_transformers import SentenceTransformer

embedding_model_name = "sentence-transformers/all-MiniLM-L6-v2"
# embedding_model_name = "sentence-transformers/multi-qa-MiniLM-L6-cos-v1"
embedding_model = SentenceTransformer(embedding_model_name)

def get_embedding(text):
    return embedding_model.encode(text, convert_to_numpy=True).astype(np.float32)

def build_faiss_index():
    conn = sqlite3.connect("./db/recommender_rag.db")
    cursor = conn.cursor()

    cursor.execute("SELECT id, name, description, benefits FROM supplements")
    supplements = cursor.fetchall()

    dimension = 384
    index = faiss.IndexFlatL2(dimension)
    supplement_ids = []
    embeddings = []

    for supp in supplements:
        text = f"{supp[1]}: {supp[2]} Benefits: {supp[3]}"
        embedding = get_embedding(text)
        embeddings.append(embedding)
        supplement_ids.append(supp[0])

    index.add(np.array(embeddings, dtype=np.float32))
    faiss.write_index(index, "./db/recommender_rag/supplement_index.faiss")
    np.save("./db/recommender_rag/supplement_ids.npy", np.array(supplement_ids))

    conn.close()
    print("FAISS index built and saved.")

if __name__ == "__main__":
    build_faiss_index()
