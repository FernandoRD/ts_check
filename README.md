# ts_check

> Connect to a host via RDP service, opens windows screen allowing automated interaction in completely headless operation.

Plugin for Nagios that connects to a windows host using TS (RDP) allowing automated interaction returning OK, WARNING, CRITICAL states as needed.

This project is a python 3 script, using Xvfb, PyVirtualDisplay wrapper and PyautoGui and optionaly x11vnc for debug purposes.

All the tests were made in Ubuntu 22.04 host targeting a Windows 2016 host.

## Installing dependencies (system packages)

```shell
 sudo apt update -y
 sudo apt install giflib-tools libimlib2 xvfb x11vnc x11-utils freerdp2-x11 giblib1 scrot python3.10-venv python3-tk python3-dev
```

## Create virtualenv and instaling Python dependencies

```shell
 su - zabbix (need to edit /etc/passwd to allow this)
 cd /usr/lib/zabbix/externalscripts
 mkdir ts_check
 python3.X -m venv venv
 source venv/bin/activate
 python3.X -m pip install --upgrade pip
 python3.X -m pip install xlib Pillow opencv-python pyautogui keyboard pyvirtualdisplay

 edit file venv/lib64/python3.X/site-packages/pyscreeze/__init__.py to prevent error messages from scrot:

 Replace:

 if scrotExists:
        subprocess.call(['scrot', '-z', tmpFilename])
        im = Image.open(tmpFilename)
 for:

 if scrotExists:
        subprocess.call(['scrot', tmpFilename])
        im = Image.open(tmpFilename)

```

## Script execution

When Nagios calls the script it creates a Xvfb and uses it to connect to the windows server and recognizes if the connection was successfull or not, and then executes.

### Pictures used in the actual script version

The pictures are actually used for the logoff process, that could be OK or NOK.

* print.png
* search_button.png
* search.png

### Sequence

> For an OK connection

1) Reads print.png to check if the screen element apears.
2) Reads search_button.png to click in search.
3) Reads search.png to click in the field and writes "logoff" and send an ENTER.
4) Obs:

* There are some Windows 2016 Server pictures in the repository that I used to develop.

* The script uses a function that will click at the center of the pictures, be carefull when take the prints to keep where do you want to click as close to the center as possible. You may do some adjustments by increasing or decreasing the x and y variables accordingly.

## Developing

Feel free to download, use and modify it:

```shell
 git clone https://github.com/FernandoRD/ts_check.git
```

## Credits

"https://github.com/ponty/PyVirtualDisplay"
"https://en.wikipedia.org/wiki/Xvfb"
"https://gist.github.com/ypandit/f4fe751bcbf3ee6a32ca"
"https://www.freerdp.com/"
"https://github.com/ponty/easyprocess"
"https://docs.python.org/3/library/subprocess.html"
"https://pypi.org/project/PyAutoGUI/"
"https://abhishekvaid13.medium.com/pyautogui-headless-docker-mode-without-display-in-python-480480599fc4"
"https://pypi.org/project/opencv-python/"
"http://packages.psychotic.ninja/7/base/x86_64/RPMS/"
"https://github.com/asweigart/pyautogui/issues/372"

## Licensing

"The code in this project is licensed under MIT license."
