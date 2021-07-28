#!/usr/bin/python
## main
''' Run this program to scan the sample and detect graphene'''
from coordinate_creator import coor_gen
from getCCDphoto import CCD_dir_save
from microscope_controller import esp, prior_motor
from datetime import datetime
import os
import sys
import pandas as pd

# [TIME] setup a start_time and record progress
start_time = datetime.now()
progress = 0.

# newport controller device, baud rate, default axis
controller = esp(dev="COM3",b=921600,axis=1,reset=True,initpos=0.0,useaxis=[],timeout=0.5)
mt = prior_motor("COM1")

# Get the origin x, y (input_1_x & y)
input_1_x, input_1_y = controller.get_pos()

# Create folder that named by current time to store photos and log file
folder_name = str(start_time)[:19].replace(':', "'")
os.mkdir(folder_name)
resultPath = f'./{folder_name}/Detection result'
os.mkdir(resultPath)

# Perfrom 9 times z scans to find the best figure ranging from -20 to 20
imgPath = './'+ folder_name +'/'+ 'Origin.png'
origin_z = mt.focusLens(9, 20, imgPath)

# Write the info to a txt file
f = open(resultPath+'/Log file.txt', 'a')
f.write('Start_time: ' + str(start_time)[:-7] + '\n')
f.write('The Origin coordinate: x = ' + str(input_1_x) + ', y = ' + str(input_1_y) + '\n')
f.close()

# generate main corrd. and extra coord. (pd.dataframe)
main, extra, num_x, num_y = coor_gen(input_1_x, input_1_y)

# get the total length of corrdinates for looping later
row_len = main.shape[0]

# creat z record
z_array = []

try:
    # Start looping every coordinate and save screenshot 
    for i in range(row_len):
        # Get the start point from corrdinate generator
        abs_x = main.iloc[i][0]
        abs_y = main.iloc[i][1]
        controller.x_y_move(abs_x, abs_y)

        imgPath = './'+ folder_name +'/'+ str(i) + '.png'
        # return the best quality z
        abs_z = mt.focusLens_fast(3, 6, imgPath, i)

        print(f'{i}th figure. Clear z is: {abs_z}')
        progress += 1
        print(f'\nCurrent progress: {round(progress/row_len*100)}%')
        z_record = (abs_x, abs_y, abs_z)
        z_array.append(z_record)
except:
    # Go back to origin x, y (input_1_x & y)
    controller.x_y_move(input_1_x, input_1_y)
    controller.close()
    # Adjust the z to the original place
    mt.move_z_pos(origin_z)
    mt.close()
    sys.exit()
    
# [TIME] Calculate the time differnece
end_time = datetime.now()    
time_delta = (end_time - start_time)

# Go back to origin x, y (input_1_x & y)
controller.x_y_move(input_1_x, input_1_y)
del controller

# Adjust the z to the original place
mt.move_z_pos(origin_z)
del mt

# [Time] Print time information
print('Run finished.\nStart time: ' + str(start_time)[:-7] + '\nEnd time: ' + str(end_time)[:-7] + '\nElapsed time: ' + str(time_delta)[:-7])

# Write info to a txt
f = open(resultPath+'/Log file.txt', 'a')
f.write('End_time: ' + str(end_time)[:-7] + '\n')
f.write('Elapsed time: ' + str(time_delta)[:-7] + '\n\n')
f.close()

# Save the coordinates and z value
z_data = pd.DataFrame(z_array)
z_data.to_csv(resultPath+'/main_coordinates.txt', sep='\t', mode='w')


# Start TF2 Object Detection
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~
from graphene_detection import detect
detect(folder_name, resultPath, main, probability=0.7, flip_horizontally=False, grayscale=False)
