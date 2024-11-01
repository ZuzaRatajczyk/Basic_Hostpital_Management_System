# import sys
# import os
# # Get the current script's directory
# current_dir = os.path.dirname(os.path.abspath(__file__))
# # Get the parent directory by going one level up
# parent_dir = os.path.dirname(current_dir)
# # Add the parent directory to sys.path
# sys.path.append(parent_dir)

from unittest.mock import patch
from Basic_Hostpital_Management_System.HmsDatabase import HmsDatabase


class TestHmsDatabase:

    @staticmethod
    @patch("HmsDatabase.PatientManagement")
    @patch("HmsDatabase.HmsDatabase._create_tables_if_not_exists")
    @patch("HmsDatabase.mysql.connector.connect")
    @patch("HmsDatabase.getpass", return_value="123")
    @patch('builtins.input', return_value="user123")
    def test_init(mocked_input, mocked_getpass, mocked_connector, mocked_create_tables, mocked_pm):
        db_obj = HmsDatabase()
        mocked_connector.assert_called_once()
        mocked_create_tables.assert_called_once()
        mocked_input.assert_called_once()
        mocked_getpass.assert_called_once()
        assert mocked_pm.return_value == db_obj.patients_management
