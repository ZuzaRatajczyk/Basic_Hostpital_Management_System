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
        if e.errno == 1049:
            print(" Database does not exists in the server")
            return False
    else:
        return hms_db, hms_db.cursor()


def create_server_connection():
    print("Connecting to hospital database server...")
    try:
        mysql_server = mysql.connector.connect(
            host="127.0.0.1",
            user=input("Enter username: "),
            password=getpass("Enter password: "),
        )
    except mysql.connector.Error as e:
        print(e)
    else:
        return mysql_server, mysql_server.cursor()


def close_db_connection(db, db_cursor):
    db.close()
    db_cursor.close()
