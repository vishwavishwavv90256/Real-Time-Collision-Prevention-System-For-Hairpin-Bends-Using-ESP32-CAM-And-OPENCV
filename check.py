import cv2
import urllib.request
import numpy as np
import pyttsx3
import serial

url = 'http://192.168.96.96/cam-hi.jpg' 
winName = 'ESP32 CAMERA'
cv2.namedWindow(winName, cv2.WINDOW_AUTOSIZE)

# Load class names
classNames = []
classFile = 'coco.names'
with open(classFile, 'rt') as f:
    classNames = f.read().rstrip('\n').split('\n')

# Valid object classes and corresponding serial codes
valid_classes = {
    'person': b'1',
    'car': b'2',
    'truck': b'3',
    'bus': b'4',
    'train': b'5',
    'motorcycle': b'6',  
    'bicycle': b'7',
    'street sign': b'8',
    'stop sign': b'9',
    'fire hydrant': b'10'
}

configPath = 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
weightsPath = 'frozen_inference_graph.pb'


net = cv2.dnn_DetectionModel(weightsPath, configPath)
net.setInputSize(256, 256)
net.setInputScale(1.0 / 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)


ser = serial.Serial('COM9', 9600)


engine = pyttsx3.init()

while True:
    imgResponse = urllib.request.urlopen(url)
    imgNp = np.array(bytearray(imgResponse.read()), dtype=np.uint8)
    img = cv2.imdecode(imgNp, -1)

    img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)

   
    classIds, confs, bbox = net.detect(img, confThreshold=0.5)
    print(classIds, bbox)

    detected_objects = []
    valid_object_detected = False  
    serial_data = b'0'  

    if isinstance(classIds, np.ndarray):
        for classId, confidence, box in zip(classIds.flatten(), confs.flatten(), bbox):
            if classId - 1 < len(classNames):
                className = classNames[classId - 1]
                if className in valid_classes and confidence > 0.5:
                    detected_objects.append(className)
                    x, y, w, h = box
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)  
                    cv2.putText(img, className, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)  

                    
                    engine.say(f"{className} detected!")
                    engine.runAndWait()

                   
                    serial_data = valid_classes[className]
                    valid_object_detected = True

   
    obj_window_height = max(len(detected_objects) * 100, 100)  
    obj_window = np.zeros((obj_window_height, 400, 3), dtype=np.uint8)  
    for i, obj_name in enumerate(detected_objects):
        cv2.putText(obj_window, obj_name, (20, 30 * (i + 1)), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.imshow("Detected Objects", obj_window)

   
    ser.write(serial_data)

    
    cv2.imshow(winName, img)

    key = cv2.waitKey(1)
    if key == 27:  
        break

cv2.destroyAllWindows()
