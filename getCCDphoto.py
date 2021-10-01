## module getCCDphoto
''' CCD_save(getphoto(),'name').
    Take a photo with charge-coupled device.

    You should change the screen magnification first.
    The photo will save as 'name.png' in folder like "2021-07-22 19'05'57".

    laplacian(imgPath) and tenengrad(imgPath)
    will return the clarity of photo
'''
import win32gui, win32ui, win32con
import os
import cv2
from datetime import datetime
from ctypes import windll
from PIL import Image

def getphoto():
    global im
    hwnd = win32gui.FindWindow(None, 'Blackfly S BFS-U3-51S5C 19370957')
    # Prevent windows from being minimized
    win32gui.SendMessage(hwnd, win32con.WM_SYSCOMMAND, win32con.SC_RESTORE, 0)
    
    # Change the line below depending on whether you want the whole window
    # or just the client area. 
    left, top, right, bot = win32gui.GetClientRect(hwnd)
    #left, top, right, bot = win32gui.GetWindowRect(hwnd)

    # Change screen magnification
    mag = 1
    w = int((right - left)*mag)
    h = int((bot - top)*mag)

    hwndDC = win32gui.GetWindowDC(hwnd)
    mfcDC  = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()
    
    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
    
    saveDC.SelectObject(saveBitMap)
    
    # Change the line below depending on whether you want the whole window
    # or just the client area. 
    result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 1)
    #result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 0)
    #if result == 1: print('screenshot succeeded')
    
    bmpinfo = saveBitMap.GetInfo()
    bmpstr = saveBitMap.GetBitmapBits(True)
    
    im = Image.frombuffer(
        'RGB',
        (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
        bmpstr, 'raw', 'BGRX', 0, 1)
    
    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwndDC)
    
    return result

def CCD_dir_save(result, name):
    global im
    if result == 1:
        im.save(str(name) + ".png")

def CCD_save(result, imgPath):
    global im
    if result == 1:
        im.save(imgPath)
        
def laplacian(imgPath):
    image_ori = cv2.imread(imgPath)
    #image = image_ori[83:1042,17:1163]
    img2gray = cv2.cvtColor(image_ori, cv2.COLOR_BGR2GRAY)
    imageVar = cv2.Laplacian(img2gray, cv2.CV_64F).var()
    return imageVar

def tenengrad(imgPath):
    image = cv2.imread(imgPath)
    x = cv2.Sobel(image,cv2.CV_16S,1,0,ksize=3) 
    y = cv2.Sobel(image,cv2.CV_16S,0,1,ksize=3)
    absX = cv2.convertScaleAbs(x)
    absY = cv2.convertScaleAbs(y)
    dst = cv2.addWeighted(absX,0.5,absY,0.5,0).var()
    print(f'tenengrad:{dst:.1f}')
    return dst
        

if __name__ == '__main__':
    def main():
        folder_name = str(datetime.now())[:19].replace(':', "'")
        photo_name = 'test'
        os.mkdir(folder_name)
        imgPath = './'+ folder_name +'/'+ photo_name + '.png'
        CCD_save(getphoto(), imgPath)
        print('laplacian:', laplacian(imgPath), '\ntenengrad:', tenengrad(imgPath))
    
    main()
