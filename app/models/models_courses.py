# models_courses.py
from app import mysql

class Courses:
    @staticmethod
    def get_all():
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM course")  # Changed from 'courses' to 'course'
        courses = cur.fetchall()
        cur.close()
        return courses

    @staticmethod
    def add(id, name, description):
        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO course(id, name, description) VALUES(%s, %s, %s)",
            (id, name, description),
        )
        mysql.connection.commit()
        cur.close()

    @staticmethod
    def update(id, name, description):
        cur = mysql.connection.cursor()
        cur.execute(
            "UPDATE course SET name=%s, description=%s WHERE id=%s",  # Changed from 'courses' to 'course'
            (name, description, id),
        )
        mysql.connection.commit()
        cur.close()

    @staticmethod
    def delete(id):
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM course WHERE id=%s", (id,))  # Changed from 'courses' to 'course'
        mysql.connection.commit()
        cur.close()
