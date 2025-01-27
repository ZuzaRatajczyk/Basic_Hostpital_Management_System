from HmsDatabase import HmsDatabase
from PatientManagement import PatientManagement
import exceptions


class HmsApp:
    """Class for HMS application."""

    def __init__(self):
        self.is_running = True
        self.is_module_running = False
        self.HmsDb = HmsDatabase()

    def check_app_status(self, **kwargs):
        module_name = kwargs.get("module_name", "HMS")
        while True:  # running while status is not returned
            try:
                status = input(f"Do you want to perform next action in {module_name}? y/n: ")
                if status in ["y", "Y", "Yes", "YES", "yes"]:
                    if module_name == "HMS":
                        self.is_running = True
                        break
                    else:
                        self.is_module_running = True
                        break
                elif status in ["n", "N", "No", "NO", "no"]:
                    if module_name == "HMS":
                        self.is_running = False
                        break
                    else:
                        self.is_module_running = False
                        break
                else:
                    raise exceptions.InvalidInputValue
            except exceptions.InvalidInputValue:
                print("Incorrect value. Please respond with 'yes' or 'no' (or 'y' or 'n')")

    def choose_action(self):
        patient_management = self.HmsDb.patients_management
        doctor_management = self.HmsDb.doctors_management
        application_modules = {1: {patient_management.module_name: {1: "Register patient", 2: "Find patient", 3: "Edit patient"}},
                               2: {doctor_management.module_name: ["Add doctor", "Find doctor", "Edit doctor"]}}
        print("Choose number of module:\n")
        for module_num in application_modules:
            for module_name in application_modules[module_num]:
                print(module_num, module_name, sep=". ")
        user_module_number = int(input())
        for module_num, module in application_modules.items():
            if module_num == user_module_number:
                module_name = [key for key in module.keys()][0]
        self.is_module_running = True
        while self.is_module_running:
            print("Choose number of action:")
            for submodule_num, submodule in application_modules[user_module_number][module_name].items():
                print(submodule_num, submodule, sep=". ")
            user_action = int(input())
            if user_action == 1:
                if module_name == patient_management.module_name:
                    patient_management.register_patient()
                self.check_app_status(module_name=module_name)
            if user_action == 2:
                if module_name == patient_management.module_name:
                    patient_management.find_patient()
                self.check_app_status(module_name=module_name)
            if user_action == 3:
                if module_name == patient_management.module_name:
                    patient_management.edit_patient()
                self.check_app_status(module_name=module_name)



