import cv2

# Load the pre-trained model
net = cv2.dnn.readNetFromDarknet('yolov3.cfg', 'yolov3.weights')
classes = []
with open('coco.names', 'r') as f:
    classes = [line.strip() for line in f.readlines()]
    
# Initialize the camera
cap = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Perform object detection
    blob = cv2.dnn.blobFromImage(frame, 1/255.0, (416,416), swapRB=True, crop=False)
    net.setInput(blob)
    outputs = net.forward(net.getUnconnectedOutLayersNames())
    
    # Find the most significant object
    confidences = []
    for output in outputs:
        for detection in output:
            confidence = detection[4]
            if confidence > 0.5:
                class_id = detection[1]
                confidences.append((class_id, confidence))
    if len(confidences) > 0:
        class_id, confidence = max(confidences, key=lambda x: x[1])
        label = f'{classes[class_id]}: {confidence:.2f}'
        cv2.putText(frame, label, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

    # Display the resulting frame
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture
cap.release()
cv2.destroyAllWindows()
