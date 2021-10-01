# -*- coding: utf-8 -*-
"""
Created on Tue Aug 24 20:37:58 2021

@author: SOC
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Jun 30 17:32:17 2021

@author: jerry
"""
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import QIntValidator, QRegExpValidator
from PyQt5.QtWidgets import QMessageBox, QFileDialog
from PyQt5.QtCore import Qt, QRegExp
from FindTargetProcessor import Ui_MainWindow
from microscope_controller import esp, prior_motor
import sys
import os
import numpy as np
from datetime import datetime

temp = 0
row_len = 0

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.cwd = os.getcwd()
               
# =============================================================================
#         # Set Window Icon
#         self.setWindowIcon(QtGui.QIcon('Qfort.png'))
# =============================================================================
        
        # Menu
        self.ui.retranslateUi(self)
        self.ui.actionQuit.setShortcut('Ctrl+Q')
        self.ui.actionQuit.triggered.connect(app.exit)

        # Load botton
        self.ui.pushButton.clicked.connect(self.LoadFile)
        self.ui.pushButton_2.clicked.connect(self.MoveToTarget)
        
        # combo box click
        self.ui.comboBox.activated.connect(self.AbsRelativeSwitch)
        

    def LoadFile(self):
        global fileName1, filetpye, name, file_address, lines
        # get single file
        fileName1, filetype = QFileDialog.getOpenFileName(self, "Please choose the Log File",self.cwd ,"Text Files (*.txt)")  
        
        if filetype != '':
            name_len = len(fileName1)
            name_start = fileName1.rfind('/') + 1
            name = fileName1[name_start:name_len]
            file_address = fileName1[:name_start]

            self.data_name = fileName1
            # Load file
            with open(fileName1) as f:
                lines = f.readlines()    
            # Read Original XY and sample XY
            self.GetOriginalXY(lines)
            self.GetSampleXY(lines, 0)
            # Display the original XY here
            self.DisplayOriginXY()
            
    def GetOriginalXY(self, read_lines):
        global origin_corrdinate, origin_x, origin_y
        origin_corrdinate = read_lines[1]
        origin_pos_1 = origin_corrdinate.find('x = ')
        origin_pos_2 = origin_corrdinate.find(',')
        origin_pos_3 = origin_corrdinate.find('y = ')
        origin_x = float(origin_corrdinate[origin_pos_1 + 4:origin_pos_2 - 1])
        origin_y = float(origin_corrdinate[origin_pos_3 + 4:-1])
        
    def GetSampleXY(self, read_lines, num):
        global sample_corrdinates, sample_list, origin_x, origin_y  
        
        if num == 0:
            sample_corrdinates = read_lines[6:len(read_lines)]
            for i in range(len(sample_corrdinates)):
                pos_1 = sample_corrdinates[i].find('.png')
                pos_2 = sample_corrdinates[i].find('(')
                pos_3 = sample_corrdinates[i].find(')')
                sample_name = sample_corrdinates[i][0:pos_2 - 1]
                sample_corrdinate = sample_corrdinates[i][pos_2 + 1:pos_3 - 1]
                x_pos = sample_corrdinate.find(',')
                y_pos = sample_corrdinate.find(' ')
                sample_x = float(sample_corrdinate[0:x_pos])
                sample_y = float(sample_corrdinate[x_pos + 2:-2])
                
                temp = [sample_name, sample_corrdinate, sample_x, sample_y]
                if i == 0:
                    sample_list = [temp]
                else:
                    sample_list.append(temp)
            self.UpdateTable(sample_list)
        
        elif num == 1:
            sample_corrdinates = read_lines[6:len(read_lines)]
            for i in range(len(sample_corrdinates)):
                pos_1 = sample_corrdinates[i].find('.png')
                pos_2 = sample_corrdinates[i].find('(')
                pos_3 = sample_corrdinates[i].find(')')
                sample_name = sample_corrdinates[i][0:pos_2 - 1]
                sample_corrdinate = sample_corrdinates[i][pos_2 + 1:pos_3 - 1]
                x_pos = sample_corrdinate.find(',')
                y_pos = sample_corrdinate.find(' ')
                sample_x = round(float(sample_corrdinate[0:x_pos]) - float(origin_x),3)
                sample_y = round(float(sample_corrdinate[x_pos + 2:-2]) - float(origin_y),3)
                sample_corrdinate = str(sample_x) + ', ' + str(sample_y)
                
                temp = [sample_name, sample_corrdinate, sample_x, sample_y]
                if i == 0:
                    sample_list = [temp]
                else:
                    sample_list.append(temp)
            self.UpdateTable(sample_list)
                
    def DisplayOriginXY(self):
        global origin_x, origin_y
        self.ui.textBrowser.clear()
        self.ui.textBrowser.setAlignment(QtCore.Qt.AlignCenter)
        self.ui.textBrowser.append(str(origin_x) + ', ' + str(origin_y))

    def AbsRelativeSwitch(self):
        global sample_list, lines
        switch = self.ui.comboBox.currentText()
        if switch == 'Absolute':
            self.GetSampleXY(lines, 0)
        elif switch == 'Relative':
            self.GetSampleXY(lines, 1)
        
    def UpdateTable(self, name_corrdinate_list):
        global sample_list
        self.ui.tableWidget.clear()
        self.ui.tableWidget.setRowCount(0)
        for i in range(len(sample_list)):
            self.ui.tableWidget.insertRow(i)
            name = name_corrdinate_list[i][0]
            coordinate = name_corrdinate_list[i][1]
            name_item = QtWidgets.QTableWidgetItem(name)
            name_item.setTextAlignment(Qt.AlignCenter)
            coordinate_item = QtWidgets.QTableWidgetItem(coordinate)
            coordinate_item.setTextAlignment(Qt.AlignCenter)
            
            self.ui.tableWidget.setItem(i, 0, name_item)
            self.ui.tableWidget.setItem(i, 1, coordinate_item)
            
    def MoveToTarget(self):
        current_row = self.ui.tableWidget.currentRow()
        target_x = sample_list[current_row][2]
        target_y = sample_list[current_row][3]
        # TODO: add the esp mover here
        controller = esp(dev="COM3",b=921600,axis=1,reset=True,initpos=0.0,useaxis=[],timeout=0.5)
        controller.x_y_move(target_x, target_y)
        del controller
        
        # auto focus
        mt = prior_motor("COM1")
        mt.focusLens(10, 50, '1.png')
        del mt
        print('complte.')
        
        
        
        
if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())        