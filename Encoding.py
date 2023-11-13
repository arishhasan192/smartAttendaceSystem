import os
import pickle
import cv2
import face_recognition



imagesListPath=os.listdir('Images')
imagesList=[]
studentIds=[]
for path in imagesListPath:
    imagesList.append(cv2.imread(os.path.join('Images',path)))
    studentIds.append(os.path.splitext(path)[0])



def findEncodings(imagesList):
    encodeList=[]
    for image in imagesList:
        #bgr to rgb in face-recognition library(uses rgb) opencv(uses bgr)
        img=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        encode=face_recognition.face_encodings(img)[0]
        encodeList.append(encode)

    return encodeList

print("Encoding started...")
encodeListKnown=findEncodings(imagesList)
encodeListKnownWithIds=[encodeListKnown,studentIds]
# print(encodeListKnown)
print("Encoding complete..")

file=open("EncodeFile.p","wb")
pickle.dump(encodeListKnownWithIds,file)
file.close()
print("File saved")