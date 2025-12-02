import os
parsed_folder = r"C:\Users\malik\OneDrive\Desktop\YCG 1\parsed_text"
chunked_folder = r"C:\Users\malik\OneDrive\Desktop\YCG 1\chunked_text"
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
for filename in os.listdir(parsed_folder):
    if filename.lower().endswith(".txt"):
        file_path = os.path.join(parsed_folder, filename)
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
        chunks = chunk_text(text)
        for i, chunk in enumerate(chunks):
            chunk_filename = f"{os.path.splitext(filename)[0]}_chunk{i+1}.txt"
            chunk_path = os.path.join(chunked_folder, chunk_filename)
            with open(chunk_path, "w", encoding="utf-8") as f_out:
                f_out.write(chunk)
print(f"Chunking complete! All chunks saved in {chunked_folder}")