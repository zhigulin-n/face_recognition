import cv2
import sqlite3

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("recognizer\\trainingData.yml")
faceDetect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
path = 'dataSet'


def getProfile(id):
    conn = sqlite3.connect("DataBase.db")
    cmd = "SELECT * FROM People WHERE ID=" + str(id)
    cursor = conn.execute(cmd)
    profile = None
    for row in cursor:
        profile = row
    conn.close()
    return profile


cam = cv2.VideoCapture(0)
rec = cv2.cv2.face.LBPHFaceRecognizer_create()
rec.read("recognizer\\trainingData.yml")
id = 0
font = cv2.FONT_HERSHEY_SIMPLEX

while (True):
    ret, img = cam.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceDetect.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        id, conf = rec.predict(gray[y:y + h, x:x + w])
        cv2.rectangle(img, (x, y), (x + y, y + h), (0, 255, 255), 2)
        profile = getProfile(id)
        if (profile != None) and conf < 60:
            cv2.putText(img, "Name: " + str(profile[1]), (x, y + h + 30), font, 1, (255, 0, 0))
        cv2.imshow("Face", img)
        if cv2.waitKey(1) == ord('q'):
            break

cam.release()
cv2.destroyAllWindows()
