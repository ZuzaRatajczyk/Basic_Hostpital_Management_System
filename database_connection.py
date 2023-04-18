import mysql.connector
from getpass import getpass


def create_db_connection():
    print("Connecting to hospital database server...")
    try:
        hms_db = mysql.connector.connect(
            host="127.0.0.1",
            user=input("Enter username: "),
            password=getpass("Enter password: "),
            database="basic_hms"
        )
    except mysql.connector.Error as e:
        print(e)
    else:
        return hms_db, hms_db.cursor()


def close_db_connection(db, db_cursor):
    db.close()
    db_cursor.close()
