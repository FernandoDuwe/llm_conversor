import os
import utils.consts as consts
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter

def CreateVectorStore(prText):
    vrTextSplitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100
    )
    vrChunks = vrTextSplitter.split_text(prText)
    
    # Certifique-se que o modelo de embeddings está baixado no Ollama
    vrEmbeddings = OllamaEmbeddings(
        model=consts.MODEL_TYPE_OLLAMA_EMBEDDINGS,
        base_url=consts.PATH_OLLAMA
    )
    
    vrVectorStore = FAISS.from_texts(vrChunks, vrEmbeddings)
    return vrVectorStore

def SaveMessageToFile(prMessage, prFileName):
    vrFilePath = os.path.join(consts.PATH_OUTPUT, prFileName)
    os.makedirs(consts.PATH_OUTPUT, exist_ok=True)

    with open(vrFilePath, "w", encoding="utf-8") as vrFile:
        vrFile.write(prMessage)

def CleanOutputDirectory():
    if os.path.exists(consts.PATH_OUTPUT):
        for filename in os.listdir(consts.PATH_OUTPUT):
            file_path = os.path.join(consts.PATH_OUTPUT, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)