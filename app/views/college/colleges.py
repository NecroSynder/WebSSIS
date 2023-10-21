
# colleges.py
from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from app.models.models_colleges import Colleges

colleges = Blueprint('colleges', __name__, template_folder='templates')

@colleges.route("/colleges/")
def colleges_page():
    colleges_data = Colleges.get_all()
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
        return jsonify(success=True, message="College updated successfully")
    else:
        college_data = Colleges.get_by_id(code)
        return jsonify(code=college_data.code, name=college_data.name)


@colleges.route("/colleges/delete/<code>", methods=["POST"])
def delete_college(code):
    Colleges.delete(code)
    return jsonify(success=True)

@colleges.route("/colleges/search", methods=["GET"])
def search_colleges():
    search_term = request.args.get("search_term", "").strip()
    if not search_term:
        results = Colleges.get_all()  # get all colleges if search_term is empty
    else:
        results = Colleges.search(search_term)  # search colleges if search_term is not empty
    return jsonify(results)
