#!/usr/bin/env python

class tt_wizard_core:
    import requests

    __LIST_PATH__ = "https://cdn.ravensburger.de/db/tiptoi.csv"

    __HEADER__={
            "Accept-Encoding": "gzip,deflate,sdch",
            "Accept-Language": "en-US,en;q=0.8",
            "User-Agent": "Chrome/33.0.1750.152",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive"}

    __mediaDict__ = {}

    __mediaNameList__ = []

    __penMountPoint__ = ""

    def __init__(self, penMountPoint: str = ""):
        """
        Contructor.

        (optional) param: String. Specifies path to storage location of gme files.
        """
        self.__penMountPoint__ = penMountPoint
        self.__mediaDict__ = {}
        self.__loadAvailableMedia__(self.__LIST_PATH__)

    def __loadAvailableMedia__(self, path: str):
        """ 
        Downloads csv of available gme-files from __LIST_PATH__ and decodes them into a dictionary, where title name is used as key.
        """
        response = self.requests.get(path, headers=self.__HEADER__)
        lines = response.content.splitlines()
        response.close()
        for line in lines:
            entries = line.decode('ISO-8859-1').split(',')
            url = entries[2]
            name = entries[3]
            if ".gme" in url:
                id = int(entries[0])
                version = int(entries[1])
                qualifiedName = (name + ".gme")
                self.__mediaNameList__.append(qualifiedName)
                self.__mediaDict__[qualifiedName] = (qualifiedName, url, id, version)
    
    def __isDateString__(self, dataBytes: bytes, position: int) -> bool:
        """
        Checks whether >>position<< is located at the end of 8 ASCII integers (i.e. the timestamp) or not.

        return: True/False
        """
        for index in range(position, position - 8, -1):
            if (dataBytes[index] >= 58) or (dataBytes[index] < 48):
                return False
        return True 

    def autoDetectPenMountPoint(self) -> bool:
        """
        Tries to find mount point of pen. If mount point is found, __penMountPoint__ is set to mount point path and True returned.

        return: True -- Bool. Mountpoint found.
                False -- Bool. Mountpoint NOT found.
        """
        import psutil
        for disk in psutil.disk_partitions():
            mnt = str(disk.mountpoint) + "/"
            if "tiptoi" in mnt.lower():
                self.__penMountPoint__ = mnt
                return True
        return False

    def setPenMountPoint(self, penMountPoint: str = ""):
        """ 
        Overwrites path to pen / download location. For example, to be used when auto detection fails.

        param: >>penMountPoint<< -- String. New path value.
        return: No return value.
        """
        # Check if mount path ends with slash or add slash if not.
        if penMountPoint[-1] == "/":
            self.__penMountPoint__ = penMountPoint
        else:
            self.__penMountPoint__ = penMountPoint + "/"

    def getAllAvailableTitles(self) -> list:
        """ 
        Return list of all titles that are available for download.

        return: [] -- List of String. List of titles (i.e. fileName + ".gme") that can be downloaded.
        """
        return self.__mediaNameList__
            
    def downloadMedia(self, fileNameList: list, filePath: str = None):
        """ 
        Downloads media files into specified folder location.

        param1: [fileNames] -- List of Strings. File name of title that shall be downloaded to specified path.
        param2: >>filePath<< -- (Optional) String. Path to download location.
        return: No return value.
        """
        if filePath is None:
            path = self.__penMountPoint__
        else:
            path = filePath
        for title in fileNameList:
            (qualifiedName, url, id, versionRemote) = self.__mediaDict__[title]
            response = self.requests.get(url, headers=self.__HEADER__)
            open((path + title), 'wb+').write(response.content)

####################################################
####################################################
#  ___   _   _  _  ___ ___ ___   _______  _  _ ___ #
# |   \ /_\ | \| |/ __| __| _ \ |_  / _ \| \| | __|#
# | |) / _ \| .` | (_ | _||   /  / / (_) | .` | _| #
# |___/_/ \_\_|\_|\___|___|_|_\ /___\___/|_|\_|___|#                                                 
############### WORK ON PROGESS ####################
####################################################

    def checkForUpdate(self, fileName, filePath=None):
        """
        Checks whether an update for title named >>fileName<<, which is stored at location >>filePath<<, is required or not.

        param1: >>fileName<< -- String. Name of file to check its update status.
        param2: >>filePath<< -- (Optional) String. Path to storage location of gme-files.
        return: TRUE -- Update is required.
                FALSE -- Update is NOT required.
        """ 
        if filePath is None:
            path = self.__penMountPoint__
        else:
            path = filePath
            
        with open((path + fileName), mode='rb') as file:
            fileContent = file.read()
        # search end of timestamp
        dataString = "CopyRight"
        arData = bytes(dataString, 'utf-8')
        firstDot = fileContent.find(arData)
        endOfVersion = fileContent[firstDot:].find(0) + firstDot - 1
        if (fileContent[endOfVersion] >= 58) or (fileContent[endOfVersion] < 48):
            for index in range(endOfVersion - 1, 8, -1):
                if self.__isDateString__(fileContent, index):
                    endOfVersion = index
                    break
        # extract timestamp
        versionLocal = (fileContent[endOfVersion] - 48) + \
                      ((fileContent[endOfVersion -1] - 48) * 10) + \
                      ((fileContent[endOfVersion - 2] - 48) * 100) + \
                      ((fileContent[endOfVersion - 3] - 48) * 1000) + \
                      ((fileContent[endOfVersion - 4] - 48) * 10000) + \
                      ((fileContent[endOfVersion - 5] - 48) * 100000) + \
                      ((fileContent[endOfVersion - 6] - 48) * 1000000) + \
                      ((fileContent[endOfVersion - 7] - 48) * 10000000)
        (qualifiedName, url, id, versionRemote) = self.__mediaDict__[fileName]
        # Theoretically updates should only be required, when versionRemote > versionLocal
        # but we are choosing the currently hosted version to be the golden master.
        # Hence, whenever a version mismatch is detected, an update is suggested. 
        if versionRemote != versionLocal:
            return True
        else:
            return False

    def performAutoUpdate(self, filePath=None, dryRun=False):
        """ 
        Iterates through all downloaded gme-files and updates all that are outdated

        param1: >>filePath<< -- (Optional) String. Path to storage location of gme-files.
        param2: >>dryRun<< -- (Optional) Bool. 
                If >>true<<: Evaluate which files require an update only (without downloading the updates). 
                If >>False<<: Perform evaluation and OVERWRITE old files with their update (default).
        return: a.) [] -- Empty list if no titles was updated.
                b.) [] -- List of all titles that received an update.
        """
        from os import listdir
        if filePath is None:
            path = self.__penMountPoint__
        else:
            path = filePath

        gmeFiles = [gme for gme in listdir(path) if "gme" in gme]
        updatedFiles = []

        for title in gmeFiles:
            if self.checkForUpdate(title, path):
                if dryRun is False:
                    self.downloadMedium(title, path)
                updatedFiles.append(title)
        return updatedFiles
