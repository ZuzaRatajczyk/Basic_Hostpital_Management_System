import database_connection


def check_if_db_exists():
    """Method to check if 'basic_hms' MySQL database already exists in the server
    :return: True if database exists, False if database not exists"""
    db_server, db_cursor = database_connection.create_db_connection()
    db_cursor.execute("SHOW DATABASES")
    exists = False
    for db in db_cursor:
        if "basic_hms" in db:
            exists = True
    database_connection.close_db_connection(db_server, db_cursor)
    return exists


def create_db():
    db_server, db_cursor = database_connection.create_db_connection()
    create_db_query = "CREATE DATABASE basic_hms"
    db_cursor.execute(create_db_query)
    print("Hospital 'basic_hms' database created.")
    database_connection.close_db_connection(db_server, db_cursor)
