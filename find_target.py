from PyQt5 import uic
from PyQt5.QtWidgets import QFileDialog, QMainWindow, QTableWidgetItem, QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap
import sys
import pathlib
import cv2
import qdarkstyle


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        uic.loadUi('./ui/find_target_processor.ui', self)
        self.default_path = str(pathlib.Path.cwd() / 'data')
        # Menu
        self.actionQuit.setShortcut('Ctrl+Q')
        self.actionQuit.triggered.connect(app.exit)
        # Load botton
        self.pushButton_openfile.clicked.connect(self.loadFolder)
        self.pushButton_originimg.clicked.connect(self.displayOriginimg)
        self.tableWidget.cellClicked.connect(self.changeImg)
        # combo box click
        self.comboBox.activated.connect(self.absRelativeSwitch)
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        
    def loadFolder(self):
        # get single file
        self.folder_name = QFileDialog.getExistingDirectory(self, "Please choose the Folder", self.default_path)
        if self.folder_name:
            # Load file
            with open(f'{self.folder_name}/Log file.txt') as f:
                self.lines = f.readlines()    
            # Read Original XY and sample XY
            self.GetOriginalXY(self.lines)
            self.GetSampleXY(self.lines, 0)
            # Display the original XY here
            self.displayOriginXY()

    def changeImg(self):
        row = self.tableWidget.currentRow()
        name = self.tableWidget.item(row,0).text()
        self.displayImg(name)

    def displayImg(self, img_name):
        self.name, datatype = img_name.split('.')
        img = cv2.imread(f'{self.folder_name}/{self.name}d.{datatype}')
        img = cv2.resize(img, (938, 831), interpolation=cv2.INTER_AREA)
        height, width, channel = img.shape
        bytesPerline = 3 * width
        self.qimg = QImage(img, width, height, bytesPerline, QImage.Format_RGB888).rgbSwapped()
        self.label_img.setPixmap(QPixmap.fromImage(self.qimg))

    def displayOriginimg(self):
        img = cv2.imread(f'{self.folder_name}/{self.name}.png')
        img = cv2.resize(img, (938, 831), interpolation=cv2.INTER_AREA)
        height, width, channel = img.shape
        bytesPerline = 3 * width
        self.qimg = QImage(img, width, height, bytesPerline, QImage.Format_RGB888).rgbSwapped()
        self.label_img.setPixmap(QPixmap.fromImage(self.qimg))
            
    def GetOriginalXY(self, read_lines):
        origin_corrdinate = read_lines[1]
        origin_pos_1 = origin_corrdinate.find('x = ')
        origin_pos_2 = origin_corrdinate.find(',')
        origin_pos_3 = origin_corrdinate.find('y = ')
        self.origin_x = float(origin_corrdinate[origin_pos_1 + 4:origin_pos_2 - 1])
        self.origin_y = float(origin_corrdinate[origin_pos_3 + 4:-1])
        
    def GetSampleXY(self, read_lines, option):        
        sample_corrdinates = read_lines[6:len(read_lines)]
        for i in range(len(sample_corrdinates)):
            pos_1 = sample_corrdinates[i].find('.png')
            pos_2 = sample_corrdinates[i].find('(')
            pos_3 = sample_corrdinates[i].find(')')
            sample_name = sample_corrdinates[i][0:pos_2 - 1]
            sample_corrdinate = sample_corrdinates[i][pos_2 + 1:pos_3 - 1]
            x_pos = sample_corrdinate.find(',')
            y_pos = sample_corrdinate.find(' ')
            if option == 0:
                sample_x = float(sample_corrdinate[0:x_pos])
                sample_y = float(sample_corrdinate[x_pos + 2:-2])
            elif option == 1:
                sample_x = round(float(sample_corrdinate[0:x_pos]) - float(self.origin_x),3)
                sample_y = round(float(sample_corrdinate[x_pos + 2:-2]) - float(self.origin_y),3)
                sample_corrdinate = str(sample_x) + ', ' + str(sample_y)
            temp = [sample_name, sample_corrdinate, sample_x, sample_y]
            if i == 0:
                sample_list = [temp]
            else:
                sample_list.append(temp)
        self.UpdateTable(sample_list)
                
    def displayOriginXY(self):
        self.textBrowser.clear()
        self.textBrowser.setAlignment(Qt.AlignCenter)
        self.textBrowser.append(f'{self.origin_x}, {self.origin_y}')

    def absRelativeSwitch(self):
        switch = self.comboBox.currentText()
        if switch == 'Absolute':
            self.GetSampleXY(self.lines, 0)
        elif switch == 'Relative':
            self.GetSampleXY(self.lines, 1)
        
    def UpdateTable(self, name_corrdinate_list):
        self.tableWidget.clear()
        self.tableWidget.setRowCount(0)
        for i in range(len(name_corrdinate_list)):
            self.tableWidget.insertRow(i)
            name = name_corrdinate_list[i][0]
            coordinate = name_corrdinate_list[i][1]
            name_item = QTableWidgetItem(name)
            name_item.setTextAlignment(Qt.AlignCenter)
            coordinate_item = QTableWidgetItem(coordinate)
            coordinate_item.setTextAlignment(Qt.AlignCenter)
            
            self.tableWidget.setItem(i, 0, name_item)
            self.tableWidget.setItem(i, 1, coordinate_item)
            
    # def moveToTarget(self):
    #     pass
    #     current_row = self.tableWidget.currentRow()
    #     target_x = sample_list[current_row][2]
    #     target_y = sample_list[current_row][3]
    #     # TODO: add the esp mover here
    #     controller = esp(dev="COM3",b=921600,axis=1,reset=True,initpos=0.0,useaxis=[],timeout=0.5)
    #     controller.x_y_move(target_x, target_y)
    #     del controller
        
    #     # auto focus
    #     mt = prior_motor("COM1")
    #     mt.focusLens(10, 50, '1.png')
    #     del mt
    #     print('complte.')
        
        
if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
    