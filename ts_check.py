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
from numpy import arange

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
    my_parser.add_argument('-w','--warning', action='store', type=int, required=False, default=5, help='WARNING threshold (seconds of execution).')
    my_parser.add_argument('-c','--critical', action='store', type=int, required=False, default=10, help='CRITICAL threshold (seconds of execution).')
    my_parser.add_argument('-v','--vnc', action='store_true', required=False, help='VNC Server for debug.')

    args = my_parser.parse_args()

    freerdpLocation = args.exec
    host = args.host
    user = args.user
    password = args.password
    resilienceValue = args.resilience
    confidenceValue = args.confidence/10
    use_vnc = args.vnc
    warning = args.warning
    critical = args.critical

    disp = Display(visible=True, size=(1115, 864), backend="xvfb", use_xauth=True)
    # Start the current display to use
    # If there is none display in use, create de :0 else create some :X to use
    disp.start()
    try:
        current_display = str(os.environ.get('DISPLAY'))
    except:
        print("Starting Xvfb default...")
        os.system("Xvfb :0")
    else:
        try:
            current_display = str(os.environ.get('DISPLAY'))
        except:
            print("Xvfb :0 init failure... aborting...")
            sys.exit(2)
        else:
            print(current_display)
            import pyautogui
    if use_vnc:
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
    failure_load_screen = 0
    for i in range(int(resilienceValue)):
        try:
            x,y = pyautogui.locateCenterOnScreen("./print.png", grayscale=True, confidence=confidenceValue)
        except Exception:
            failure_load_screen += 1
        else:
            break 
        time.sleep(1)

    # Set to 0 the number os recognition failures
    failure_search_buttom = 0
    failure_search = 0

    if failure_load_screen == int(resilienceValue) - 1:
        print("RDP connection failure!")
        disp.stop()
        sys.exit(2)
    else:
        # At this point we should have a working RDP connection...
        #
        # Here you may write your own code doing automated stuff inside your server ;-)
        #
        # LOGOFF PROCESS BEGINS...
        for i in range(int(resilienceValue)):
            try:
                x,y = pyautogui.locateCenterOnScreen("./search_buttom.png", grayscale=True, confidence=confidenceValue)
                time.sleep(0.5)
            except Exception as e:
                failure_search_buttom += 1
            else:
                pyautogui.moveTo(x,y)
                time.sleep(1)
                pyautogui.click()
                time.sleep(1)
                for i in range(int(resilienceValue)):
                    try:
                        x,y = pyautogui.locateCenterOnScreen("./search.png", grayscale=True, confidence=confidenceValue)
                        time.sleep(0.5)
                    except Exception as e:
                        failure_search += 1
                    else:
                        pyautogui.moveTo(x,y)
                        time.sleep(1)
                        pyautogui.click()
                        time.sleep(1)
                        pyautogui.typewrite('logoff', interval=0.1)
                        pyautogui.press('enter')
                        print("RDP connection success!")
                        total_time=time.time() - start_time
                    break
        if use_vnc:
            print("Statistics (Reconition failures): Load Screen: {}, Search Buttom: {}, Search: {}".format(failure_load_screen, failure_search_buttom, failure_search))
        disp.stop()
                        
    if total_time < warning:
        print("OK: Execution time: {:.2f} s | exec_time={:.2f}s;{};{};0;{}".format(total_time, total_time, warning, critical, critical*2))
        exit(0)
    elif total_time > warning and total_time < critical:
        print("WARNING: Execution time: {:.2f} s | exec_time={:.2f}s;{};{};0;{}".format(total_time, total_time,warning, critical, critical*2))
        exit(1)
    elif total_time > critical:
        print("CRITICAL: Execution time: {:.2f} s | exec_time={:.2f}s;{};{};0;{}".format(total_time, total_time, warning, critical, critical*2))
        exit(2)

if __name__ == "__main__":
   main()
