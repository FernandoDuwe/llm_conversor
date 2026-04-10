import os
import utils.consts as consts

from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import (
    TextLoader,
    PyPDFLoader,
    Docx2txtLoader
)

def get_loader(file_path):
    _, ext = os.path.splitext(file_path)

    ext = ext.lower()

    if ext == ".txt":
        return TextLoader(file_path, encoding="latin-1")
    elif ext == ".pdf":
        return PyPDFLoader(file_path)
    elif ext in [".docx", ".doc"]:
        return Docx2txtLoader(file_path)
    else:
        return TextLoader(file_path, encoding="latin-1")

def config_retriever(doc_list):
    docs = []

    # 📄 leitura dos arquivos
    for file in doc_list:
        file_path = os.path.join(consts.PATH_INPUT, file)

        print(f"Lendo arquivo: {file_path}")

        loader = get_loader(file_path)
        docs.extend(loader.load())

    print("Efetuando split...")

    # ✂️ Split de documentos
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    splits = text_splitter.split_documents(docs)

    print("Gerando embeddings (Ollama)...")

    # 🧠 Embeddings via Ollama
    embeddings = OllamaEmbeddings(
        model=consts.MODEL_TYPE_OLLAMA_EMBEDDINGS
    )

    print("Armazenando no FAISS...")

    # 🗄️ Vector store
    vectorstore = FAISS.from_documents(splits, embeddings)

    vectorstore.save_local(consts.DATABASE_PATH)

    print("Configurando retriever...")

    # 🔍 Retriever
    retriever = vectorstore.as_retriever(
        search_type=consts.SEARCH_TYPE_MMR,
        search_kwargs={
            "k": consts.RETRIEVER_K,
            "fetch_k": consts.RETRIEVER_FETCH_K
        }
    )

    print("Retriever pronto!")

    return retriever