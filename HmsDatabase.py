import mysql.connector
from getpass import getpass
from exceptions import DbNotExist, WrongCredentials
from PatientManagement import PatientManagement


class HmsDatabase:
    """Class for HMS database."""

    def __init__(self):
        self.db, self.db_cursor = self._db_connection_at_startup()
        self._create_tables_if_not_exists()
        self.patients_management = PatientManagement(self.db, self.db_cursor)

    def _db_connection_at_startup(self):
        """Method for database connection at application startup. If database does not exists it is created"""
        while True:
            try:
                db, db_cursor = self._create_db_connection()
                return db, db_cursor
            except DbNotExist:
                db_server, server_cursor = self._create_server_connection()
                print("Creating 'basic_hms' database...")
                self._create_db(server_cursor)
                server_cursor.close()
                db_server.close()

    @staticmethod
    def _create_server_connection():
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

    @staticmethod
    def _create_db_connection():
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

    @staticmethod
    def _create_db(server_cursor):
        create_db_query = "CREATE DATABASE basic_hms"
        server_cursor.execute(create_db_query)
        print("Hospital 'basic_hms' database created.")

    def _create_tables_if_not_exists(self):
        patients_table = "CREATE TABLE IF NOT EXISTS patients " \
                         "(patient_id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), surname VARCHAR(255), age INT, " \
                         "ward VARCHAR(255), room_num INT, bed_num INT, main_doctor VARCHAR(255), personal_id BIGINT)"
        doctors_table = "CREATE TABLE IF NOT EXISTS doctors " \
                        "(doctor_id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), surname VARCHAR(255), ward INT)"
        wards_table = "CREATE TABLE IF NOT EXISTS wards " \
                      "(ward_id INT AUTO_INCREMENT PRIMARY KEY, ward_name VARCHAR(255), head_of_the_ward VARCHAR(255))"
        hospital_rooms = "CREATE TABLE IF NOT EXISTS rooms " \
                         "(room_id INT AUTO_INCREMENT PRIMARY KEY, warn VARCHAR(255), num_of_beds INT)"
        self.db_cursor.execute(patients_table)
        self.db_cursor.execute(doctors_table)
        self.db_cursor.execute(wards_table)
        self.db_cursor.execute(hospital_rooms)
        self.db.commit()

    def close_db_connection(self):
        self.db.close()
        self.db_cursor.close()
