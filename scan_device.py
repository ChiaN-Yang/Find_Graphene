import sys
import pathlib
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QFileDialog
from utils import scan_device, detect_again


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        uic.loadUi('./ui/finder.ui', self)
        self.scanButton.clicked.connect(self.startScan)
        self.folderButton.clicked.connect(self.selectFoldrer)
        self.detectButton.clicked.connect(self.startDetect)

    def startScan(self):
        scan_device()

    def selectFoldrer(self):
        folder_address = QFileDialog.getExistingDirectory(self, "Please define the folder name", str(pathlib.Path.cwd()/'data'))
        if folder_address:
            self.label.setText(folder_address)

    def startDetect(self):
        folder = self.label.text()
        thresh = float(self.lineEdit.text())
        detect_again(folder, thresh)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())