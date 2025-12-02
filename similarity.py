import os
import warnings
from langchain_community.document_loaders import PyPDFLoader
from langchain_classic.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.base import init_embeddings
from langchain_community.vectorstores import FAISS
from langchain_classic.prompts import PromptTemplate
from langchain.chat_models.base import init_chat_model
from dotenv import load_dotenv
load_dotenv()
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
warnings.filterwarnings("ignore")
OPENAI_API_KEY = os.getenv("API_KEY")
embeddings = init_embeddings(
    model="openai:text-embedding-3-small",
    openai_api_key=OPENAI_API_KEY
)
pdf_folder = r"C:\Users\malik\OneDrive\Desktop\YCG 1\pdfs"
all_docs = []
for filename in os.listdir(pdf_folder):
    if filename.endswith(".pdf"):
        loader = PyPDFLoader(os.path.join(pdf_folder, filename))
        docs = loader.load()
        for d in docs:
            d.metadata["source_pdf"] = filename
        all_docs.extend(docs)
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)
split_docs = text_splitter.split_documents(all_docs)
faiss_path = r"C:\Users\malik\OneDrive\Desktop\YCG 1\faiss_index"
if os.path.exists(faiss_path):
    vectorstore = FAISS.load_local(
        faiss_path,
        embeddings,
        allow_dangerous_deserialization=True
    )
    print("Loaded existing FAISS index from disk.")
else:
    print("Creating new FAISS index (this may take a few minutes)...")
    vectorstore = FAISS.from_documents(split_docs, embeddings)
    vectorstore.save_local(faiss_path)
    print("FAISS index created and saved to disk.")
llm = init_chat_model(
    model="gpt-4o-mini",
    openai_api_key=OPENAI_API_KEY,
)
prompt = PromptTemplate(
    template="""
Use the following context to answer the question.
Context:
{context}
Question: {question}
Answer:
Note: If there are no relevant chunks in the PDFs, display "Sorry, no relevant chunks found in the folder."
""",
    input_variables=["context", "question"]
)
print("\nType 'exit' to quit.\n")
while True:
    question = input("Enter your question: ").strip()
    if question.lower() == "exit":
        print("Exiting program. Goodbye!")
        break
    docs_and_scores = vectorstore.similarity_search_with_score(question, k=5)
    threshold = 0.3  
    filtered_docs = [doc for doc, score in docs_and_scores if score >= threshold]
    if filtered_docs:
        pdf_answer = " ".join([d.page_content.strip().replace("\n", " ") for d in filtered_docs])
        source_pdfs = ", ".join(list({d.metadata.get("source_pdf", "Unknown PDF") for d in filtered_docs}))
        context = pdf_answer
        print("-----------------------")
        print("PDF Extracted Answer")
        print("-----------------------")
        print(pdf_answer)
    else:
        context = "" 
        print("\n-----------------------")
        print("Sorry, no relevant chunks found in the folder.")
        print("-----------------------")
    full_prompt = prompt.format(context=context, question=question)
    gpt_answer = llm.invoke(full_prompt)
    print("\n-----------------------")
    print("GPT Generated Answer")
    print("-----------------------")
    print(gpt_answer.content if hasattr(gpt_answer, "content") else gpt_answer)
    print("\n=======================\n")
