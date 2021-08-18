# base image 
FROM docker.corp.jabil.org/raspberry-pi/xwindow

# install dependences
RUN apt-get update && apt-get install -y python3-dev \
	python3-requests \
	python3-pip \
	python3-pyqt5  
    
# copy script files
COPY /. /sd/

WORKDIR /sd

# run flash commands
RUN apt-get install -y pv curl unzip hdparm \
    curl -LO https://github.com/hypriot/flash/releases/download/2.7.2/flash \
    chmod +x flash \
    mv flash /usr/local/bin/flash 

RUN chmod +x /sd/startup.sh
ENV START_UP="/sd/startup.sh"