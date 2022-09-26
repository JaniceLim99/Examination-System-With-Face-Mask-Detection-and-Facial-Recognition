import cv2
import time

# Load the custom cascade
face_cascade = cv2.CascadeClassifier(
    'haarcascades/haarcascade_frontalface_default.xml')
mouth_cascade = cv2.CascadeClassifier(
    'haarcascades/haarcascade_mcs_mouth.xml')

# To capture video from webcam.
cap = cv2.VideoCapture(0)


prevTime = 0

while True:
    # Read the frame
    _, img = cap.read()
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Detect the faces
    faces = face_cascade.detectMultiScale(
        gray, scaleFactor=1.1, minNeighbors=10, minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)
    # Draw the rectangle around each face
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
        rol_gray = gray[y:y+h, x:x+w]
        rol_color = img[y:y+h, x:x+w]

        mouth = mouth_cascade.detectMultiScale(
            rol_gray, scaleFactor=1.3, minNeighbors=10, minSize=(10, 10), flags=cv2.CASCADE_SCALE_IMAGE)
        for (mx, my, mw, mh) in mouth:
            cv2.rectangle(rol_color, (mx, my), (mx+mw, my+mh), (255, 0, 0), 2)
    curTime = time.time()
    sec = curTime - prevTime
    prevTime = curTime
    fps = 1/(sec)
    str = "FPS : %0.1f" % fps
    cv2.putText(img, str, (0, 100), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255))
    # Display
    cv2.imshow('HAAR Detection - Custom', img)
    # Stop if escape key is pressed
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
# Release the VideoCapture object
cap.release()
