import database_connection
import database_management
import exceptions
import patient_management


def find_item_in_db(db_cursor, table, column_name, value):
    select_query = f"SELECT * FROM {table} WHERE {column_name} = %s"
    item_params = (value,)
    db_cursor.execute(select_query, item_params)
    item = db_cursor.fetchall()    # fetchall returns list of tuples
    return item


def edit_db_data(db, db_cursor, table, column_to_edit, where_column, where_val, new_val):
    update_query = f"UPDATE {table} SET {column_to_edit} = %s WHERE {where_column} = %s"
    item_params = (new_val, where_val)
    db_cursor.execute(update_query, item_params)
    db.commit()


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
                patient_management.register_patient()
                module_status = check_module_status(module_name)
            if user_action == 2:
                patient_management.find_patient()
                module_status = check_module_status(module_name)
            if user_action == 3:
                patient_management.edit_patient()
                module_status = check_module_status(module_name)


def main():
    db_connection = database_connection.create_db_connection()
    if not db_connection:
        print("Hospital database doesn't exist. Creating 'basic_hms' database...")
        database_management.create_db()
    database_management.create_tables_if_not_exists()
    app_status = "running"
    while app_status == "running":
        choose_action()
        app_status = check_app_status()


if __name__ == "__main__":
    main()
