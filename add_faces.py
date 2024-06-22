import cv2
import pickle
import numpy as np
import os

if not os.path.exists('data/'):
    os.makedirs('data/')

video = cv2.VideoCapture(0)
facedetect= cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
faces_data = []

i=0
name = input("Enter your aadhar number: ")
framesTotal=51
captureAfterFrame=2

while True:
    ret, frame = video.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces=facedetect.detectMultiScale(gray, 1.3 ,5)
    for(x, y, w, h) in faces:
        crop_img = frame[y:y+h, x:x+w]
        resized_img = cv2.resize(crop_img, (50, 50))
        if len(faces_data)<=framesTotal and i%captureAfterFrame==0:
            faces_data.append(resized_img)
        i=i+1
        cv2.putText(frame,str(len(faces_data)),(50,50),cv2.FONT_HERSHEY_COMPLEX, 1, (50,50,255), 1)
        cv2.rectangle(frame, (x,y), (x+w, y+h), (50,50,255), 1)   


    cv2.imshow('frame', frame)
    k=cv2.waitKey(1)
    if k== ord('q') or len(faces_data) >= framesTotal:
        break
    

video.release()
cv2.destroyAllWindows()

#print(len(faces_data))
faces_data = np.asarray(faces_data)
faces_data = faces_data.reshape((framesTotal, -1))
print(len(faces_data))



if 'names.pk1' not in os.listdir('data/'):
    names=[name]*framesTotal
    with open('data/names.pk1', 'wb') as f:
        pickle.dump(names, f)
else:
    with open('data/names.pk1', 'rb') as f:
        names=pickle.load(f)
    names=names+[name]*framesTotal  
    with open('data/names.pk1', 'wb') as f:
        pickle.dump(names, f)


if 'faces_data.pk1' not in os.listdir('data/'):
    with open('data/faces_data.pk1', 'wb') as f:
        faces=pickle.dump(faces_data, f)
else:
    with open('data/faces_data.pk1', 'rb') as f:
        faces=pickle.load(f)
    faces=np.append(faces, faces_data, axis=0)
    with open('data/faces_data.pk1', 'wb') as f:
        pickle.dump(faces,f)