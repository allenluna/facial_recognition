from flask import Blueprint
from .models import Status

view_person = Blueprint("view_person", __name__)


def return_data(status):
    return {
        "name": f"{status.firstname} {status.lastname}",
        "position": status.position,
        "status": status.status,
        "address": status.address,
        "contact": status.number,
        "date": status.date,
    }


@view_person.route("/view_camera", methods=["GET","POST"])
def list_cam():

    list_status = Status.query.all()
    
    return {"results":[return_data(status) for status in list_status]}