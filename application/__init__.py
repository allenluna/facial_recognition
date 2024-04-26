from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
import urllib.parse

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "dsadsadada sadasdasdas"
    conn_str = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=DESKTOP-LCBQ72M;DATABASE=facial_recognized;Trusted_Connection=yes;'
    conn_uri = urllib.parse.quote_plus(conn_str)
    app.config["SQLALCHEMY_DATABASE_URI"] = "mssql+pyodbc:///?odbc_connect={}".format(conn_uri)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    from .view import view
    from .student import student
    from .view_person import view_person
    
    app.register_blueprint(view, url_prefix="/")
    app.register_blueprint(view_person, url_prefix="/")
    app.register_blueprint(student, url_prefix="/add")

    db.init_app(app)

    with app.app_context():
        db.create_all()

    return app
