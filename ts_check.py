#!/usr/bin/python3

#pip install keyboard pyautogui numpy==1.19.3 Pillow opencv-contrib-python


import pyautogui
import time 
import keyboard 
import random
import cv2
import time
import os
import sys, getopt

def usage():
    print("Usage: ./tscheck.py [-H HOST] [-u user_login] [-p user_password] [-r resilience] [-c confidence]")

def main(argv):

    freerdpLocation = ""
    host = ""
    user = ""
    password = ""
    resilience = ""
    confidenceValue = ""

    f = open(os.devnull, 'w')
    sys.stderr = f

    try:
        opts, args = getopt.getopt(argv,"h?:H:u:p:x:r:c:")
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt == "-h" or opt == "-?":
            usage()
            sys.exit()
        elif opt == "-H":
            host = arg
        elif opt == "-u":
            user = arg
        elif opt == "-p":
            password = arg
        elif opt == "-x":
            freerdpLocation = arg
        elif opt == "-r":
            resilience = arg
        elif opt == "-c":
            confidenceValue = arg
    
    if freerdpLocation == "" or host == "" or user == "" or password == "":
        usage()
        sys.exit(2)
        
    execCommand = "DISPLAY=:0.0 {} /v:{} /u:{} /p:{} > /dev/null 2>&1 &".format(freerdpLocation, host, user, password)
    os.system(execCommand)

    time.sleep(5)
    ERRO = 0
    count = 0
    while count < 5:
        try:
            x,y = pyautogui.locateCenterOnScreen('/home/fernando/tscheck/print.png', grayscale=True, confidence=float(confidenceValue))
        except Exception as e:
            ERRO += 1
        else:
            ERRO -= 1 

        count += 1
        time.sleep(1)
    
    if ERRO > 0:
        for i in range(int(resilience)):
            try:
                x,y = pyautogui.locateCenterOnScreen("/home/fernando/tscheck/botao_fecha.png", grayscale=True, confidence=float(confidenceValue))
                time.sleep(0.5)
            except Exception as e:
                print("Botao fecha {}".format(e))
            else:
                time.sleep(1)
                pyautogui.moveTo(x,y)
                time.sleep(1)
                pyautogui.click()
                print("Falha na conexao RDP!")
                exit(2)
    else:
        for i in range(int(resilience)):
            try:
                x,y = pyautogui.locateCenterOnScreen("/home/fernando/tscheck/botao_iniciar.png", grayscale=True, confidence=float(confidenceValue))
                time.sleep(0.5)
            except Exception as e:
                print("Botao iniciar {}".format(e))
            else:
                pyautogui.moveTo(x,y)
                time.sleep(1)
                pyautogui.click()
                for i in range(int(resilience)):
                    try:
                        x,y = pyautogui.locateCenterOnScreen("/home/fernando/tscheck/botao_executar.png", grayscale=True, confidence=float(confidenceValue))
                        time.sleep(0.5)
                    except Exception as e:
                        print("Botao executar {}".format(e))
                    else:
                        pyautogui.moveTo(x,y-10)
                        time.sleep(1)            
                        pyautogui.click()
                        for i in range(int(resilience)):
                            try:
                                x,y = pyautogui.locateCenterOnScreen("/home/fernando/tscheck/executar.png", grayscale=True, confidence=float(confidenceValue))
                                time.sleep(0.5)
                            except Exception as e:
                                print("executar {}".format(e))
                            else:
                                pyautogui.moveTo(x,y)
                                time.sleep(1)
                                pyautogui.click()
                                time.sleep(1)
                                pyautogui.typewrite(['backspace','backspace','backspace','backspace','backspace','backspace','backspace','backspace', ], interval=0.1)
                                pyautogui.typewrite('logoff\n', interval=0.1)
                                print("Conexao RDP realizada com sucesso!")
                                exit(0)

if __name__ == "__main__":
   main(sys.argv[1:])
