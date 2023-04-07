import cv2
import numpy as np
import tensorflow as tf

# Load the pre-trained model
model = tf.saved_model.load('C:/Users/salro/Desktop/LAST SEMESTER BCA/site stick/code/models/research/object_detection/test_data/efficientdet_d5_coco17_tpu-32/saved_model')

# Initialize the voice assistant
#engine = pyttsx3.init()
object_data = {}
# Define the categories of objects that the model can detect
category_index = { 
   1 : {'id':1 ,'name' : 'person'},
   2 : {'id':2 ,'name' : 'bicycle'},
   3 : {'id':3 ,'name' : 'car'},
   4 : {'id':4 ,'name' : 'motorbike'},
   5 : {'id':5 ,'name' : 'aeroplane'},
   6 : {'id':6 ,'name' : 'bus'},
   7 : {'id':7 ,'name' : 'train'},
   8 : {'id':8 ,'name' : 'truck'},
   9 : {'id':9 ,'name' : 'boat'},
   10 : {'id':10 ,'name' : 'traffic light'},
   11 : {'id':11 ,'name' : 'fire hydrant'},
   12 : {'id':12 ,'name' : 'stop sign'},
   13 : {'id':13 ,'name' : 'parking meter'},
   14 : {'id':14 ,'name' : 'bench'},
   15 : {'id':15 ,'name' : 'bird'},
   16 : {'id':16 ,'name' : 'cat'},
   17 : {'id':17 ,'name' : 'dog'},
   18 : {'id':18 ,'name' : 'horse'},
   19 : {'id':19 ,'name' : 'sheep'},
   20 : {'id':20 ,'name' : 'cow'},
   21 : {'id':21 ,'name' : 'elephant'},
   22 : {'id':22 ,'name' : 'bear'},
   23 : {'id':23 ,'name' : 'zebra'},
   24 : {'id':24 ,'name' : 'giraffe'},
   25 : {'id':25 ,'name' : 'backpack'},
   26 : {'id':26 ,'name' : 'umbrella'},
   27 : {'id':27 ,'name' : 'handbag'},
   28 : {'id':28 ,'name' : 'tie'},
   29 : {'id':29 ,'name' : 'suitcase'},
   30 : {'id':30 ,'name' : 'frisbee'},
   31 : {'id':31 ,'name' : 'skis'},
   32 : {'id':32 ,'name' : 'snowboard'},
   33 : {'id':33 ,'name' : 'sports ball'},
   34 : {'id':34 ,'name' : 'kite'},
   35 : {'id':35 ,'name' : 'baseball bat'},
   36 : {'id':36 ,'name' : 'baseball glove'},
   37 : {'id':37 ,'name' : 'skateboard'},
   38 : {'id':38 ,'name' : 'surfboard'},
   39 : {'id':39 ,'name' : 'tennis racket'},
   40 : {'id':40 ,'name' : 'bottle'},
   41 : {'id':41 ,'name' : 'wine glass'},
   42 : {'id':42 ,'name' : 'cup'},
   43 : {'id':43 ,'name' : 'fork'},
   44 : {'id':44 ,'name' : 'knife'},
   45 : {'id':45 ,'name' : 'spoon'},
   46 : {'id':46 ,'name' : 'bowl'},
   47 : {'id':47 ,'name' : 'banana'},
   48 : {'id':48 ,'name' : 'apple'},
   49 : {'id':49 ,'name' : 'sandwich'},
   50 : {'id':50 ,'name' : 'orange'},
   51 : {'id':51 ,'name' : 'broccoli'},
   52 : {'id':52 ,'name' : 'carrot'},
   53 : {'id':53 ,'name' : 'hot dog'},
   54 : {'id':54 ,'name' : 'pizza'},
   55 : {'id':55 ,'name' : 'donut'},
   56 : {'id':56 ,'name' : 'cake'},
   57 : {'id':57 ,'name' : 'chair'},
   58 : {'id':58 ,'name' : 'sofa'},
   59 : {'id':59 ,'name' : 'pottedplant'},
   60 : {'id':60 ,'name' : 'bed'},
   61 : {'id':61 ,'name' : 'diningtable'},
   62 : {'id':62 ,'name' : 'toilet'},
   63 : {'id':63 ,'name' : 'tvmonitor'},
   64 : {'id':64 ,'name' : 'laptop'},
   65 : {'id':65 ,'name' : 'mouse'},
   66 : {'id':66 ,'name' : 'remote'},
   67 : {'id':67 ,'name' : 'keyboard'},
   68 : {'id':68 ,'name' : 'crll phone'},
   69 : {'id':69 ,'name' : 'microwave'},
   70 : {'id':70 ,'name' : 'toaster'},
   71 : {'id':71 ,'name' : 'sink'},
   72 : {'id':72 ,'name' : 'refrigerator'},
   73 : {'id':73 ,'name' : 'book'},
   74 : {'id':74 ,'name' : 'clock'},
   75 : {'id':75 ,'name' : 'vase'},
   76 : {'id':76 ,'name' : 'scissors'},
   77 : {'id':77 ,'name' : 'teddy bear'},
   78 : {'id':78 ,'name' : 'hair drier'},
   79 : {'id':79 ,'name' : 'toothbrush'},
}
# Initialize the webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    
    frame = tf.image.convert_image_dtype(frame, tf.uint8)
    input_tensor = tf.convert_to_tensor(np.expand_dims(frame, 0), dtype=tf.uint8)
    detections = model(input_tensor)

    # Extract the required information from the detections
    num_detections = int(detections.pop('num_detections'))
    detections = {key: value[0, :num_detections].numpy() for key, value in detections.items()}
    detections['num_detections'] = num_detections

   # Filter out the detections with low confidence scores
    detections['detection_scores'] = detections['detection_scores'][detections['detection_scores'] > 0.5]

   # Extract the boxes and scores of the remaining detections
    boxes = detections['detection_boxes'][:len(detections['detection_scores'])]
    scores = detections['detection_scores']
    classes = detections['detection_classes'][:len(detections['detection_scores'])]

   # Draw the bounding boxes and labels of the detected objects on the frame
   # image_np_with_detections = frame.copy()
    image_np_with_detections = np.copy(frame.numpy())
    for box, score, class_id in zip(boxes, scores, classes):
         ymin, xmin, ymax, xmax = box
         im_height, im_width, _ = image_np_with_detections.shape
         left, right, top, bottom = int(xmin * im_width), int(xmax * im_width), int(ymin * im_height), int(ymax * im_height)
         width, height = right - left, bottom - top
         area = width * height

         class_id = int(class_id)
         object_name = category_index[class_id]['name']
         # Add the object name and area to the dictionary
         object_data[object_name] = area
         cv2.rectangle(image_np_with_detections, (left, top), (right, bottom), (0, 255, 0), thickness=2)
         cv2.putText(image_np_with_detections, category_index[class_id]['name'], (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), thickness=1)

        # Display the resulting image with detected objects
         cv2.imshow('Object Detection', image_np_with_detections)
         # Initialize an empty array to store the areas

         print(object_data)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

print(areas)



   
