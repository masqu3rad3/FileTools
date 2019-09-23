#! /usr/bin/env python
import subprocess
import sys
import os
import getopt
import logging
import shutil
import json
import string
import win32api
# import warnings

logging.basicConfig()
logger = logging.getLogger('zBackHelper')
logger.setLevel(logging.WARNING)

class BackupHelper(object):
    def __init__(self):
        super(BackupHelper, self).__init__()
        self.selfDir = os.path.dirname(os.path.abspath(__file__))
        self.settingsFile = os.path.join(self.selfDir, "backupHelperConfig.json")
        self.settings = self._getSettings()

    def getdrivefromname(self, name):
        for char in string.ascii_uppercase:
            try:
                volumename = win32api.GetVolumeInformation("%s:\\" %char)[0]
                if volumename.lower() == name.lower():
                    drive, rest = os.path.splitdrive(self.targetRoot)
                    return os.path.join("%s:" %char, rest)
                    # return "%s:\\" %char
            except:
                pass
        print("Drive Letter cannot resolved. Aborting")
        return




    def _getSettings(self):
        """Gets settings from the settings file"""
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
        """Returns list of projects actively backing up on the nearline folder"""
        logger.debug("Func: _getProjectList")
        return self.settings["backupList"]
        pass

    def getRemainingSpace(self):
        """Returns the left gigabytes on the nearline drive"""
        logger.debug("Func: _getRemainingSpace")
        if not self.targetRoot:
            print("target root is not defined. use -t or --targetroot flags to define projects root")
            return
        total, used, free = shutil.disk_usage(self.targetRoot)
        totalAsGb = total // (2**30)
        usedAsGb = used // (2**30)
        freeAsGb = free // (2**30)
        drive=(os.path.splitdrive(self.targetRoot))[0]
        print ("Free Space in %s Drive= %s GB" %(drive, freeAsGb))
        return freeAsGb

    @property
    def projectsRoot(self):
        """returns defined projects root in the settings file"""
        return self.settings["projectsRoot"]

    @projectsRoot.setter
    def projectsRoot(self, absPath):
        """Sets the projects root and writes it on the settings file"""
        self.settings["projectsRoot"] = absPath
        self._dumpJson(self.settings, self.settingsFile)

    @property
    def targetRoot(self):
        """returns defined target root in the settings file"""
        return self.settings["targetRoot"]

    @targetRoot.setter
    def targetRoot(self, absPath):
        """Sets the target root and writes it on the settings file"""
        self.settings["targetRoot"] = absPath
        self._dumpJson(self.settings, self.settingsFile)

    @property
    def minimumDiskSpace(self):
        """Returns the minimum disk space value defined on the settings file"""
        return self.settings["minimumDiskSpace"]

    @minimumDiskSpace.setter
    def minimumDiskSpace(self, gigabytes):
        """Sets the minimum disk space and writes it on the settings file"""
        self.settings["minimumDiskSpace"] = gigabytes
        self._dumpJson(self.settings, self.settingsFile)

    @property
    def maximumNumberOfProjects(self):
        """Returns the maximum number of project on the settings file. 0 means unlimited"""
        return self.settings["maximumNumberOfProjects"]

    @maximumNumberOfProjects.setter
    def maximumNumberOfProjects(self, intValue):
        """Sets the maximum number of projects and writes it on the settings file"""
        self.settings["maximumNumberOfProjects"] = intValue
        self._dumpJson(self.settings, self.settingsFile)

    def addProject(self, folderPath, force=False):
        """Adds the project to the Nearline Backup List"""
        logger.debug("Func: addProject")
        if not os.path.isdir(folderPath):
            # in case the given path is relative
            folderPath = os.path.join(self.projectsRoot, folderPath)
            if not os.path.isdir(folderPath):
                print("%s is not a valid path" %folderPath)
                return

        listOfProjects = self.settings["backupList"]
        listOfProjects.append(folderPath)
        if int(self.settings["maximumNumberOfProjects"]) > 0 and len(listOfProjects) > int(self.settings["maximumNumberOfProjects"]):
            if force:
                oldestNearlineProject = listOfProjects[0]
                self.removeProject(oldestNearlineProject)
            else:
                print("Maximum Number of Projects limit reached. Use -r or --remove flags to remove old projects or increase the limit with -n or --maximumprojects flag\nAborting")
                return
        self._dumpJson(self.settings, self.settingsFile)

    def removeProject(self, folderPath):
        """Removes the project from the Nearline Backup"""
        logger.debug("Func: removeProject")
        if os.path.dirname(folderPath) is '': # if the path is not absolute make sure it is
            folderPath = os.path.join(self.projectsRoot, folderPath)

        listOfProjects = self.settings["backupList"]
        try:
            listOfProjects.remove(folderPath)
            backedUpCopy = self.isBackedup(folderPath)
            if backedUpCopy:
                shutil.rmtree(backedUpCopy)
                print("Deleted from Nearline Backup: %s" % backedUpCopy)
        except ValueError: print("%s is not in the backup list" %folderPath)
        self._dumpJson(self.settings, self.settingsFile)
        pass

    def executeBackup(self, force=False, drivebyname=None):
        logger.debug("Func: executeBackup")
        exeLocation = os.path.join(self.selfDir, "zBack")
        exeFile = os.path.join(exeLocation, "zback.exe")
        if not os.path.isfile(exeFile):
            print("zback.exe file cannot be found at %s.\nAborting") %exeLocation
            return

        if drivebyname:
            self.targetRoot = self.getdrivefromname(drivebyname)

        if not self.projectsRoot:
            print("projectsRoot is not defined. use -p or --projectroot flags to define projects root")
            return
        if not self.targetRoot:
            print("target root is not defined. use -t or --targetroot flags to define projects root")
            return
        if not self.getBackupList():
            print("Backup List is empty. use -a or --add flags to add project folders")

        if self.getRemainingSpace() < int(self.minimumDiskSpace):
            if force:
                # delete the oldest project from the list and give it another go
                oldestNearlineProject = self.getBackupList()[0]
                self.removeProject(oldestNearlineProject)
                backedUpCopy = self.isBackedup(oldestNearlineProject)
                if backedUpCopy:
                    shutil.rmtree(backedUpCopy)
                    print("Deleted from Nearline Backup: %s" %backedUpCopy)
                self.executeBackup(force=True)
            else:
                print("Remaining space at Target Volume is below specified minimum (%s)\n"
                      "Delete some projects from the nearline backup unit or change the minimum disk space tieh -d or --minimumdiskspace flags" %self.minimumDiskSpace)
                return

        balFile = self.createBalFile()

        # subprocess.Popen([exeFile, "%s" %balFile, "/Rs"], shell=True)


    def isBackedup(self, projectFolder):
        """
        Checks for the nearline backup folder of the given path.
        :param projectFolder: Project Path to look up. Can be relative or absolute
        :return: (String, None) returns the path of the paired nearline backup or none
        """
        if os.path.dirname(projectFolder) is not '': # if the path is absolute make sure to take its basename
            projectFolder = os.path.basename(projectFolder)
        targetFolder = os.path.join(self.targetRoot, projectFolder)
        if os.path.isdir(targetFolder):
            return targetFolder
        else:
            return

    def createBalFile(self):
        data = ""
        backupList = self.getBackupList()
        for x in backupList:
            line = "{0}\\*.* > {1} /us\n".format(x, os.path.join(self.targetRoot, os.path.basename(x)))
            data = "%s%s" %(data, line)

        balFile = os.path.join(os.path.dirname(os.path.abspath(__file__)), "nearlineBackup.bal")

        if os.path.isfile(balFile):
            backupFile = os.path.join(self.selfDir, "nearlineBackup.bak")
            print(backupFile)
            shutil.copyfile(balFile, backupFile)
            tempFile = "nearlineBackup_TMP.bal"
            f = open(tempFile, "w+")
            f.write(data)
            f.close()
            shutil.copyfile(tempFile, balFile)
            os.remove(tempFile)
        else:
            f = open(balFile, "w+")
            f.write(data)
            f.close()

        return balFile

    def help(self):
        logger.debug("Func: help")
        msg="""
usage: python nearlineBackup.py [-h] [-f] [-e] [-g]
                                [--add <Absolute or Relative Folder Path>]
                                [--remove <Absolute or Relative Folder Path>]
                                [--projectsroot <Absolute Path>]
                                [--targetroot <Absolute Path>]
                                [--drivebyname <String>]
                                [--minimumdiskspace <integer value>]
                                [--maximumprojects <integer value>]
                                [--isbackedup <Absolute or Relative Folder Path>]

-h, --help              show this help message and exit
-f, --force             force deleting folders in nearline unit if min. required space or maximum project count exceeded
-e, --execute           executes the backup progress
-g, --getlist           returns the backup list
-a, --add               add the project to the backup list
-r, --remove            remove the project from the backup list and delete it from the nearline unit
-p, --projectsroot      defines the source root of projects
-b, --drivebyname       target drive letter will resolved using this volume name
-t, --targetroot        defines the target root of nearline backups
-d, --minimumdiskspace  defines the minimum disk space required before executing a new backup.
-n, --maximumprojects   maximum number of projects kept in the nearline unit
-i, --isbackedup        checks if the given project backed up at the nearline unit. Returns the backup path if exists.                                
"""
        print(msg)

    def main(self, args):
        logger.debug("Func: main")
        opts, remainder = getopt.getopt(args, "a:r:ep:t:d:n:i:b:fhg", ["add=", "remove=", "execute", "projectsroot=", "targetroot=", "minimumdiskspace=", "maximumprojects=", "isbackedup=", "drivebyname=", "force", "help", "getlist"])

        if not opts:
            self.executeBackup()
            return

        if opts[0][0] in ("-h", "--help"):
            self.help()
            return

        force=False
        drivebyname=None
        #loop once to get force and drivebyname
        for opt, arg in opts:
            if opt in ("-f", "--force"):
                force = True
            if opt in ("-d", "--drivebyname"):
                drivebyname=arg


        for opt, arg in opts:
            if opt in ("-a", "--add"):
                self.addProject(arg, force=force)
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
            if opt in ("-i", "--isbackedup"):
                print(self.isBackedup(arg))
            if opt in ("-g", "--getlist"):
                print("\n".join(self.getBackupList()))
            # if opt in ("-f", "--force"):
            #     force=True
            if opt in ("-e", "--execute"):
                self.executeBackup(force=force, drivebyname=drivebyname)

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


