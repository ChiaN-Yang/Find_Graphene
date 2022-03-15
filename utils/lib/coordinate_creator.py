## module coordinate_creator
''' coor_gen(input_1_x, input_1_y, multiple=20, Lx=10, Ly=10).
    Create coordinate that microscope should scanned.

    (input_1_x, input_1_y) is the coordinates of the upper left corner.
    multiple=20 represents a lens with 20 magnification.
    Lx and Ly are the length and width of the sample. unit: mm.

    You can run the program directly to know how the microscope will scan
'''
from math import floor
import pandas as pd
#TODO: confirm the period of every block size

def coordinate_generator(input_1_x, input_1_y, multiple=10, Lx=10, Ly=10):
    # Define the period of every block size
    if multiple == 2:
        Px = 3.2
        Py = 3.2
    elif multiple == 10:
        Px = 0.813
        Py = 0.748
    elif multiple == 20:
        Px = 0.36875
        Py = 0.34
    elif multiple == 50:
        Px = 0.1475
        Py = 0.128

    # Find out the number of blocks in x and y direction
    number_x = floor(Lx/Px)
    number_y = floor(Ly/Py)
    
    # check if number can be devided without rem
    # if so, add extra points to coordinates dataframe
    extra_x = extra_y = 0
    if Lx % Px != 0:    extra_x = 1
    if Ly % Py != 0:    extra_y = 1

    # Creat the empty list for recording the coordinates
    coordinate_x = []
    coordinate_y = []
    extra_coor_x = []
    extra_coor_y = []
    
    # Define the origin coordinates
    Origin_x = input_1_x - Px/2
    Origin_y = input_1_y + Py/2
    
    # Write the coordinates to
    y_acc = 0
    for i in range(number_x):
        for j in range(number_y):
            if j != 0:  y_acc += Py * (-1)**i
            var_x = Origin_x - (i * Px)
            var_y = Origin_y + y_acc
    
            coordinate_x.append(round(var_x,3))
            coordinate_y.append(round(var_y,3))
            
    # Create extra coordinates
    input_2_x = input_1_x - Lx
    input_2_y = input_1_y + Ly
            
    if extra_x == 1:
        for j in range(number_y):
            var_x = input_2_x + Px/2
            var_y = Origin_y + (j * Py)
            extra_coor_x.append(var_x)
            extra_coor_y.append(var_y)
    
    if extra_y == 1:    
        for i in range(number_x):
            var_x = Origin_x - (i * Px)        
            var_y = input_2_y - Py/2
            extra_coor_x.append(var_x)
            extra_coor_y.append(var_y)
            
    if extra_x and extra_y == 1:
        var_x = input_2_x + Px/2
        var_y = input_2_y - Py/2
        extra_coor_x.append(var_x)
        extra_coor_y.append(var_y)
        
    coordinate = pd.DataFrame({'x': coordinate_x, 'y':coordinate_y}) 
    extra_coor = pd.DataFrame({'x': extra_coor_x, 'y':extra_coor_y}) 
    
    return coordinate, extra_coor, number_x, number_y


if __name__ == '__main__':
    import matplotlib.pyplot as plt

    def plot():
        plt.grid()
        plt.xlim(0,-10)
        plt.ylim(10,0)
        plt.scatter(coordinate['x'],coordinate['y'])
        plt.scatter(extra_coor['x'],extra_coor['y'], c="red")
        plt.show()

    def plot_dynamic():
        plt.ion()
        plt.figure(1, figsize=(10,10))
        plt.xlim(0,-10)
        plt.ylim(10,0)
        for x,y in zip(coordinate['x'], coordinate['y']):
            plt.plot(x, y, '.')
            plt.pause(10e-9)

    # Input the coordinate of left top corner
    coordinate, extra_coor, number_x, number_y = coor_gen(0, 0)
    print('\nnumber x:',number_x, '\nnumber y:', number_y, '\ntotal spots:',coordinate.shape[0])

    # Change the line below depending on whether you want dynamic drawing or static drawing
    plot()
    #plot_dynamic()
