from . import db


class Student(db.Model):
    __tablename__ = "employee"
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String)
    lastname = db.Column(db.String)
    position = db.Column(db.String)
    address = db.Column(db.String)
    number = db.Column(db.String)
    status = db.Column(db.String)
    image_url = db.Column(db.String)
    date = db.Column(db.String)


class Status(db.Model):
    __tablename__ = "employee_status"
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String)
    lastname = db.Column(db.String)
    position = db.Column(db.String)
    address = db.Column(db.String)
    number = db.Column(db.String)
    status = db.Column(db.String)
    image_url = db.Column(db.String)
    date = db.Column(db.String)
