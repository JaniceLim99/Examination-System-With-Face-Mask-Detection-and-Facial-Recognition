import mysql.connector
from mysql.connector import Error
# Global variables
status = None


class DbCheck():
    global status
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='examination_attendance',
                                             user='root',
                                             password='root')
        if connection.is_connected():
            status = True
    except Error as e:
        print("Error while connecting to MySQL", e)
        status = False
