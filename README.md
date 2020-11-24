# ts_check

> Check if a RDP service is stil responsive and opens windows screen after connection

 Plugin for Nagios fully conects to a windows host using TS (RDP) and verifies if the windows screen loads and after that disconect returning an OK/CRITICAL state

This project is a python 3 script, aided with a shell script that allows Nagios open a graphcal TS session from an Linux server with a GUI installed.

## Installing / Getting started

What do you need to run ts_check

* Linux server with GUI installed
* Python 3
* xfreerdp package

> Installing graphcal interface:

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

```shell
 gnome-control-center display - adjust resolution to fit your needs
```

![Resolution](https://github.com/FernandoRD/ts_check/blob/main/images/picture1.png)

```shell
 gnome-control-center privacy - Turn off block screen
```

![Lock Screen](https://github.com/FernandoRD/ts_check/blob/main/images/picture2.png)

```shell
 gnome-control-center energy - "Turn off screen" - Adjust to Never
```

![Lock Screen](https://github.com/FernandoRD/ts_check/blob/main/images/picture4.png)

Define automatic login for user

![Lock Screen](https://github.com/FernandoRD/ts_check/blob/main/images/picture3.png)

As root alter /var/run/gdm permissions:

```shell
 chmod 755 /var/run/gdm
```

no diretorio do usuário que executa o script:
In the user´s directory:

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


### Initial Configuration

Before running you need to fill the two text files, servers.txt and tokens.txt in the following way:

```shell
$ nano servers.txt
test1:192.168.0.1
test2:192.168.0.2
test3:192.168.0.3

$ nano tokens.txt
test1:845gbjukUjI6eaNujgUnfohtdFPTZb3JAEH05rWcdrXbvxjh7lh6jnZfTJJTl8m
test2:ponvt666atI6eaNoprq08sUEqqgi873vEH05rWxdrkXbvgjh7lh6jnZfTJJTl8m
test3:yuhnbrtdteI6eaNoprq08sUEFPTZb3JAxH05rWcdrkXbvgjh7lh6jnZfTJJTl8m
```

## Developing

Feel free to download, use e modify it:

```shell
git clone https://github.com/FernandoRD/NagiosXI_api.git
```

## Features

## Licensing

"The code in this project is licensed under MIT license."
