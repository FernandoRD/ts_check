#!/usr/local/nagios/libexec/python_web_checks/ts_check/venv/bin/python3.9
import os
import time
import keyboard 
import random
#import cv2
import time
import sys
from pyvirtualdisplay import Display
import Xlib.display
import argparse
import datetime


def actions(pyautogui, resilienceValue, confidenceValue, debug, disp, interval, failure_search_buttom, failure_search):    
    i = 0
    while i < resilienceValue:
        try:
            pyautogui.hotkey('win', 's')
            time.sleep(interval)
            x,y = pyautogui.locateCenterOnScreen("./search.png", grayscale=True, confidence=confidenceValue)
            pyautogui.moveTo(x,y)
            pyautogui.click()
        except:
            try:
                x,y = pyautogui.locateCenterOnScreen("./search_buttom.png", grayscale=True, confidence=confidenceValue)
            except Exception as e:
                failure_search_buttom += 1
                if failure_search_buttom == resilienceValue:
                    print("CRITICAL: Could not find search buttom!")
                    if debug:
                        print(f"Search Buttom recognition failures: {failure_search_buttom}")
                        pyautogui.screenshot('./screenshot_failure_search_buttom.png')
                    disp.stop()
                    sys.exit(2)
                time.sleep(interval)
                i += 1
                print("Aqui falhou 1")
            else:
                pyautogui.moveTo(x,y)
                time.sleep(interval)
                pyautogui.click()
                if debug:
                    print(f"Search Buttom recognition failures: {failure_search_buttom}")
                    pyautogui.screenshot('./screenshot_failure_search_buttom.png')
                i += resilienceValue
                print("Aqui achou 1")
        else:
            #pyautogui.moveTo(x,y)
            #time.sleep(interval)
            pyautogui.typewrite('notepad ', interval=0.1)
            time.sleep(interval)
            if debug:
                print(f"Search recognition failures: {failure_search}")
                pyautogui.screenshot('./screenshot_failure_search.png')
            pyautogui.press('enter')
            time.sleep(interval)
            i += resilienceValue
            print("Aqui achou 2")

    i = 0
    while i < resilienceValue:
        try:
            x,y = pyautogui.locateCenterOnScreen("./notepad.png", grayscale=True, confidence=confidenceValue)                    
        except Exception as e:
            failure_search += 1
            if failure_search == resilienceValue:
                print("CRITICAL: Could not find notepad!")
                if debug:
                    print(f"Search recognition failures: {failure_search}")
                    pyautogui.screenshot('./screenshot_failure_search.png')
                disp.stop()
                sys.exit(2)
            time.sleep(interval)
            i += 1
            print("Aqui falhou 3")
        else:
            pyautogui.moveTo(x,y)
            time.sleep(interval)
            pyautogui.click()
            time.sleep(interval)
            pyautogui.typewrite('Some test you wanna write', interval=0.1)
            time.sleep(interval)
            pyautogui.hotkey('ctrl', 's')
            time.sleep(interval)
            x = datetime.datetime.now()
            pyautogui.typewrite(f'arquivo-{x.strftime("%Y-%m-%d %H-%M-%S")}.txt', interval=0.1)
            time.sleep(interval)
            pyautogui.press('enter')
            time.sleep(interval)
            pyautogui.hotkey('alt', 'f4')
            time.sleep(interval)
            if debug:
                print(f"Search recognition failures: {failure_search}")
                pyautogui.screenshot('./screenshot_failure_search.png')
            pyautogui.press('enter')
            i += resilienceValue
            print("Aqui achou 3")