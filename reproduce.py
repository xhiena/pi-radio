from time import sleep
from pathlib import Path  # for directory listing
import pygame


DIRECTORY = Path('/home/pi/Music/Amaral - Estrella de mar')
pygame.mixer.init()

for fp in DIRECTORY.glob('*.mp3'):
    # add each file to the queue
    pygame.mixer.music.load(str(fp))
    pygame.mixer.music.play()

    #now wait until the song is over
    while pygame.mixer.music.get_busy():
        sleep(1)  # wait 1 second
