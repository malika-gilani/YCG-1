import psycopg2
import pickle
import json
import os
from dotenv import load_dotenv
load_dotenv()
embeddings_file = r"C:\Users\malik\OneDrive\Desktop\YCG 1\embeddings_hf.json"
if not os.path.exists(embeddings_file):
    raise FileNotFoundError(f"Embeddings file not found: {embeddings_file}")
db_config = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT")
}
with open(embeddings_file, "r", encoding="utf-8") as f:
    embeddings_data = json.load(f)
conn = psycopg2.connect(**db_config)
cur = conn.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS documents (
    id SERIAL PRIMARY KEY,
    filename TEXT,
    content TEXT,
    embedding BYTEA
)
""")
conn.commit()
for item in embeddings_data:
    filename = item.get("filename", "unknown.txt")
    text = item.get("text", "")
    emb = item.get("embedding", [])
    emb_bytes = pickle.dumps(emb)

    cur.execute(
        "INSERT INTO documents (filename, content, embedding) VALUES (%s, %s, %s)",
        (filename, text, emb_bytes)
    )
    print(f"Inserted: {filename}")
conn.commit()
cur.close()
conn.close()
print("All embeddings inserted successfully!")
