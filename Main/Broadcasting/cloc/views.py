from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
import json
from django.http import HttpResponse
#import os
import base64


# Create your views here.
def index(request):
    f = open("./cloc/data.json", "r")
    data = json.loads(f.read())
    f.close()
    return render(request, "cloc/index.html", data)

@ensure_csrf_cookie
def settings(request):
    if request.method == "GET":
        return render(request, "cloc/settings.html")
    elif request.method == "POST":
        body = json.loads(request.body.decode('utf-8'))
        
        if (body["id"] == "Fingerprint_REC"):
            if (body['is_done'] == 0):
                if check_rec_status() == 0:
                    rec_fp()

                elif check_rec_status() == 1:
                    body["is_done"] = 1
                    
                elif check_rec_status() == 2:
                    body["is_done"] = 0
                
                elif check_rec_status() == 3:
                    body["time_out"] = 1
        
        if (body["id"] == "image_data"):
            #print(os.listdir())
            d = open("./cloc/static/test_img.jpg", "wb")
            d.write(base64.b64decode(body["image"].split(',')[1]))
            d.close()
            body["image"] = "ok"
        
        if (body["id"] == "save_user_data"):
            #Reading and checking password and password hint
            f = open("./cloc/data.json", "r")
            data = json.loads(f.read())
            f.close()
            
            #updating data
            if (body["password"] ==  data["password"]) or (body["phint"] ==  data["phint"]):
                d = open("./cloc/data.json", "w")
                d.write(json.dumps(body))
                d.close()
                body.clear()
                body["done"] = 1
            else:
                body.clear()
                body["done"] = 0
                body["msg"] = "Wrong Password or Hint!"
            
        to_send = json.dumps(body)
        #print("Respose:", to_send)                                       
        return HttpResponse(to_send, content_type="application/json")

def check_rec_status():
    #0- start, 1- done, 2- in-progress, 3- time-out
    return 1

def rec_fp():
    return 2
