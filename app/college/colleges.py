from flask import Blueprint, render_template

colleges = Blueprint('colleges', __name__, template_folder='templates')

@colleges.route("/colleges/")
def colleges_page():
    colleges = [
        {
            "code": "CCS",
            "name": "College of Computer Studies"
        },
        # Add more colleges as needed
    ]
    return render_template("colleges.html", colleges=colleges)

