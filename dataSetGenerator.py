import cv2
import sqlite3
from datetime import datetime


cam = cv2.VideoCapture(0)
faceDetect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')


def insertOrUpdate(Id, Name, date, cam_id):
    conn = sqlite3.connect("DataBase.db")
    cmd = "SELECT * FROM People WHERE ID=" + str(Id)
    cursor = conn.execute(cmd)
    isRecordExist = 0
    for row in cursor:
        isRecordExist = 1
    if isRecordExist == 1:
        cmd = "UPDATE People SET Name=' " + str(name) + " ', date = ' " + str(date) + " ', cam_id = " + str(cam_id) + " WHERE ID=" + str(Id)
    else:
        cmd = "INSERT INTO people(ID,Name, date, cam_id) Values(" + str(Id) + ",' " + str(name) + " ',' " + str(date) + " ', " + str(cam_id) + ")"

    conn.execute(cmd)
    conn.commit()
    conn.close()


id = input('Enter your id: ')
name = input('Enter your name: ')
insertOrUpdate(id, name, datetime.now(), 0)
sampleNum = 0

while True:
    ret, img = cam.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceDetect.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        sampleNum = sampleNum + 1
        cv2.imwrite("dataSet/User." + str(id) + "." + str(sampleNum) + ".jpg", gray[y:y + h, x:x + w])
        cv2.rectangle(img, (x, y), (x + y, y + h), (0, 255, 255), 2)
        cv2.waitKey(100)
        cv2.imshow("Face", img)
        cv2.waitKey(1)
        if sampleNum > 120 or cv2.waitKey(1) == ord('q'):
            break

cam.release()
cv2.destroyAllWindows()
