import psycopg2
import pickle
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import os
from dotenv import load_dotenv
load_dotenv()
db_config = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT")
}
conn = psycopg2.connect(**db_config)
cur = conn.cursor()
cur.execute("SELECT content, embedding FROM documents")
rows = cur.fetchall()
contents = []
embeddings = []
for content, emb_bytes in rows:
    contents.append(content)
    embeddings.append(pickle.loads(emb_bytes))
embeddings = np.array(embeddings)
model = SentenceTransformer("all-MiniLM-L6-v2")
def query_documents(text, top_k=5):
    query_embedding = model.encode(text)
    similarities = cosine_similarity([query_embedding], embeddings)[0]
    indices = similarities.argsort()[::-1][:top_k]
    return [(contents[i], similarities[i]) for i in indices]
if __name__ == "__main__":
    while True:
        question = input("\nEnter your query (or type 'exit' to quit): ")
        if question.lower() in ["exit", "quit"]:
            print("Exiting...")
            break
        results = query_documents(question, top_k=5)
        print("\nTop relevant documents:")
        for score, (doc, sim) in enumerate(results, 1):
            print(f"\n{score}. Similarity: {sim:.4f}\n{doc[:500]}")  
cur.close()
conn.close()
