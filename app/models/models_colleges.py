
# models_colleges.py
from app import mysql

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
        print(colleges)  # Print data to console
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
        cur.execute("DELETE FROM college WHERE code=%s", (code,))  # Changed from 'colleges' to 'college'
        mysql.connection.commit()
        cur.close()
