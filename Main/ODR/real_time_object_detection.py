from imutils.video import VideoStream
import numpy as np
import imutils
import time
import cv2
import threading

data = []
key = 1

CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
	"dog", "horse", "motorbike", "person", "pottedplant", "sheep", "sofa", "train", "tvmonitor"]

def dandr():
	net = cv2.dnn.readNetFromCaffe("D:\\BCA\\S6\\CAP463- PROJECT\\Main\\ODR\\MobileNetSSD_deploy.prototxt.txt", "D:\\BCA\\S6\\CAP463- PROJECT\\Main\\ODR\\MobileNetSSD_deploy.caffemodel")
	vs = VideoStream(src = 0).start()
	time.sleep(2.0)

	while True:
		frame = vs.read()
		frame = imutils.resize(frame, width = 500)

		(h, w) = frame.shape[:2]
		blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5)

		net.setInput(blob)
		detections = net.forward()

		for i in np.arange(0, detections.shape[2]):
			probability = detections[0, 0, i, 2]

			if probability > 0.2:
				idx = int(detections[0, 0, i, 1])
				box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
				(startX, startY, endX, endY) = box.astype("int")
	
				item = CLASSES[idx]

				#area of item
				area = (endY - startY) * (endX - startX)

				#queue size is 50
				if len(data) > 50:
					data.pop(0)
				data.append([item, area])
		global key
		if key == 0:
			vs.stop()
			return

		time.sleep(0.1)#10 fps

t = threading.Thread(target=dandr,)
def start():
    global key, t
    key = 1
    t = threading.Thread(target=dandr,)
    t.start()

def stop():
    global key
    key = 0

def fs_unique(data, items):
    #Finding Unique Items
    lst = []
    high = -1
    for i in items:
        for j in data:
            if (i == j[0]) and (high < j[1]):
                high = j[1]
        
        for j in data:
            if j[1] == high:
                lst.append(j)
                break
        high = 0
    
    #Sorting Unique Items
    for i in range(len(lst)):
        for j in range(0, len(lst) - i - 1):
            if lst[j][1] < lst[j + 1][1]:
                temp = lst[j]
                lst[j] = lst[j+1]
                lst[j+1] = temp
        
    return lst

if __name__ == "__main__":
	start()
	time.sleep(10)
	print(fs_unique(data, CLASSES))
	stop()
 
	time.sleep(5)
 
	start()
	time.sleep(10)
	print(fs_unique(data, CLASSES))
	stop()