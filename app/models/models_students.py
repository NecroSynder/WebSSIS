
# models_students.py
from app import mysql
class Students(object):
    def __init__(
        self,
        id=None,
        firstname=None,
        lastname=None,
        coursecode=None,
        year=None,
        gender=None,
    ):
        self.id = id
        self.firstname = firstname
        self.lastname = lastname
        self.coursecode = coursecode
        self.year = year
        self.gender = gender

    def add(self):
        cursor = mysql.connection.cursor()
        sql = f"INSERT INTO students(id, firstname, lastname, coursecode, year, gender) \
            VALUES('{self.id}', '{self.firstname}', '{self.lastname}', '{self.coursecode}', '{self.year}', '{self.gender}')"
        cursor.execute(sql)
        mysql.connection.commit()

    @classmethod
    def all(cls):
        cursor = mysql.connection.cursor()
        sql = "SELECT * FROM students"
        cursor.execute(sql)
        result = cursor.fetchall()
        return result

    @classmethod
    def delete(cls, student_id):
        try:
            cursor = mysql.connection.cursor()
            sql = "DELETE FROM students WHERE id = %s"
            cursor.execute(sql, (student_id,))
            mysql.connection.commit()
            return True
        except Exception as e:
            print(f"Error deleting student: {e}")
            return False
        finally:
            cursor.close()

    @classmethod
    def update(cls, id, firstname, lastname, coursecode, year, gender):
        cursor = mysql.connection.cursor()
        cursor.execute(
            """
            UPDATE students
            SET firstname = %s,
                lastname = %s,
                coursecode = %s,
                year = %s,
                gender = %s
            WHERE id = %s
            """,
            (firstname, lastname, coursecode, year, gender, id),
        )
        mysql.connection.commit()

    @classmethod
    def search(cls, info):
        print(info)
        cursor = mysql.connection.cursor()
        keywords = info.split()
        conditions = []
        for keyword in keywords:
            conditions.append(
                "(firstname LIKE %s OR lastname LIKE %s)"
            )
        conditions_sql = " OR ".join(conditions)
        conditions_data = [f"%{keyword}%" for keyword in keywords for _ in (0, 1)]
        sql = f"""
            SELECT *
            FROM students
            WHERE id = %s
            OR coursecode = %s
            OR year = %s
            OR gender = %s
            OR ({conditions_sql})
        """
        cursor.execute(sql, [info, info, info, info] + conditions_data)
        result = cursor.fetchall()
        return result