import cv2
import numpy as np
import os
import shutil
from PIL import Image

class Recognize:
    def __init__(self, number:int, names:list):
        self.recognizer = cv2.face_LBPHFaceRecognizer.create()
        self.face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.path = os.getcwd()
        self.dataset_path = os.path.join(self.path, "dataset")
        self.trainer_path = os.path.join(self.path, "trainer")
        self.number = number
        self.names = names

    def predict(self):
        self.recognizer.read('trainer/trainer.yml')
        cam = cv2.VideoCapture(0)
        font = cv2.FONT_HERSHEY_SIMPLEX
        while True:
            _, im =cam.read()
            gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
            faces = self.face_detector.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=3, minSize=(60, 60))

            for(x,y,w,h) in faces:
                cv2.rectangle(im, (x, y), (x+w, y+h), (0, 255, 0), 2)

                Id = self.recognizer.predict(gray[y:y+h,x:x+w])
                name = self.getNameById(Id)
                rate = Id[1]

                if self.isUnknown(name, rate):
                    cv2.rectangle(im, (x-22,y-90), (x+w+22, y-22), (0,255,0), -1)
                    cv2.putText(im, "Unknown", (x,y-40), font, 2, (255,255,255), 3)
                else:
                    cv2.rectangle(im, (x-22,y-90), (x+w+22, y-22), (0,255,0), -1)
                    cv2.putText(im, name, (x,y-40), font, 2, (255,255,255), 3)

            cv2.imshow('Recognize', im) 
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

        cam.release()
        cv2.destroyAllWindows()
        shutil.rmtree(self.dataset_path)
        shutil.rmtree(self.trainer_path)

    def toTrain(self):
        faces, ids = self.getImagesAndLabels()
        self.recognizer.train(faces, np.array(ids))
        self.recognizer.save('trainer/trainer.yml')

    def getImagesAndLabels(self):
        imagePaths = [os.path.join("dataset", f) for f in os.listdir("dataset")]
        faceSamples=[]
        ids = []
        for imagePath in imagePaths:
            PIL_img = Image.open(imagePath).convert('L')
            img_numpy = np.array(PIL_img,'uint8')
            id = int(os.path.split(imagePath)[-1].split(".")[1])
            faces = self.face_detector.detectMultiScale(img_numpy)
            for (x,y,w,h) in faces:
                faceSamples.append(img_numpy[y:y+h,x:x+w])
                ids.append(id)
        return faceSamples, ids

    def getNameById(self, Id:tuple):
        id = Id[0]
        files = os.listdir(self.dataset_path)
        for file in files:
            if str(id) in file:
                name = file.split(".")
                name = name[0]
        return str(name)

    def getNamesAndRates(self):
        rates, max_rates = list(), list()
        files = os.listdir(self.dataset_path)
        for i in range(self.number*30+1):
            i += 1
            if i > self.number*30:
                break
            path = os.path.join(self.dataset_path, files[i-1])
            rates.append(self.getRateByImage(path))
            if i%30==0:
                max_rates.append(max(rates))
                rates = list()
        names_and_rates = list(zip(self.names, max_rates))
        return names_and_rates

    def isUnknown(self, pred_name:str, pred_rate):
        names_and_rates = self.getNamesAndRates()
        for name, rate in names_and_rates:
            if pred_name == name:
                if pred_rate > rate + 60:
                    return True
        return False
         
    def getRateByImage(self, path):
        img = cv2.imread(path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.face_detector.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=3, minSize=(60, 60))
        rate = 0.0
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
            test = gray[x:x+w,y:y+h]
            test_img = np.array(test, 'uint8')
            Id = self.recognizer.predict(test_img)
            rate = Id[1]
        return rate
