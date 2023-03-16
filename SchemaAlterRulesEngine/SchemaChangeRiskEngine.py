class SchemaChangeRiskEngine:
    def __init__(self):
        self.rules = [method_name for method_name in dir(self) if method_name.startswith('rule_')]

    def validate(self, sql_command):
        # Split SQL command into individual statements
        statements = []
        statement = ''
        for line in sql_command.splitlines():
            statement += line.strip()
            if statement.endswith(';'):
                statements.append(statement)
                statement = ''

        # Check each statement against the rules
        for stmt in statements:
            # Only consider CREATE and ALTER TABLE statements
            if not stmt.startswith(('CREATE TABLE', 'ALTER TABLE')):
                continue

            # Extract table name and column definitions
            parts = stmt.split()
            table_name = parts[2]
            column_defs = ' '.join(parts[3:]).strip('()')
            columns = [col.strip() for col in column_defs.split(',') if col.strip()]

            # Check for rule violations
            for rule in self.rules:
                method = getattr(self, rule)
                result, message = method(stmt, columns)
                if not result:
                    return False, message

        # All rules passed
        return True, None

    def rule_no_rename(self, stmt, columns):
        if 'RENAME' in stmt:
            return False, f"Renaming of tables or columns is not allowed: {stmt}"
        return True, None

    def rule_no_datatype_change(self, stmt, columns):
        for col in columns:
            col_parts = col.split()
            col_name = col_parts[0]
            col_type = col_parts[1].upper()
            if 'ENUM' in col_type or 'SET' in col_type:
                return False, f"Changing data type from {col_type} is not allowed: {stmt}"
            elif 'VARCHAR' in col_type and 'INT' in col_type:
                return False, f"Changing data type from {col_type} is not allowed: {stmt}"
        return True, None

    def rule_no_primary_key(self, stmt, columns):
        if 'PRIMARY KEY' not in stmt:
            return False, f"Table must have a primary key: {stmt}"
        return True, None

    def rule_no_blob_or_text(self, stmt, columns):
        for col in columns:
            col_parts = col.split()
            col_name = col_parts[0]
            col_type = col_parts[1].upper()
            if 'BLOB' in col_type or 'TEXT' in col_type:
                return False, f"{col_type} columns are not allowed: {stmt}"
        return True, None

    def rule_no_triggers(self, stmt, columns):
        if 'TRIGGER' in stmt:
            return False, f"Triggers are not allowed: {stmt}"
        return True, None

    def rule_no_foreign_keys(self, stmt, columns):
        if 'FOREIGN KEY' in stmt:
            return False, f"Foreign keys are not allowed: {stmt}"
        return True, None

    def rule_no_redundant_indexing(self, stmt, columns):
        if 'INDEX' in stmt and 'KEY' in stmt:
            return False, f"Redundant indexing is not allowed: {stmt}"
        return True, None

    def rule_no_datetime(self, stmt, columns):
        if 'DATETIME' in stmt:
            return False, f"DATETIME data type is not allowed: {stmt}"
        return True, None

    def rule_no_enum_or_set(self, stmt, columns):
        for col in columns:
            col_parts = col.split()
            col_name = col_parts[0]
            col_type = col_parts[1].upper()
            if 'ENUM' in col_type or 'SET' in col_type:
                return False, f"{col_type} data type is not allowed: {stmt}"
        return True, None

    def rule_no_column_removal(self, stmt, columns):
        if 'DROP COLUMN' in stmt:
            parts = stmt.split()
            col_name = parts[parts.index('COLUMN') + 1]
            for col in columns:
                if col.startswith(col_name + ' '):
                    return False, f"Column {col_name} cannot be removed because it is used by an index: {stmt}"
        return True, None
