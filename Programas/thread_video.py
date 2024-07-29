from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6 import QtCore, QtGui

import cv2
import cvzone
import math
import time
import numpy as np
import csv
import datetime
from sort import Sort
from ultralytics import YOLO


class Work(QThread):
    Imageupd = pyqtSignal(QtGui.QImage)
    errorReading = pyqtSignal(str)
    detected_signal = pyqtSignal(str, str)

    def __init__(self, path_csv="", sourceType="", videoSource="", sendEmail=False):
        super().__init__()
        self.current_detected_Head = None
        self.current_detected_Vet = None
        self.sendEmail = sendEmail
        self.path_csv = path_csv
        self.sourceType = sourceType
        self.videoSource = videoSource
        print(f"{self.videoSource}")
        self.thread_running = True
        self.trackerHead = Sort(max_age=30, min_hits=12, iou_threshold=0.3)
        self.trackerVet = Sort(max_age=30, min_hits=12, iou_threshold=0.3)
        self.detected_Head = []
        print(f"esta es el tipo de variable al iniciar{type(self.detected_Head)}\n")
        self.detected_Vet = []
        self.cap = cv2.VideoCapture()
        self.classNames = ['CASCO', 'MASCARA', 'SIN CASCO', 'SIN MASCARA', 'SIN CHALECO', 'PERSONA',
                           'CONO DE SEGURIDAD',
                           'CHALECO', 'maquinaria', 'VEHICULO']
        self.model = YOLO('ppe.pt')

    def run(self):
        if self.sourceType == "Camara Integrada":
            self.cap.open(0, cv2.CAP_DSHOW)
        elif self.sourceType == "Camara IP":
            print("se va a iniciar la camara IP")
            self.cap.open(self.videoSource)
        elif self.sourceType == "Ejemplo":
            self.cap.open(self.videoSource)
        else:
            self.errorReading.emit("Error en los datos")
            self.stop()

        while self.thread_running:
            success, img = self.cap.read()
            if success:
                self.current_detected_Vet, self.current_detected_Head = self.detect_objets(img, self.classNames,
                                                                                           self.model)
                #self.detected_Vet, self.detected_Head = detection_epp.detect_objects(img, self.classNames, self.model)
                self.process_detections(self.current_detected_Vet, self.current_detected_Head, img, self.path_csv)
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                convertir_QT = QtGui.QImage(img.data, img.shape[1], img.shape[0], QtGui.QImage.Format.Format_RGB888)
                pic = convertir_QT.scaled(640, 480, QtCore.Qt.AspectRatioMode.KeepAspectRatio)
                self.Imageupd.emit(pic)
                #cv2.waitKey(100)
            else:
                self.errorReading.emit("Error al leer la fuente")
                self.stop()
                break

        self.cap.release()
        self.finished.emit()

    def stop(self):
        self.thread_running = False
        self.quit()
        self.wait()

    def detect_objets(self, img, classNames, model):
        results = model(img, verbose=False, stream=True)
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
                    if currentClass == 'SIN CASCO' and w > 0 :# retornar
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

    def process_detections(self, detectionsHead, detectionsVet, img, cvs_path):
        resultsTrackerHead = self.trackerHead.update(detectionsHead)
        for resultHead in resultsTrackerHead:
            x1, y1, x2, y2, id = resultHead
            cvzone.putTextRect(img, f'{int(resultHead[4])} con {x2-x1} Registrado!', (35, 35))
            if id not in self.detected_Head:
                #print(f"esta es el tipo de variable al iniciar{type(self.detected_Head)}\n")
                self.detected_Head.append(id)
                cv2.imwrite(f'capturas/{int(resultHead[4])}Casco.jpg', img)
                print("Nueva detection guardando imagen y enviando correo")
                self.write_to_csv("Sin Casco", self.path_csv)
                if self.sendEmail:
                    self.detected_signal.emit("Este email fue mandado desde  la thread de Video",
                                              f'capturas/{int(resultHead[4])}Casco.jpg')

        resultsTrackerVet = self.trackerVet.update(detectionsVet)
        for resultVet in resultsTrackerVet:
            x1, y1, x2, y2, id = resultVet
            cvzone.putTextRect(img, f'{int(resultVet[4])} Registrado!', (35, 35))
            if id not in self.detected_Vet:
                self.detected_Vet.append(id)
                cv2.imwrite(f'capturas/{int(resultVet[4])}Chaleco.jpg', img)
                self.write_to_csv("Sin Casco", self.path_csv)
                if self.sendEmail:
                    self.detected_signal.emit("Este email fue mandado desde  la thread de Video",
                                              f'capturas/{int(resultHead[4])}Casco.jpg')

    def write_to_csv(self, tipo, csv_path):
        now = datetime.datetime.now()
        fecha = now.strftime("%Y-%m-%d")
        hora = now.strftime("%H:%M:%S")
        with open(csv_path, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([tipo, fecha, hora])
