# __init__.py 
from flask import Flask, render_template, Blueprint
from flask_mysqldb import MySQL
from flask_bootstrap import Bootstrap
from config import DB_USERNAME, DB_PASSWORD, DB_NAME, DB_HOST, SECRET_KEY, BOOTSTRAP_SERVE_LOCAL
from flask_wtf.csrf import CSRFProtect
import cloudinary
import cloudinary.uploader
import cloudinary.api
import os

mysql = MySQL()
bootstrap = Bootstrap()

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=SECRET_KEY,
        MYSQL_USER=DB_USERNAME,
        MYSQL_PASSWORD=DB_PASSWORD,
        MYSQL_HOST=DB_HOST,
        MYSQL_DB=DB_NAME,
        #BOOTSTRAP_SERVE_LOCAL=BOOTSTRAP_SERVE_LOCAL
    )

    # Cloudinary configuration
    cloudinary.config( 
        cloud_name = os.getenv('CLOUD_NAME'), 
        api_key = os.getenv('API_KEY'), 
        api_secret = os.getenv('API_SECRET') 
    )

    bootstrap.init_app(app)
    mysql.init_app(app)
    CSRFProtect(app)

    from app.views.student.students import students
    from app.views.course.courses import courses
    from app.views.college.colleges import colleges

    app.register_blueprint(students)
    app.register_blueprint(courses)
    app.register_blueprint(colleges)

    @app.route("/")
    def hello_world():
        return render_template("base.html")

    return app

