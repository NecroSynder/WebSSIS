
# colleges.py
from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from app.models.models_colleges import Colleges

colleges = Blueprint('colleges', __name__, template_folder='templates')

@colleges.route("/colleges/")
def colleges_page():
    colleges_data = Colleges.get_all()
    print(colleges_data)  # Print data to console
    return render_template("colleges.html", colleges=colleges_data)
    
@colleges.route("/colleges/add", methods=["POST"])
def add_college():
    code = request.form["code"]
    name = request.form["name"]
    existing_college = Colleges.get_by_id(code)
    if existing_college:
        return jsonify(success=False, message="A college with this code already exists.")
    else:
        Colleges.add(code, name)
        return jsonify(success=True)


@colleges.route("/colleges/edit/<code>", methods=["GET", "POST"])
def edit_college(code):
    if request.method == "POST":
        new_code = request.form["code"]
        name = request.form["name"]
        if new_code != code:
            existing_college = Colleges.get_by_id(new_code)
            if existing_college:
                return jsonify(success=False, message="A college with this code already exists.")
        Colleges.update(code, new_code, name)
        return redirect(url_for("colleges.colleges_page"))
    else:
        college_data = Colleges.get_by_id(code)
        return jsonify(code=college_data.code, name=college_data.name)


@colleges.route("/colleges/delete/<code>", methods=["POST"])
def delete_college(code):
    Colleges.delete(code)
    return jsonify(success=True)



