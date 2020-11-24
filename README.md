# ts_check

> Check if a RDP service is stil responsive and opens windows screen after connection

 Plugin for Nagios fully conects to a windows host using TS (RDP) and verifies if the windows screen loads and after that disconect returning an OK/CRITICAL state
 
This project is a python 3 script, aided with a shell script that allows Nagios open a graphcal TS session from an Linux server with a GUI installed.

## Installing / Getting started

What do you need to run ts_check
* Linux server with GUI installed
* Python 3
* xfreerdp package


```shell
python 3
pip install requests
$ python3 nagios_api.py
```

This will run the app opening the GUI for use.

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

![Screenshot 1](https://github.com/FernandoRD/NagiosXI_api/blob/main/Screen1.png)

![Screenshot 2](https://github.com/FernandoRD/NagiosXI_api/blob/main/Screen2.png)

![Screenshot 3](https://github.com/FernandoRD/NagiosXI_api/blob/main/Screen3.png)

## Licensing

"The code in this project is licensed under MIT license."

