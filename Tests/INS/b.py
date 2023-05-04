import random

objects = [
    "Train",
    "Bus",
    "Bike",
    "Bottle",
]

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

mod = [
    #Query             Answer
    [[("hi", "hello"), ], ["hello","hi"]],
    
    #how are you
    #are you ok
    [[("how", "are"), ("you",), ], ["i am fine"]],
    
    
    #what is in the front of me
    #who is their
    #What is this
    [[("what", "who"), ("their", "this", "front")], [f"Their is {make(objects, 's')}.", f"I see {make(objects, 's')}.", make(objects, 's')]],
    
    
    #please tell everything/anything visible
    #name all the objects
    #name all the things
    [[("tell", "name"), ("all", "everything", "anything", "things", "objects"), ], [make(objects, 'm')]],
    
    #Last query
    [[], ["Sorry! I don't understand.", "Please repeat!", "I am not an human."]],
]

while True:
    p = input("In:")
    for qs in mod:
        check_p = qs[0]
        targate = len(check_p)
        score = 0
        for i in check_p:
            for j in i:
                #print(j, p.split(" "))
                if j in p.split(" "):
                    score += 1
                    break
        
        if score == targate:
            to_say = random.choice(qs[1])
            print(to_say)
            break