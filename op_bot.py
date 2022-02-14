import cv2
import numpy as np
from PIL import ImageGrab
import pymem.process
import time
from pynput.mouse import Controller as Controller
from pynput.mouse import Button
import keyboard
import win32con,win32api
import pyautogui

#Game offsets
################################################
dwForceJump = (0x52789F8)
dwLocalPlayer = (0xDB35EC)
m_fFlags = (0x104)
dwEntityList = (0x4DCEB7C)
m_iTeamNum = (0xF4)
dwGlowObjectManager = (0x5316E98)
m_iGlowIndex = (0x10488)
################################################
pm = pymem.Pymem('csgo.exe')
client = pymem.process.module_from_name(pm.process_handle,'client.dll').lpBaseOfDll
# c_x = 0
# c_y = 0
imgWidth = 420
imgHeight = 648

def execGlow():
    glow_manager = pm.read_int(client+dwGlowObjectManager)
    for i in range(1,32):
        entity = pm.read_int(client + dwEntityList + i*0x10)
        #Glow
        if entity:
            entity_team_id = pm.read_int(entity + m_iTeamNum)
            entity_glow = pm.read_int(entity + m_iGlowIndex)

            if entity_team_id == 2:
                pm.write_float(glow_manager + entity_glow * 0x38 + 0x8, float(1))
                pm.write_float(glow_manager + entity_glow * 0x38 + 0xC, float(0))
                pm.write_float(glow_manager + entity_glow * 0x38 + 0x10, float(0))
                pm.write_float(glow_manager + entity_glow * 0x38 + 0x14, float(1))
                pm.write_int(glow_manager + entity_glow * 0x38 + 0x28, 1)

            if entity_team_id == 3:
                pm.write_float(glow_manager + entity_glow * 0x38 + 0x8, float(0))
                pm.write_float(glow_manager + entity_glow * 0x38 + 0xC, float(1))
                pm.write_float(glow_manager + entity_glow * 0x38 + 0x10, float(0))
                pm.write_float(glow_manager + entity_glow * 0x38 + 0x14, float(1))
                pm.write_int(glow_manager + entity_glow * 0x38 + 0x28, 1)

def getContours(imgMask,imgDraw):
    contours, hierarchy = cv2.findContours(imgMask,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    biggerArea,biggerCont, biggerPeri = 0,0,0
    x,y,w,h = 0,0,0,0

    for cnt in contours:
        area = cv2.contourArea(cnt)
        peri = cv2.arcLength(cnt, True)
        if area > biggerArea:
            biggerCont = cnt
            biggerPeri = peri
            biggerArea = area

    if biggerArea != 0 and biggerArea > 700:
        #cv2.drawContours(imgDraw, cnt, -1, (255, 0, 0), 2)
        approx = cv2.approxPolyDP(biggerCont,0.02*biggerPeri,True)
        x,y,w,h = cv2.boundingRect(approx)
        cv2.rectangle(imgDraw,(x,y),(x+w,y+h),(255,0,0),2)
        cv2.circle(imgDraw,(x+w//2-1,y+5),5,(0,150,150),cv2.FILLED)

    return x+w//2-1, y+5,w,h

lower = np.array([0,203,117]) #hue,sat,val(min)
upper = np.array([125,255,255])#hue,sat,val(max)
mouse = Controller()
enabled = False

while True:
    execGlow()

    croppedImg = (500,144,780,576)

    img = ImageGrab.grab(bbox=(500,144,780,576))
    frame = np.array(img)
    img = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)



    imgHsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(imgHsv, lower, upper)
    imgResult = cv2.bitwise_and(img, img, mask = mask)

    x,y,w,h = getContours(mask,imgResult)


    if keyboard.is_pressed('p'):
        if enabled == True:
            enabled = False
        else:
            enabled = True


    if enabled == True:
        if x!=0 and y!=0:

            c_x, c_y = pyautogui.position()
            xDist = x - c_x
            yDist = y - c_y

            # print('x:', x,'y:',y)
            # print('cx:',c_x,'cy:',c_y)
            # print('xDist:',xDist,'yDist:',yDist)
            # print()
            
            win32api.mouse_event(win32con.MOUSEEVENTF_MOVE,xDist*2,yDist*2,0,0)

            time.sleep(0.06)
            mouse.press(Button.left)
            time.sleep(0.2)
            mouse.release(Button.left)
            enabled = False

    imgResult = cv2.resize(imgResult,(imgWidth,imgHeight))
    cv2.imshow('Output', imgResult)

    if cv2.waitKey(1) and keyboard.is_pressed('end'):
        break

