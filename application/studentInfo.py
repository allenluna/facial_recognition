from . import create_app, db
from .models import Student, Status
import os
from datetime import datetime
import pandas as pd


def studentInfo(data):

    return {
        "id": data.id,
        "firstname": data.firstname,
        "lastname": data.lastname,
        "address": data.address,
        "number": data.number,
        "image_url": data.image_url,
    }


def names():
    app = create_app()
    with app.app_context():
        students = Student.query.order_by(Student.id).all()
        student_names = [""]

        for student in students:
            student_names.append(f"{student.firstname} {student.lastname}")

        return student_names


def append_attendance(id):
    app = create_app()
    with app.app_context():

        filter_present_student = Student.query.get(int(id))
        file_name = datetime.now().strftime("%B %d %Y")
        file_path = os.path.realpath(
            f"application/static/attendance/{file_name}.csv")

        time = datetime.now().strftime("%I:%M:%S %p")
        # time should student time in
        present = datetime.strptime("08:00:00 AM", "%I:%M:%S %p")
        # time out of the student
        time_out = datetime.strptime("06:00:00 PM", "%I:%M:%S %p")
        # student time time_in
        time_in = datetime.strptime(time, "%I:%M:%S %p")

        # date for student status database
        date_now = datetime.now().strftime("%B %d %Y")

        # check if the train faces if exists
        if os.path.exists(os.path.realpath(f"application/static/trainer/images.yml")):
            if present >= time_in:
                files_data = pd.read_csv(file_path)["ID"].values
                # update student status in database
                filter_present_student.status = "Present"
                check_stats_exists = Status.query.filter_by(
                    date=date_now).first()
                if not check_stats_exists:
                    stud_status = Status(
                        firstname=filter_present_student.firstname,
                        lastname=filter_present_student.lastname,
                        position=filter_present_student.position,
                        address=filter_present_student.address,
                        number=filter_present_student.number,
                        status="Present",
                        image_url=filter_present_student.image_url,
                        date=date_now
                    )
                    db.session.add(stud_status)
                    db.session.commit()
                # append data in csv file
                data = {
                    "ID": filter_present_student.id,
                    "Name": f"{filter_present_student.firstname} {filter_present_student.lastname}",
                    "Status": "Present",
                    "Time in": time,
                    "Time Out": "",
                    "Address": filter_present_student.address
                }

                if data["ID"] not in files_data:
                    df = pd.DataFrame(data, index=[0])
                    df.to_csv(file_path, mode="a", header=False, index=False)
            elif time_in > present and time_in < time_out:
                filter_present_student.status = "Late"
                files_data = pd.read_csv(file_path)["ID"].values
                # update student status in database
                check_stats_exists = Status.query.filter_by(
                    date=date_now).first()
                if not check_stats_exists:
                    stud_status = Status(
                        firstname=filter_present_student.firstname,
                        lastname=filter_present_student.lastname,
                        position=filter_present_student.position,
                        address=filter_present_student.address,
                        number=filter_present_student.number,
                        status="Late",
                        image_url=filter_present_student.image_url,
                        date=date_now
                    )
                    db.session.add(stud_status)
                    db.session.commit()
                data = {
                    "ID": filter_present_student.id,
                    "Name": f"{filter_present_student.firstname} {filter_present_student.lastname}",
                    "Status": "Late",
                    "Time in": time,
                    "Time Out": "",
                    "Address": filter_present_student.address
                }

                if data["ID"] not in files_data:
                    df = pd.DataFrame(data, index=[0])
                    df.to_csv(file_path, mode="a", header=False, index=False)

            # time out condition

            if time_in >= time_out:
                files_data = pd.read_csv(file_path)["ID"].values
                if filter_present_student.id in files_data:
                    csv_data = pd.read_csv(file_path)
                    update_timeout = csv_data[csv_data["ID"]
                                              == filter_present_student.id]
                    update_timeout["Time Out"] = time
                    update_timeout.to_csv(file_path, index=False)

                exists = Student.query.filter_by(status=None).all()

                for stud_exists in exists:
                    if stud_exists:
                        stud_exists.status = "Absent"

                    # append data to database
                    check_name_exists = Status.query.filter_by(
                        firstname=stud_exists.firstname).first()
                    if not check_name_exists:
                        stud_status = Status(
                            firstname=stud_exists.firstname,
                            lastname=stud_exists.lastname,
                            position=stud_exists.position,
                            address=stud_exists.address,
                            number=stud_exists.number,
                            status="Absent",
                            image_url=stud_exists.image_url,
                            date=date_now,
                        )
                        db.session.add(stud_status)
                    db.session.commit()
            db.session.commit()


def absents():
    app = create_app()
    with app.app_context():
        time = datetime.now().strftime("%I:%M:%S %p")
        # time out of the student
        time_out = datetime.strptime("06:00:00 PM", "%I:%M:%S %p")
        # student time time_in
        time_in = datetime.strptime(time, "%I:%M:%S %p")
        # date time for all student absent in specific date
        date = datetime.now().strftime("%B %d %Y")

        absent_students = Status.query.filter_by(date=date).all()
        file_name = datetime.now().strftime("%B %d %Y")
        file_path = os.path.realpath(
            f"application/static/absents/{file_name}.csv")
        files_data = pd.read_csv(file_path)["ID"].values

        if time_in > time_out:
            for student in absent_students:
                data = {
                    "ID": student.id,
                    "Name": f"{student.firstname} {student.lastname}",
                    "Status": "Absent",
                    "Time in": "",
                    "Time Out": "",
                    "Address": student.address
                }

                if data["ID"] not in files_data or student.id not in files_data:
                    df = pd.DataFrame(data, index=[0])
                    df.to_csv(file_path, mode="a", header=False, index=False)


def generate_csv():
    path = os.path.realpath("application/static/attendance")
    absent = os.path.realpath("application/static/absents")
    date = datetime.now().strftime("%B %d %Y")
    if not os.path.exists(f"{path}/{date}.csv") and not os.path.exists(f"{absent}/{date}.csv"):
        headers = ["ID", "Name", "Status",
                   "Time In", "Time Out", "Address"]
        df = pd.DataFrame(columns=headers)
        df.to_csv(f"{path}/{date}.csv", index=False)
        df.to_csv(f"{absent}/{date}.csv", index=False)

    return {"message": f"Attendance {date}.csv successfully created"}
