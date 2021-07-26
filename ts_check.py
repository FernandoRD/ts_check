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

def main():

    freerdpLocation = ""
    host = ""
    user = ""
    password = ""
    
    my_parser = argparse.ArgumentParser(description='Conect to a windows host through RDP anda run commands .', epilog='Created by Fernando Durso')
    my_parser.add_argument('-H','--host', action='store', type=str, required=True, help='Host to connect.')
    my_parser.add_argument('-u','--user', action='store', type=str, required=True, help='Username.')
    my_parser.add_argument('-p','--password', action='store', type=str, required=True, help='Password.')
    my_parser.add_argument('-x','--exec', action='store', type=str, required=True, help='Location of xfreerdp executable.')
    my_parser.add_argument('-R','--resilience', action='store', type=int, required=False, default=2, choices=range(2, 11), help='Resilience Value.')
    my_parser.add_argument('-C','--confidence', action='store', type=float, required=False, default=0.9, choices=range(1, 11), help='Confidence Value.')
    my_parser.add_argument('-i','--interval', action='store', type=float, required=False, default=0.5, help='Action interval time.')
    my_parser.add_argument('-w','--warning', action='store', type=int, required=False, default=5, help='WARNING threshold (seconds of execution).')
    my_parser.add_argument('-c','--critical', action='store', type=int, required=False, default=10, help='CRITICAL threshold (seconds of execution).')
    my_parser.add_argument('-v','--vnc', action='store_true', required=False, help='VNC Server see whats going on.')
    my_parser.add_argument('-d','--debug', action='store_true', required=False, help='Debug info.')
    my_parser.add_argument('-s','--screenshot', action='store_true', required=False, help='Take the first screenshot after successfull connection and exit.')

    args = my_parser.parse_args()

    freerdpLocation = args.exec
    host = args.host
    user = args.user
    password = args.password
    resilienceValue = args.resilience
    confidenceValue = args.confidence/10
    vnc = args.vnc
    debug = args.debug
    interval = args.interval
    screenshot = args.screenshot
    warning = args.warning
    critical = args.critical

    disp = Display(visible=True, size=(1115, 864), backend="xvfb", use_xauth=True)
    # Start the current display to use
    # If there is none display in use, create de :0 else create some :X to use
    disp.start()
    try:
        current_display = str(os.environ.get('DISPLAY'))
    except:
        if debug:
            print("Starting Xvfb default...")
        os.system("Xvfb :0")
    else:
        try:
            current_display = str(os.environ.get('DISPLAY'))
        except:
            print("Xvfb :0 init failure... aborting...")
            sys.exit(2)
        else:
            if debug:
                print(f'Current DISPLAY is {current_display}')
            import pyautogui
    if vnc:
        os.system(f"x11vnc -display {current_display} -bg -forever -nopw -quiet -xkb")
        print("Please connect to this host at VNC port (5900)...continuing in 10 sec...")
        time.sleep(10)
    # Pass to pyautogui the display number to use
    pyautogui._pyautogui_x11._display = Xlib.display.Display(os.environ['DISPLAY'])
    # Start measuring execution time
    start_time=time.time()
    # Start RDP Connection...
    execCommand = "export DISPLAY={} && {} /v:{} /u:{} /p:{} /cert:tofu /f /bpp:15 +compression -themes -wallpaper /audio-mode:2 >/dev/null 2>&1 &".format(current_display, freerdpLocation, host, user, password)
    os.system(execCommand)
    # Give some time to RDP to open....
    time.sleep(5)
    # Test if windows screen loaded successfully...
    # Take the screenshot
    failure_load_screen = 0
    i = 0
    while i < resilienceValue:
        try:
            x,y = pyautogui.locateCenterOnScreen("./screen.png", grayscale=True, confidence=confidenceValue)
        except Exception as e:
            failure_load_screen += 1
            if failure_load_screen == resilienceValue:
                print("CRITICAL: RDP connection failure!")
                disp.stop()
                sys.exit(2)
            time.sleep(interval)
            i += 1
        else:
            i += resilienceValue
                    
    if debug:
        print(f"Load Screen recognition failures: {failure_load_screen}")
        
    # Set to 0 the number os recognition failures
    failure_search_buttom = 0
    failure_search = 0

    # At this point we should have a working RDP connection...
    if screenshot:
        try:
            pyautogui.screenshot('./screen.png')
        except Exception as e:
            print(f'Screenshot failed...{e}')
            disp.stop()
            sys.exit(2)
        else:
            print('Screenshot saved...')
            disp.stop()
            sys.exit(0)
    #
    # Here you may write your own code doing automated stuff inside your server ;-)
    #
    # LOGOFF PROCESS BEGINS...
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
            pyautogui.typewrite('logoff', interval=0.2)
            if debug:
                print(f"Search recognition failures: {failure_search}")
                pyautogui.screenshot('./screenshot_failure_search.png')
            pyautogui.press('enter')
            total_time=time.time() - start_time
            i += resilienceValue
            print("Aqui achou 2")

    if debug:
        print(f"Statistics (Reconition failures): Load Screen: {failure_load_screen}, Search Buttom: {failure_search_buttom}, Search: {failure_search}")
    # Stop display after a successfull execution.     
    disp.stop()

    try:
        if total_time < warning:
            print(f"OK: Execution time: {total_time:.2f} s | exec_time={total_time:.2f}s;{warning};{critical};0;{critical*2}")
            exit(0)
        elif total_time > warning and total_time < critical:
            print(f"WARNING: Execution time: {total_time:.2f} s | exec_time={total_time:.2f}s;{warning};{critical};0;{critical*2}")
            exit(1)
        elif total_time > critical:
            print(f"CRITICAL: Execution time: {total_time:.2f} s | exec_time={total_time:.2f}s;{warning};{critical};0;{critical*2}")
            exit(2)
    except Exception as e:
        print(f"CRITICAL: RDP connection failure! {e}")
        sys.exit(2)

if __name__ == "__main__":
   main()
