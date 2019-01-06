#!/usr/bin/env /usr/bin/python

# Import du GPIO pour acces au detecteur de mouvements
import RPi.GPIO as GPIO

# Import de la biblio de temps pour integrer des pauses dans le code
import time
from datetime import datetime

# Import de la biblio de son
import pygame.mixer

# Import de la biblio pour tirage au sort de la ligne dans le fichier
import linecache

# Import de la biblio pour tirage aleatoire
import random

import signal
import sys

def sigterm_handler(signal, frame):
    print("Exiting Navi.py")
    GPIO.cleanup()
    sys.exit(0)
    
signal.signal(signal.SIGTERM, sigterm_handler)

# On precise ou est branche le capteur de mouvements
GPIO.setmode(GPIO.BCM)

capteur = 7
led_pwm = 18

GPIO.setup(led_pwm, GPIO.OUT)  # Set GPIO pin 12 to output mode.

print(str(datetime.now()))
print("Demarrage LED PWM")
pwm = GPIO.PWM(led_pwm, 100)   # Initialize PWM on pwmPin 100Hz frequency
dc=50                                   # set dc variable to 0 (will start PWM at 0% duty cycle)
time.sleep(2)
print("LED PWM prete")

# On active la detection GPIO
GPIO.setup(capteur, GPIO.IN)
print("Demarrage du capteur")
time.sleep(2)
print("Capteur pret a detecter un mouvement")

# Compteur pour voir combien de fois un passage a ete detecte
cpt = 0

# Fonction pour calculer le nombre de lignes dans un fichier
def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

# Fonction pour recuperer une ligne au hasard d'un fichier playlist
def get_random_line(soundlist):
    return random.randrange(1,file_len(soundlist)+1)

# Fonction pour charger un son au hasard a partir d'un fichier playlist
def get_random_sound(soundlist):
    return linecache.getline(soundlist,get_random_line(soundlist)).rstrip('\n')

print("Number of audio files : " + str(file_len("/home/pi/Desktop/HeyNavi/list.txt")));

while True:
    if GPIO.input(capteur):
        cpt=cpt+1
        pygame.init()
        pygame.mixer.init()
        chosen_sound = str(get_random_sound("/home/pi/Desktop/HeyNavi/list.txt"))
        print("Chosen : " + chosen_sound)
        #print(str(linecache.getline("/home/pi/Desktop/list.txt", random.randrange(0,1+file_len("/home/pi/Desktop/list.txt")))))
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.load(chosen_sound)
        #pygame.mixer.music.load(linecache.getline("/home/pi/Desktop/list.txt", random.randrange(0,file_len("/home/pi/Desktop/list.txt")) )) #"/home/pi/Downloads/Listen.ogg"
        pygame.mixer.music.play()
        pwm.start(dc)                          # Start PWM with 0% duty cycle
        while(pygame.mixer.music.get_busy()): 
            for dc in range(0, 101, 5):          # Loop with dc set from 0 to 100 stepping dc up by 5 each loop
                pwm.ChangeDutyCycle(dc)
                time.sleep(0.01)                   # wait for .05 seconds at current LED brightness level
                print(dc)
            for dc in range(95, 0, -5):          # Loop with dc set from 95 to 5 stepping dc down by 5 each loop
                pwm.ChangeDutyCycle(dc)
                time.sleep(0.01)                   # wait for .05 seconds at current LED brightness level
                print(dc)
        for dc in range(0, 101, 5):          # Loop with dc set from 0 to 100 stepping dc up by 5 each loop
            pwm.ChangeDutyCycle(dc)
            time.sleep(0.01)                   # wait for .05 seconds at current LED brightness level
            print(dc)
            print()
        for dc in range(95, 0, -5):          # Loop with dc set from 95 to 5 stepping dc down by 5 each loop
            pwm.ChangeDutyCycle(dc)
            time.sleep(0.01)                   # wait for .05 seconds at current LED brightness level
            print(dc)
            print(pygame.mixer.music.get_busy())
        pwm.stop()
        print(str(datetime.now()))
        print("Mouvement detecte : " + str(cpt))
        time.sleep(3)
    time.sleep(1)