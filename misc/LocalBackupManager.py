from PyQt5.QtWidgets import QApplication, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QFileDialog, QComboBox, QMessageBox, QScrollArea
import yaml
import os
import sys
import shutil
from hurry.filesize import size
import datetime

class CustomWidgets(QWidget):
    # this is copy-paste from the internet with modifications

    def __init__(self) -> None:
        super().__init__() 
    
    def openDirDialog(self, startingDir=os.path.expanduser("~")):
        dir = QFileDialog.getExistingDirectory(self, "Please select a directory (ᵔᴥᵔ)", directory=startingDir)
        
        return dir
    
    def openFileNamesDialog(self, startingDir=os.path.expanduser("~")):
        files = QFileDialog.getOpenFileNames(self,"Please select files ʕ•ᴥ•ʔ", directory=startingDir)

        # files[0] is a list of the paths, files[1] is some additional info
        return files[0]
    
    def resetPopup(self):
        ret = QMessageBox.critical(self, "Reset config", "Warning! \nThis will delete all file paths, directories and meta data in the current config file. \nThis can not be undone!", QMessageBox.Cancel | QMessageBox.Ok, defaultButton=QMessageBox.Cancel)
        
        if ret == QMessageBox.Ok:
            return True
        if ret == QMessageBox.Cancel:
            return False
    
    def infoPopup(self, msg, title="", flag="Warning"):
        box = QMessageBox(self)
        box.setText(msg)
        box.setWindowTitle(title)

        if flag == "Warning":
            box.setIcon(QMessageBox.Warning)
        if flag == "Information":
            box.setIcon(QMessageBox.Information)

        box.exec()

# these get put in the init qt for convenience
DEFAULT_YML_PATHS = ['Y:/yanni/Dokumente/GitHub/Q3python/misc/test.yml', 'Y:/yanni/Desktop/important files on Y.yml']

MAIN_QT_WIDTH = 800
MAIN_QT_HEIGHT = 600


class LocalBackupManager():

    def __init__(self) -> None:
        # get self.CONFIG_PATH
        self.initQT()

        # try in order to handle when the initQT is manually closed
        # otherwise VSCode doesnt recognize the existence of configPath because is was delcared in a weird function (i guess)
        try:
            self.configPath = self.configPath 
        except:
            sys.exit()
        
        self.mainQT()

    def initQT(self) -> None:
        self.app = QApplication([])
        self.window = QWidget()
        self.layout = QVBoxLayout()

        ymlSelectionCombo = QComboBox()
        self.layout.addWidget(ymlSelectionCombo)
        for path in DEFAULT_YML_PATHS:
            ymlSelectionCombo.addItem(path)

        self.layout.addWidget(QLabel("Absolute filepath of the .yml file"))
        lineedit = QLineEdit()
        self.layout.addWidget(lineedit)
        
        button = QPushButton("Enter")
        # so that the push button can be triggered by pressing enter
        button.setShortcut('Return')
        self.layout.addWidget(button)

        feedback = QLabel("\n")
        self.layout.addWidget(feedback)

        def buttonFunc(temppath=lineedit.text()):
            # fileExtension is the last four characters of path
            fileExtension = temppath[len(temppath)-4] + temppath[len(temppath)-3] + temppath[len(temppath)-2] + temppath[len(temppath)-1]
            if fileExtension != ".yml":
                feedback.setText("[Errno 3.141] " + temppath + " does not lead to a .yml file :(")

                # return and don't exit the app
                return None

            self.configPath = temppath

            # try to open the file
            try:
                self.loadConfig()
            except Exception as e:
                feedback.setText(str(e) + " :(")
                return None
            
            # if the keys do not exist, make them
            if (self.ymlDict is None) or (("meta" or "files" or "directories") not in self.ymlDict):
                    self.ymlDict = {}
                    self.ymlDict["meta"] = {}
                    self.ymlDict["meta"]["lastBackupTime"] = None
                    self.ymlDict["meta"]["lastBackupPath"] = None
                    self.ymlDict["files"] = {}
                    self.ymlDict["directories"] = {}

                    file = open(self.configPath, 'w')
                    yaml.dump(self.ymlDict, file)
                    file.close()

                    self.loadConfig()
                

            # exit once the config was successfully loaded and is correct
            self.app.exit()

        def comboFunc():
            buttonFunc(ymlSelectionCombo.currentText())

        button.clicked.connect(buttonFunc)
        ymlSelectionCombo.activated.connect(comboFunc)

        self.window.setLayout(self.layout)
        self.window.show()
        self.app.exec()

    def mainQT(self):
        # delete the init qt layout
        self.deleteLayout()

        self.window.setMinimumSize(MAIN_QT_WIDTH, MAIN_QT_HEIGHT)

        self.myCustomWidgets = CustomWidgets()

        # self.window.resize(800, 600)
        self.window.setWindowTitle("This is my homemade local backup application! yay")

        self.addFilesButton = QPushButton("Add files to the config")
        self.layout.addWidget(self.addFilesButton)

        self.addDirButton = QPushButton("Add a directory to the config")
        self.layout.addWidget(self.addDirButton)

        self.layout.addWidget(QLabel("Add files of the selected directory to a blacklist. If a selected file is already in the blacklist, it is removed."))
        self.blacklistComboBox = QComboBox()
        self.layout.addWidget(self.blacklistComboBox)

        self.ymlAllPathsLabel = QLabel("\n")
        self.layout.addWidget(self.ymlAllPathsLabel)

        scroll = QScrollArea()
        scroll.setWidget(self.ymlAllPathsLabel)
        scroll.setWidgetResizable(True)
        self.layout.addWidget(scroll)

        self.ymlSizeLabel = QLabel("\n")
        self.layout.addWidget(self.ymlSizeLabel)

        self.backupLocationButton = QPushButton("Select the backup location")
        self.layout.addWidget(self.backupLocationButton)

        self.backupLocationLabel = QLabel("\n")
        self.layout.addWidget(self.backupLocationLabel)
        
        if self.ymlDict["meta"]["lastBackupPath"] is not None:
            self.backupPath = self.ymlDict["meta"]["lastBackupPath"]
            space = self.getAvailableSpace()
            self.backupLocationLabel.setText("Backup Location: " + self.backupPath + "\nTotal space of the drive is " + size(space[0]) + " with " + size(space[2]) + " of free space.\nThe last backup was made on " + str(self.ymlDict["meta"]["lastBackupTime"]))
        else:
            self.backupPath = ""

        self.doBackupButton = QPushButton("Backup the config to the specified location!")
        self.layout.addWidget(self.doBackupButton)

        self.deleteConfigButton = QPushButton("Completely reset the config")
        self.layout.addWidget(self.deleteConfigButton)
        
        def addFilesFunc():
            paths = self.myCustomWidgets.openFileNamesDialog()
            self.addFilesToConfig(paths)
  
        def addDirFunc():
            path = self.myCustomWidgets.openDirDialog()
            self.addDirToConfig(path)
        
        def addToDirBlacklistFunc():
            paths = self.myCustomWidgets.openFileNamesDialog(self.blacklistComboBox.currentText())
            self.addPathsToBlacklist(self.blacklistComboBox.currentIndex(), paths)

        def backupLocationFunc():
            self.backupPath = self.myCustomWidgets.openDirDialog()
            if not self.backupPath:
                return
            space = self.getAvailableSpace()
            self.backupLocationLabel.setText("Backup Location: " + self.backupPath + "\nTotal space of the drive is " + size(space[0]) + " with " + size(space[2]) + " of free space\nThe last backup was made on " + str(self.ymlDict["meta"]["lastBackupTime"]))

        def doBackupFunc():
            # check is self.backupPath exists
            try:
                self.backupPath = self.backupPath
            except:
                self.myCustomWidgets.infoPopup("No backup path selected!", "Problem")
                return 

            # if the size of the backup is bigger than the available space, cancel
            if self.getBackupSize() > (self.getAvailableSpace()[2] * 0.9):
                self.myCustomWidgets.infoPopup("Not enough space available!", "Problem")
            
            else:
                self.copyAllFiles(self.backupPath)
                self.myCustomWidgets.infoPopup("Successfully backed up!", "Success", "Information")

        def deleteConfigFunc():
            if self.myCustomWidgets.resetPopup():
                self.resetConfig()

        self.addFilesButton.clicked.connect(addFilesFunc)
        self.addDirButton.clicked.connect(addDirFunc)
        self.blacklistComboBox.activated.connect(addToDirBlacklistFunc)
        self.deleteConfigButton.clicked.connect(deleteConfigFunc)
        self.backupLocationButton.clicked.connect(backupLocationFunc)
        self.doBackupButton.clicked.connect(doBackupFunc)

        self.updateQTLabels()

        self.window.setLayout(self.layout)
        self.window.show()
        self.app.exec()

    def deleteLayout(self):
        for i in reversed(range(self.layout.count())): 
            self.layout.itemAt(i).widget().setParent(None)

    def loadConfig(self):
        self.ymlDict = yaml.safe_load(open(self.configPath, 'r'))

    def updateConfig(self):
        # save the altered self.ymlDict to the config file
        file = open(self.configPath, 'w')
        yaml.dump(self.ymlDict, file)
        file.close()

        self.loadConfig()
        self.updateQTLabels()

    def addFilesToConfig(self, listOfPaths):
        # check if list is empty
        if not len(listOfPaths):
            return None

        # convert self.ymlDict["files"] to a dict
        # try adding existing paths to the list, otherwise self.ymlDict["files"] is None and we have to make it a dict
        tempFileList = []
        try:
            for i in range(self.ymlDict["files"].keys()):
                tempFileList.append(self.ymlDict["files"][str(i)])
        except:
            self.ymlDict["files"] = {}

        # if a path that was already in the list is selected again, it is deleted from the list
        for newPath in listOfPaths:
            for existingPath in tempFileList:
                if existingPath == newPath:
                    tempFileList.remove(existingPath)
                    listOfPaths.remove(newPath)
            
        # append all new paths
        for newPath in listOfPaths:
            tempFileList.append(newPath)

        # convert the temporary list back to a dict
        self.ymlDict["files"] = {}
        for i in range(len(tempFileList)):
            self.ymlDict["files"][str(i)] = tempFileList[i]
        
        # save the changes
        self.updateConfig()
  
    def addDirToConfig(self, path):        
        # check if path is empty
        if not path:
            return None

        # try if directory already exists
        try:
            # check if the path already exists
            for a in self.ymlDict["directories"]:
                if path == self.ymlDict["directories"][a]["path"]:
                    return None
        except Exception as e:
            print(e)
            self.ymlDict["directories"] = {}

        # append new directory with the right formating
        lengthOfDirectories = len(self.ymlDict["directories"].keys())
        self.ymlDict["directories"] [str(lengthOfDirectories)] = {}
        
        self.ymlDict["directories"][str(lengthOfDirectories)]["path"] = path
        self.ymlDict["directories"][str(lengthOfDirectories)]["blacklist"] = {}
        
        # save the changes
        self.updateConfig()

    def resetConfig(self):
        self.ymlDict["directories"] = None
        self.ymlDict["files"] = None
        self.ymlDict["meta"]["lastBackupPath"] = None
        self.ymlDict["meta"]["lastBackupTime"] = None

        self.updateConfig()

    def addPathsToBlacklist(self, dirNo, paths):
        #for path in paths:
        #    self.ymlDict["directories"][str(dirNo)]["blacklist"].append(path)

        #self.updateQTLabels()

        
        # check if list is empty
        if not len(paths):
            return None

        # convert self.ymlDict["files"] to a dict
        # try adding existing paths to the list, otherwise self.ymlDict["files"] is None and we have to make it a dict
        tempFileList = []
        try:
            for key in self.ymlDict["directories"][str(dirNo)]["blacklist"].keys():
                tempFileList.append(self.ymlDict["directories"][str(dirNo)]["blacklist"][key])
        except:
            self.ymlDict["directories"][str(dirNo)]["blacklist"] = {}

        # if a path that was already in the blacklist was again selected, it is deleted from the blacklist
        for path in paths:
            for existingPath in tempFileList:
                if existingPath == path:
                    paths.remove(path)
                    tempFileList.remove(path)
        
        # append all new paths
        for path in paths:
            tempFileList.append(path)

        # convert the temporary list back to a dict
        self.ymlDict["directories"][str(dirNo)]["blacklist"] = {}
        for i in range(len(tempFileList)):
            self.ymlDict["directories"][str(dirNo)]["blacklist"][str(i)] = tempFileList[i]
        
        # save the changes
        self.updateConfig()

    def updateQTLabels(self):
        # update BlacklistComboBox
        self.blacklistComboBox.clear()
        if self.ymlDict["directories"] is not None:
            for a in self.ymlDict["directories"]:
                    self.blacklistComboBox.addItem(self.ymlDict["directories"][a]["path"])
        

        # update ymlString
        self.ymlAllPathsLabel.setText(self.printYmlDict())

        self.ymlSizeLabel.setText("Estimated size of the backup is " + size(self.getBackupSize()))

    def printYmlDict(self):
        def getDictStrRec(out, dicti, indent=0):

            if indent > 100:
                return "[ERRNO 420] too much recursion :("

            # for every key in the dict
            keys = dicti.keys()
            for key in keys:

                # if this entry is not a dict itself, add it to out
                if type(dicti[key]) is not dict:
                    out += indent * " " + str(key) + ": "  + str(dicti[key]) + "\n"
                
                # if it is a dict, add the dict name and run recFunc again
                else:
                    out += indent * " " + str(key) + ": \n"
                    
                    out = getDictStrRec(out, dicti[key], indent+4)
            
            # after everything was went through
            return out

        # prints the dict nicely formatted with all is layers using a recursive function (ohh fancy)
        out = " ~~~ Yaml file at " + self.configPath + " ~~~\n\n"

        return getDictStrRec(out, self.ymlDict) + "\n~~~~~~~~~"

    def getAvailableSpace(self):
        
        # should work for windows and linux
        try:
            space = shutil.disk_usage(self.backupPath)
        except Exception as e:
            print(e)
            space = (0,0,0)
        
        out = []
        out.append(space[0])
        out.append(space[1])
        out.append(space[2])

        return out

    def getBackupSize(self):
        # in bytes
        totalSize = 0

        if self.ymlDict["directories"] is None:
            return 69

        # for every entry in directories
        for key in self.ymlDict["directories"].keys():

            for dirpath, dirnames, filenames in os.walk(self.ymlDict["directories"][key]["path"]):

                for f in filenames:
                    fp = os.path.join(dirpath, f).replace("\\", "/")

                    # if the filepath isn't blacklisted
                    if fp not in self.ymlDict["directories"][key]["blacklist"].values():
                        # skip if it is symbolic link
                        if not os.path.islink(fp):
                            totalSize += os.path.getsize(fp)


        return totalSize

    def copyAllFiles(self, targetDir):
        def myCopyTree(src, dst, symlinks=False, ignore=None, blacklist=[]):
            if not os.path.exists(dst):
                os.makedirs(dst)
            for item in os.listdir(src):
                s = os.path.join(src, item).replace("\\", "/")
                d = os.path.join(dst, item).replace("\\", "/")
                if os.path.isdir(s):
                    myCopyTree(s, d, symlinks, ignore, blacklist=blacklist)
                else:
                    # check if file is in blacklist
                    if s not in blacklist:
                        if not os.path.exists(d) or os.stat(s).st_mtime - os.stat(d).st_mtime > 1:
                            shutil.copy2(s, d)
        
        # copy all directories 
        if self.ymlDict["directories"] is not None:
            # for every entry in directories
            for key in self.ymlDict["directories"].keys():
                templist = list(self.ymlDict["directories"][key]["path"])

                #remove forbidden characters from foldername
                for i in range(len(templist)):
                    if templist[i] == "/":
                        templist[i] = "_"
                    # remove the drive letter
                    if templist[i] == ":":
                        templist[i-1] = ""
                        templist[i] = ""

                folderName = ""
                for char in templist:
                    folderName += char
                
                newTarget = targetDir + "/" + folderName

                myCopyTree(self.ymlDict["directories"][key]["path"], newTarget, blacklist=self.ymlDict["directories"][key]["blacklist"].values())

        # copy all single files
        if self.ymlDict["files"] is not None:
            fileList = []

            for i in range(len(self.ymlDict["files"].keys())):
                fileList.append(self.ymlDict["files"][str(i)])
            
            for path in fileList:
                newTarget = targetDir + "/files"
                            
                if not os.path.exists(newTarget):
                    os.makedirs(newTarget)
                shutil.copy2(path, newTarget)
        
        # set metadata
        self.ymlDict["meta"]["lastBackupTime"] = str(datetime.datetime.now())
        self.ymlDict["meta"]["lastBackupPath"] = targetDir

        space = self.getAvailableSpace()
        self.backupLocationLabel.setText("Backup Location: " + self.backupPath + "\nTotal space of the drive is " + size(space[0]) + " with " + size(space[2]) + " of free space.\nThe last backup was made on " + str(self.ymlDict["meta"]["lastBackupTime"]))
        self.updateConfig()

        # copy the yml file used for the backup
        shutil.copy2(self.configPath, targetDir)


LocalBackupManager()
