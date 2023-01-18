#! /usr/bin/env python

import RPi.GPIO as GPIO
from pn532 import *

from time import sleep
from pathlib import Path  # for directory listing
import pygame
import multiprocessing

BASEDIRECTORY='/home/pi/Music/' #where music and mapping is
VOLUME=0.4

def findFolder(index):
    folder=""
    with open(BASEDIRECTORY+'mapping.txt', "r") as f:
        line = f.readline()
        while line != '':
            x = line.split("|||")
            if (x[0]==index):
                folder=x[1].strip()
                break
            line = f.readline()

    return folder

def playfolder(folder):
    musicfolder = Path(BASEDIRECTORY+folder)
    pygame.mixer.init()
    if musicfolder.exists():
        print('folder exists')
        for fp in sorted(musicfolder.glob('*.mp3')):
            pygame.mixer.music.set_volume(VOLUME)
            pygame.mixer.music.load(str(fp))
            print ("playing: "+str(fp))
            pygame.mixer.music.play()
            #now wait until the song is over
            while pygame.mixer.music.get_busy():
                sleep(1)  # wait 1 second
    else:
        print("folder does not exist")

def getUIDfromCard():
    print('Waiting for RFID/NFC card...')
    while True:
        # Check if a card is available to read
        uid2=''
        uid = pn532.read_passive_target(timeout=0.5)
        print('.', end="")
        # Try again if no card is available.
        if uid is None:
            continue
        print('Found card with UID:', [hex(i) for i in uid])
        for i in uid:
            uid2+=hex(i)+'-'

        return "-"+uid2



running=False
pn532 = None
attempt = 0
while not running:
    try:
        attempt+=1
        pn532 = PN532_UART(debug=False, reset=20)
        if pn532 != None:
            running = True

    except Exception as e:
        print(e)
        GPIO.cleanup()
        continue

    finally:
        GPIO.cleanup()

ic, ver, rev, support = pn532.get_firmware_version()
print('Found PN532 with firmware version: {0}.{1}'.format(ver, rev))
pn532.SAM_configuration()
nowplaying=""
proc=None
while True:
    uid=getUIDfromCard()
    print("card uid: "+uid)
    directory=findFolder(uid)
    print("folder of the card: "+directory)
    if(uid!=nowplaying):
        print("this folder is not being played, switching to this folder")
        nowplaying=uid
        if(proc != None):
            proc.terminate()
            print("something is playing, stoping")
        proc = multiprocessing.Process(target=playfolder, args=(directory,))
        proc.start()
    else:
        print(uid+" is playing! No need to change music")

    sleep(2)
