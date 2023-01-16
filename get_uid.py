import RPi.GPIO as GPIO
from pn532 import *

if __name__ == '__main__':
    try:
        #pn532 = PN532_SPI(debug=False, reset=20, cs=4)
        #pn532 = PN532_I2C(debug=False, reset=20, req=16)
        pn532 = PN532_UART(debug=False, reset=20)
        found = False
        while not found:
            try:
                ic, ver, rev, support = pn532.get_firmware_version()
                found=True
                print('Found PN532 with firmware version: {0}.{1}'.format(ver, rev))
            except Exception as e:
                print(e)
                continue
        # Configure PN532 to communicate with MiFare cards
        pn532.SAM_configuration()

        print('Waiting for RFID/NFC card...')
        while True:
            # Check if a card is available to read
            uid = pn532.read_passive_target(timeout=0.5)
            print('.', end="")
            # Try again if no card is available.
            if uid is None:
                continue
            print('Found card with UID:', [hex(i) for i in uid])
            uid2=""
            for i in uid:
                uid2+=hex(i)+'-'
            print("uid to map: -"+uid2)
            break
    except Exception as e:
        print(e)

    finally:
        GPIO.cleanup()
