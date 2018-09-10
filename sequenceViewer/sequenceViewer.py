"""Creates a tree structure for image sequences

Image sequences can be listed recursively if the checkbox is checked.
Meaning all the sequence under the selected folder will be listed
recursively.
Double clicking on the seguence will execute the file on the defined application
"""

from PyQt4 import QtCore, QtGui, Qt
import sys, os
import pyseq_mod as seq
import json
import datetime
import fileCopyProgressSW as fCopy

__author__ = "Arda Kutlu"
__copyright__ = "Copyright 2018"
__credits__ = ["Ryan Galloway"]
__license__ = "GPL"
__version__ = "0.1.1"
__maintainer__ = "Arda Kutlu"
__email__ = "ardakutlu@gmail.com"
__status__ = "Beta"


windowName = "Sequence Viewer v%s" %__version__


def folderCheck(folder):
    if not os.path.isdir(os.path.normpath(folder)):
        os.makedirs(os.path.normpath(folder))

def loadJson(file):
    if os.path.isfile(file):
        with open(file, 'r') as f:
            # The JSON module will read our file, and convert it to a python dictionary
            data = json.load(f)
            return data
    else:
        return None

def dumpJson(data, file):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)

def initDB():
    homedir = os.path.join(os.path.expanduser("~"), "sequenceViewer")
    folderCheck(homedir)
    userDBpath = os.path.join(homedir, "sequenceViewer_locDB.json")

    if os.path.isfile(userDBpath):
        locationsDictionary = loadJson(userDBpath)
    else:
        locationsDictionary = {"rootLocation": homedir,
                               "raidLocation": "N/A"}
    return locationsDictionary, userDBpath

def setTlocations(path, locationType):
    db, userDBpath  = initDB()
    db[locationType] = path
    dumpJson(db, userDBpath)

def transferFiles(files, tLocation, projectPath):
    """
    Copies the files to the remote server with proper directory structure. The files maintains the same folder structure\
    as rendered and gathered under a current date folder (YYMMDD)
    Args:
        files: (List) List of files
        tLocation: (String) Remote server base directory
        projectPath: (String) Base directory of files

    Returns: (Bool) True if canceled All remaining transfer commands

    """
    if not os.path.isdir(tLocation):
        # transfer location is not exist
        return -1, "Transfer Location not exists"

    subPath = os.path.split(os.path.relpath(files[0], projectPath))[0] ## get the relative path


    now = datetime.datetime.now()
    currentDate = now.strftime("%y%m%d")

    targetPath = os.path.join(tLocation, currentDate, subPath)
    folderCheck(targetPath)

    ret = fCopy.FileCopyProgress(src=files, dest=targetPath)
    ret.close()
    return ret.cancelAll


class MainUI(QtGui.QMainWindow):
    def __init__(self):
        super(MainUI, self).__init__()
        # self.projectPath = os.path.normpath("M:\Projects\Bambi_Yatak_shortcut_171130\images")
        self._generator = None
        self._timerId = None
        self.locationsDic = initDB()[0]
        self.sequenceData = []
        self.extensionDictionary = {"jpg": ["*.jpg", "*.jpeg"],
                                   "png": ["*.png"],
                                   "exr": ["*.exr"],
                                   "tif": ["*.tif", "*.tiff"],
                                   "tga": ["*.tga"]
                                   }
        self.filterList = sum(self.extensionDictionary.values(),[])


        self.setObjectName(windowName)
        self.resize(670, 624)
        self.setWindowTitle(windowName)
        self.centralwidget = QtGui.QWidget(self)
        # self.centralwidget.setObjectName(("centralwidget"))
        self.model = QtGui.QFileSystemModel()
        self.model.setRootPath(self.locationsDic["rootLocation"])
        # filter = Qt.QStringList("")
        self.model.setFilter(QtCore.QDir.AllDirs|QtCore.QDir.NoDotAndDotDot)
        self.buildUI()


        self.setCentralWidget(self.centralwidget)

    def buildUI(self):
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(("gridLayout"))

        self.recursive_checkBox = QtGui.QCheckBox(self.centralwidget)
        self.recursive_checkBox.setText(("Recursive"))
        self.recursive_checkBox.setChecked(False)
        # self.recursive_checkBox.setObjectName(("recursive_checkBox"))
        self.gridLayout.addWidget(self.recursive_checkBox, 0, 3, 1, 1)

        self.rootFolder_label = QtGui.QLabel(self.centralwidget)
        self.rootFolder_label.setFrameShape(QtGui.QFrame.Box)
        self.rootFolder_label.setLineWidth(1)
        self.rootFolder_label.setText(("Root Folder:"))
        self.rootFolder_label.setTextFormat(QtCore.Qt.AutoText)
        self.rootFolder_label.setScaledContents(False)
        # self.rootFolder_label.setObjectName(("rootFolder_label"))
        self.gridLayout.addWidget(self.rootFolder_label, 0, 0, 1, 1)

        self.rootFolder_lineEdit = DropLineEdit(self.centralwidget)
        self.rootFolder_lineEdit.setText((self.locationsDic["rootLocation"]))
        self.rootFolder_lineEdit.setReadOnly(True)
        self.rootFolder_lineEdit.setPlaceholderText((""))
        # self.rootFolder_lineEdit.setObjectName(("rootFolder_lineEdit"))
        self.gridLayout.addWidget(self.rootFolder_lineEdit, 0, 1, 1, 1)

        self.browse_pushButton = QtGui.QPushButton(self.centralwidget)
        self.browse_pushButton.setText(("Browse"))
        # self.browse_pushButton.setObjectName(("browse_pushButton"))
        self.gridLayout.addWidget(self.browse_pushButton, 0, 2, 1, 1)

        self.raidFolder_label = QtGui.QLabel(self.centralwidget)
        self.raidFolder_label.setFrameShape(QtGui.QFrame.Box)
        self.raidFolder_label.setLineWidth(1)
        self.raidFolder_label.setText(("Transfer Folder:"))
        self.raidFolder_label.setTextFormat(QtCore.Qt.AutoText)
        self.raidFolder_label.setScaledContents(False)
        # self.raidFolder_label.setObjectName(("rootFolder_label"))
        self.gridLayout.addWidget(self.raidFolder_label, 1, 0, 1, 1)

        self.raidFolder_lineEdit = DropLineEdit(self.centralwidget)
        self.raidFolder_lineEdit.setText(self.locationsDic["raidLocation"])
        self.raidFolder_lineEdit.setReadOnly(True)
        self.raidFolder_lineEdit.setPlaceholderText((""))
        # self.raidFolder_lineEdit.setObjectName(("raidFolder_lineEdit"))
        self.gridLayout.addWidget(self.raidFolder_lineEdit, 1, 1, 1, 1)

        self.browseRaid_pushButton = QtGui.QPushButton(self.centralwidget)
        self.browseRaid_pushButton.setText(("Browse"))
        # self.browseRaid_pushButton.setObjectName(("browseRaid_pushButton"))
        self.gridLayout.addWidget(self.browseRaid_pushButton, 1, 2, 1, 1)

        self.chkboxLayout = QtGui.QHBoxLayout()
        self.chkboxLayout.setAlignment(QtCore.Qt.AlignRight)

        self.checkboxes=[]
        for key in (self.extensionDictionary.keys()):
            tCheck = QtGui.QCheckBox()
            tCheck.setText(key)
            tCheck.setChecked(True)
            # name = lambda x=key: key
            # tCheck.setObjectName(str(name))
            self.chkboxLayout.addWidget(tCheck)
            tCheck.toggled.connect(lambda state, item=self.extensionDictionary[key]: self.onCheckbox(item, state))
            self.checkboxes.append(tCheck)

        self.selectAll_pushbutton = QtGui.QPushButton()
        self.selectAll_pushbutton.setText("Select All")

        self.selectNone_pushbutton = QtGui.QPushButton()
        self.selectNone_pushbutton.setText("Select None")

        spacerItem = QtGui.QSpacerItem(400, 25, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)

        self.chkboxLayout.addWidget(self.selectAll_pushbutton)
        self.chkboxLayout.addWidget(self.selectNone_pushbutton)
        self.chkboxLayout.addItem(spacerItem)

        self.gridLayout.addLayout(self.chkboxLayout, 2, 0, 1, 4)

        self.splitter = QtGui.QSplitter(self.centralwidget)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        # self.splitter.setObjectName(("splitter"))

        self.directories_treeView = DeselectableTreeView(self.splitter)
        # self.directories_treeView.setObjectName(("directories_treeView"))
        self.directories_treeView.setModel(self.model)
        self.directories_treeView.setRootIndex(self.model.index(self.locationsDic["rootLocation"]))

        # self.directories_treeView.setRootIsDecorated(False)
        self.directories_treeView.setSortingEnabled(True)
        self.directories_treeView.sortByColumn(0, QtCore.Qt.AscendingOrder)
        self.directories_treeView.setColumnWidth(0, 250)
        self.directories_treeView.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)

        self.directories_treeView.hideColumn(1)
        self.directories_treeView.hideColumn(2)
        # self.directories_treeView.hideColumn(3)

        self.sequences_listWidget = QtGui.QListWidget(self.splitter)
        # self.sequences_listWidget.setObjectName(("sequences_listWidget"))
        self.sequences_listWidget.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.gridLayout.addWidget(self.splitter, 3, 0, 1, 4)

        self.browse_pushButton.clicked.connect(self.onBrowse)
        self.directories_treeView.selectionModel().selectionChanged.connect(self.populate)
        self.recursive_checkBox.toggled.connect(self.populate)
        self.sequences_listWidget.doubleClicked.connect(self.onRunItem)
        self.browseRaid_pushButton.clicked.connect(self.onBrowseRaid)

        ## RIGHT CLICK MENUS
        self.sequences_listWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.sequences_listWidget.customContextMenuRequested.connect(self.onContextMenu_images)
        self.popMenu = QtGui.QMenu()

        rcAction_0 = QtGui.QAction('Show in Explorer', self)
        rcAction_1 = QtGui.QAction('Transfer Files to Raid', self)
        self.popMenu.addAction(rcAction_0)
        self.popMenu.addAction(rcAction_1)
        rcAction_0.triggered.connect(lambda: self.onShowInExplorer())
        rcAction_1.triggered.connect(lambda: self.onTransferFiles())

        self.rootFolder_lineEdit.dropped.connect(self.setRootPath)
        self.raidFolder_lineEdit.dropped.connect(self.setRaidPath)

        self.selectAll_pushbutton.clicked.connect(self.selectAll)
        self.selectNone_pushbutton.clicked.connect(self.selectNone)
        # self.popMenu.addSeparator()
        self.directories_treeView.deselected.connect(self.deselectTree)

        ## check if there is a json file on the project data path for target drive
    def deselectTree(self):
        index = QtCore.QModelIndex()

        # self.directories_treeView.setCurrentIndex(index,0)
        self.directories_treeView.currentIndex(index,0)
        # self.directories_treeView.selectionModel().setCurrentIndex(index, QtGui.QItemSelectionModel.NoUpdate)

        self.populate()

    def selectAll(self):
        for c in self.checkboxes:
            c.setChecked(True)

    def selectNone(self):
        for c in self.checkboxes:
            c.setChecked(False)

    def setRootPath(self, dir):
        dir = str(dir)
        self.directories_treeView.reset()
        setTlocations(os.path.normpath(dir), "rootLocation")
        self.locationsDic["rootLocation"] = os.path.normpath(dir)
        self.model.setRootPath(dir)
        self.directories_treeView.setRootIndex(self.model.index(dir))
        self.rootFolder_lineEdit.setText(self.locationsDic["rootLocation"])
        self.sequences_listWidget.clear()

    def setRaidPath(self, dir):
        dir = str(dir)
        setTlocations(os.path.normpath(dir), "raidLocation")
        self.locationsDic["raidLocation"] = os.path.normpath(dir)
        self.raidFolder_lineEdit.setText(dir)


    def onCheckbox(self, extensions, state):
        if state:
            self.filterList += extensions
        else:
            self.filterList = list(set(self.filterList)-set(extensions))
        self.populate()


    # @Qt.QtCore.pyqtSlot("QItemSelection, QItemSelection")
    def onContextMenu_images(self, point):
        self.popMenu.exec_(self.sequences_listWidget.mapToGlobal(point))

    def onBrowse(self):
        dir = str(QtGui.QFileDialog.getExistingDirectory(self, "Select Directory"))
        if dir:
            self.setRootPath(dir)
        else:
            return

    def onBrowseRaid(self):
        raidLocation = self.locationsDic["raidLocation"] if not self.locationsDic["raidLocation"] == "N/A" else ""
        path = str(QtGui.QFileDialog.getExistingDirectory(self, "Select Directory", raidLocation))
        if path:
            self.setRaidPath(path)
            return

    def onTransferFiles(self):
        raidLocation = self.locationsDic["raidLocation"] if not self.locationsDic["raidLocation"] == "N/A" else None
        if not raidLocation:
            return
        row = self.sequences_listWidget.currentRow()
        selList = [x.row() for x in self.sequences_listWidget.selectedIndexes()]
        # return
        if row == -1:
            return

        for sel in selList:
            tFilesList = [i.path for i in self.sequenceData[sel]]


            ret = transferFiles(tFilesList, tLocation=raidLocation, projectPath=self.locationsDic["rootLocation"])
            if ret: ## cancel all?
                return
        pass

    def onShowInExplorer(self):
        row = self.sequences_listWidget.currentRow()
        if row == -1:
            return
        os.startfile(self.sequenceData[row].dirname)

    def populate(self, deselect=0):
        self.sequences_listWidget.clear()
        self.sequenceData=[] # clear the custom list
        if not self.filterList:
            self.stop()
            return
        index = self.directories_treeView.currentIndex()

        if index.row() == -1 or deselect == -1: # no row selected
            fullPath = self.locationsDic["rootLocation"]
        else:
            fullPath = str(self.model.filePath(index))

        if self.recursive_checkBox.isChecked():
            rec=-1
        else:
            rec=1
        filter = (x for x in self.filterList)
        # gen = seq.walk(fullPath, level=rec, includes=self.filterList)
        gen = seq.walk(fullPath, level=rec, includes=filter)

        self.stop() # Stop any existing Timer
        self._generator = self.listingLoop(gen) # start the loop
        self._timerId = self.startTimer(0) # idle timer

    def listingLoop(self, gen):
        # id = 0
        for x in gen:
            for i in x[2]:
                app.processEvents(QtCore.QEventLoop.ExcludeUserInputEvents)
                self.sequenceData.append(i)
                self.sequences_listWidget.addItem(i.format('%h%t %R'))
                yield

    def onRunItem(self):
        row = self.sequences_listWidget.currentRow()
        item = self.sequenceData[row]
        firstImagePath = os.path.join(os.path.normpath(item.dirname), item.name)
        os.startfile(firstImagePath)

    def stop(self):  # Connect to Stop-button clicked()
        if self._timerId is not None:
            self.killTimer(self._timerId)
        self._generator = None
        self._timerId = None


    def timerEvent(self, event):
        # This is called every time the GUI is idle.
        if self._generator is None:
            return
        try:
            next(self._generator)  # Run the next iteration
        except StopIteration:
            self.stop()  # Iteration has finshed, kill the timer


class DropLineEdit(QtGui.QLineEdit):
    dropped = QtCore.pyqtSignal(str)
    def __init__(self, type, parent=None):
        super(DropLineEdit, self).__init__(parent)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat('text/uri-list'):
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasFormat('text/uri-list'):
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        rawPath = event.mimeData().data('text/uri-list').__str__()
        path = rawPath.replace("file:///", "").splitlines()[0]
        self.dropped.emit(path)
        # self.addItem(path)

class DeselectableTreeView(QtGui.QTreeView):
    deselected = QtCore.pyqtSignal(bool)
    def mousePressEvent(self, event):
        index = self.indexAt(event.pos()) # returns  -1 if click is outside
        if index.row() == -1:
            self.clearSelection()
            self.deselected.emit(True)
        QtGui.QTreeView.mousePressEvent(self, event)
if __name__ == '__main__':


    app = QtGui.QApplication(sys.argv)
    window = MainUI()
    window.show()
    sys.exit(app.exec_())
