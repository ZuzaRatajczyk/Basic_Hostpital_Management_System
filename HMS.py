import mysql.connector
from getpass import getpass
from operator import itemgetter
import exceptions


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


def get_patient_data_from_user():
    data_keys = ["name", "surname", "personal_id", "age", "ward", "room_num", "bed_num"]
    data_values = []
    for key in data_keys:
        data_values.append(input(f"Patient {key}: "))   # enter without value will add empty string to dict
    return dict(zip(data_keys, data_values))


def add_patient_to_db(db, db_cursor, patient_data):
    insert_query = "INSERT INTO patients (name, surname, personal_id, age, ward, room_num, bed_num) " \
                   "VALUES (%s, %s, %s, %s, %s, %s, %s)"
    patient_info = itemgetter("name", "surname", "personal_id", "age", "ward", "room_num", "bed_num")(patient_data)   # itemgetter return  dict values as tuple
    db_cursor.execute(insert_query, patient_info)
    db.commit()
    print("Patient registered")


def register_patient():
    db, db_cursor = create_db_connection()  # db connection per action
    dict_of_user_data = get_patient_data_from_user()
    add_patient_to_db(db, db_cursor, dict_of_user_data)
    close_db_connection(db, db_cursor)    # db connection per action


def find_item_in_db(db_cursor, table, column_name, value):
    select_query = f"SELECT * FROM {table} WHERE {column_name} = %s"
    item_params = (value,)
    db_cursor.execute(select_query, item_params)
    item = db_cursor.fetchall()    # fetchall returns list of tuples
    return item


def show_patient_data(db_cursor, patient_data_list):
    column_num = 1
    for column_name, patient_data in zip(db_cursor.column_names, patient_data_list):
        print(column_num, end=". ")
        print(*column_name.capitalize().split("_"), end=": ")  # * is used because split is returning list
        print(patient_data)
        column_num += 1


def find_patient():
    db, db_cursor = create_db_connection()
    try:
        personal_id_val = input("Patients' personal id: ")
        found_patient = find_item_in_db(db_cursor, "patients", "personal_id", int(personal_id_val))
        show_patient_data(db_cursor, found_patient[0])
    except IndexError:
        print("Patient not found.")
    except ValueError:
        print("Patient not found. Patients' personal id needs to be numeric value.")
    close_db_connection(db, db_cursor)


def edit_db_data(db, db_cursor, table, column_to_edit, where_column, where_val, new_val):
    update_query = f"UPDATE {table} SET {column_to_edit} = %s WHERE {where_column} = %s"
    item_params = (new_val, where_val)
    db_cursor.execute(update_query, item_params)
    db.commit()


def edit_patient():
    db, db_cursor = create_db_connection()
    personal_id = input("Patients' personal id: ")
    found_patient = find_item_in_db(db_cursor, "patients", "personal_id", int(personal_id))
    show_patient_data(db_cursor, found_patient[0])
    column_to_edit = input("Choose number of parameter which you want to edit: ")
    name_of_col_to_edit = db_cursor.column_names[int(column_to_edit) - 1]
    new_value = input(f"Provide new value for patients' {name_of_col_to_edit} : ")
    edit_db_data(db, db_cursor, "patients", name_of_col_to_edit, "personal_id", personal_id, new_value)
    close_db_connection(db, db_cursor)


def close_db_connection(db, db_cursor):
    db.close()
    db_cursor.close()


def check_app_status():
    while True:  # running while status is not returned
        try:
            status = input("Do you want to perform next action in the HMS system? y/n: ")
            if status in ["y", "Y", "Yes", "YES", "yes"]:
                return "running"
            elif status in ["n", "N", "No", "NO", "no"]:
                return "exit"
            else:
                raise exceptions.InvalidInputValue
        except exceptions.InvalidInputValue:
            print("Incorrect value. Please respond with 'yes' or 'no' (or 'y' or 'n')")


def check_module_status(module_name):
    while True:  # running while status is not returned
        try:
            status = input(f"Do you want to perform next action in {module_name} module? y/n: ")
            if status in ["y", "Y", "Yes", "YES", "yes"]:
                return "continue"
            elif status in ["n", "N", "No", "NO", "no"]:
                return "exit"
            else:
                raise exceptions.InvalidInputValue
        except exceptions.InvalidInputValue:
            print("Incorrect value. Please respond with 'yes' or 'no' (or 'y' or 'n')")


def choose_action():
    application_modules = {1: {"Patient Management": ["Register patient", "Find patient", "Edit patient"]}}
    print("Choose number of module:\n")
    for module_num in application_modules:
        for module_name in application_modules[module_num]:
            print(module_num, module_name, sep=". ")
    module_number = int(input())
    if module_number == 1:
        module_name = "Patient Management"
        module_status = "continue"
        while module_status == "continue":
            print("Choose number of action:")
            for submodule_num, submodule in enumerate(application_modules[module_number][module_name], start=1):
                print(submodule_num, submodule, sep=". ")
            user_action = int(input())
            if user_action == 1:
                register_patient()
                module_status = check_module_status(module_name)
            if user_action == 2:
                find_patient()
                module_status = check_module_status(module_name)
            if user_action == 3:
                edit_patient()
                module_status = check_module_status(module_name)


def main():
    app_status = "running"
    while app_status == "running":
        choose_action()
        app_status = check_app_status()


if __name__ == "__main__":
    main()
