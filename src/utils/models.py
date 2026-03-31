import os
import utils.consts as consts
import utils.tools as tools
import utils.utils as utils
from operator import itemgetter
from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# Executa uma query com parâmetros e base de conhecimento, sem uso de ferramentas
def ExecuteFormArtifact(prForm, prArtifact, prDocumentation):
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
    vrVectorStore = utils.CreateVectorStore(prDocumentation)
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
        "form": prForm,
        "artifact": prArtifact
    }).strip()

    return vrResult

# Executa uma query simples, sem uso de ferramentas
def ExecuteQuery(prQuery):
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

    # --- NOVA ARQUITETURA LCEL (Substitui o RetrievalQA) ---
    # Esta cadeia faz o seguinte:
    # 1. Recupera documentos para o 'context' usando a query
    # 2. Passa a 'query' adiante
    # 3. Formata o prompt, envia ao LLM e extrai o texto
    vrChain = (
        {
            "query": RunnablePassthrough()
        }
        | vrPromptObj
        | vrLLM
        | StrOutputParser()
    )

    # Executando a cadeia
    vrResult = vrChain.invoke(prQuery).strip()

    return vrResult

# Executa uma query simples, com uso de ferramentas.
def ExecuteQueryWithTools(prQuery):
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
    ).bind_tools([tools.WriteFile])

    # Criando o prompt template
    # Importante: O LCEL preencherá 'context' e 'query' automaticamente
    vrPromptObj = PromptTemplate.from_template(vrPrompt)

    vrPromptValue = vrPromptObj.invoke({"query": prQuery})

    vrResult = tools.InvokeWithWriteFile(vrLLM, vrPromptValue.to_string())

    return vrResult