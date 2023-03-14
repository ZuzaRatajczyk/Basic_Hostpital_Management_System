import mysql.connector
from getpass import getpass
from operator import itemgetter


def create_db_connection():
    print("Creating conntection to hospital database...")
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


def get_patient_data():
    data_keys = ["name", "surname", "age", "ward", "room_num", "bed_num"]
    data_values = []
    for key in data_keys:
        data_values.append(input(f"Patient {key}: "))   # enter without value will add empty string to dict
    return dict(zip(data_keys, data_values))


def add_patient_to_db(db, db_cursor, patient_data):
    insert_query = "INSERT INTO patients (name, surname, age, ward, room_num, bed_num) " \
                   "VALUES (%s, %s, %s, %s, %s, %s)"
    patient_info = itemgetter("name", "surname", "age", "ward", "room_num", "bed_num")(patient_data)
    db_cursor.execute(insert_query, patient_info)
    db.commit()
    print("Patient registered")


def register_patient():
    db, db_cursor = create_db_connection()  # db connection per action
    dict_of_user_data = get_patient_data()
    add_patient_to_db(db, db_cursor, dict_of_user_data)


def close_db_connection(db, db_cursor):
    db.close()
    db_cursor.close()


def choose_action():
    print("Choose number of action:"
          "1. Register patient")
    user_action = input()
    if user_action == "1":
        register_patient()


def main():
    choose_action()


if __name__ == "__main__":
    main()
