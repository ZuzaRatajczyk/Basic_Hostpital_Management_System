import mysql.connector
import database_management
from getpass import getpass
from exceptions import DbNotExist, WrongCredentials


def db_connection_at_startup():
    while True:
        try:
            db, db_cursor = create_db_connection()
            database_management.create_tables_if_not_exists(db, db_cursor)
            return db, db_cursor
        except DbNotExist:
            db_server, server_cursor = create_server_connection()
            print("Creating 'basic_hms' database...")
            database_management.create_db(server_cursor)
            close_db_connection(db_server, server_cursor)


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
            print("Database does not exists in the server")
            raise DbNotExist
        if e.errno == 1045:
            print("Wrong credentials.")
            raise WrongCredentials
    else:
        return hms_db, hms_db.cursor()


def create_server_connection():
    print("Connecting to database server...")
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
