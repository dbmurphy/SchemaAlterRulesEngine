import re


class SchemaChangeRiskEngine:
    def __init__(self):
        self.rules = [
            method_name for method_name in dir(self) if method_name.startswith("rule_")
        ]

    def validate(self, sql_command):
        # Split SQL command into individual statements
        statements = []
        statement = ""
        for line in sql_command.splitlines():
            statement += line.strip()
            if statement.endswith(";"):
                statements.append(statement)
                statement = ""

        # Check each statement against the rules
        for stmt in statements:
            # Only consider CREATE and ALTER TABLE statements
            if not stmt.startswith(("CREATE TABLE", "ALTER TABLE")):
                continue

            # Extract table name and column definitions
            parts = stmt.split()
            column_defs = " ".join(parts[3:]).strip("()")
            columns = [col.strip() for col in column_defs.split(",") if col.strip()]

            # Check for rule violations
            for rule in self.rules:
                method = getattr(self, rule)
                result, message = method(stmt, columns)
                if not result:
                    return False, message

        # All rules passed
        return True, None

    @staticmethod
    def rule_no_rename(stmt, columns):
        if "RENAME COLUMN" in stmt:
            return False, "Renaming columns is not allowed"
        elif "RENAME TABLE" in stmt or "RENAME TO" in stmt:
            return False, "Renaming tables is not allowed"
        else:
            return True, None

    @staticmethod
    def rule_no_primary_key(stmt, columns):
        has_primary_key = "PRIMARY KEY" in stmt
        if not has_primary_key and stmt.startswith("CREATE TABLE"):
            return False, f"Table must have a primary key: {stmt}"
        return True, None

    @staticmethod
    def rule_no_blob_or_text(stmt, columns):
        for col_type in ["BLOB", "TEXT"]:
            if col_type in stmt:
                return False, f"{col_type} columns are not allowed"
        return True, None

    @staticmethod
    def rule_no_triggers(stmt, columns):
        if "TRIGGER" in stmt:
            return False, f"Triggers are not allowed: {stmt}"
        return True, None

    @staticmethod
    def rule_no_foreign_keys(stmt, columns):
        if "FOREIGN KEY" in stmt:
            return False, f"Foreign keys are not allowed: {stmt}"
        return True, None

    # Not usefule yet
    # @staticmethod
    # def rule_no_redundant_indexing(stmt, columns):
    #     if 'INDEX' in stmt and 'KEY' in stmt:
    #         return False, f"Redundant indexing is not allowed: {stmt}"
    #     return True, None

    @staticmethod
    def rule_no_datetime(stmt, columns):
        if "DATETIME" in stmt:
            return False, f"DATETIME data type is not allowed: {stmt}"
        return True, None

    @staticmethod
    def rule_no_enum_or_set(stmt, columns):
        pattern = r"\((.*?)\)"
        matches = re.findall(pattern, stmt)
        if matches:
            column_defs = matches[0]
            column_defs = [col.strip() for col in column_defs.split(",")]
            for col_def in column_defs:
                col_parts = col_def.split()
                col_type = col_parts[1]
                col_type = re.findall(r"^\w+", col_type)[0]
                if "ENUM" in col_type or "SET" in col_type:
                    return False, f"{col_type} data type is not allowed"
        return True, None
