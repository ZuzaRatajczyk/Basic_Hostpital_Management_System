import sys
import os

import pytest

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from unittest.mock import patch, MagicMock
from HmsDatabase import HmsDatabase
from exceptions import DbNotExist


class TestHmsDatabase:

    @staticmethod
    @pytest.fixture
    @patch("HmsDatabase.PatientManagement")
    @patch("HmsDatabase.HmsDatabase._create_tables_if_not_exists")
    @patch("HmsDatabase.HmsDatabase._db_connection_at_startup")
    def hms_database_obj(mocked_connection, _, __):
        mocked_connection.return_value = MagicMock(), MagicMock()
        return HmsDatabase()

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

    @patch("HmsDatabase.HmsDatabase._create_db_connection")
    def test_db_connection_at_startup(self, mocked_connection, hms_database_obj):
        mocked_connection.return_value = MagicMock(), MagicMock()
        db, db_cursor = hms_database_obj._db_connection_at_startup()
        assert mocked_connection.called_once()
        assert db, db_cursor == mocked_connection.return_value

    @patch("HmsDatabase.HmsDatabase._create_server_connection", return_value=(MagicMock(), MagicMock()))
    @patch("HmsDatabase.HmsDatabase._create_db")
    def test_db_connection_at_startup_negative(self, mocked_create_db, mocked_connection, hms_database_obj):
        hms_database_obj._create_db_connection = MagicMock(side_effect=DbNotExist())
        hms_database_obj._db_connection_at_startup()
        mocked_connection.assert_called_once()
        mocked_create_db.assert_called_once_with(mocked_connection.return_value[1])

    @patch("HmsDatabase.mysql.connector.connect")
    @patch("HmsDatabase.getpass")
    @patch("builtins.input")
    def test_create_server_connection(self, mocked_connect, mocked_getpass, mocked_input, hms_database_obj):
        hms_database_obj._create_server_connection()
        mocked_connect.assert_called_once()
        mocked_input.assert_called_once()
        mocked_getpass.assert_called_once()
