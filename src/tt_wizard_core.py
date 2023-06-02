#!/usr/bin/env python

class tt_wizard_core:
    import requests

    LIST_PATH = "https://cdn.ravensburger.de/db/tiptoi.csv"

    __HEADER__={
            "Accept-Encoding": "gzip,deflate,sdch",
            "Accept-Language": "en-US,en;q=0.8",
            "User-Agent": "Chrome/33.0.1750.152",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive"}

    __mediaDict = {}

    __downloadPath = ""

    def __init__(self, downloadPath = ""):
        self.__downloadPath = downloadPath
        self.__mediaDict = {}
        self.__getAvailableMedia(self.LIST_PATH)

    def __getAvailableMedia(self, path):
        response = self.requests.get(path, headers=self.__HEADER__)
        lines = response.content.splitlines()
        response.close()
        self.__mediaList = []
        for line in lines:
            entries = line.decode('ISO-8859-1').split(',')
            url = entries[2]
            name = entries[3]
            if ".gme" in url:
                id = int(entries[0])
                version = int(entries[1])
                qualifiedName = (name + ".gme")
                self.__mediaDict[qualifiedName] = (qualifiedName, url, id, version)
        
    def searchEntry(self, searchString):
        result = []
        for item in self.__mediaDict.keys():
            qualifiedName, url, id, version = self.__mediaDict[item] 
            if searchString.upper() in qualifiedName.upper():
                result.append(item)
        return result
        
    def downloadMedium(self, fileName):
        #qualifiedName, url, id, version = medium
        #filename = url.split('/')[-1]
        #filename = str(qualifiedName)
        (qualifiedName, url, id, versionRemote) = self.__mediaDict[fileName]
        print(f"Downloading: {fileName}")
        response = self.requests.get(url, headers=self.__HEADER__)
        open((self.__downloadPath + fileName), 'wb').write(response.content)

    def checkForUpdate(self, filePath, fileName):
        with open((filePath + fileName), mode='rb') as file:
            fileContent = file.read()
        #version = fileContent[82:90]
        versionLocal = (fileContent[89] - 48) + \
                      ((fileContent[88] - 48) * 10) + \
                      ((fileContent[87] - 48) * 100) + \
                      ((fileContent[86] - 48) * 1000) + \
                      ((fileContent[85] - 48) * 10000) + \
                      ((fileContent[84] - 48) * 100000) + \
                      ((fileContent[83] - 48) * 1000000) + \
                      ((fileContent[82] - 48) * 10000000)
        (qualifiedName, url, id, versionRemote) = self.__mediaDict[fileName]
        # Theoretically updates should only be required, when versionRemote > versionLocal
        # but we are choosing the currently hosted version to be the golden master.
        # Hence, whenever a version mismatch is detected, an update is suggested. 
        if versionRemote != versionLocal:
            print(f"Local Version: {versionLocal} vs. Remote Version: {versionRemote}")
            return True
        else:
            return False