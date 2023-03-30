import pyttsx3, random
engine = pyttsx3.init()

def speak(obj):
    l = [
        f"There is a {obj} in front of you.", 
        f"You have a {obj} in front of you.",
        f"There's a {obj} directly in front of you.",
        f"There's a {obj} in your path.",
         ]
    
    engine.say(random.choice(l))