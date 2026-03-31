import os
import utils.consts as consts
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage

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


def InvokeWithWriteFile(prLLM, prPromptText):
    vrMessages = [HumanMessage(content=prPromptText)]

    for _ in range(5):
        vrResponse = prLLM.invoke(vrMessages)
        vrMessages.append(vrResponse)

        vrToolCalls = getattr(vrResponse, "tool_calls", []) or []

        if not vrToolCalls:
            return NormalizeMessageContent(vrResponse.content).strip()

        for vrToolCall in vrToolCalls:
            vrToolName = vrToolCall.get("name")
            vrToolArgs = vrToolCall.get("args", {})
            vrToolCallId = vrToolCall.get("id")

            if vrToolName != "WriteFile":
                vrToolResult = f"Tool não suportada: {vrToolName}"
            else:
                try:
                    vrToolResult = tools.WriteFile.invoke(vrToolArgs)
                except Exception as vrError:
                    vrToolResult = f"Erro ao executar WriteFile: {vrError}"

            vrMessages.append(ToolMessage(content=vrToolResult, tool_call_id=vrToolCallId))

    return "Não foi possível concluir a execução da tool WriteFile após múltiplas tentativas."


@tool
def WriteFile(prContent: str, prFileName: str) -> str:
    """
    Salva um arquivo no diretório de saída.

    Sempre use esta tool quando precisar salvar arquivos em disco.

    Args:
        prContent: Conteúdo do arquivo.
        prFileName: Nome do arquivo (ex: 'teste.txt').
    """

    vrFilePath = os.path.join(consts.PATH_OUTPUT, prFileName)
    os.makedirs(consts.PATH_OUTPUT, exist_ok=True)

    with open(vrFilePath, "w", encoding="utf-8") as vrFile:
        vrFile.write(prContent)

    return f"Arquivo gravado com sucesso: {vrFilePath}"
