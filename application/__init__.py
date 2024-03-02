from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
import urllib
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "dsadsadada sadasdasdas"
    conn = urllib.parse.quote_plus(os.getenv("DATABASE"))
    app.config["SQLALCHEMY_DATABASE_URI"] = "mssql+pyodbc:///?odbc_connect=%s" % conn
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    from .view import view
    from .student import student

    app.register_blueprint(view, url_prefix="/")
    app.register_blueprint(student, url_prefix="/add")

    db.init_app(app)

    with app.app_context():
        db.create_all()

    return app
