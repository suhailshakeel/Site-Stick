import time
import adafruit_fingerprint
import serial


uart = serial.Serial("COM5", baudrate=57600, timeout=1)

finger = adafruit_fingerprint.Adafruit_Fingerprint(uart)

"""
0-3
4-6
7-00
"""

count = 0

single = "Off"
double = "Off"
long = "Off"

def single_tap(option):
    print("Single Tap: ", option)

def double_tap(option):
    print("Double Tap: ", option)

def long_touch(option):
    print("Long Tap: ", option)

while True:
    finger.get_image()
    if finger.get_image() == adafruit_fingerprint.OK:
        count += 1
        
        tx = time.time()
        
        while (time.time() - tx) < 3:
            if finger.get_image() == adafruit_fingerprint.OK:
                count += 1
        print(count)
        
        #single tap
        if (count <= 10):
            if double == "On":
                double = "Off"
                double_tap("Off")
                count = 0
                continue
            
            if single == "Off":
                single = "On"
                single_tap("On")
            else:
                single = "Off"
                single_tap("Off")
            
            count = 0
            
            continue
            
        if (count>10) and (count<25):
            if single == "On":
                single = "Off"
                single_tap("Off")
                count = 0
                continue
            
            if double == "Off":
                double = "On"
                double_tap("On")
            else:
                double = "Off"
                double_tap("Off")
            
            count = 0
            
            continue
            
        if (count >= 25):
            
            if single == "On":
                single = "Off"
                single_tap("Off")
                count = 0
                continue
            
            if double == "On":
                double = "Off"
                double_tap("Off")
                count = 0
                continue
            
            long = 1
            long_touch("On")
            
            while finger.get_image() == adafruit_fingerprint.OK:
                pass
            else:
                long = 0
                long_touch("Off")
                
            count = 0
    