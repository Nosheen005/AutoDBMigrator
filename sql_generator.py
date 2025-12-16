# sql_generator.py

def quote_identifier(name: str) -> str:
    """
    Safely quote SQL identifiers (table/column names).
    Uses standard SQL double quotes: "MyColumn"
    Escapes any internal double quotes as "".
    """
    safe = name.replace('"', '""')
    return f'"{safe}"'


def generate_create_table_sql(tables_data: dict, default_type: str = "TEXT") -> str:
    """
    Generate SQL CREATE TABLE statements based on tables_data.

    tables_data example:
        {
            "Employees": ["Id", "Name", "Age"],
            "Departments": ["DeptId", "DeptName"]
        }

    All columns use the same default_type (TEXT by default).
    """
    sql_statements = []

    for table_name, columns in tables_data.items():
        # Skip empty tables
        if not columns:
            continue

        table_sql_name = quote_identifier(table_name)

        # Build columns list, each as:    "ColumnName" TEXT
        col_lines = [
            f"    {quote_identifier(col)} {default_type}"
            for col in columns
        ]
        col_block = ",\n".join(col_lines)

        # CREATE TABLE IF NOT EXISTS "TableName" (...)
        statement = f"CREATE TABLE IF NOT EXISTS {table_sql_name} (\n{col_block}\n);"
        sql_statements.append(statement)

    # Final script: all CREATE TABLEs separated by a blank line
    return "\n\n".join(sql_statements) + "\n"
