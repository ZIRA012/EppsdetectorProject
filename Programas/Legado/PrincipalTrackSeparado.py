from torchvision.transforms.v2.functional import crop_image
from ultralytics import YOLO
import cv2
import cvzone
import math
import time
import numpy as np
import csv
import datetime
from sort import *

csv_file = "C:/Users/Ronald/Anheuser-Busch InBev/TECH - DetecionEpps/reporte.csv"

def write_to_csv(tipo):
    now = datetime.datetime.now()
    fecha = now.strftime("%Y-%m-%d")
    hora = now.strftime("%H:%M:%S")
    with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([tipo, fecha, hora])


#cap = cv2.VideoCapture("http://admin:nbcm2018@10.160.78.33/ISAPI/Streaming/channels/102/httpPreview") #acceso a cama
#cap = cv2.VideoCapture(0,cv2.CAP_DSHOW) Acceso a camara
cap = cv2.VideoCapture("video1.mp4")
#cap = cv2.VideoCapture("rtsp://admin:nbcm2018@10.160.78.33:554/Streaming/channels/102",cv2.CAP_FFMPEG)  # For Webcam
#cap.set(3, 480)
#cap.set(4, 360)


model = YOLO('ppe.pt')
#sin casco 2, sin chaleco 4
Detected_Head = []
Detected_Vet = []
classNames = ['CASCO', 'MASCARA', 'SIN CASCO', 'SIN MASCARA', 'SIN CHALECO', 'PERSONA', 'CONO DE SEGURIDAD',
              'CHALECO', 'maquinaria', 'VEHICULO']
myColor = (0, 0, 255)
success = 1
trackerHead = Sort(max_age =20, min_hits =12, iou_threshold=0.3)
trackerVet = Sort(max_age =20, min_hits =12, iou_threshold=0.3)

while success:
    start_time = time.time()
    while True:
        success, img = cap.read()
        if success == 0:
            print("error")

        if success == 1:
            print("imagen leida")
            break

    #img = cv2.resize(img, (640, 480))


    #img = crop_image(img, 300, 300, 300, 300)
    results = model(img, stream=True)
    detectionsHead = np.empty((0, 5))
    detectionsVet = np.empty((0,5))
    for r in results:
        boxes = r.boxes
        for box in boxes:
            # Bounding Box
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            #cv2.rectangle(img,(x1,y1),(x2,y2),(255,0,255),3)
            w, h = x2 - x1, y2 - y1
            #cvzone.cornerRect(img, (x1, y1, w, h))

            # Nivel  de confianza
            conf = math.ceil((box.conf[0] * 100)) / 100
            # Class Name
            cls = int(box.cls[0])
            currentClass = classNames[cls]
            print(currentClass)
            if conf > 0.5:
                if currentClass == 'SIN CASCO' and w>45:
                    myColor = (0, 0, 255)
                    cvzone.putTextRect(img, f'{classNames[cls]} {conf}%',
                                       (max(0, x1), max(35, y1)), scale=1, thickness=1, colorB=myColor,
                                       colorT=(255, 255, 255), colorR=myColor, offset=5)
                    CurrentArray = np.array([x1,y1,x2,y2,conf])
                    detectionsHead =np.vstack((detectionsHead, CurrentArray))
                    cv2.rectangle(img, (x1, y1), (x2, y2), myColor, 3)
                elif currentClass == 'SIN CHALECO' and w >45:
                    myColor = (0, 0, 255)
                    cvzone.putTextRect(img, f'{classNames[cls]} {conf}%',
                                       (max(0, x1), max(35, y1)), scale=1, thickness=1, colorB=myColor,
                                       colorT=(255, 255, 255), colorR=myColor, offset=5)
                    CurrentArray = np.array([x1, y1, x2, y2, conf])
                    detectionsVet = np.vstack((detectionsVet, CurrentArray))
                    cv2.rectangle(img, (x1, y1), (x2, y2), myColor, 3)

                elif currentClass == 'CASCO' or currentClass == 'CHALECO':
                    myColor = (0, 255, 0)
                    cv2.rectangle(img, (x1, y1), (x2, y2), myColor, 1)
                    #cvzone.putTextRect(img, f'{classNames[cls]} {conf}',
                    #                  (max(0, x1), max(35, y1)), scale=1, thickness=1, colorB=myColor,
                                 #      colorT=(255, 255, 255), colorR=myColor, offset=5)
                else:
                    myColor = (0, 0, 0)


    #Conteo de personas sin CASCO
    resultsTrackerHead = trackerHead.update(detectionsHead)
    for resultHead in resultsTrackerHead:
        print(resultHead)
        x1,y1,x2,y2,id = resultHead
        cvzone.putTextRect(img, f'{(resultHead)[4]} Registrado!',(35, 35))
        if Detected_Head.count(id) == 0:
            Detected_Head.append(id)
            cv2.imwrite(f'capturas/{(resultHead)[4]}Casco.jpg', img)
            write_to_csv("Sin Casco")



    #conteo de personas sin Chaleco de seguridad

    resultsTrackerVet = trackerVet.update(detectionsVet)
    for resultVet in resultsTrackerVet:
        print(resultVet)
        x1, y1, x2, y2, id = resultVet
        cvzone.putTextRect(img, f'{(resultVet)[4]} Registrado!', (35, 35))
        if Detected_Vet.count(id) == 0:
            Detected_Vet.append(id)
            cv2.imwrite(f'capturas/{(resultVet)[4]}Chaleco.jpg', img)



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
