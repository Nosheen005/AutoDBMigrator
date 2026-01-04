# sql_generator.py

def quote_identifier(name: str) -> str:
    safe = (name or "").replace('"', '""')
    return f'"{safe}"'


def _to_bool(v, default=False) -> bool:
    if isinstance(v, bool):
        return v
    if v is None:
        return default
    return str(v).strip().lower() in ("true", "1", "yes", "y")


def _build_type(meta: dict) -> str:
    t = str(meta.get("type", "VARCHAR") or "VARCHAR").upper()
    length = str(meta.get("length", "") or "").strip()

    # your UI shows length only for VARCHAR
    if t == "VARCHAR":
        if length:
            return f"VARCHAR({length})"
        return "VARCHAR(255)"
    return t


def generate_sql_from_working_data(working_data: dict) -> str:
    """
    working_data format from your ColumnDetails:
    {
      "Table": {
        "Column": {
          "type": "VARCHAR",
          "length": "255",
          "nullable": "True"/"False",
          "key": "None"/"Primary Key"/"Foreign Key",
          "auto_increment": "True"/"False",
          "references_table": "...",
          "references_column": "...",
          "unique": "True"/"False"
        }
      }
    }
    """
    sql_statements = []

    for table_name, cols in (working_data or {}).items():
        if not cols:
            continue

        col_lines = []

        for col_name, meta in (cols or {}).items():
            meta = meta or {}

            col_id = quote_identifier(col_name)
            key_type = str(meta.get("key", "None") or "None")
            nullable = _to_bool(meta.get("nullable", "False"), default=False)
            unique = _to_bool(meta.get("unique", "False"), default=False)
            auto_inc = _to_bool(meta.get("auto_increment", "False"), default=False)

            col_type = _build_type(meta)

            # Start building column definition
            parts = [col_id, col_type]

            # PRIMARY KEY (SQLite-safe)
            if key_type == "Primary Key":
                if auto_inc:
                    # SQLite requires: INTEGER PRIMARY KEY AUTOINCREMENT
                    parts = [col_id, "INTEGER", "PRIMARY KEY", "AUTOINCREMENT"]
                else:
                    parts.append("PRIMARY KEY")

            # FOREIGN KEY
            elif key_type == "Foreign Key":
                ref_table = str(meta.get("references_table", "") or "").strip()
                ref_col = str(meta.get("references_column", "") or "").strip()
                if ref_table and ref_col:
                    parts.append(
                        f"REFERENCES {quote_identifier(ref_table)}({quote_identifier(ref_col)})"
                    )

            # UNIQUE (don’t add if already primary key)
            if unique and key_type != "Primary Key":
                parts.append("UNIQUE")

            # NOT NULL (skip forcing NOT NULL on PK)
            if (not nullable) and key_type != "Primary Key":
                parts.append("NOT NULL")

            col_lines.append("    " + " ".join(parts))

        statement = (
            f"CREATE TABLE IF NOT EXISTS {quote_identifier(table_name)} (\n"
            + ",\n".join(col_lines)
            + "\n);"
        )
        sql_statements.append(statement)

    return "\n\n".join(sql_statements) + "\n"
