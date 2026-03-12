import os
import utils.consts as consts
import utils.extractor as extractor
import utils.models as models

def main():
    os.makedirs(consts.PATH_INPUT, exist_ok=True)
    os.makedirs(consts.PATH_OUTPUT, exist_ok=True)

    vrDocumentation = extractor.extract_text(consts.PATH_INPUT + "/de_para.md")
    vrForm = extractor.extract_text(consts.PATH_INPUT + "/Form.aspx")
    vrArtifact = extractor.extract_text(consts.PATH_INPUT + "/Artefato.xml")

    models.ExecuteToFile(vrForm, vrArtifact, vrDocumentation, consts.PATH_OUTPUT + "/resultado.xml")



if __name__ == "__main__":
    main()