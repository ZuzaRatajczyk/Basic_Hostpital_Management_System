import database_connection


def create_db():
    db_server, db_cursor = database_connection.create_server_connection()
    create_db_query = "CREATE DATABASE basic_hms"
    db_cursor.execute(create_db_query)
    print("Hospital 'basic_hms' database created.")
    database_connection.close_db_connection(db_server, db_cursor)


def create_tables_if_not_exists():
    db_server, db_cursor = database_connection.create_db_connection()
    patients_table = "CREATE TABLE IF NOT EXISTS patients " \
                     "(patient_id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), surname VARCHAR(255), age INT, " \
                     "ward VARCHAR(255), room_num INT, bed_num INT, main_doctor VARCHAR(255), personal_id BIGINT)"
    doctors_table = "CREATE TABLE IF NOT EXISTS doctors " \
                    "(doctor_id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), surname VARCHAR(255), ward INT)"
    wards_table = "CREATE TABLE IF NOT EXISTS wards " \
                  "(ward_id INT AUTO_INCREMENT PRIMARY KEY, ward_name VARCHAR(255), head_of_the_ward VARCHAR(255))"
    hospital_rooms = "CREATE TABLE IF NOT EXISTS rooms " \
                     "(room_id INT AUTO_INCREMENT PRIMARY KEY, warn VARCHAR(255), num_of_beds INT)"
    db_cursor.execute(patients_table)
    db_cursor.execute(doctors_table)
    db_cursor.execute(wards_table)
    db_cursor.execute(hospital_rooms)
    db_server.commit()
    database_connection.close_db_connection(db_server, db_cursor)
