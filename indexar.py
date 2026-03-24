import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings

# Configurações de Caminho
PDF_PATH = "docs/artigo_ia.pdf"
DB_DIR = "./banco_vetorial"

def preparar_banco():
    # 1. Verificação de Segurança
    if not os.path.exists(PDF_PATH):
        print(f"❌ Erro: O arquivo {PDF_PATH} não foi encontrado!")
        return

    print(f"📂 Carregando documento: {PDF_PATH}...")
    loader = PyPDFLoader(PDF_PATH)
    paginas = loader.load()

    # 2. Divisão inteligente (Chunking)
    print(f"✂️ Dividindo {len(paginas)} páginas em blocos de texto...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, 
        chunk_overlap=150 # Aumentei um pouco para melhorar o contexto da V2
    )
    docs = text_splitter.split_documents(paginas)

    # 3. Vetorização com Hardware Local (Sua RTX 2060)
    print(f"🧠 Iniciando vetorização com Ollama (Llama 3)...")
    print("⏳ Isso pode levar alguns segundos dependendo do hardware.")
    
    embeddings = OllamaEmbeddings(model="llama3")
    
    # Criando o banco
    vector_db = Chroma.from_documents(
        documents=docs, 
        embedding=embeddings, 
        persist_directory=DB_DIR
    )
    
    print(f"✅ Sucesso! Banco criado com {len(docs)} fragmentos na pasta '{DB_DIR}'.")

if __name__ == "__main__":
    preparar_banco()