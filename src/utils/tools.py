import os
import utils.models as models
import utils.consts as consts
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage


def NormalizeMessageContent(prContent):
    if isinstance(prContent, str):
        return prContent

    if isinstance(prContent, list):
        vrParts = []
        for vrPart in prContent:
            if isinstance(vrPart, dict) and vrPart.get("type") == "text":
                vrParts.append(vrPart.get("text", ""))
        return "\n".join(vrParts).strip()

    return str(prContent)


def FormatRetrievedDocs(prDocs):
    if not prDocs:
        return ""

    return "\n\n".join(
        getattr(vrDoc, "page_content", str(vrDoc))
        for vrDoc in prDocs
    )


def ResolvePromptFile(prPromptFile: str) -> str:
    vrPromptFile = (prPromptFile or "").strip()
    vrConfigDirectory = os.path.abspath("./config")

    if not vrPromptFile:
        return os.path.abspath(consts.FILE_CONFIG_PROMPT)

    if os.path.isabs(vrPromptFile):
        vrResolvedPath = os.path.abspath(vrPromptFile)
    else:
        if not vrPromptFile.endswith(".txt"):
            vrPromptFile += ".txt"
        vrResolvedPath = os.path.abspath(os.path.join(vrConfigDirectory, vrPromptFile))

    if os.path.commonpath([vrConfigDirectory, vrResolvedPath]) != vrConfigDirectory:
        raise ValueError("O prompt informado deve estar dentro do diretório ./config.")

    if not os.path.isfile(vrResolvedPath):
        raise FileNotFoundError(f"Prompt não encontrado: {vrPromptFile}")

    return vrResolvedPath


def BuildRagContext(prQuery: str) -> str:
    import utils.utils as utils

    vrVectorStore = utils.LoadVectorStore()
    if vrVectorStore is None:
        return ""

    vrRetriever = vrVectorStore.as_retriever(
        search_type=consts.SEARCH_TYPE_MMR,
        search_kwargs={
            "k": consts.RETRIEVER_K,
            "fetch_k": consts.RETRIEVER_FETCH_K
        }
    )

    return FormatRetrievedDocs(vrRetriever.invoke(prQuery))


def InvokeWithTools(prLLM, prPromptText, prSupportedTools=None):
    vrMessages = [HumanMessage(content=prPromptText)]

    if prSupportedTools is None:
        prSupportedTools = {
            "WriteFile": WriteFile,
            "CallSubAgent": CallSubAgent
        }

    for i in range(consts.EXECUTION_TOOLS_TIMES):
        vrResponse = prLLM.invoke(vrMessages)
        vrMessages.append(vrResponse)

        if (consts.MODE_DEBUG):
            print("Execução: ", i, " ...............................")
            print(type(vrResponse))
            print(type(vrMessages))

        vrToolCalls = getattr(vrResponse, "tool_calls", []) or []

        if not vrToolCalls:
            if (consts.MODE_DEBUG):
                print("tools_calls vazio, retornando resposta final.")

            return NormalizeMessageContent(vrResponse.content).strip()

        for vrToolCall in vrToolCalls:
            vrToolName = vrToolCall.get("name")
            vrToolArgs = vrToolCall.get("args", {})
            vrToolCallId = vrToolCall.get("id")

            if (consts.MODE_DEBUG):
                print(f"Tool chamada: {vrToolName} com args: {vrToolArgs}")

            vrToolFunction = prSupportedTools.get(vrToolName)
            if vrToolFunction is None:
                vrToolResult = f"Tool não suportada: {vrToolName}"
            else:
                try:
                    vrToolResult = vrToolFunction.invoke(vrToolArgs)
                except Exception as vrError:
                    vrToolResult = f"Erro ao executar {vrToolName}: {vrError}"

            vrMessages.append(ToolMessage(content=str(vrToolResult), tool_call_id=vrToolCallId))

    return "Não foi possível concluir a execução das tools após múltiplas tentativas."


def InvokeWithWriteFile(prLLM, prPromptText):
    return InvokeWithTools(
        prLLM,
        prPromptText,
        prSupportedTools={"WriteFile": WriteFile}
    )


@tool
def WriteFile(prContent: str, prFileName: str) -> str:
    """
    Salva um arquivo no diretório de saída.

    Sempre use esta tool quando precisar salvar arquivos em disco.

    Args:
        prContent: Conteúdo do arquivo.
        prFileName: Nome do arquivo (ex: 'teste.txt').
    """

    vrFilePath = os.path.join(consts.PATH_OUTPUT + "/", prFileName)

    if (consts.MODE_DEBUG):
        print(f"WriteFile chamado com prContent: {prContent} e prFileName: {prFileName}. Arquivo: {vrFilePath}")

    os.makedirs(consts.PATH_OUTPUT, exist_ok=True)

    with open(vrFilePath, "a", encoding="utf-8") as vrFile:
        vrFile.write(prContent)

    return f"Arquivo gravado com sucesso: {vrFilePath}"


@tool
def CallSubAgent(
    prQuery: str,
    prPromptFile: str = "prompt.txt",
    prUseRag: bool = True,
) -> str:
    """
    Chama um subagente especializado com um prompt do diretório ./config.

    Use esta tool para delegar uma tarefa para outro agente com instruções específicas,
    como `prompt_decorator.txt`, `prompt_convert.txt` ou `prompt_files.txt`.

    Args:
        prQuery: Solicitação principal que o subagente deve executar.
        prPromptFile: Nome do prompt especializado dentro de ./config.
        prUseRag: Indica se o subagente deve buscar contexto no FAISS.
    """
    
    if (prUseRag):
        models.ExecuteQueryWithToolsWithRAG(prQuery, prPromptFile)

    if (not prUseRag):
        models.ExecuteQueryWithTools(prQuery, prPromptFile)