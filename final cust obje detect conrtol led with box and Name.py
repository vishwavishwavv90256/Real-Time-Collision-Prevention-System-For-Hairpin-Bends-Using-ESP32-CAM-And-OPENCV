import cv2
import urllib.request
import numpy as np
import serial

url = 'http://192.168.204.37/cam-hi.jpg'
winName = 'ESP32 CAMERA'
cv2.namedWindow(winName, cv2.WINDOW_AUTOSIZE)

classNames = []
classFile = 'coco.names'
with open(classFile, 'rt') as f:
    classNames = f.read().rstrip('\n').split('\n')

valid_classes = ['person']

configPath = 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
weightsPath = 'frozen_inference_graph.pb'

net = cv2.dnn_DetectionModel(weightsPath, configPath)
net.setInputSize(256, 256)
net.setInputScale(1.0 / 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)

ser = serial.Serial('COM6', 9600)  # Change 'COM1' to your Arduino's COM port

while True:
    imgResponse = urllib.request.urlopen(url)
    imgNp = np.array(bytearray(imgResponse.read()), dtype=np.uint8)
    img = cv2.imdecode(imgNp, -1)

    img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)

    classIds, confs, bbox = net.detect(img, confThreshold=0.5)
    

    valid_object_detected = False
    if isinstance(classIds, np.ndarray):
        for classId, confidence, box in zip(classIds.flatten(), confs.flatten(), bbox):
            if classId - 1 < len(classNames):
                className = classNames[classId - 1]
                if className in valid_classes and confidence > 0.5:
                    valid_object_detected = True
                    x, y, w, h = box
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Draw rectangle around the object
                    cv2.putText(img, className, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)  # Add object label

    data_to_send = b'1' if valid_object_detected else b'0'
    ser.write(data_to_send)

    cv2.imshow(winName, img)

    key = cv2.waitKey(1)
    if key == 27:
        break

cv2.destroyAllWindows()
