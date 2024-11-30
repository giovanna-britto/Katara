import os
from PyPDF2 import PdfReader
from pinecone import Pinecone, ServerlessSpec
from langchain_openai import OpenAIEmbeddings  # Updated import
from dotenv import load_dotenv

load_dotenv()

api_key_from_env = os.getenv("PINECONE_API_KEY")
pc = Pinecone(api_key=api_key_from_env)

index_name = "agriculture-data"

if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=1536,
        metric='euclidean',
        spec=ServerlessSpec(
            cloud='aws',
            region='us-east-1' 
        )
    )

index = pc.Index(index_name)

openai_api_key = os.getenv("OPENAI_API_KEY") 
embeddings = OpenAIEmbeddings(model="text-embedding-3-small", openai_api_key=openai_api_key) 

def extract_text_from_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def index_pdf(file_path, document_id_prefix="doc"):
    print(f"Processando arquivo: {file_path}")
    text = extract_text_from_pdf(file_path)
    chunks = [text[i:i+500] for i in range(0, len(text), 500)] 
    
    for i, chunk in enumerate(chunks):
        vector = embeddings.embed_query(chunk)  
        doc_id = f"{document_id_prefix}_{i}"    
        index.upsert([(doc_id, vector, {"content": chunk})])  

    print(f"Arquivo {file_path} indexado com sucesso! Total de chunks: {len(chunks)}")

pdf_files = [
    "../assets/manual_cultivo_milho.pdf",
    "../assets/manual_cultivo_milho.pdf",
    "../assets/manual_cultivo_milho.pdf"
]

for file_path in pdf_files:
    index_pdf(file_path, document_id_prefix=os.path.basename(file_path).split(".")[0])