
# course.py
from flask import Blueprint, render_template

courses = Blueprint('courses', __name__, template_folder='templates')


@courses.route("/courses/")
def courses_page():
    courses = [
        {
            "code": "BSCS",
            "name": "Bachelor of Science In Computer Science",
            "college_code": "CSS"
        },
        # Add more courses as needed
    ]
    return render_template("courses.html", courses=courses)

