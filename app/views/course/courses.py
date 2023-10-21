
# courses.py
from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from app.models.models_courses import Courses
from app.models.models_colleges import Colleges


courses = Blueprint('courses', __name__, template_folder='templates')

@courses.route("/courses/")
def courses_page():
    courses_data = Courses.get_all()
    colleges_data = Colleges.get_all()
    return render_template("courses.html", courses=courses_data, colleges=colleges_data)

@courses.route('/courses/add', methods=['POST'])
def add_course():
    # Get form data
    code = request.form.get('code')
    name = request.form.get('name')
    college_code = request.form.get('college_code')
    
    # Check if the course already exists
    existing_course = Courses.get_by_code(code)
    if existing_course:
        return jsonify({'success': False, 'message': 'A course with this code already exists.'})

    # Call the add() method from the Courses model
    try:
        Courses.add(code, name, college_code)
        return jsonify({'success': True})
    except:
        return jsonify({'success': False, 'message': 'Error adding course'})


@courses.route('/courses/delete/<code>', methods=['POST'])
def delete_course(code):
    try:
        # Call the delete() method from the Courses model
        Courses.delete(code)
        return jsonify({'success': True})
    except:
        return jsonify({'success': False, 'message': 'Error deleting course'})

import logging

@courses.route('/courses/edit/<code>', methods=['POST'])
def edit_course(code):
    # Get form data
    new_code = request.form.get('code')
    new_name = request.form.get('name')
    new_college_code = request.form.get('college_code')

    # Check if a different course with the new code already exists
    existing_course = Courses.get_by_code(new_code)
    if existing_course and existing_course.code != code:
        return jsonify({'success': False, 'message': 'A different course with this code already exists.'})

    # Update the course in the database
    try:
        Courses.update(code, new_code, new_name, new_college_code)
        return jsonify({'success': True})
    except Exception as e:
        logging.exception("Exception occurred")
        return jsonify({'success': False, 'message': 'Error updating course'})
