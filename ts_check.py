import os
import time
import keyboard 
import random
import time
import sys
from pyvirtualdisplay import Display
import Xlib.display
import argparse


def main():

    host = ""
    user = ""
    password = ""
    
    my_parser = argparse.ArgumentParser(description='Conect to a windows host through RDP anda run commands .', epilog='Created by Fernando Durso, GitHub: FernandoRD')
    my_parser.add_argument('-H','--host', action='store', type=str, required=True, help='Host to connect.')
    my_parser.add_argument('-u','--user', action='store', type=str, required=True, help='Username.')
    my_parser.add_argument('-p','--password', action='store', type=str, required=True, help='Password.')
    my_parser.add_argument('-x','--xfree', action='store', type=str, required=False, help='Location of xfreerdp executable. (if not running in docker)')
    my_parser.add_argument('-R','--resilience', action='store', type=int, required=False, default=2, choices=range(2, 11), help='Resilience Value.')
    my_parser.add_argument('-C','--confidence', action='store', type=float, required=False, default=0.9, choices=range(1, 11), help='Confidence Value.')
    my_parser.add_argument('-i','--interval', action='store', type=float, required=False, default=0.5, help='Action interval time.')
    my_parser.add_argument('-l','--load', action='store', type=int, required=False, default=5, help='RDP load time.')
    my_parser.add_argument('-v','--vnc', action='store_true', required=False, help='VNC Server see whats going on.')
    my_parser.add_argument('-d','--debug', action='store_true', required=False, help='Debug info.')
    my_parser.add_argument('-s','--screenshot', action='store_true', required=False, help='Take the first screenshot after successfull connection and exit.')
    my_parser.add_argument('-e','--exec', action='store', type=str, required=False, help='Python script to import & execute')
    my_parser.add_argument('-y','--system', action='store', type=str, required=True, help='Images folder')
    my_parser.add_argument('-w','--warning', action='store', type=int, required=False, default=5, help='WARNING threshold (seconds of execution).')
    my_parser.add_argument('-c','--critical', action='store', type=int, required=False, default=10, help='CRITICAL threshold (seconds of execution).')
    
    args = my_parser.parse_args()

    freerdpLocation = args.xfree
    host = args.host
    user = args.user
    password = args.password
    resilienceValue = args.resilience
    confidenceValue = args.confidence/10
    vnc = args.vnc
    debug = args.debug
    interval = args.interval
    screenshot = args.screenshot
    exec_script = args.exec
    load = args.load
    warning = args.warning
    critical = args.critical
    system = args.system
    
    images_folder = "/images"
    exec_folder = "/exec"

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
    if freerdpLocation:
        execCommand = f"export DISPLAY={current_display} && {freerdpLocation} /v:{host} /u:{user} /p:{password} /cert:tofu /f /bpp:15 +compression -wallpaper /audio-mode:2 >/dev/null 2>&1 &"
    else:
        execCommand = f"export DISPLAY={current_display} && /usr/bin/xfreerdp /v:{host} /u:{user} /p:{password} /cert:tofu /f /bpp:15 +compression -wallpaper /audio-mode:2 >/dev/null 2>&1 &"

    os.system(execCommand)
    if exec_script:
        # Give some time to RDP to open....
        time.sleep(load)
        # Test if windows screen loaded successfully...
        # Take the screenshot
        if screenshot:
            try:
                pyautogui.screenshot(f"{images_folder}/screen.png")
            except Exception as e:
                print(f'Screenshot failed...{e}')
                disp.stop()
                sys.exit(2)
            else:
                print('Screenshot saved...')
                disp.stop()
                sys.exit(0)    
        failure_load_screen = 0
        i = 0
        while i < resilienceValue:
            try:
                x,y = pyautogui.locateCenterOnScreen(f"{images_folder}/screen.png", grayscale=True, confidence=confidenceValue)
            except Exception as e:
                failure_load_screen += 1
                if failure_load_screen == resilienceValue:
                    print("CRITICAL: RDP connection failure!")
                    print(e)
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

        # Import a module with its name passed as argument
        # The module will have one function called actions that do the interaction with the RDP
        # In this way, just need a .py for each interaction e pass it as parameter (without the .py extension)
        
        sys.path.append(exec_folder)
        exec_module = __import__(exec_script)
    
        # Escrever exemplo, abrir notepad, escrever alguma coisa e salvar
        exec_module.actions(pyautogui, resilienceValue, confidenceValue, debug, disp, interval, failure_search_buttom, failure_search, images_folder)

        # LOGOFF PROCESS BEGINS...
        pyautogui.hotkey('win', 's')
        time.sleep(interval)
        pyautogui.typewrite('logoff', interval=0.1)
        time.sleep(interval)
        pyautogui.press('enter')

        if debug:
            print(f"Statistics (Reconition failures): Load Screen: {failure_load_screen}, Search Buttom: {failure_search_buttom}, Search: {failure_search}")
        # Stop display after a successfull execution.     
        disp.stop()

        total_time=time.time() - start_time
        if system == 'zabbix':
            print(f"{total_time:.2f}")
        elif system == 'nagios':
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
