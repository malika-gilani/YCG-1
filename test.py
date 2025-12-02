from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
hf_embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectordb = Chroma(
    collection_name="my_texts",
    persist_directory="chroma_db",
    embedding_function=hf_embeddings
)
print("Type 'exit' to quit.\n")
while True:
    user_query = input("Enter your question: ")
    if user_query.lower() == "exit":
        break
    results = vectordb.similarity_search(user_query, k=3)
    if results:
        print("\nTop matching PDF content:\n")
        for idx, r in enumerate(results, 1):
            text_snippet = r.page_content[:300] + ("..." if len(r.page_content) > 300 else "")
            source = r.metadata.get("source", "unknown")
            print(f"{idx}. Source: {source}\n{text_snippet}\n")
    else:
        print("No matching content found.\n")
