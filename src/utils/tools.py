import os
import utils.consts as consts
from langchain_core.tools import tool

@tool
def WriteFile(prContent: str, prFileName: str) -> str:
    """
    Grava um arquivo no diretório de saída.

    Sempre use esta tool quando precisar gravar arquivos em disco.

    Args:
        prContent: Conteúdo do arquivo.
        prFileName: Nome do arquivo (ex: 'teste.txt').
    """
    
    vrFilePath = os.path.join(consts.PATH_OUTPUT, prFileName)
    os.makedirs(consts.PATH_OUTPUT, exist_ok=True)

    with open(vrFilePath, "w", encoding="utf-8") as vrFile:
        vrFile.write(prContent)

    return f"Arquivo gravado com sucesso: {vrFilePath}"
