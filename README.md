# ts_check

> Connect to a host via RDP service, opens windows screen allowing automated interaction in completely headless operation.

Plugin for Nagios fully conects to a windows host using TS (RDP) allowing automated interaction returning OK, WARNING, CRITICAL states as needed.

This project is a python 3 script, using Xvfb, PyVirtualDisplay wrapper and PyautoGui and optionaly x11vnc for debug purposes.

All the tests were made in CENTOS 7 host with it´s "Stock" python3 version (3.6) and with python 3.9.6 built from source targeting a Windows 2016 host.

## Installing dependencies (system packages)

```shell
 sudo yum update -y
 sudo yum install -y epel-release giflib imlib2 xfreerdp xorg-x11-server-Xvfb python3 python3-tkinter python3-devel x11vnc xdpyinfo
```

## Installing dependencies (compile python)

```shell
 sudo yum update -y
 sudo yum install -y epel-release giflib imlib2 xfreerdp xorg-x11-server-Xvfb x11vnc xdpyinfo tcl-devel tk-devel ncurses-devel bzip2-devel gdbm-devel xz-devel sqlite-devel uuid-devel readline-devel
```

## VNC

For debuging purposes we can install a VNC server to actually see whats going on when the connection is made. We need to open the VNC port:

```shell
firewall-cmd --permanent --add-port=5900/tcp
systemctl reload firewalld
 ´´´

## Installing other dependencies

```shell
 rpm -ivh http://mirror.ghettoforge.org/distributions/gf/el/7/gf/x86_64/giblib-1.2.4-27.gf.el7.x86_64.rpm
 rpm -ivh http://packages.psychotic.ninja/7/base/x86_64/RPMS/scrot-0.8-12.el7.psychotic.x86_64.rpm
 ```

## Create virtualenv and instaling Python dependencies

```shell
 su - nagios
 cd /usr/local/nagios/libexec
 mkdir ts_check
 python3.6 -m venv venv
 source venv/bin/activate
 python3.6 -m pip install --upgrade pip
 python3.6 -m pip install xlib Pillow opencv-python pyautogui keyboard pyvirtualdisplay

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

> For a NOK connection

1) Reads button_close.png to close the RDP window in gnome.
2) Obs:

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
