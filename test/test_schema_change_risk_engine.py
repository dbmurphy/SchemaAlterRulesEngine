import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from schema_change_risk_engine.schema_change_risk_engine import SchemaChangeRiskEngine


@pytest.fixture
def engine():
    return SchemaChangeRiskEngine()


@pytest.fixture
def columns():
    return ["id", "name", "age"]


def test_rule_no_rename(engine, columns):
    stmt1 = "ALTER TABLE my_table RENAME TO your_table;"
    stmt2 = "ALTER TABLE my_table RENAME COLUMN old_column TO new_column;"
    stmt3 = "CREATE INDEX my_index ON my_table (column1);"
    stmt4 = "ALTER TABLE my_table RENAME INDEX my_index TO your_index;"
    stmt5 = "SELECT * FROM my_table;"
    success1, error_msg1 = engine.rule_no_rename(stmt1, columns)
    success2, error_msg2 = engine.rule_no_rename(stmt2, columns)
    success3, error_msg3 = engine.rule_no_rename(stmt3, columns)
    success4, error_msg4 = engine.rule_no_rename(stmt4, columns)
    success5, error_msg5 = engine.rule_no_rename(stmt5, columns)
    assert success1 is False
    assert "Renaming tables is not allowed" in error_msg1
    assert success2 is False
    assert "Renaming columns is not allowed" in error_msg2
    assert success3 is True
    assert error_msg3 is None
    assert success4 is True
    assert error_msg4 is None
    assert success5 is True
    assert error_msg5 is None


def test_rule_no_primary_key(engine, columns):
    stmt1 = "CREATE TABLE my_table (id INT);"
    stmt2 = "CREATE TABLE my_table (id INT PRIMARY KEY);"
    stmt3 = "CREATE TABLE my_table (id INT, PRIMARY KEY (id));"
    success1, error_msg1 = engine.rule_no_primary_key(stmt1, columns)
    success2, error_msg2 = engine.rule_no_primary_key(stmt2, columns)
    success3, error_msg3 = engine.rule_no_primary_key(stmt3, columns)
    assert success1 is False
    assert "Table must have a primary key" in error_msg1
    assert success2 is True
    assert error_msg2 is None
    assert success3 is True
    assert error_msg3 is None


def test_rule_no_datetime(engine, columns):
    stmt1 = "CREATE TABLE my_table (id INT, created_at DATETIME);"
    stmt2 = "CREATE TABLE my_table (id INT, created_at TIMESTAMP);"
    success1, error_msg1 = engine.rule_no_datetime(stmt1, columns)
    success2, error_msg2 = engine.rule_no_datetime(stmt2, columns)
    assert success1 is False
    assert "DATETIME data type is not allowed" in error_msg1
    assert success2 is True
    assert error_msg2 is None


def test_rule_no_foreign_keys(engine, columns):
    stmt1 = "ALTER TABLE my_table ADD CONSTRAINT fk FOREIGN KEY (column1) REFERENCES other_table(id);"
    stmt2 = "ALTER TABLE my_table ADD COLUMN column1 INT;"
    success1, error_msg1 = engine.rule_no_foreign_keys(stmt1, columns)
    success2, error_msg2 = engine.rule_no_foreign_keys(stmt2, columns)
    assert success1 is False
    assert "Foreign keys are not allowed" in error_msg1
    assert success2 is True
    assert error_msg2 is None


def test_rule_no_triggers(engine, columns):
    stmt1 = "CREATE TRIGGER my_trigger AFTER INSERT ON my_table FOR EACH ROW BEGIN END;"
    stmt2 = "CREATE TABLE my_table (id INT);"
    success1, error_msg1 = engine.rule_no_triggers(stmt1, columns)
    success2, error_msg2 = engine.rule_no_triggers(stmt2, columns)
    assert success1 is False
    assert "Triggers are not allowed" in error_msg1
    assert success2 is True
    assert error_msg2 is None


# Not implemented yet
# def test_rule_no_redundant_indexing(engine, columns):
#     stmt1 = "CREATE INDEX my_index ON my_table (column1);"
#     stmt2 = "CREATE UNIQUE INDEX my_index ON my_table (column1);"
#     stmt3 = "ALTER TABLE my_table ADD INDEX my_index (column1);"
#     success1, error_msg1 = engine.rule_no_redundant_indexing(stmt1, columns)
#     success2, error_msg2 = engine.rule_no_redundant_indexing(stmt2, columns)
#     success3, error_msg3 = engine.rule_no_redundant_indexing(stmt3, columns)
#     assert success1 is True
#     assert error_msg1 is None
#     assert success2 is True
#     assert error_msg2 is None
#     assert success3 is False
#     assert "Redundant indexing is not allowed" in error_msg3


def test_rule_no_blob_or_text(engine, columns):
    stmt1 = "CREATE TABLE my_table (id INT, data BLOB);"
    stmt2 = "CREATE TABLE my_table (id INT, data TEXT);"
    stmt3 = "CREATE TABLE my_table (id INT, data VARCHAR(255));"
    success1, error_msg1 = engine.rule_no_blob_or_text(stmt1, columns)
    success2, error_msg2 = engine.rule_no_blob_or_text(stmt2, columns)
    success3, error_msg3 = engine.rule_no_blob_or_text(stmt3, columns)
    assert success1 is False
    assert "BLOB columns are not allowed" in error_msg1
    assert success2 is False
    assert "TEXT columns are not allowed" in error_msg2
    assert success3 is True
    assert error_msg3 is None


def test_rule_no_enum_or_set(engine, columns):
    stmt1 = "CREATE TABLE my_table (id INT, options ENUM('A', 'B', 'C'));"
    stmt2 = "CREATE TABLE my_table (id INT, options SET('A', 'B', 'C'));"
    stmt3 = "CREATE TABLE my_table (id INT, options VARCHAR(255));"
    success1, error_msg1 = engine.rule_no_enum_or_set(stmt1, columns)
    success2, error_msg2 = engine.rule_no_enum_or_set(stmt2, columns)
    success3, error_msg3 = engine.rule_no_enum_or_set(stmt3, columns)
    assert success1 is False
    assert "ENUM data type is not allowed" in error_msg1
    assert success2 is False
    assert "SET data type is not allowed" in error_msg2
    assert success3 is True
    assert error_msg3 is None
