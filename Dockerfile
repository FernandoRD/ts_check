FROM ubuntu:22.04
RUN DEBIAN_FRONTEND=noninteractive
RUN ln -fs /usr/share/zoneinfo/America/Sao_Paulo /etc/localtime
RUN apt-get update -y
RUN apt-get install -y --no-install-recommends giflib-tools libimlib2 xvfb x11vnc x11-utils xauth freerdp2-x11 giblib1 scrot python3-venv python3-tk python3-dev python3-pip python3-opencv python3-xlib python3-pillow python3-pyvirtualdisplay
RUN pip install --upgrade pip
RUN python3 -m pip install pyautogui keyboard 
RUN /usr/bin/sed -i "s/'scrot', '-z', tmpFilename/'scrot', tmpFilename/g" ./usr/local/lib/python3.10/dist-packages/pyscreeze/__init__.py
RUN mkdir /images
RUN mkdir /exec
WORKDIR /app
COPY ts_check.py .
EXPOSE 5900
ENV DISPLAY :0
ENTRYPOINT [ "/usr/bin/python3", "ts_check.py" ]
