
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
        cur.execute("""
            SELECT student.id, student.firstname, student.lastname, 
                course.name, student.year, student.gender,
                college.name, course.college_code, student.profile_pic_url  # Include profile_pic_url in the SELECT clause
            FROM student
            INNER JOIN course ON student.course_code = course.code
            INNER JOIN college ON course.college_code = college.code
        """)
        students = cur.fetchall()
        cur.close()
        return students


    @staticmethod
    def add(id, first_name, last_name, course_code, year_level, gender, profile_pic_url):  # Include profile_pic_url
        cur = mysql.connection.cursor()
        
        # Fetch the college_code associated with the provided course_code
        cur.execute("SELECT college_code FROM course WHERE code=%s", (course_code,))
        college_code = cur.fetchone()[0]  # Assuming college_code is the first column in the result

        # Insert the new student with the fetched college_code and profile picture URL
        cur.execute(
            "INSERT INTO student(id, firstname, lastname, course_code, year, gender, college_code, profile_pic_url) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)",
            (id, first_name, last_name, course_code, year_level, gender, college_code, profile_pic_url),  # Include profile_pic_url
        )
        mysql.connection.commit()
        cur.close()

    @staticmethod
    def update(old_id, new_id, first_name, last_name, course_code, year_level, gender, profile_pic_url):  # Include profile_pic_url
        cur = mysql.connection.cursor()

        # Fetch the college_code associated with the provided course_code
        cur.execute("SELECT college_code FROM course WHERE code=%s", (course_code,))
        college_code = cur.fetchone()[0]  # Assuming college_code is the first column in the result

        # Update the student with the new data and profile picture URL
        cur.execute(
            "UPDATE student SET id=%s, firstName=%s, lastName=%s, course_code=%s, year=%s, gender=%s, college_code=%s, profile_pic_url=%s WHERE id=%s",
            (new_id, first_name, last_name, course_code, year_level, gender, college_code, profile_pic_url, old_id),  # Include profile_pic_url
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
        
    @staticmethod
    def delete_by_college(college_code):
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM student WHERE course_code IN (SELECT code FROM course WHERE college_code=%s)", (college_code,))
        mysql.connection.commit()
        cur.close()
    
    @staticmethod
    def search(term):
        cur = mysql.connection.cursor()
        term = '%' + term.lower() + '%'
        cur.execute(
            """
            SELECT student.id, student.firstname, student.lastname, 
            course.name, student.year, student.gender,
            college.name, course.college_code, student.profile_pic_url  # Include profile_pic_url in the SELECT clause
            FROM student 
            INNER JOIN course ON student.course_code = course.code
            INNER JOIN college ON course.college_code = college.code
            WHERE LOWER(student.id) LIKE %s 
            OR LOWER(student.firstname) LIKE %s 
            OR LOWER(student.lastname) LIKE %s 
            OR LOWER(course.name) LIKE %s 
            OR LOWER(college.name) LIKE %s
            OR LOWER(course.college_code) LIKE %s
            """,
            (term, term, term, term, term, term,),
        )
        data = cur.fetchall()        
        cur.close()
        return data
