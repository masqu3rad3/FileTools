#! /usr/bin/env python
import sys
import os
import getopt
import logging
import shutil
import json
import warnings

logging.basicConfig()
logger = logging.getLogger('zBackHelper')
logger.setLevel(logging.DEBUG)

class BackupHelper(object):
    def __init__(self):
        super(BackupHelper, self).__init__()
        selfDir = os.path.dirname(os.path.abspath(__file__))
        self.settingsFile = os.path.join(selfDir, "backupHelperConfig.json")
        self.settings = self._getSettings()

    def _getSettings(self):
        logger.debug("Func: _getSettings")
        try:
            data = self._loadJson(self.settingsFile)
        except FileNotFoundError:
            data = {"projectsRoot": None,
                    "backupList": [],
                    "targetRoot": None,
                    "minimumDiskSpace": 200,
                    "maximumNumberOfProjects": 0}
            self._dumpJson(data, self.settingsFile)
        return data

    def getBackupList(self):
        logger.debug("Func: _getProjectList")
        return self.settings["backupList"]
        pass

    def getRemainingSpace(self):
        logger.debug("Func: _getRemainingSpace")
        pass

    @property
    def projectsRoot(self):
        return self.settings["projectsRoot"]

    @projectsRoot.setter
    def projectsRoot(self, absPath):
        self.settings["projectsRoot"] = absPath
        self._dumpJson(self.settings, self.settingsFile)

    @property
    def targetRoot(self):
        return self.settings["targetRoot"]

    @targetRoot.setter
    def targetRoot(self, absPath):
        self.settings["targetRoot"] = absPath
        self._dumpJson(self.settings, self.settingsFile)

    @property
    def minimumDiskSpace(self):
        return self.settings["minimumDiskSpace"]

    @minimumDiskSpace.setter
    def minimumDiskSpace(self, gigabytes):
        self.settings["minimumDiskSpace"] = gigabytes
        self._dumpJson(self.settings, self.settingsFile)

    @property
    def maximumNumberOfProjects(self):
        return self.settings["maximumNumberOfProjects"]

    @maximumNumberOfProjects.setter
    def maximumNumberOfProjects(self, intValue):
        self.settings["maximumNumberOfProjects"] = intValue
        self._dumpJson(self.settings, self.settingsFile)

    def addProject(self, folderPath):
        logger.debug("Func: addProject")
        if not os.path.isdir(folderPath):
            warnings.warn("%s is not a valid path" %folderPath)

        listOfProjects = self.settings["backupList"]
        listOfProjects.append(folderPath)
        self._dumpJson(self.settings, self.settingsFile)
        pass

    def removeProject(self, folderPath):
        logger.debug("Func: removeProject")
        listOfProjects = self.settings["backupList"]
        try: listOfProjects.remove(folderPath)
        except ValueError: warnings.warn("%s is not in the backup list" %folderPath)
        pass

    def executeBackup(self):
        logger.debug("Func: executeBackup")
        if not self.projectsRoot or not self.targetRoot or self.getBackupList() is []:
            warnings.warn("projectsRoot is not defined. use -p or --projectroot flags to define projects root")
            return
        if not self.targetRoot:
            warnings.warn("target root is not defined. use -t or --targetroot flags to define projects root")
            return
        if self.getBackupList() is []:
            warnings.warn("Backup List is empty. use -a or --add flags to add project folders")


        pass

    def help(self):
        logger.debug("Func: help")
        pass

    def main(self, args):
        logger.debug("Func: main")
        opts, remainder = getopt.getopt(args, "a:r:ep:t:h", ["add=", "remove=", "execute", "projectsroot=", "targetroot=", "help"])

        if not opts:
            self.executeBackup()
            return
        if opts[0][0] in ("-h", "--help"):
            self.help()
            return
        for opt, arg in opts:
            if opt in ("-a", "--add"):
                self.addProject(arg)
            if opt in ("-r", "--remove"):
                self.removeProject(arg)
            if opt in ("-p", "--projectsroot"):
                self.projectsRoot = arg
            if opt in ("-t", "--targetroot"):
                self.targetRoot = arg
            if opt in ("-d", "--minimumdiskspace"):
                self.minimumDiskSpace = arg
            if opt in ("-n", "--maximumprojects"):
                self.maximumNumberOfProjects = arg
            if opt in ("e", "--execute"):
                self.executeBackup()

    def _loadJson(self, file):
        try:
            with open(file, 'r') as f:
                data = json.load(f)
                return data
        except ValueError:
            msg = "Corrupted JSON file => %s" % file
            print(msg)
            raise ValueError

    def _dumpJson(self, data, file):
        """Saves the data to the json file"""
        name, ext = os.path.splitext(file)
        tempFile = ("{0}.tmp".format(name))
        with open(tempFile, "w") as f:
            json.dump(data, f, indent=4)
        shutil.copyfile(tempFile, file)
        os.remove(tempFile)

if __name__ == '__main__':
    backup = BackupHelper()
    backup.main(sys.argv[1:])


