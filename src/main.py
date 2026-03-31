import os
import utils.consts as consts
import utils.extractor as extractor
import utils.models as models

def main():
    os.makedirs(consts.PATH_INPUT, exist_ok=True)
    os.makedirs(consts.PATH_OUTPUT, exist_ok=True)

    vrData = models.ExecuteQuery("Explique como funciona a sequência de fibonacci. Salve a resposta em um arquivo de texto.")

    print(vrData)

if __name__ == "__main__":
    main()