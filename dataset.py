import cv2

class Dataset:
    def __init__(self):
        self.face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.recognizer = cv2.face_LBPHFaceRecognizer.create()
        self.count = 0

    def createDataset(self, name:str):
        vid_cam = cv2.VideoCapture(0)
        cv2.namedWindow("Face Detect")
        count = 0
        while(True):
            _, frame = vid_cam.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_detector.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=3, minSize=(60, 60))
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                self.count += 1
                count += 1
                cv2.imwrite(f"dataset/" + str(name) + '.' + str(self.count) + ".jpg", gray[y:y+h,x:x+w])
            cv2.imshow('Face Detect', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            if count == 30:
                break
            
        vid_cam.release()
        cv2.destroyAllWindows()
