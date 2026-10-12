from unittest.mock import Mock

from app import db


def test_database_url_connects_without_databricks(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "postgresql://example/db")
    connect = Mock(return_value=Mock())
    monkeypatch.setattr(db.psycopg, "connect", connect)
    workspace = Mock(side_effect=AssertionError("Databricks must not be needed"))
    monkeypatch.setattr(db, "WorkspaceClient", workspace)

    connection = db.connect()

    connect.assert_called_once_with("postgresql://example/db", connect_timeout=30, row_factory=db.dict_row)
    connection.execute.assert_called_once_with("SET TIME ZONE 'UTC'")
