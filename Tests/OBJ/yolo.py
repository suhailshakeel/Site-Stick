import cv2
import numpy as np
from collections import deque

# Load YOLOv4-Tiny model
net = cv2.dnn.readNet('D:/BCA/S6/CAP463- PROJECT/Tests/OBJ/yolov4-tiny.weights', 'D:/BCA/S6/CAP463- PROJECT/Tests/OBJ/yolov4-tiny.cfg')

# Load class names
classes = ["person"
,"bicycle"
,"car"
,"motorbike"
,"aeroplane"
,"bus"
,"train"
,"truck"
,"boat"
,"traffic light"
,"fire hydrant"
,"stop sign"
,"parking meter"
,"bench"
,"bird"
,"cat"
,"dog"
,"horse"
,"sheep"
,"cow"
,"elephant"
,"bear"
,"zebra"
,"giraffe"
,"backpack"
,"umbrella"
,"handbag"
,"tie"
,"suitcase"
,"frisbee"
,"skis"
,"snowboard"
,"sports ball"
,"kite"
,"baseball bat"
,"baseball glove"
,"skateboard"
,"surfboard"
,"tennis racket"
,"bottle"
,"wine glass"
,"cup"
,"fork"
,"knife"
,"spoon"
,"bowl"
,"banana"
,"apple"
,"sandwich"
,"orange"
,"broccoli"
,"carrot"
,"hot dog"
,"pizza"
,"donut"
,"cake"
,"chair"
,"sofa"
,"pottedplant"
,"bed"
,"diningtable"
,"toilet"
,"tvmonitor"
,"laptop"
,"mouse"
,"remote"
,"keyboard"
,"cell phone"
,"microwave"
,"oven"
,"toaster"
,"sink"
,"refrigerator"
,"book"
,"clock"
,"vase"
,"scissors"
,"teddy bear"
,"hair drier"
,"toothbrush"
]

# Set up the queue to store object information
max_queue_length = 50
object_queue = deque(maxlen=max_queue_length)

#with open('C:/Users/salro/Desktop/Final Project/coco_labels.names', 'r') as f:
#    classes = [line.strip() for line in f.readlines()]
# Get layer names
layer_names = net.getLayerNames()
output_layer_indices = net.getUnconnectedOutLayers()
# Check if output layers are empty
output_layers = [layer_names[int(i) - 1] for i in output_layer_indices]

if not output_layers:
    print("Error: No output layers found. Check YOLO model configuration.")
    exit()
#output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
# Set up webcam
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Loop through webcam frames
while True:
    ret, frame = cap.read()

    # Create blob from input frame
    blob = cv2.dnn.blobFromImage(frame, 1/255, (416, 416), swapRB=True, crop=False)
    #print(blob)

    # Set input to the YOLOv4-Tiny network
    net.setInput(blob)

    # Forward pass through network
    layer_names = net.getLayerNames()
    output_layers = [layer_names[int(i) - 1] for i in net.getUnconnectedOutLayers()]
    #print(output_layers)
    outs = net.forward(output_layers)

    # Process detection results
    class_ids = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                # Object detected
                center_x = int(detection[0] * frame.shape[1])
                center_y = int(detection[1] * frame.shape[0])
                width = int(detection[2] * frame.shape[1])
                height = int(detection[3] * frame.shape[0])
                left = int(center_x - width / 2)
                top = int(center_y - height / 2)
                class_ids.append(class_id)
                confidences.append(float(confidence))
                boxes.append([left, top, width, height])

    # Non-maximum suppression
    indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

    # Draw bounding boxes and class labels
    font = cv2.FONT_HERSHEY_PLAIN
    colors = np.random.uniform(0, 255, size=(len(classes), 3))
    if len(indices) > 0:
        for i in indices.flatten():
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            color = colors[class_ids[i]]
            #calculate area
            area = w * h
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            cv2.putText(frame, label, (x, y - 5), font, 1, color, 1)
            obj_dict = {'name': label, 'area': area}

            object_queue.append(obj_dict)
            print(object_queue)

    # Display output
    cv2.imshow('Object Detection', frame)
    if cv2.waitKey(1) == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
