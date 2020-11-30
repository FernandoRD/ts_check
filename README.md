# ts_check

> Check if a RDP service is stil responsive and opens windows screen after connection

 Plugin for Nagios fully conects to a windows host using TS (RDP) and verifies if the windows screen loads and after that disconect returning an OK/CRITICAL state

This project is a python 3 script, aided with a shell script that allows Nagios open a graphcal TS session from an Linux server with a GUI installed.

## Installing graphical interface

```shell
 sudo yum groups list
 sudo yum groups install "Servidor com GUI"
 sudo systemctl set-default graphical.target
```

## Installing python3 and other dependencies

```shell
 wget http://packages.psychotic.ninja/7/base/x86_64/RPMS/psychotic-release-1.0.0-1.el7.psychotic.noarch.rpm
 sudo rpm -Uvh psychotic-release-1.0.0-1.el7.psychotic.noarch.rpm
 sudo yum --enablerepo=psychotic install scrot
 sudo yum install python3 python3-tkinter python3-devel
 pip3 install keyboard pyautogui numpy==1.19.3 Pillow opencv-contrib-python
 ```

## Installing xfreerdp

```shell
 sudo yum install xfreerdp
```

## OPTIONAL: Install x11VNC and make it connect at default screen for remote management

```shell
 sudo yum install x11vnc
 sudo x11vnc -storepasswd yourVNCpasswordHERE /etc/x11vnc.pass
 sudo nano /usr/lib/systemd/system/x11vnc.service
    [Unit]
    Description="x11vnc"
    Requires=display-manager.service
    After=display-manager.service

    [Service]
    ExecStart=/usr/bin/x11vnc -xkb -noxrecord -noxfixes -noxdamage -display :0 -auth guess -rfbauth /etc/x11vnc.pass
    ExecStop=/usr/bin/killall x11vnc
    Restart=on-failure
    Restart-sec=2

    [Install]
    WantedBy=multi-user.target

 sudo systemctl daemon-reload && sudo systemctl enable x11vnc && sudo systemctl start x11vnc

 sudo reboot
```

## Preparing system for Nagios use start RDP session remotely:

* As the user that runs the script (nagios), inside GUI:

```shell
 gnome-control-center display - adjust resolution to fit your needs
```

![Resolution](https://github.com/FernandoRD/ts_check/blob/main/images/picture1.png)

```shell
 gnome-control-center privacy - Turn off block screen
```

![Block Screen](https://github.com/FernandoRD/ts_check/blob/main/images/picture2.png)

```shell
 gnome-control-center energy - "Turn off screen" - Adjust to Never
```

![Turn off Screen](https://github.com/FernandoRD/ts_check/blob/main/images/picture4.png)

* Define automatic login for user nagios

![Automatic Login](https://github.com/FernandoRD/ts_check/blob/main/images/picture3.png)

* Alter /var/run/gdm permissions:

```shell
 sudo chmod 755 /var/run/gdm
```

* Create a symbolic lynk in the user´s directory:

```shell
 sudo ln -s /var/run/gdm/auth-for-nagios-XXX/database .Xauthority
```

This link will become broken at each reboot of the server, because the XXX value changes, but the shell script handle to look at it.

Edit /etc/sudoers for user nagios that runs the script
Quickest way...

```shell
# visudo

    # NEEDED TO ALLOW NAGIOS TO CHECK SERVICE STATUS
    Defaults:nagios !requiretty
    nagios ALL=(ALL) NOPASSWD: ALL

    # ASTERISK-SPECIFIC CHECKS
    # NOTE: You can uncomment the following line if you are monitoring Asterisk locally
    #nagios ALL=NOPASSWD: /usr/local/nagios/libexec/check_asterisk_sip_peers.sh, /usr/local/nagios/libexec/nagisk.pl, /usr/sbin/asterisk
```

## Connection Configuration

> This time the script uses a ssh connection to execute, due to several problems that occured trying to make nrpe runs it properly.

* Creating ssh key to passwordless connection between Nagios and the Linux GUI Server.

> At Nagios server in nagio´s user dir:

```shell
 ssh-keygen
 Generating public/private rsa key pair.
 Enter file in which to save the key (/home/nagios/.ssh/id_rsa):
```

> You may choose the default or create a key for this connection

```shell
 Enter file in which to save the key (/home/nagios/.ssh/id_rsa): monitor
 Enter passphrase (empty for no passphrase):
 Enter same passphrase again:
 Your identification has been saved in monitor.
 Your public key has been saved in monitor.pub.
```

> After you need to send the key to the Linux GUI Server:

```shell
 ssh-copy-id -i monitor nagios@Linux_GUI_Server_IP
```

> Test the connection:

```shell
 ssh -i monitor nagios@Linux_GUI_Server_IP
```

You must connect directly without having to type a password...

> Copy the plugin scripts (ts_check.sh and ts_check.py) to nagios´s libexec directory:

```shell
 cp ts_check* /usr/local/nagios/libexec/
```

> Create an tscheck dir inside libexec to store the pictures the script will use:

```shell
mkdir /usr/local/nagios/libexec/tscheck
```
## Script execution

When Nagios calls the script it connects to the windows server and recognizes if the connection was successfull or not, and then executes some procedures.

### Pictures used in the actual script version

The pictures are actually used for the logoff process, that could be OK or NOK.

* print.png
* button_close.png
* button_start.png
* button_execute.png
* dialog_execute.png

### Sequence

> For an OK connection

1) Reads print.png to check if the screen element apears.
2) Reads button_start.png to click in start.
3) Reads button_exec.png to open exec dialog box
4) Reads dialog_exec.png to click in the field and writes "logoff" and send an ENTER

> For a NOK connection

1) Reads button_close.png to close the RDP window in gnome.
2) Obs:

* There are some WindowsXP pictures in the repository that I used to develop

* The script uses a function that will click at the center of the pictures, be carefull when take the prints to keep where do you want to click as colse to the center as possible. You may do some adjustments by increasing or decreasing the x and y variables accordingly.

## Nagios Configuration



![Nagios Config](https://github.com/FernandoRD/ts_check/blob/main/images/picture5.png)

> Check_by_ssh parameters options:
* -t \<timeout\> 
* -i \<created ssh key location\>
* -C \<ssh command to execute\>

> ts_check parameters options:

* -H \<host_name or IP\>
* -u \<ts_user\>
* -p \<ts_user password\>
* -r \<resilience int\>
* -c \<confidence float\>
* -x \<xfreerdp path\>

### Example of $ARG1$

-t 60 -i /home/nagios/.ssh/monitoramento

### Example of $ARG2$

-C "/usr/local/nagios/libexec/ts_check.sh -H 192.168.0.109 -u rdp_win_user -p foo -x xfreerdp -r 3 -c 0.8"

> Tip: Command takes a wile to execute, it is better to use at least a timeout of 60 sec.

## Developing

Feel free to download, use e modify it:

```shell
 git clone https://github.com/FernandoRD/ts_check.git
```

## Credits

Thanks to Kian Brose <https://github.com/KianBrose>

With the image recognition insigts.

## Licensing

"The code in this project is licensed under MIT license."
