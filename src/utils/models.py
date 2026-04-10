import os
import utils.consts as consts
import utils.tools as tools
import utils.utils as utils
from operator import itemgetter
from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser


def FormatRetrievedDocs(prDocs):
    if not prDocs:
        return ""

    return "\n\n".join(
        getattr(vrDoc, "page_content", str(vrDoc))
        for vrDoc in prDocs
    )

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
def ExecuteQueryWithTools(prQuery, prPrompt = consts.FILE_CONFIG_PROMPT):
    if (consts.MODE_DEBUG):
        print("DEBUG: Executando ExecuteQueryWithTools com a query:")
        print(prQuery)
        print("DEBUG: Usando o prompt do arquivo:")
        print(prPrompt)
        print("DEBUG: Configurações do modelo:")
        print(f"  Modelo: {consts.MODEL_TYPE_OLLAMA}")
        print(f"  Temperatura: {consts.TEMPERATURE_LOW_CREATIVITY}")
        print(f"  Top P: {consts.TOP_P}")
        print(f"  Top K: {consts.TOP_K}")
        print(f"  Path Ollama: {consts.PATH_OLLAMA}")

    # Lendo o prompt do arquivo
    with open(prPrompt, 'r', encoding='utf-8') as vrFile:
        vrPrompt = vrFile.read()

    # Configurando o ChatOllama
    vrLLM = ChatOllama(
        model=consts.MODEL_TYPE_OLLAMA, 
        temperature=consts.TEMPERATURE_LOW_CREATIVITY, 
        top_p=consts.TOP_P, 
        top_k=consts.TOP_K, 
        base_url=consts.PATH_OLLAMA #  
        # num_predict=consts.MAX_NEW_TOKENS_LONG
    ).bind_tools([tools.WriteFile, tools.CallSubAgent])

    # Criando o prompt template
    # Importante: O LCEL preencherá 'context' e 'query' automaticamente
    vrPromptObj = PromptTemplate.from_template(vrPrompt)

    vrPromptValue = vrPromptObj.invoke({"query": prQuery})

    vrResult = tools.InvokeWithTools(vrLLM, vrPromptValue.to_string())

    return vrResult

# Executa uma query simples, com uso de ferramentas e RAG.
def ExecuteQueryWithToolsWithRAG(prQuery, prPrompt = consts.FILE_CONFIG_PROMPT):
    if (consts.MODE_DEBUG):
        print("DEBUG: Executando ExecuteQueryWExecuteQueryWithToolsWithRAGthTools com a query:")
        print(prQuery)
        print("DEBUG: Usando o prompt do arquivo:")
        print(prPrompt)
        print("DEBUG: Configurações do modelo:")
        print(f"  Modelo: {consts.MODEL_TYPE_OLLAMA}")
        print(f"  Temperatura: {consts.TEMPERATURE_LOW_CREATIVITY}")
        print(f"  Top P: {consts.TOP_P}")
        print(f"  Top K: {consts.TOP_K}")
        print(f"  Path Ollama: {consts.PATH_OLLAMA}")

    # Lendo o prompt do arquivo
    with open(prPrompt, 'r', encoding='utf-8') as vrFile:
        vrPrompt = vrFile.read()

    # Configurando o ChatOllama
    vrLLM = ChatOllama(
        model=consts.MODEL_TYPE_OLLAMA, 
        temperature=consts.TEMPERATURE_LOW_CREATIVITY, 
        top_p=consts.TOP_P, 
        top_k=consts.TOP_K, 
        base_url=consts.PATH_OLLAMA #  
        # num_predict=consts.MAX_NEW_TOKENS_LONG
    ).bind_tools([tools.WriteFile, tools.CallSubAgent])

    vrVectorStore = utils.LoadVectorStore()

    # Criando o prompt template
    # Importante: O LCEL preencherá 'context' e 'query' automaticamente
    vrPromptObj = PromptTemplate.from_template(vrPrompt)

    vrContext = ""
    if vrVectorStore is not None:
        vrRetriever = vrVectorStore.as_retriever(
            search_type=consts.SEARCH_TYPE_MMR,
            search_kwargs={
                "k": consts.RETRIEVER_K,
                "fetch_k": consts.RETRIEVER_FETCH_K
            }
        )
        vrContext = FormatRetrievedDocs(vrRetriever.invoke(prQuery))

    vrPromptValue = vrPromptObj.invoke({
        "context": vrContext,
        "query": prQuery
    })

    vrResult = tools.InvokeWithTools(vrLLM, vrPromptValue.to_string())

    return vrResult