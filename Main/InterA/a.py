from vosk import Model, KaldiRecognizer
import pyaudio
import threading
import time
import random
import pyttsx3

engine = pyttsx3.init()

"""
Note:
Data must satisfy a query.
If no query must be satisfied last one will be exicuted as default. 
If you add multiple answers, any one randomly will be picked.
"""

objects = [
    "Train",
    "Bus",
    "Bike",
    "Bottle",
]

model = Model("./vosk-model-small-en-in-0.4")
recog = KaldiRecognizer(model, 16000)

mic = pyaudio.PyAudio()
stream = mic.open(rate=16000, channels=1, format=pyaudio.paInt16, input=True, frames_per_buffer=8192)                                                                                
stream.start_stream()

def make(objects, flag):
    if len(objects) == 0:
        return "nothing"
    
    #Returning a single object
    if flag == "s":
        return objects[0]
    
    #Returning all the objects
    elif flag == "m":
        if len(objects) == 1:
            return objects[0]
        else:
            stat = ""
            for i in range(len(objects)-1):
                    stat = stat + objects[i] + ", "
                    
            return stat + "and " + objects[-1]
    else:
        raise "Invalid Flag!"

def getDate(p):
    if p == 'd':
        return "12"
    elif p == 'm':
        return "May"
    elif p == 'y':
        return "2023"

def getTime():
    return ""

mod = [
    #Format:    Query             Answer
    [[("hi", "hello"), ], ["hello","hi"]],
    
    #how are you
    #are you ok
    [[("how", "are"), ("you",), ], ["i am fine"]],
    
    #what is in the front of me
    #who is their
    #What is this
    #Is there any object
    #Is there any obstacle 
    [[("what", "who", "is"), ("their", "this", "front", "object", "obstacle")], [f"Their is {make(objects, 's')}.", f"I see {make(objects, 's')}.", make(objects, 's')]],
    
    #please tell everything/anything visible
    #name all the objects
    #name all the things
    #Are you able to see any objects
    [[("tell", "name", "see"), ("all", "everything", "anything", "things", "objects"), ], [f"I see {make(objects, 'm')}." ,make(objects, 'm')]],
    
    #What's today's date?
    #Could you tell me today's date, please?
    #Do you know what the date is today?
    #Date?
    [[("today", "date", "tell"), ("date",)], ["Today is "+getDate('m')+" "+getDate('d')+", "+getDate('y')+".", "Today is the "+getDate('d')+" of "+getDate('m')+", "+getDate('y')+"."]],
    
    #What time is it?
    #Could you tell me the time, please?
    #Please tell current time.
    #time now
    #Time?
    [[("tell", "time", "current"), ("time",)], ["It's "+getTime()+" hours.", ]],
    
    #Last query
    [[], ["Sorry! I don't understand.", "Please repeat!", "I am not an human.", "I am a bot."]],
]

cd = 1
def mps():
    while cd:
        data = stream.read(4096)
        if recog.AcceptWaveform(data):
            data = recog.Result()[14:-3]
            if data == "":
                continue
            print("In:", data)
            for qs in mod:
                check_p = qs[0]
                targate = len(check_p)
                score = 0
                for i in check_p:
                    for j in i:
                        #print(j, p.split(" "))
                        if j in data.split(" "):
                            score += 1
                            break
                
                if score == targate:
                    to_say = random.choice(qs[1])
                    print("Out:", to_say)
                    engine.say(to_say)
                    engine.runAndWait()
                    break

def start():
    threading.Thread(target=mps,).start()
    global cd
    cd = 1

def stop():
    global cd
    cd = 0

if __name__ == "__main__":
    print("Program Started!")
    start()
    time.sleep(25)
    stop()
    print("Program Ended!")
    
    time.sleep(5)
    
    print("Program Started!")
    start()
    time.sleep(25)
    stop()
    print("Program Ended!")