from flask import Blueprint, Response, request
from .models import Student
from .studentInfo import studentInfo, append_attendance, names, absents
from . import db
import cv2
import os
import numpy as np
from PIL import Image

student = Blueprint("student", __name__)  # blueprint of the student file

# where the image of the student save
FILE_IMAGE_TO_SAVE = os.path.realpath("application/static/img")

global IMAGE_CAPTURE, IMAGE_NAME, FACE_DETECT, image_url, FACE_VERIFEID
IMAGE_CAPTURE = 0
IMAGE_NAME = ""
START = 1
FACE_DETECT = 0
count = 0

videoCam = cv2.VideoCapture(0)

face_detect = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

recognizer = cv2.face.LBPHFaceRecognizer.create()

if os.path.exists(os.path.realpath(f"application/static/trainer/images.yml")):
    recognizer.read(os.path.realpath(f"application/static/trainer/images.yml"))


def train_faces():

    global face_detect
    path = os.path.realpath("application/static/img")
    path_url = [os.path.join(path, f) for f in os.listdir(path)]
    faceData = []
    imageId = []
    for pathData in path_url:
        PIL_img = Image.open(pathData).convert("L")
        img_arr = np.array(PIL_img)
        id = int(os.path.split(pathData)[-1].split(".")[1])
        faceData.append(img_arr)
        imageId.append(id)
    return faceData, imageId


def student_camera():
    global IMAGE_CAPTURE, IMAGE_NAME, FACE_DETECT, list_img, list_recognizer

    while True:
        success, frame = videoCam.read()  # read the camera frame

        # check if camera is open if not the application will stop
        if not success:
            pass
        else:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_detect.detectMultiScale(
                gray,
                scaleFactor=1.3,
                minNeighbors=5,
                minSize=(20, 20)
            )

            if IMAGE_CAPTURE == 1:
                IMAGE_CAPTURE = 0

                for (x, y, w, h) in faces:
                    cv2.imwrite(
                        f"{FILE_IMAGE_TO_SAVE}/{IMAGE_NAME}.{count}.png", gray[y:y+h, x:x+w])

            if FACE_DETECT == 1:
                if os.path.exists(os.path.realpath(f"application/static/trainer/images.yml")):
                    for (x, y, w, h) in faces:
                        id, confidence = recognizer.predict(gray[y:y+h, x:x+w])
                        append_attendance(id)
                        absents()
                        if confidence < 50:
                            id = names()[id]
                            # append to the csv file
                            cv2.rectangle(frame, (x, y), (x+w, y+h),
                                          (0, 255, 0), 2)

                            cv2.rectangle(frame, (x, y), (x + w, y - 35),
                                          (0, 255, 0), cv2.FILLED)
                            cv2.putText(frame, id, (x+5, y-5),
                                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                        else:
                            id = "Unknown"

                            cv2.rectangle(frame, (x, y), (x+w, y+h),
                                          (0, 0, 255), 2)

                            cv2.rectangle(frame, (x, y), (x + w, y - 35),
                                          (0, 0, 255), cv2.FILLED)
                            cv2.putText(frame, id, (x+5, y-5),
                                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                else:
                    for (x, y, w, h) in faces:
                        id = "Unknown"

                        cv2.rectangle(frame, (x, y), (x+w, y+h),
                                      (0, 0, 255), 2)
                        cv2.rectangle(frame, (x, y), (x + w, y - 35),
                                      (0, 0, 255), cv2.FILLED)
                        cv2.putText(frame, id, (x+5, y-5),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

            _, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@student.route("/open-cam")
def open_cam():

    return Response(student_camera(), mimetype="multipart/x-mixed-replace; boundary=frame")


@student.route("/open-attendance", methods=["GET", "POST"])
def open_attendance():
    global videoCam, FACE_DETECT, names
    if request.method == "POST":
        open = request.json["open_attendance"]
        if open == "openAttendance":
            videoCam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            FACE_DETECT = 1

        else:
            FACE_DETECT = 0
            videoCam.release()
            cv2.destroyAllWindows()
    return {"message": "Open"}


@student.route("/start-cam", methods=["GET", "POST"])
def take_shot():

    global START, videoCam, IMAGE_CAPTURE
    if request.method == "POST":
        if request.json["start"] == "openCamera":
            videoCam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        elif request.json["close"] == "closeCamera":
            videoCam.release()
            cv2.destroyAllWindows()

    return {"message": "start/close"}


@student.route("/train-student-data")
def train_student():
    """Train image data for face recognition"""
    id = request.args.get("student")

    # recognizer for the image recognizer
    global recognizer
    recognizer = cv2.face.LBPHFaceRecognizer.create()
    face, ids = train_faces()
    recognizer.train(face, np.array(ids))
    recognizer.write(os.path.realpath(
        f"application/static/trainer/images.yml"))
    return {"message": "Trained"}


@student.route("/add-student-data", methods=["GET", "POST"])
def addStudent():
    """Add student to the database"""
    if request.method == "POST":
        firstname = request.form.get("firstname").title()
        lastname = request.form.get("lastname").title()
        address = request.form.get("address")
        number = request.form.get("number")

        exists = Student.query.filter_by(firstname=firstname).first()

        if exists:
            return {"message": f"{firstname} already exists in the database."}
        elif firstname == "":
            return {"message": "First name is empty"}
        elif lastname == "":
            return {"message": "Last name is empty"}
        elif address == "":
            return {"message": "Address is empty"}
        elif number == "":
            return {"message": "Phone number is empty."}
        elif len(number) < 11:
            return {"message": "Phone number should be lenght of 11 numbers"}
        else:
            global IMAGE_NAME, IMAGE_CAPTURE, count
            new_data = Student(
                firstname=firstname,
                lastname=lastname,
                address=address,
                number=number,
            )

            db.session.add(new_data)
            db.session.commit()

            IMAGE_NAME = firstname
            count = new_data.id
            updateId = Student.query.get(count)
            updateId.image_url = f"{firstname}.{count}.png"
            IMAGE_CAPTURE = 1
            db.session.commit()

            return {"message": studentInfo(updateId)}
