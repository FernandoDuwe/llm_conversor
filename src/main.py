import os
import utils.consts as consts
import utils.extractor as extractor
import utils.models as models

def main():
    os.makedirs(consts.PATH_INPUT, exist_ok=True)
    os.makedirs(consts.PATH_OUTPUT, exist_ok=True)

    # Lendo o conteúdo dos arquivos de entrada
    vrPDFData = extractor.extract_pdf(consts.PATH_INPUT + "/analise_tecnica.pdf")
    vrTextData = extractor.extract_text(consts.PATH_INPUT + "/exemplo_codigo.py")

    # Processando
    vrPrompt = ""

    with open(consts.FILE_CONFIG_PROMPT_USER, 'r', encoding='utf-8') as vrFile:
        vrPrompt = vrFile.read()

    models.ExecuteToFile(vrPrompt, consts.PATH_OUTPUT + "/doc_user.md",  vrTextData, vrPDFData);

if __name__ == "__main__":
    main()