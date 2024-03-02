from flask import Blueprint, render_template
from .studentInfo import generate_csv
from .models import Student, Status
from datetime import datetime

view = Blueprint("view", __name__)


@view.route("/")
def home():
    generate_csv()
    return render_template("home.html")


@view.route("/dashboard")
def dashboard():
    generate_csv()
    date = datetime.now().strftime("%B %d %Y")
    students = Student.query.all()

    status = Status.query.filter_by(date=date).all()
    present = len(
        [student.status for student in status if student.status == "Present"])
    absent = len(
        [student.status for student in status if student.status == "Absent"])

    late = len(
        [student.status for student in status if student.status == "Late"])

    return render_template("dashboard.html", students=students, present=present, late=late, absent=absent)


@view.route("/attendance-open")
def attendance_open():
    generate_csv()
    return render_template("attendance_camera.html")


@view.route("/camera-open")
def camera_open():
    generate_csv()
    return render_template("video.html")
