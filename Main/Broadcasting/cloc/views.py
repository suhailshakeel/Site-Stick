from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
import json
from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request, "cloc/index.html")

@ensure_csrf_cookie
def settings(request):
    if request.method == "GET":
        return render(request, "cloc/settings.html")
    elif request.method == "POST":
        body = json.loads(request.body.decode('utf-8'))
        
        if (body['is_done'] == 0):
            if check_rec_status() == 0:
                rec_fp()

            elif check_rec_status() == 1:
                body["is_done"] = 1
                
            elif check_rec_status() == 2:
                body["is_done"] = 0
            
            elif check_rec_status() == 3:
                body["time_out"] = 1
        
        to_send = json.dumps(body)
        #print("Respose:", to_send)                                       
        return HttpResponse(to_send, content_type="application/json")

def check_rec_status():
    #0- start, 1- done, 2- in-progress, 3- time-out
    return 1

def rec_fp():
    return 2
