import json
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
embeddings_file = "embeddings_hf.json"
persist_directory = "chroma_db"
with open(embeddings_file, "r", encoding="utf-8") as f:
    data = json.load(f)
texts = [item["filename"] for item in data]
vectors = [item["embedding"] for item in data]
hf_embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectordb = Chroma(
    collection_name="my_texts",
    embedding_function=hf_embeddings,
    persist_directory=persist_directory
)
BATCH_SIZE = 5000
for i in range(0, len(texts), BATCH_SIZE):
    batch_texts = texts[i:i+BATCH_SIZE]
    batch_vectors = vectors[i:i+BATCH_SIZE]
    batch_metadatas = [{"source": t} for t in batch_texts]

    vectordb.add_texts(
        texts=batch_texts,
        metadatas=batch_metadatas,
        embeddings=batch_vectors
    )
    print(f"Inserted batch {i//BATCH_SIZE + 1} / {(len(texts) + BATCH_SIZE - 1)//BATCH_SIZE}")
vectordb.persist()
print(f"Chroma vector DB created successfully at '{persist_directory}'!")
