
# students.py
from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash
from app.models.models_students import Students
from app.models.models_courses import Courses
import cloudinary
import cloudinary.uploader
import cloudinary.api



students = Blueprint('students', __name__, template_folder='templates')

@students.route("/students/")
def students_page():
    students_data = Students.get_all()
    courses_data = Courses.get_all()  # Fetch the college codes
    return render_template("students.html", students=students_data, courses=courses_data)


@students.route('/add', methods=['POST'])
def add_student():
    # Get form data
    id = request.form.get('id')
    first_name = request.form.get('firstName')
    last_name = request.form.get('lastName')
    course_code = request.form.get('courseCode')
    year_level = request.form.get('yearLevel')
    gender = request.form.get('gender')
    profile_pic_file = request.files.get('profilePic')  # Use get() instead of []

    # Check if the student already exists
    existing_student = Students.get_by_id(id)
    if existing_student:
        return jsonify({'success': False, 'message': 'A student with this ID already exists.'})

    if profile_pic_file and profile_pic_file.filename != '':  # Check if a profile picture was provided
        # Upload the profile picture file to Cloudinary
        upload_response = cloudinary.uploader.upload(profile_pic_file)
        if upload_response is None:
            return jsonify({'success': False, 'message': 'Image upload failed.'})
        profile_pic_url = upload_response['url']
    else:
        # Use the default profile picture from Cloudinary by asset_id
        try:
            # Fetch the default image using its asset_id
            default_image = cloudinary.api.resource_by_asset_id("764f65563c0559414b15d10d6db3dcac")
            profile_pic_url = default_image['url']
        except cloudinary.api.NotFound:
            return jsonify({'success': False, 'message': 'Default profile picture not found.'})
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)})

    # Call the add() method from the Students model
    try:
        Students.add(id, first_name, last_name, course_code, year_level, gender, profile_pic_url)  # Include profile_pic_url
        return jsonify({'success': True, 'profile_pic_url': profile_pic_url})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@students.route('/students/delete/<id>', methods=['POST'])
def delete_student(id):
    # Fetch the student record
    student = Students.get_by_id(id)
    
    # Fetch the default profile picture from Cloudinary
    try:
        default_image = cloudinary.api.resource_by_asset_id("764f65563c0559414b15d10d6db3dcac")
        default_profile_pic_url = default_image['url']
    except cloudinary.api.NotFound:
        return jsonify({'success': False, 'message': 'Default profile picture not found.'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

    if student is None:
        return jsonify({'success': False, 'message': 'No student with this ID exists.'})

    # Extract public_id from the profile_pic_url
    profile_pic_url = student[7]
    if profile_pic_url and profile_pic_url != default_profile_pic_url:  # Check if profile_pic_url exists and is not the default one
        public_id = profile_pic_url.split("/")[-1].split(".")[0]
        
        # Delete the image from Cloudinary
        try:
            cloudinary.uploader.destroy(public_id)
        except Exception as e:
            return jsonify({'success': False, 'message': f"Error deleting image from Cloudinary: {str(e)}"})
            
    # Delete the student from the database
    try:
        Students.delete(id)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': f"Error deleting student from database: {str(e)}"})


@students.route("/students/edit", methods=["POST"])
def edit_student():
    new_id = request.form["id"]
    old_id = request.form["old_id"]
    first_name = request.form["firstName"]
    last_name = request.form["lastName"]
    course_code = request.form["courseCode"]
    year_level = request.form["yearLevel"]
    gender = request.form["gender"]
    profile_pic_file = request.files.get('profilePic')  # Get the new profile picture file

    # Fetch the old student data
    old_student = Students.get_by_id(old_id)
    if old_student is None:
        return jsonify({'success': False, 'message': 'No student with this ID exists.'})

    # Fetch the default profile picture from Cloudinary
    try:
        default_image = cloudinary.api.resource_by_asset_id("764f65563c0559414b15d10d6db3dcac")
        default_profile_pic_url = default_image['url']
    except cloudinary.api.NotFound:
        return jsonify({'success': False, 'message': 'Default profile picture not found.'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

    if profile_pic_file:  # Check if a new profile picture file is provided
        # Extract public_id from the old profile_pic_url
        old_profile_pic_url = old_student[7]
        if old_profile_pic_url and old_profile_pic_url != default_profile_pic_url:  # Check if old_profile_pic_url exists and is not the default one
            old_public_id = old_profile_pic_url.split("/")[-1].split(".")[0]

            # Delete the old image from Cloudinary
            try:
                cloudinary.uploader.destroy(old_public_id)
            except Exception as e:
                return jsonify({'success': False, 'message': f"Error deleting old image from Cloudinary: {str(e)}"})

        # Upload the new profile picture file to Cloudinary
        upload_response = cloudinary.uploader.upload(profile_pic_file)
        if upload_response is None:
            return jsonify({'success': False, 'message': 'New image upload failed.'})
        new_profile_pic_url = upload_response['url']
    else:  # If no new profile picture file is provided, use the old profile_pic_url
        new_profile_pic_url = old_student[7]

    # Update the student data in the database
    if Students.update(old_id, new_id, first_name, last_name, course_code, year_level, gender, new_profile_pic_url):
        return jsonify({'success': True, 'new_profile_pic_url': new_profile_pic_url})
    else:
        return jsonify({'success': False, 'message': 'Error updating student'})
