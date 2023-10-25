
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
        try:
            # Start transaction
            cur.execute("START TRANSACTION")

            # Update the college code in the college table
            cur.execute(
                "UPDATE college SET code=%s, name=%s WHERE code=%s",  
                (new_code, name, old_code),
            )

            # Commit transaction
            mysql.connection.commit()

        except Exception as e:
            # Rollback transaction in case of error
            mysql.connection.rollback()
            raise e

        finally:
            cur.close()

    @staticmethod
    def delete(code):
        cur = mysql.connection.cursor()
        try:
            # Start transaction
            cur.execute("START TRANSACTION")

            # Delete all students and courses associated with the college
            Students.delete_by_college(code)
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
    
    @staticmethod
    def search(term):
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM college WHERE code LIKE %s OR name LIKE %s", ('%' + term + '%', '%' + term + '%',))
        data = cur.fetchall()
        cur.close()
        return data
