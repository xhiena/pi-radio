import RPi.GPIO as GPIO
from pn532 import *

from time import sleep
from pathlib import Path  # for directory listing
import pygame


def findFolder(index):
    folder=""
    with open('/home/pi/Music/mapping.txt', "r") as f:
        line = f.readline()
        while line != '':
            x = line.split("|||")
            if (x[0]==index):
                folder=x[1]
                break
            line = f.readline()

    return folder

def getUIDfromCard():
    while True:
    # Check if a card is available to read
        uid = pn532.read_passive_target(timeout=0.5)
        print('.', end="")
        # Try again if no card is available.
        if uid is None:
            continue
        print('Found card with UID:', [hex(i) for i in uid])
        return uid


pygame.mixer.init()
running=False
pn532 = None
attempt = 0
while not running:
    try:
        attempt+=1
        print(attempt)
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
print('Waiting for RFID/NFC card...')

uid=getUIDfromCard()
print(uid)
directory=findFolder(uid)

DIRECTORY = Path('/home/pi/Music/Amaral - Estrella de mar')
for fp in DIRECTORY.glob('*.mp3'):
    # add each file to the queue
    pygame.mixer.music.load(str(fp))
    pygame.mixer.music.play()

    #now wait until the song is over
    while pygame.mixer.music.get_busy():
        sleep(1)  # wait 1 second
