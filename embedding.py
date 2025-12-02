import os
from sentence_transformers import SentenceTransformer
import json
parsed_folder = r"C:\Users\malik\OneDrive\Desktop\YCG 1\parsed_text"  
chunked_folder = r"C:\Users\malik\OneDrive\Desktop\YCG 1\chunked_text_recursive"
os.makedirs(chunked_folder, exist_ok=True)
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
def chunk_text(text, size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    if not text:
        return []
    chunks = []
    start = 0
    while start < len(text):
        end = start + size
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start += size - overlap
    return chunks
def generate_embeddings(text_folder, output_file, model_name='all-MiniLM-L6-v2'):
    model = SentenceTransformer(model_name)
    all_embeddings = []
    for filename in os.listdir(text_folder):
        if filename.lower().endswith(".txt"):
            file_path = os.path.join(text_folder, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read().strip()
            if not text:
                continue
            chunks = chunk_text(text)
            for i, chunk in enumerate(chunks):
                embedding_vector = model.encode(chunk).tolist()
                chunk_name = f"{os.path.splitext(filename)[0]}_chunk{i+1}.txt"
                all_embeddings.append({
                    "filename": chunk_name,
                    "embedding": embedding_vector
                })
                chunk_path = os.path.join(chunked_folder, chunk_name)
                with open(chunk_path, "w", encoding="utf-8") as f_out:
                    f_out.write(chunk)
    with open(output_file, "w", encoding="utf-8") as f_out:
        json.dump(all_embeddings, f_out, ensure_ascii=False, indent=4)
    print(f" Chunking + Embeddings saved for {len(all_embeddings)} chunks in {output_file}")
if __name__ == "__main__":
    output_file = r"C:\Users\malik\OneDrive\Desktop\YCG 1\embeddings_hf.json"
    generate_embeddings(parsed_folder, output_file)
