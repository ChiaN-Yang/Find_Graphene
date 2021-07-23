#!/usr/bin/python
## main
''' Run this program to scan the sample and detect graphene'''
from coordinate_creator import coor_gen
from getCCDphoto import getphoto, CCD_save, tenengrad
from microscope_controller import esp, prior_motor
from datetime import datetime
from time import sleep
import os
import sys
import pandas as pd

# [TIME] setup a start_time
start_time = datetime.now()
progress = 0.

# Get the origin x, y (input_1_x & y)
# newport controller device, baud rate, default axis
controller = esp(dev="COM3",b=921600,axis=1,reset=True,initpos=0.0,useaxis=[],timeout=0.5)
input_1_x, input_1_y = controller.get_pos()

# Create folder that named by current time to store photos and log file
folder_name = str(start_time)[:19].replace(':', "'")
os.mkdir(folder_name)

# Save the original corner figure
CCD_save(getphoto(), folder_name, 'Origin')

# Save the original z
mt = prior_motor("COM1")
origin_z = mt.get_z_pos()

# Write the info to a txt file
f = open('./'+ folder_name +'/'+'Log file.txt', 'a')
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
        # Connect the esp to apply the start point to it
        # Get the start point from corrdinate generator
        abs_x = main.iloc[i][0]
        abs_y = main.iloc[i][1]
        controller.x_y_move(abs_x, abs_y)
        
        # Form the image-Quality list ot record the quality of the figure
        image_Q = []
    
        # Connect the z motor as mt and get current z position
        current_z = mt.get_z_pos()
    
        # Perfrom 5 times z scans to find the best figure ranging from -10 to 10
        for j in range(6):
            tar_z = current_z - 10 + (j * 5)
            mt.move_z_pos(tar_z)
            #sleep(0.2)
            CCD_save(getphoto(), folder_name, i)
            imgPath = './'+ folder_name +'/'+ str(i) + '.png'
            imageVar = tenengrad(imgPath)
            image_QVar = (imageVar, tar_z)
            image_Q.append(image_QVar)
            
        # Move to the z position which is corresponding to the best quality figure
        mt.move_z_pos(max(image_Q)[1])
        #sleep(0.2)
        # Save the figure again
        CCD_save(getphoto(), folder_name, i)
        print(f'{i}th figure. Clear z is: {max(image_Q)[1]:.3f}')
        progress += 1
        print(f'\nCurrent progress: {round(progress/row_len*100)}%')
        z_record = (abs_x, abs_y, max(image_Q)[1])
        z_array.append(z_record)
except KeyboardInterrupt:
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
f = open('./'+ folder_name +'/'+'Log file.txt', 'a')
f.write('End_time: ' + str(end_time)[:-7] + '\n')
f.write('Elapsed time: ' + str(time_delta)[:-7] + '\n\n')
f.close()

csvPath = './'+ folder_name +'/'+'main_coordinates.txt'
main.to_csv(csvPath, sep=' ', mode='w')
# =============================================================================
# data = pd.read_table('main_coordinates.txt', sep=' ')
# =============================================================================
