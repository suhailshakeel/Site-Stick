import time
import adafruit_fingerprint
import serial
import pyttsx3

engine = pyttsx3.init()

uart = serial.Serial("COM5", baudrate=57600, timeout=1)

finger = adafruit_fingerprint.Adafruit_Fingerprint(uart)

def enroll_finger(location):
    for fingerimg in range(1, 3):
        if fingerimg == 1:
            print("Place finger on sensor...")
            engine.say("Place finger on sensor...")
            engine.runAndWait()
        else:
            print("Place same finger again...", end="")
            engine.say("Place same finger again...")
            engine.runAndWait()
        
        while True:
            i = finger.get_image()
            if i == adafruit_fingerprint.OK:
                print("Image taken")
                break
            if i == adafruit_fingerprint.NOFINGER:
                print(".", end="")
            elif i == adafruit_fingerprint.IMAGEFAIL:
                print("Imaging error")
                return False
            else:
                print("Other error")
                return False

        print("Templating...", end="")
        i = finger.image_2_tz(fingerimg)
        if i == adafruit_fingerprint.OK:
            print("Templated")
        else:
            if i == adafruit_fingerprint.IMAGEMESS:
                print("Image too messy")
            elif i == adafruit_fingerprint.FEATUREFAIL:
                print("Could not identify features")
            elif i == adafruit_fingerprint.INVALIDIMAGE:
                print("Image invalid")
            else:
                print("Other error")
            return False

    print("Creating model...", end="")
    i = finger.create_model()
    if i == adafruit_fingerprint.OK:
        print("Created")
    else:
        if i == adafruit_fingerprint.ENROLLMISMATCH:
            print("Prints did not match")
        else:
            print("Other error")
        return False

    print("Storing model #%d..." % location, end="")
    i = finger.store_model(location)
    if i == adafruit_fingerprint.OK:
        print("Stored")
    else:
        if i == adafruit_fingerprint.BADLOCATION:
            print("Bad storage location")
        elif i == adafruit_fingerprint.FLASHERR:
            print("Flash storage error")
        else:
            print("Other error")
        return False

    return True

if __name__ == "__main__":
    while True:
        if enroll_finger(0) == True:
            engine.say("Fingerprint Successfully Taken!")
            engine.runAndWait()
            break
        else:
            engine.say("Some error occured! Please try again later!")
            engine.runAndWait()