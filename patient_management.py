from operator import itemgetter
import HMS


def get_patient_data_from_user():
    data_keys = ["name", "surname", "personal_id", "age", "ward", "room_num", "bed_num"]
    data_values = []
    for key in data_keys:
        data_values.append(input(f"Patient {key}: "))   # enter without value will add empty string to dict
    return dict(zip(data_keys, data_values))


def add_patient_to_db(db, db_cursor, patient_data):
    insert_query = "INSERT INTO patients (name, surname, personal_id, age, ward, room_num, bed_num) " \
                   "VALUES (%s, %s, %s, %s, %s, %s, %s)"
    patient_info = itemgetter("name", "surname", "personal_id", "age", "ward", "room_num", "bed_num")(patient_data)  # itemgetter return  dict values as tuple
    db_cursor.execute(insert_query, patient_info)
    db.commit()
    print("Patient registered")


def register_patient():
    db, db_cursor = HMS.create_db_connection()  # db connection per action
    dict_of_user_data = get_patient_data_from_user()
    add_patient_to_db(db, db_cursor, dict_of_user_data)
    HMS.close_db_connection(db, db_cursor)    # db connection per action


def show_patient_data(db_cursor, patient_data_list):
    column_num = 1
    for column_name, patient_data in zip(db_cursor.column_names, patient_data_list):
        print(column_num, end=". ")
        print(*column_name.capitalize().split("_"), end=": ")  # * is used because split is returning list
        print(patient_data)
        column_num += 1


def find_patient():
    db, db_cursor = HMS.create_db_connection()
    try:
        personal_id_val = input("Patients' personal id: ")
        found_patient = HMS.find_item_in_db(db_cursor, "patients", "personal_id", int(personal_id_val))
        show_patient_data(db_cursor, found_patient[0])
    except IndexError:
        print("Patient not found.")
    except ValueError:
        print("Patient not found. Patients' personal id needs to be numeric value.")
    HMS.close_db_connection(db, db_cursor)


def edit_patient():
    db, db_cursor = HMS.create_db_connection()
    personal_id = input("Patients' personal id: ")
    found_patient = HMS.find_item_in_db(db_cursor, "patients", "personal_id", int(personal_id))
    show_patient_data(db_cursor, found_patient[0])
    column_to_edit = input("Choose number of parameter which you want to edit: ")
    name_of_col_to_edit = db_cursor.column_names[int(column_to_edit) - 1]
    new_value = input(f"Provide new value for patients' {name_of_col_to_edit} : ")
    HMS.edit_db_data(db, db_cursor, "patients", name_of_col_to_edit, "personal_id", personal_id, new_value)
    HMS.close_db_connection(db, db_cursor)
