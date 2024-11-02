import sys
import os
from unittest.mock import patch
from HmsDatabase import HmsDatabase

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)


class TestHmsDatabase:

    @staticmethod
    @patch("HmsDatabase.PatientManagement")
    @patch("HmsDatabase.HmsDatabase._create_tables_if_not_exists")
    @patch("HmsDatabase.mysql.connector.connect")
    @patch("HmsDatabase.getpass")
    @patch("builtins.input")
    def test_init(_, __, ___, mocked_create_tables, mocked_pm):
        db_obj = HmsDatabase()
        mocked_create_tables.assert_called_once()
        assert mocked_pm.return_value == db_obj.patients_management
