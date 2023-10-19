
# models_colleges.py
from app import mysql
from app.models.models_courses import Courses
from app.models.models_students import Students


class College:
    def __init__(self, code, name):
        self.code = code
        self.name = name

class Colleges:
    def __init__(self, code, name):
        self.code = code
        self.name = name
    
    @staticmethod
    def get_all():
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM college")  
        colleges = cur.fetchall()
        # print(colleges)  # Print data to console
        cur.close()
        return colleges
    
    @staticmethod
    def get_by_id(code):
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM college WHERE code=%s", (code,))
        data = cur.fetchone()
        cur.close()
        if data is not None:
            return College(data[0], data[1])
        else:
            return None
    
    @staticmethod
    def add(code, name):
        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO college(code, name) VALUES(%s, %s)",  # Changed from 'colleges' to 'college'
            (code, name),
        )
        mysql.connection.commit()
        cur.close()

    @staticmethod
    def update(old_code, new_code, name):
        cur = mysql.connection.cursor()
        cur.execute(
            "UPDATE college SET code=%s, name=%s WHERE code=%s",  
            (new_code, name, old_code),
        )
        mysql.connection.commit()
        cur.close()


    @staticmethod
    def delete(code):
        cur = mysql.connection.cursor()
        try:
            # Start transaction
            cur.execute("START TRANSACTION")

            # Delete all students and courses associated with the college
            courses = Courses.get_all()
            for course in courses:
                if course[2] == code:  # Assuming 'college_code' is at position 2
                    Students.delete_by_course(course[0])  # Assuming 'code' is at position 0
                    Courses.delete_by_college(code)

            # Delete the college
            cur.execute("DELETE FROM college WHERE code=%s", (code,))
            
            # Commit transaction
            mysql.connection.commit()

        except Exception as e:
            # Rollback transaction in case of error
            mysql.connection.rollback()
            raise e

        finally:
            cur.close()
    
    # @staticmethod
    # def delete(code):
    #     cur = mysql.connection.cursor()
    #     cur.execute("DELETE FROM college WHERE code=%s", (code,))  # Changed from 'colleges' to 'college'
    #     mysql.connection.commit()
    #     cur.close()


    @staticmethod
    def delete_by_college(college_code):
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM course WHERE college_code=%s", (college_code,))
        mysql.connection.commit()
        cur.close()