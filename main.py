import os
import pickle
from datetime import datetime
import cv2
import cvzone
import face_recognition
import numpy as np
import firebase_admin
import firebase_admin.db
from firebase_admin import credentials
import firebase_admin
from firebase_admin import storage

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL': "https://smartattendance-5a59e-default-rtdb.firebaseio.com/",
    'storageBucket': "smartattendance-5a59e.appspot.com"
})



cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)

imageBackground = cv2.imread('Resources/background.png')

#Loading mode images to imgModeList begin.
folderModePath='Resources/Modes'
modePathList=os.listdir(folderModePath)
imgModeList=[]
for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModePath,path)))
#Loading mode images end.
# print(len(imgModeList))

#import the encoding File
print("Loading Encoded File ....")
file=open("EncodeFile.p",'rb')
encodeListKnownWithIds=pickle.load(file)
file.close()
encodeListKnown,studentIds=encodeListKnownWithIds
# print(studentIds)
print("Encode File Loaded ....")

#Mode type initially if attendance is not marked it will be 0
modeTypeIdx = 0
#we need to download the data if the first frame is matched right after
counter = 0
#id of image
id = -1

while True:
    success,img = cap.read()

    imgS = cv2.resize(img,(0,0),None,0.25,0.25,)
    imgS = cv2.cvtColor(imgS,cv2.COLOR_BGR2RGB)

    faceCurrFrame = face_recognition.face_locations(imgS)
    encodeCurrFrame=face_recognition.face_encodings(imgS,faceCurrFrame)


    imageBackground[162:162+480,55:55+640]=img
    imageBackground[44:44+633,808:808+414]=imgModeList[modeTypeIdx]


    if faceCurrFrame:
        for encodeface, faceLoc in zip(encodeCurrFrame, faceCurrFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeface)
            faceDist = face_recognition.face_distance(encodeListKnown, encodeface)
            matchIndex = np.argmin(faceDist)
            if matches[matchIndex]:
                # print("known face detected " ,studentIds[matchIndex])
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
                imgBackground = cvzone.cornerRect(imageBackground, bbox, rt=0)
                id = studentIds[matchIndex]
                if counter == 0:
                    counter = 1
                    modeTypeIdx = 1

        if counter != 0:

            if counter == 1:
                studentInfo = firebase_admin.db.reference(f'Students/{id}').get()
                print(studentInfo)

                # Updatae data of attendance if timeElapse
                datetimeObject = datetime.strptime(studentInfo['last_attendacne_time'],
                                                   "%Y-%m-%d %H:%M:%S")
                timeElapse = (datetime.now() - datetimeObject).total_seconds()
                # print(timeElapse)
                if timeElapse > 30:
                    ref = firebase_admin.db.reference(f'Students/{id}')
                    studentInfo['total_attendance'] += 1
                    ref.child('total_attendance').set(studentInfo['total_attendance'])
                    ref.child('last_attendacne_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                else:
                    modeTypeIdx = 3
                    counter = 0
                    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeTypeIdx]
            if modeTypeIdx != 3:
                if 10 < counter < 20:
                    modeTypeIdx = 2

                imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeTypeIdx]

                if counter <= 10:
                    cv2.putText(imgBackground, "Total Attendance " + str(studentInfo['total_attendance']), (840, 125),
                                cv2.FONT_HERSHEY_COMPLEX,
                                1, (255, 255, 255), 1)

                    cv2.putText(imgBackground, str(studentInfo['name']), (808, 500),
                                cv2.FONT_HERSHEY_COMPLEX,
                                1, (255, 255, 255), 1)
                    cv2.putText(imgBackground, "Branch: " + str(studentInfo['branch']), (808, 600),
                                cv2.FONT_HERSHEY_COMPLEX,
                                1, (255, 255, 255), 1)
                    cv2.putText(imgBackground, "Id: " + str(id), (808, 550),
                                cv2.FONT_HERSHEY_COMPLEX,
                                1, (255, 255, 255), 1)
                    cv2.putText(imgBackground, "Year: " + str(studentInfo['year']), (808, 650),
                                cv2.FONT_HERSHEY_COMPLEX,
                                1, (255, 255, 255), 1)
                counter += 1

                if counter >= 20:
                    counter = 0
                    modeTypeIdx = 0

                    studentInfo = []
                    imageBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeTypeIdx]


    else :
        modeTypeIdx = 0
        counter = 0
    cv2.imshow('image background',imageBackground)
    cv2.waitKey(1)