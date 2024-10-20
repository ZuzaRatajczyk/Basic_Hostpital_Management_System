from operator import itemgetter
from datetime import date
from exceptions import InvalidPersonalId
from dateutil.relativedelta import relativedelta
from HmsDatabaseOperations import HmsDatabaseOperations


class PatientManagement:

    def __init__(self, db, db_cursor):
        self.db, self.db_cursor = db, db_cursor
        self.basic_database_operations = HmsDatabaseOperations(self.db, self.db_cursor)

    @staticmethod
    def get_patient_data_from_user():
        data_keys = ["name", "surname", "personal_id", "ward", "main_doctor", "room_num", "bed_num"]
        data_values = []
        for key in data_keys:
            data_values.append(input(f"Patient {key}: "))  # enter without value will add empty string to dict
        return dict(zip(data_keys, data_values))

    def add_patient_to_db(self, patient_data):
        insert_query = "INSERT INTO patients (name, surname, personal_id, ward, main_doctor, room_num, bed_num) " \
                       "VALUES (%s, %s, %s, %s, %s, %s, %s)"
        insert_age = f"UPDATE patients SET age = %s WHERE personal_id = {patient_data['personal_id']}"
        patient_info = itemgetter("name", "surname", "personal_id", "ward", "main_doctor", "room_num", "bed_num")(
            patient_data)  # itemgetter return  dict values as tuple
        age = self.calc_patients_age(patient_data["personal_id"])
        self.db_cursor.execute(insert_query, patient_info)
        self.db_cursor.execute(insert_age, (age,))
        self.db.commit()

    def register_patient(self):
        dict_of_user_data = self.get_patient_data_from_user()
        self.add_patient_to_db(dict_of_user_data)
        print("Patient registered")

    def calc_patients_age(self, personal_id):
        current_date = date.today()
        day_of_birth = int(personal_id[4:6])
        pid_month_of_birth = int(personal_id[2:4])
        try:
            month_of_birth, century = self.calc_month_and_century(pid_month_of_birth)
        except InvalidPersonalId:
            print("Invalid personal id value. Couldn't calculate patients' age.")
        else:
            year_of_birth = century + int(personal_id[0:2])
            date_of_birth = date(year_of_birth, month_of_birth, day_of_birth)
            age = relativedelta(current_date, date_of_birth).years
            return age

    @staticmethod
    def calc_month_and_century(pid_month):
        n_month = 12
        offset_century_map = [(0, 1900), (20, 2000), (40, 2100), (60, 2200), (80, 1800)]
        for (off, cent) in offset_century_map:
            if off < pid_month <= off + n_month:
                return pid_month - off, cent
        raise InvalidPersonalId

    def show_patient_data(self, patient_data_list):
        column_num = 1
        for column_name, patient_data in zip(self.db_cursor.column_names, patient_data_list):
            print(column_num, end=". ")
            print(*column_name.capitalize().split("_"), end=": ")  # * is used because split is returning list
            print(patient_data)
            column_num += 1

    def find_patient(self):
        try:
            personal_id_val = input("Patients' personal id: ")
            found_patient = self.basic_database_operations.find_item_in_db("patients", "personal_id", int(personal_id_val))
            self.show_patient_data(found_patient[0])
        except IndexError:
            print("Patient not found.")
        except ValueError:
            print("Patient not found. Patients' personal id needs to be numeric value.")

    def edit_patient(self):
        try:
            personal_id = input("Patients' personal id: ")
            found_patient = self.basic_database_operations.find_item_in_db("patients", "personal_id", int(personal_id))
            self.show_patient_data(found_patient[0])
            column_to_edit = input("Choose number of parameter which you want to edit: ")
            name_of_col_to_edit = self.db_cursor.column_names[int(column_to_edit) - 1]
            new_value = input(f"Provide new value for patients' {name_of_col_to_edit} : ")
            self.basic_database_operations.edit_db_data("patients", name_of_col_to_edit, "personal_id", personal_id, new_value)
        except IndexError:
            print("Provided value not found in database.")
        except ValueError:
            print("Provided value not found in database. Try again with numeric value.")