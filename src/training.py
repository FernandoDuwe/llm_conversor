import os
import utils.consts as consts
import utils.rag_utils as imports

fileList = os.listdir(consts.PATH_INPUT)

fileToRead = []

for row in fileList:
    nome, extensao = os.path.splitext(row)

    fileToRead.append(row)

if (len(fileToRead) > 0):
    imports.config_retriever(fileToRead)