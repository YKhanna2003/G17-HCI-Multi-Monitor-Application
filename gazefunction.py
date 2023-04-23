import socket
import xml.etree.ElementTree as ET
import pygetwindow as pgw
import keyboard
import mouse
import pyautogui
import openpyxl
import time

workbook = openpyxl.Workbook()
worksheet = workbook.active
worksheet['A1'] = 'S.No.'
worksheet['B1'] = 'Data X'
worksheet['C1'] = 'Data Y'
LEFT = 'left'

#Run this file after running the gazepointer application
alt_pressed = False
w_pressed = False
s_pressed = False
a_pressed = False
z_pressed = False


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("127.0.0.1",43333)) #connect to the socket

s.send("xml\n".encode("utf-8"))#Send data format
print(s.send('AppKeyDemo\n'.encode("utf-8"))) #Send AppKey
#s.settimeout(1.0)
def press(button=LEFT):
    _os_mouse.press(button)

def release(button=LEFT):
    _os_mouse.release(button)

def click(button=LEFT):
    _os_mouse.press(button)
    _os_mouse.release(button)

def onaltpres(key):
    global alt_pressed
    alt_pressed = True

def onwpres(key):
    global w_pressed
    w_pressed = True

def onspres(key):
    global s_pressed
    s_pressed = True

# def onapres(key):
#     global a_pressed
#     global alt_pressed
#     if alt_pressed:
#         if a_pressed:
#             a_pressed = False
#         else:
#             a_pressed = True

def onapres(key):
    global a_pressed
    a_pressed = True

def onaltrel(key):
    global alt_pressed
    alt_pressed = False

def onwrel(key):
    global w_pressed
    w_pressed = False

def onsrel(key):
    global s_pressed
    s_pressed = False

def onarel(key):
    global a_pressed
    a_pressed = False

def onzpres(key):
    global z_pressed
    z_pressed = True

def onzrel(key):
    global z_pressed
    z_pressed = False

# def click(button=LEFT):
#     mouse.press(button)
#     mouse.release(button)

def click(x,y):
    original_x, original_y = pyautogui.position()
    target_x, target_y = x, y
    pyautogui.moveTo(target_x, target_y, duration=0)
    pyautogui.click(button='left')
    pyautogui.moveTo(original_x, original_y, duration=0)

keyboard.on_press_key('alt',onaltpres)
keyboard.on_press_key('w',onwpres)
keyboard.on_release_key('alt',onaltrel)
keyboard.on_release_key('w',onwrel)
keyboard.on_press_key('s',onspres)
keyboard.on_release_key('s',onsrel)
keyboard.on_press_key('a',onapres)
keyboard.on_release_key('a',onarel)
keyboard.on_press_key('z',onzpres)
keyboard.on_release_key('z',onzrel)



sincedone = time.time()
i=2
while True:
    
    data = s.recv(4096)
    try:
        data = data.decode("utf-8")
    except:
        # print(repr(data))
        #print("-------------------------------------------------------------------------------")
        continue
    
    try:
        root=ET.fromstring(data[1:])
        print(root)	
        X = float(root[0].text)
        Y = float(root[1].text)
    except:
        if data.find("GazeX")!=-1 and data.find("/GazeX")!=-1:
            x1 = data.find("GazeX")
            x2 = data.find("</GazeX")
            X = float(data[x1+6:x2])
        else:
            continue
        if data.find("GazeY")!=-1 and data.find("GazeY")!=-1:
            x1 = data.find("GazeY")
            x2 = data.find("</GazeY")
            Y = float(data[x1+6:x2])
        else:
            continue
        print("alternate")
        
    
    active_window = pgw.getActiveWindow()
    if X>1350 and time.time()-sincedone>1:
        sincedone = time.time()
        keyboard.send('windows+ctrl+right')
    if X<30 and time.time()-sincedone>1:
        sincedone = time.time()
        keyboard.send('windows+ctrl+left')
    if alt_pressed:
        if w_pressed:
            try:
                print(active_window.title)
                active_window.moveTo(int(X),int(Y))
            except Exception as e:
                print(e)
                print("oopss")
                continue
        #active window follow the coordinate of gaze
        elif s_pressed:
            active_window.resizeTo(int(1000*Y/1000),int(1000*Y/1000))
        elif a_pressed:
            mouse.wheel(int(10*(500-Y)/500))
        elif z_pressed:
            click(X,Y)
    # if a_pressed:
    #     mouse.wheel(int((500-Y)/5000))
        

    print("{}: {}".format("GazeX", str(X)))
    print("{}: {}".format("GazeY", str(Y)))
    print("-------------------------------------------------------------------------------")

    a='A'+str(i)
    b='B'+str(i)
    c='C'+str(i)
    worksheet[a]=i-1
    worksheet[b]=str(X)
    worksheet[c]=str(Y)
    i+=1

    workbook.save('data.xlsx')