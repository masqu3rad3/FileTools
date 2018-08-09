
from shutil import copyfile
from PyQt4 import QtCore, QtGui
import os


class FileCopyProgress(QtGui.QWidget):

    def __init__(self, src=None, dest=None):
        super(FileCopyProgress, self).__init__()

        self.src = src
        self.dest = dest
        self.build_ui()
        self.terminated = False
        self.cancelAll = False
        self.copyfileobj(src=self.src, dst=self.dest)


    def build_ui(self):

        hbox = QtGui.QVBoxLayout()

        vbox = QtGui.QHBoxLayout()

        lbl_src = QtGui.QLabel('Source: %s' %os.path.split(self.src[0])[0])
        lbl_dest = QtGui.QLabel('Destination: %s' %self.dest)
        self.pb = QtGui.QProgressBar()
        self.cancelButton = QtGui.QPushButton("Cancel")
        self.cancelAllButton = QtGui.QPushButton("Cancel All")

        self.pb.setMinimum(0)
        self.pb.setMaximum(100)
        self.pb.setValue(0)

        hbox.addWidget(lbl_src)
        hbox.addWidget(lbl_dest)
        hbox.addWidget(self.pb)
        vbox.addWidget(self.cancelButton)
        vbox.addWidget(self.cancelAllButton)
        hbox.addLayout(vbox)
        self.setLayout(hbox)




        self.setWindowTitle('File copy')


        self.cancelButton.clicked.connect(self.terminate)
        self.cancelAllButton.clicked.connect(lambda: self.terminate(all=True))

        self.show()

    def closeEvent(self, *args, **kwargs):
        self.terminated = True

    def terminate(self, all=False):
        self.terminated = True
        self.cancelAll = all
        self.pb.setValue(100)
        self.close()



    def copyfileobj(self, src, dst):
        totalCount = len(src)
        current = 0

        for i in src:
            targetPath = os.path.join(dst, os.path.basename(i))
            copyfile(i, targetPath)
            percent = (100 * current) / totalCount
            self.pb.setValue(percent)
            current += 1
            QtGui.QApplication.processEvents()
            if self.terminated:
                break

