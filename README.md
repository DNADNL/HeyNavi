# HeyNavi

Source to configure Raspberry Pi :
- USB Sound (Raspbian Stretch) : https://learn.adafruit.com/usb-audio-cards-with-a-raspberry-pi/updating-alsa-config

Power for RPi : 5V 3A

Please modify the /etc/rc.local to boot on navi.py (assuming you cloned it on your RPi desktop)
- python /home/pi/Desktop/HeyNavi/Navi.py > /home/pi/Desktop/HeyNavi/Navi.log 2>&1 & 

Thanks to Thomas Cyrix, elegoo tutorials and the whole Raspberry Pi community
