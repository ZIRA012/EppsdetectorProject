from torchvision.transforms.v2.functional import crop_image
from ultralytics import YOLO
import cv2
import cvzone
import math
import time
import numpy as np

from sort import *
cap = cv2.VideoCapture("http://admin:nbcm2018@10.160.78.33/ISAPI/Streaming/channels/102/httpPreview") #acceso a cama
#cap = cv2.VideoCapture(0,cv2.CAP_DSHOW) Acceso a camara
#cap = cv2.VideoCapture("video1.mp4")
#cap = cv2.VideoCapture("rtsp://admin:nbcm2018@10.160.78.33:554/Streaming/channels/102",cv2.CAP_FFMPEG)  # For Webcam
#cap.set(3, 480)
#cap.set(4, 360)


model = YOLO('ppe.pt')
#sin casco 2, sin chaleco 4
Detected_peopleID = []
classNames = ['CASCO', 'MASCARA', 'SIN CASCO', 'SIN MASCARA', 'SIN CHALECO', 'PERSONA', 'CONO DE SEGURIDAD',
              'CHALECO', 'maquinaria', 'VEHICULO']
myColor = (0, 0, 255)
success = 1
tracker = Sort(max_age =20, min_hits =12, iou_threshold=0.3)

while success:
    start_time = time.time()
    while True:
        success, img = cap.read()
        if success == 0:
            print("error")
            #Waitkey
        if success == 1:
            print("imagen leida")
            break

    #img = cv2.resize(img, (640, 480))


    #img = crop_image(img, 300, 300, 300, 300)
    results = model(img, stream=True)
    #results.boxes
    detections = np.empty((0,6))

    for r in results:
        boxes = r.boxes
        for box in boxes:
            # Bounding Box
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            #cv2.rectangle(img,(x1,y1),(x2,y2),(255,0,255),3)
            w, h = x2 - x1, y2 - y1
            #cvzone.cornerRect(img, (x1, y1, w, h))

            # Confidence
            conf = math.ceil((box.conf[0] * 100)) / 100
            # Class Name
            cls = int(box.cls[0])
            currentClass = classNames[cls]
            print(currentClass)
            if conf > 0.5:
                if (currentClass == 'SIN CASCO' or currentClass == 'SIN CHALECO') and w>45:
                    myColor = (0, 0, 255)
                    cvzone.putTextRect(img, f'{classNames[cls]} {conf}%',
                                       (max(0, x1), max(35, y1)), scale=1, thickness=1, colorB=myColor,
                                       colorT=(255, 255, 255), colorR=myColor, offset=5)
                    CurrentArray = np.array([x1,y1,x2,y2,conf,cls])
                    detections =np.vstack((detections, CurrentArray))
                    cv2.rectangle(img, (x1, y1), (x2, y2), myColor, 3)
                elif currentClass == 'CASCO' or currentClass == 'CHALECO':
                    myColor = (0, 255, 0)
                    cv2.rectangle(img, (x1, y1), (x2, y2), myColor, 1)
                    #cvzone.putTextRect(img, f'{classNames[cls]} {conf}',
                    #                  (max(0, x1), max(35, y1)), scale=1, thickness=1, colorB=myColor,
                                 #      colorT=(255, 255, 255), colorR=myColor, offset=5)
                else:
                    myColor = (0, 0, 0)


    #Conteo
    resultsTracker = tracker.update(detections[:, :-1])
    for result in resultsTracker:
        print(result)
        x1,y1,x2,y2,id = result
        cvzone.putTextRect(img, f'{(result)[4]} Registrado!',(35, 35))
        if Detected_peopleID.count(id) == 0:
            Detected_peopleID.append(id)
            cv2.imwrite(f'capturas/{(result)[4]}.jpg', img)



    cv2.imshow("Image", img)
    end_time = time.time()
    # Calcular el tiempo transcurrido en segundos
    elapsed_time = end_time - start_time

    # Calcular los FPS

    fps = 1.0 / elapsed_time
    print(f"FPS: {fps} and tiempo de espera: {100-elapsed_time*1000}")
    if(100-elapsed_time*1000>20):
        cv2.waitKey(int(100 - elapsed_time * 1000))
    else:
        cv2.waitKey(1000)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
