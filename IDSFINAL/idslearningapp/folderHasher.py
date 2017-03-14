
import os
import hashingclass

class FolderHasher:
    def __init__(self,_hashFile,_folderPath=None):

        self.hashFile = _hashFile
        self.folderPath = _folderPath

        self.curFileIndex=0
        self.filePathList=[]
        self.fileHashList=[]

    def addFilesToValidHashList(self):
        hasher = hashingclass.HashChecker(self.hashFile)
        with open(self.hashFile,'a') as f:
            for fileName in os.listdir(self.folderPath):
                if os.path.isdir(os.path.join(self.folderPath,fileName)):
                    continue
               # print(fileName)
                filePath = str(self.folderPath) + "/" + fileName

                f.write(hasher.getHash(filePath)+"\n")
        f.close()

    def addSingleFileToValidHashList(self,_filepath):
        hasher = hashingclass.HashChecker(self.hashFile)
        with open(self.hashFile, 'a') as f:
            f.write(hasher.getHash(_filepath) + "\n")
        f.close()



    def getFilesInFolder(self):
        outputList=[]
        for fileName in os.listdir(self.folderPath):
            if os.path.isdir(os.path.join(self.folderPath, fileName)):
                continue
            #print(fileName)
            filePath=str(self.folderPath)+"/"+fileName
            #print(filePath)
            outputList.append(filePath)

        return outputList

    def getFileNamesInFolder(self):
        outputList = []
        for fileName in os.listdir(self.folderPath):
            outputList.append(fileName)
        return outputList


    def getHashesInFolder(self):
        outputList = []
        hasher=hashingclass.HashChecker(self.hashFile)
        for fileName in os.listdir(self.folderPath):
            if os.path.isdir(os.path.join(self.folderPath, fileName)):
                continue
            filePath = str(self.folderPath) + "/" + fileName
            outputList.append(hasher.getHash(filePath))

        return outputList

    def getValidationInFolder(self):
        outputList = []
        hasher=hashingclass.HashChecker(self.hashFile)
        for fileName in os.listdir(self.folderPath):
            if os.path.isdir(os.path.join(self.folderPath, fileName)):
                continue
            filePath = str(self.folderPath) + "/" + fileName
            outputList.append(hasher.validate(filePath))

        return outputList







