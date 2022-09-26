# Import required Libraries
from datetime import datetime
import mysql.connector
import cv2 as cv
from tkinter import *
import time

# --mark attendance--


def ImageRecognition():
    recognizer = cv.face.LBPHFaceRecognizer_create()
    recognizer.read("StudentLabel\Trainner.yml")
    harcascadepath = "haarcascades/haarcascade_frontalface_default.xml"
    facecascade = cv.CascadeClassifier(harcascadepath)

    cam = cv.VideoCapture(0)
    font = cv.FONT_ITALIC
    while True:
        ret, frame = cam.read()
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        faces = facecascade.detectMultiScale(gray, 1.1, 10)
        r = 15
        d = 10
        color = (255, 238, 66)
        thickness = 3
        for (x, y, w, h) in faces:
            roi_gray = gray[y:y + h, x:x + w]
            x1, y1 = (x, y)
            x2, y2 = (x + w, y + h)
            # Top left
            cv.line(frame, (x1 + r, y1),
                    (x1 + r + d, y1), color, thickness)
            cv.line(frame, (x1, y1 + r),
                    (x1, y1 + r + d), color, thickness)
            cv.ellipse(frame, (x1 + r, y1 + r), (r, r),
                       180, 0, 90, color, thickness)
            # Top right
            cv.line(frame, (x2 - r, y1),
                    (x2 - r - d, y1), color, thickness)
            cv.line(frame, (x2, y1 + r),
                    (x2, y1 + r + d), color, thickness)
            cv.ellipse(frame, (x2 - r, y1 + r), (r, r),
                       270, 0, 90, color, thickness)
            # Bottom left
            cv.line(frame, (x1 + r, y2),
                    (x1 + r + d, y2), color, thickness)
            cv.line(frame, (x1, y2 - r),
                    (x1, y2 - r - d), color, thickness)
            cv.ellipse(frame, (x1 + r, y2 - r), (r, r),
                       90, 0, 90, color, thickness)
            # Bottom right
            cv.line(frame, (x2 - r, y2),
                    (x2 - r - d, y2), color, thickness)
            cv.line(frame, (x2, y2 - r),
                    (x2, y2 - r - d), color, thickness)
            cv.ellipse(frame, (x2 - r, y2 - r), (r, r),
                       0, 0, 90, color, thickness)
            sid, conf = recognizer.predict(roi_gray)
            try:
                connection = mysql.connector.connect(host='localhost',
                                                     database='examination_attendance',
                                                     user='root',
                                                     password='root')
                cursor = connection.cursor()
                sql_select_query = """SELECT * from student_examination_list WHERE student_id = %s"""
                # set variable in query
                cursor.execute(sql_select_query, (sid,))
                # fetch result
                record = cursor.fetchall()

                for row in record:
                    # print(row[1])
                    row[1]

            except mysql.connector.Error as e:
                print("Error reading data from MySQL table", e)

            print(conf)
            if 20 <= conf <= 65:
                no = "SID: " + str(sid)
                name = "Name: " + str(row[1])
                ts = time.time()
                date = datetime.fromtimestamp(
                    ts).strftime('%y-%m-%d')
                current_time = datetime.fromtimestamp(
                    ts).strftime('%H:%M:%S')
                present = 'P'
                # check attendance record
                check_cursor = connection.cursor()
                check_cursor.execute(
                    "SELECT * from attendance_records WHERE student_id = %s AND date = %s", (sid, date))
                data_check = check_cursor.fetchall()
                if not data_check:
                    attendance_cursor = connection.cursor()
                    attendance_cursor.execute(
                        "INSERT INTO attendance_records (student_id,time,date,status) VALUES (%s,%s,%s,%s)",
                        (sid, current_time, date, present))
                    connection.commit()
                    status = "Status: Successfully Clocked In"
                    masked = "NO MASK - PLEASE WEAR MASK"
                else:
                    status = "Status: Attended"
                    masked = "NO MASK - PLEASE WEAR MASK"
            else:
                no = "Unknown"
                name = ""
                status = ""
                masked = ""
            cv.putText(frame, no, (x, y + h + 30),
                       font, 0.5, (5, 5, 5), 2)
            cv.putText(frame, name, (x, y + h + 50),
                       font, 0.5, (5, 5, 5), 2)
            cv.putText(frame, status, (x, y + h + 70),
                       font, 0.5, (5, 5, 5), 2)
            cv.putText(frame, masked, (x, y + h + 90),
                       font, 0.5, (0, 0, 255), 2)

        cv.imshow('Recognition Window', frame)

        if cv.waitKey(1) == ord('q'):
            break

    cam.release()
    cv.destroyAllWindows()
