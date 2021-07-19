import os
import time
import keyboard 
import random
#import cv2
import time
import sys, getopt
from pyvirtualdisplay import Display
import Xlib.display

def usage():
    print("Usage: ./tscheck.sh [-H HOST] [-u user_login] [-p user_password] [-r resilienceValue int min 2] [-c confidence float 0 up to 1] [-x xfreerdp_path] [-v] Debug (VNC connection)")

def main(argv):

    freerdpLocation = ""
    host = ""
    user = ""
    password = ""
    resilienceValue = ""
    confidenceValue = ""
    use_vnc=False

    try:
        opts, args = getopt.getopt(argv,"h?:H:u:p:x:r:c:v")
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
            resilienceValue = arg
        elif opt == "-c":
            confidenceValue = arg
        elif opt == "-v":
            use_vnc=True
    
    if freerdpLocation == "" or host == "" or user == "" or password == "" or resilienceValue < 2 or confidenceValue < 0 or confidenceValue > 1:
        usage()
        sys.exit(2)
    
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
            import pyautogui
    if use_vnc:
        os.system(f"x11vnc -display {current_display} -bg -forever -nopw -quiet -xkb")
        print("Please connect to this host at VNC port (5900)...continuing in 10 sec...")
        time.sleep(10)
    # Pass to pyautogui the display number to use
    pyautogui._pyautogui_x11._display = Xlib.display.Display(os.environ['DISPLAY'])
    # Start RDP Connection...
    execCommand = "export DISPLAY={} && {} /v:{} /u:{} /p:{} /cert:tofu /f /bpp:15 +compression -themes -wallpaper /audio-mode:2 >/dev/null 2>&1 &".format(current_display, freerdpLocation, host, user, password)
    os.system(execCommand)
    # Give some time to RDP to open....
    time.sleep(5)
    # Test if windows screen loaded successfully...
    failure_load_screen = 0
    for i in range(int(resilienceValue)):
        try:
            x,y = pyautogui.locateCenterOnScreen("./print.png", grayscale=True, confidence=float(confidenceValue))
        except Exception:
            failure_load_screen += 1
        else:
            break 
        time.sleep(1)

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
                x,y = pyautogui.locateCenterOnScreen("./search_buttom.png", grayscale=True, confidence=float(confidenceValue))
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
                        x,y = pyautogui.locateCenterOnScreen("./search.png", grayscale=True, confidence=float(confidenceValue))
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
                        print("Statistics (Reconition failures): Search Buttom: {}, Search: {}".format(failure_search_buttom, failure_search))
                        disp.stop()
                        sys.exit(0)

if __name__ == "__main__":
   main(sys.argv[1:])
