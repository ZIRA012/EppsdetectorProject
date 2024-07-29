import cv2
import cvzone
import math
import time
import numpy as np
import csv
import datetime
from sort import Sort
from ultralytics import YOLO


#se debe generar un forma de utilizar las rutas y las variables internas
#buscar como verificar las rutas propuestas
#Variable externas que deben ser cargadas o verificadas
csv_path = "C:/Users/Ronald/Anheuser-Busch InBev/TECH - DetecionEpps/reporte.csv"
classNames = ['CASCO', 'MASCARA', 'SIN CASCO', 'SIN MASCARA', 'SIN CHALECO', 'PERSONA', 'CONO DE SEGURIDAD',
              'CHALECO', 'maquinaria', 'VEHICULO']
model = YOLO('ppe.pt')

# Trackers variable internas del algoritmo
trackerHead = Sort(max_age=20, min_hits=12, iou_threshold=0.3)
trackerVet = Sort(max_age=20, min_hits=12, iou_threshold=0.3)
Detected_Head = []
Detected_Vet = []


def write_to_csv(tipo,csv_path):
    now = datetime.datetime.now()
    fecha = now.strftime("%Y-%m-%d")
    hora = now.strftime("%H:%M:%S")
    with open(csv_path, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([tipo, fecha, hora])


def detect_objects(img, classNames, model):
    results = model(img, stream=True)
    detectionsHead = np.empty((0, 5))
    detectionsVet = np.empty((0, 5))

    for r in results:
        boxes = r.boxes
        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            w, h = x2 - x1, y2 - y1
            conf = math.ceil((box.conf[0] * 100)) / 100
            cls = int(box.cls[0])
            currentClass = classNames[cls]

            if conf > 0.5:
                if currentClass == 'SIN CASCO' and w > 45:
                    myColor = (0, 0, 255)
                    cvzone.putTextRect(img, f'{classNames[cls]} {conf}%',
                                       (max(0, x1), max(35, y1)), scale=1, thickness=1, colorB=myColor,
                                       colorT=(255, 255, 255), colorR=myColor, offset=5)
                    CurrentArray = np.array([x1, y1, x2, y2, conf])
                    detectionsHead = np.vstack((detectionsHead, CurrentArray))
                    cv2.rectangle(img, (x1, y1), (x2, y2), myColor, 3)
                elif currentClass == 'SIN CHALECO' and w > 45:
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
                else:
                    myColor = (0, 0, 0)

    return detectionsHead, detectionsVet

def process_detections(detectionsHead, detectionsVet, img, cvs_path):
    resultsTrackerHead = trackerHead.update(detectionsHead)
    for resultHead in resultsTrackerHead:
        x1, y1, x2, y2, id = resultHead
        cvzone.putTextRect(img, f'{int(resultHead[4])} Registrado!', (35, 35))
        if id not in Detected_Head:
            Detected_Head.append(id)
            cv2.imwrite(f'capturas/{int(resultHead[4])}Casco.jpg', img)

            write_to_csv("Sin Casco", csv_path)

    resultsTrackerVet = trackerVet.update(detectionsVet)
    for resultVet in resultsTrackerVet:
        x1, y1, x2, y2, id = resultVet
        cvzone.putTextRect(img, f'{int(resultVet[4])} Registrado!', (35, 35))
        if id not in Detected_Vet:
            Detected_Vet.append(id)
            cv2.imwrite(f'capturas/{int(resultVet[4])}Chaleco.jpg', img)

def main():
    cap = cv2.VideoCapture("video1.mp4")
    success = 1

    while success:
        start_time = time.time()
        while True:
            success, img = cap.read()
            if not success:
                print("Error al leer la imagen")
                break
            print("Imagen leída")
            break

        detectionsHead, detectionsVet = detect_objects(img,classNames, model)
        process_detections(detectionsHead, detectionsVet, img, csv_path)

        cv2.imshow("Image", img)
        end_time = time.time()
        elapsed_time = end_time - start_time
        fps = 1.0 / elapsed_time
        print(f"FPS: {fps} y tiempo de espera: {100 - elapsed_time * 1000}")
        wait_time = max(1, int(100 - elapsed_time * 1000))
        if cv2.waitKey(wait_time) & 0xFF == ord('q'):
            break

    cap.release()


if __name__ == "__main__":
    main()
