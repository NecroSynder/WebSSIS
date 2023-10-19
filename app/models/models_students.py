

# models_students.py
from app import mysql

class Students:
    @staticmethod
    def get_by_id(id):
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM student WHERE id=%s", (id,))
        student = cur.fetchone()
        cur.close()
        return student

    @staticmethod
    def get_all():
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM student")
        students = cur.fetchall()
        cur.close()
        return students

    @staticmethod
    def add(id, first_name, last_name, course_code, year_level, gender):
        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO student(id, firstname, lastname, course_code, year, gender) VALUES(%s, %s, %s, %s, %s, %s)",
            (id, first_name, last_name, course_code, year_level, gender),
        )
        mysql.connection.commit()
        cur.close()

    @staticmethod
    def update(old_id, new_id, first_name, last_name, course_code, year_level, gender):
        cur = mysql.connection.cursor()
        cur.execute(
            "UPDATE student SET id=%s, firstName=%s, lastName=%s, course_code=%s, year=%s, gender=%s WHERE id=%s",
            (new_id, first_name, last_name, course_code, year_level, gender, old_id),
        )
        affected_rows = cur.rowcount
        mysql.connection.commit()
        cur.close()
        return affected_rows > 0

    @staticmethod
    def delete(id):
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM student WHERE id=%s", (id,))
        mysql.connection.commit()
        cur.close()

    @staticmethod
    def delete_by_course(course_code):
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM student WHERE course_code=%s", (course_code,))
        mysql.connection.commit()
        cur.close()