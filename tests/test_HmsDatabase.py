import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from unittest.mock import patch, MagicMock
from HmsDatabase import HmsDatabase


class TestHmsDatabase:

    @staticmethod
    @patch("HmsDatabase.PatientManagement")
    @patch("HmsDatabase.HmsDatabase._create_tables_if_not_exists")
    @patch("HmsDatabase.HmsDatabase._db_connection_at_startup")
    def test_init(mocked_connection, mocked_create_tables, mocked_pm):
        mocked_connection.return_value = MagicMock(), MagicMock()
        db_obj = HmsDatabase()
        mocked_connection.assert_called_once()
        mocked_create_tables.assert_called_once()
        mocked_pm.called_once_with(db_obj.db, db_obj.db_cursor)
        assert mocked_pm.return_value == db_obj.patients_management
