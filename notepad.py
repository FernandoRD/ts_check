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

def actions(pyautogui, resilienceValue, confidenceValue, debug, disp, interval, failure_search_buttom, failure_search):    
    i = 0
    while i < resilienceValue:
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

    i = 0
    while i < resilienceValue:
        try:
            x,y = pyautogui.locateCenterOnScreen("./search.png", grayscale=True, confidence=confidenceValue)                    
        except Exception as e:
            failure_search += 1
            if failure_search == resilienceValue:
                print("CRITICAL: Could not find search field!")
                if debug:
                    print(f"Search recognition failures: {failure_search}")
                    pyautogui.screenshot('./screenshot_failure_search.png')
                disp.stop()
                sys.exit(2)
            time.sleep(interval)
            i += 1
            print("Aqui falhou 2")
        else:
            pyautogui.moveTo(x,y)
            time.sleep(interval)
            pyautogui.typewrite('notepad', interval=0.2)
            if debug:
                print(f"Search recognition failures: {failure_search}")
                pyautogui.screenshot('./screenshot_failure_search.png')
            pyautogui.press('enter')
            i += resilienceValue
            print("Aqui achou 2")
