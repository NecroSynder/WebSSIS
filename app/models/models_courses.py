
# models_courses.py
from app import mysql

class Courses:
    
    @staticmethod
    def get_by_code(code):
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM course WHERE code=%s", (code,))
        result = cur.fetchone()
        cur.close()
        if result is None:
            return None
        else:
            # Construct a Course instance from the result
            course = Courses()
            course.code, course.name, course.college_code = result
            return course
    
    @staticmethod
    def get_all():
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM course")
        courses = cur.fetchall()
        cur.close()
        return courses

    @staticmethod
    def add(code, name, college_code):
        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO course(code, name, college_code) VALUES(%s, %s, %s)",
            (code, name, college_code),
        )
        mysql.connection.commit()
        cur.close()


    @staticmethod
    def update(old_code, new_code, name, college_code):
        cur = mysql.connection.cursor()
        cur.execute(
            "UPDATE course SET code=%s, name=%s, college_code=%s WHERE code=%s",
            (new_code, name, college_code, old_code),
        )
        mysql.connection.commit()
        cur.close()

    @staticmethod
    def delete(code):
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM course WHERE code=%s", (code,))
        mysql.connection.commit()
        cur.close()

    @staticmethod
    def delete(code):
        cur = mysql.connection.cursor()
        # Delete any students associated with the course
        cur.execute("DELETE FROM student WHERE course_code=%s", (code,))
        # Delete the course
        cur.execute("DELETE FROM course WHERE code=%s", (code,))
        mysql.connection.commit()
        cur.close()

        
    @staticmethod
    def delete_by_college(college_code):
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM course WHERE college_code=%s", (college_code,))
        mysql.connection.commit()
        cur.close()
        
    @staticmethod
    def search(term):
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM course WHERE code LIKE %s OR name LIKE %s OR college_code LIKE %s", ('%' + term + '%', '%' + term + '%', '%' + term + '%',))
        data = cur.fetchall()
        cur.close()
        return data

