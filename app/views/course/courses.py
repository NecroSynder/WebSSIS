# courses.py
from flask import Blueprint, render_template, request, redirect, url_for
from app.models.models_courses import Courses

courses = Blueprint('courses', __name__, template_folder='templates')

@courses.route("/courses/")
def courses_page():
    courses_data = Courses.get_all()
    return render_template("courses.html", courses=courses_data)

@courses.route("/courses/add", methods=["POST"])
def add_course():
    id = request.form["id"]
    name = request.form["name"]
    description = request.form["description"]

    Courses.add(id, name, description)
    return redirect(url_for("courses.courses_page"))

@courses.route("/courses/edit/<id>", methods=["GET", "POST"])
def edit_course(id):
    if request.method == "POST":
        name = request.form["name"]
        description = request.form["description"]

        Courses.update(id, name, description)
        return redirect(url_for("courses.courses_page"))
    else:
        course_data = Courses.get_by_id(id)
        return render_template("edit_course.html", course=course_data)

@courses.route("/courses/delete/<id>", methods=["POST"])
def delete_course(id):
    Courses.delete(id)
    return redirect(url_for("courses.courses_page"))
