import win32gui, win32print, win32con
from win32.win32api import GetSystemMetrics
import sys
from utils.lib.microscope_controller import esp

def get_real_resolution():
    """Get the true resolution"""
    hDC = win32gui.GetDC(0)
    # Horizontal resolution
    w = win32print.GetDeviceCaps(hDC, win32con.DESKTOPHORZRES)
    # Vertical resolution
    h = win32print.GetDeviceCaps(hDC, win32con.DESKTOPVERTRES)
    return w, h

def get_screen_size():
    """Get the scaled resolution"""
    w = GetSystemMetrics (0)
    h = GetSystemMetrics (1)
    return w, h

def check_screen_scale_rate(rate):
    """check if screen scale rate equal to 1.5"""
    real_resolution = get_real_resolution()
    screen_size = get_screen_size()
    screen_scale_rate = round(real_resolution[0] / screen_size[0], 1)
    print(f'screen_scale_rate: {screen_scale_rate}')
    if screen_scale_rate != rate:
        print("Please change the screen scale rate")
        sys.exit()


def placed_correctly():
    """Confirm that the sample is placed correctly"""
    try:
        controller = esp()
        x, y = controller.get_pos()
        input("Please confirm the upper left corner of the sample to align with the red cross (y/n)")
        controller.x_y_move(x, y+7.2)
        input("Please confirm the lower left corner of the sample to align with the red cross (y/n)")
        controller.x_y_move(x-7.2, y+7.2)
        x2, y2 = controller.get_pos()
        if x2 != x-7.2 or y2 != y+7.2:
            print("The microscope does not have enough room to move")
            controller.x_y_move(x, y)
        controller.x_y_move(x, y)
    except:
        # Go back to origin x, y
        controller.x_y_move(x, y)
        controller.close()
        sys.exit()


if __name__ == '__main__':
    check_screen_scale_rate(1.5)
    placed_correctly()
    