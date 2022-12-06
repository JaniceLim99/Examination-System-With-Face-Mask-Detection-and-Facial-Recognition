# Import required Libraries
import cv2 as cv
from tkinter import *
from tkinter.messagebox import showinfo
import numpy as np
import os
from PIL import Image
import time


def cam_recognize(sid, name, detection_file, dataset_folder, recognition_file):

    sampleNum = 0
    faceCascade = cv.CascadeClassifier(detection_file)
    video_capture = cv.VideoCapture(0)

    while True:
        # Capture frame-by-frame
        ret, frame = video_capture.read()
        # Convert BGR image to grayscale
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        # Detect Faces
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=12,
            minSize=(100, 100)
        )
        r = 15
        d = 10
        color = (255, 238, 66)
        thickness = 3
        # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            # cropping the only required face area
            faceROI = gray[y:y + h, x:x + w]
            x1, y1 = (x, y)
            x2, y2 = (x + w, y + h)
            # Top left
            cv.line(frame, (x1 + r, y1), (x1 + r + d, y1), color, thickness)
            cv.line(frame, (x1, y1 + r), (x1, y1 + r + d), color, thickness)
            cv.ellipse(frame, (x1 + r, y1 + r), (r, r),
                       180, 0, 90, color, thickness)
            # Top right
            cv.line(frame, (x2 - r, y1), (x2 - r - d, y1), color, thickness)
            cv.line(frame, (x2, y1 + r), (x2, y1 + r + d), color, thickness)
            cv.ellipse(frame, (x2 - r, y1 + r), (r, r),
                       270, 0, 90, color, thickness)
            # Bottom left
            cv.line(frame, (x1 + r, y2), (x1 + r + d, y2), color, thickness)
            cv.line(frame, (x1, y2 - r), (x1, y2 - r - d), color, thickness)
            cv.ellipse(frame, (x1 + r, y2 - r), (r, r),
                       90, 0, 90, color, thickness)
            # Bottom right
            cv.line(frame, (x2 - r, y2), (x2 - r - d, y2), color, thickness)
            cv.line(frame, (x2, y2 - r), (x2, y2 - r - d), color, thickness)
            cv.ellipse(frame, (x2 - r, y2 - r), (r, r),
                       0, 0, 90, color, thickness)
            # add logic
            cv.imwrite(dataset_folder + "\ " + name + "." + sid +
                       '.' + str(sampleNum) + ".png", faceROI)
            time.sleep(0.08)
            sampleNum = sampleNum + 1
            print(sampleNum)
        # Display the resulting frame
        cv.imshow('Capture - Face detection', frame)
        if sampleNum >= 50:
            train_image(detection_file, dataset_folder, recognition_file)
            time.sleep(0.30)
            showinfo(title='Image Side', message='Image successfully taken.')
            break

        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything is done, release the capture
    video_capture.release()
    cv.destroyAllWindows()


def train_image(detection_file, dataset_folder, recognition_file):
    recognizer = cv.face_LBPHFaceRecognizer.create()
    cv.CascadeClassifier(detection_file)
    faces, Id = getImagesAndLabels(dataset_folder)
    recognizer.train(faces, np.array(Id))
    recognizer.write(f"StudentLabel/{recognition_file}.yml")


def getImagesAndLabels(path):
    imagepaths = [os.path.join(path, f) for f in os.listdir(path)]
    faces = []
    Ids = []
    for imagepath in imagepaths:
        pilImage = Image.open(imagepath).convert('L')
        imageNp = np.array(pilImage, 'uint8')
        Id = int(os.path.split(imagepath)[-1].split(".")[1])
        faces.append(imageNp)
        Ids.append(Id)
    return faces, Ids
