import os
import utils.consts as consts
from operator import itemgetter
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

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

def Execute(prForm, prArtifact, prDocumentation):
    # Lendo o prompt do arquivo
    with open(consts.FILE_CONFIG_PROMPT, 'r', encoding='utf-8') as vrFile:
        vrPrompt = vrFile.read()

    # Configurando o ChatOllama
    vrLLM = ChatOllama(
        model=consts.MODEL_TYPE_OLLAMA, 
        temperature=consts.TEMPERATURE_LOW_CREATIVITY, 
        top_p=consts.TOP_P, 
        top_k=consts.TOP_K, 
        base_url=consts.PATH_OLLAMA #  
        # num_predict=consts.MAX_NEW_TOKENS_LONG
    )

    # Criando o prompt template
    # Importante: O LCEL preencherá 'context' e 'query' automaticamente
    vrPromptObj = PromptTemplate.from_template(vrPrompt)

    # Criando a base de conhecimento
    vrVectorStore = CreateVectorStore(prDocumentation)
    vrRetriever = vrVectorStore.as_retriever()

    # --- NOVA ARQUITETURA LCEL (Substitui o RetrievalQA) ---
    # Esta cadeia faz o seguinte:
    # 1. Recupera documentos para o 'context' usando a query
    # 2. Passa a 'query' adiante
    # 3. Formata o prompt, envia ao LLM e extrai o texto
    vrChain = (
        {
            "context": itemgetter("form") | vrRetriever,
            "form": itemgetter("form"),
            "artifact": itemgetter("artifact")
        }
        | vrPromptObj
        | vrLLM
        | StrOutputParser()
    )

    # Executando a cadeia
    vrResult = vrChain.invoke({
        "form": "Teste",
        "artifact": "Teste"
    }).strip()

    return vrResult

def ExecuteToFile(prForm, prArtifact, prDocumentation, prFileName):  
    vrResult = Execute(prForm, prArtifact, prDocumentation)

    if os.path.exists(prFileName):
        os.remove(prFileName)

    with open(prFileName, "w", encoding="utf-8") as vrFile:
        vrFile.write(vrResult)