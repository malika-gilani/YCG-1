import psycopg2
import numpy as np
import pickle
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
cur.execute("""
CREATE TABLE IF NOT EXISTS documents (
    id SERIAL PRIMARY KEY,
    content TEXT,
    embedding BYTEA
)
""")
conn.commit()
text = "This is a sample text to store in the database."
emb = np.random.rand(384).tolist()  
emb_bytes = pickle.dumps(emb)
cur.execute(
    "INSERT INTO documents (content, embedding) VALUES (%s, %s)",
    (text, emb_bytes)
)
conn.commit()
print("Text and embedding inserted successfully!")
cur.close()
conn.close()
