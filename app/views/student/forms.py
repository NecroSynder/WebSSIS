
# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField, SelectField
import app.models.models_students as models


class StudentForm(FlaskForm):
    id = StringField("ID Number", [validators.DataRequired()])
    firstname = StringField("First Name", [validators.DataRequired()])
    lastname = StringField("Last Name", [validators.DataRequired()])
    coursecode = StringField("Course", [validators.DataRequired()])
    year = StringField("Year", [validators.DataRequired()])
    gender = StringField("Gender", [validators.DataRequired()])
    submit = SubmitField("Submit")