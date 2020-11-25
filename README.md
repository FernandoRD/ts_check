# ts_check

> Check if a RDP service is stil responsive and opens windows screen after connection

 Plugin for Nagios fully conects to a windows host using TS (RDP) and verifies if the windows screen loads and after that disconect returning an OK/CRITICAL state

This project is a python 3 script, aided with a shell script that allows Nagios open a graphcal TS session from an Linux server with a GUI installed.

## Installing / Getting started

What do you need to run ts_check

* Linux server with GUI installed
* Python 3
* xfreerdp package

### Installing graphical interface

* As root:

```shell
 yum groups list
 yum groups install "Servidor com GUI"
 systemctl set-default graphical.target
 yum install xfreerdp
 yum install python3-tkinter python3-devel
 pip install keyboard pyautogui numpy==1.19.3 Pillow opencv-contrib-python

 wget http://packages.psychotic.ninja/7/base/x86_64/RPMS/psychotic-release-1.0.0-1.el7.psychotic.noarch.rpm
 rpm -psychotic-release-1.0.0-1.el7.psychotic.noarch.rpm
 yum --enablerepo=psychotic install scrot
```

> Preparing system for Nagios use start RDP session remotely:

* As the user that runs the script, inside GUI:

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

* Define automatic login for user

![Automatic Login](https://github.com/FernandoRD/ts_check/blob/main/images/picture3.png)

* As root alter /var/run/gdm permissions:

```shell
 chmod 755 /var/run/gdm
```

* Create a symbolic lynk in the user´s directory:

```shell
 ln -s /var/run/gdm/auth-for-user-XXX/database .Xauthority
```

This link will become broken at each reboot of the server, because the XXX value chenges, but the shell script handle to lokk at it.

Edit /etc/sudoers for user that runs the script (ex: nagios)
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

### NRPE Configuration

> Before running you need to configure nrpe to execute the plugin.

* Edit the nrpe.cfg

```shell
 nano /usr/local/nagios/etc/nrpe.cfg
```

* Append to end of the file:

```shell
 command[ts_check]=sudo /home/nagios/tscheck/ts_check.sh $ARG1
```

* Restart NRPE:

```shell
 service xinetd restart
```

### Nagios Configuration

![Nagios Config](https://github.com/FernandoRD/ts_check/blob/main/images/picture5.png)

> Parameters options:

* -H \<host_name or IP\>
* -u \<ts_user\>
* -p \<ts_user password\>
* -r \<resilience int\>
* -c \<confidence float\>
* -x \<xfreerdp path\>

### Example of $ARG1$

-a '-H 192.168.0.100 -u ts_user -p foo -r 3 -c 0.8 -x xfreerdp'

> Tip: Command takes a wile to execute, it is better to create a nrpe command with a timeout of 60 sec.

### Final preparation

You gonna find 3 .png files together with the scripts. They´re used in the image recognition, take the screeshots that suits your enviroment. (Those are taken from WinXP for testing)

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
