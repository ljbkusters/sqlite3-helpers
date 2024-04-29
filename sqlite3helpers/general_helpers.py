import re

import sqlite3


class InvalidTableName(ValueError):
    pass


def scrub_table_name(table_name: str) -> str:
    if re.match("^[a-zA-Z0-9_]+$", table_name):
        return table_name
    raise InvalidTableName(f"table_name ({table_name}) contained invalid characters."
                           " Make sure the table_name only contains alphanumeric values"
                           " and/or underscores.")


def table_exists(conn: sqlite3.Connection,
                 table_name: str) -> bool:
    curs = conn.cursor()
    with conn:
        curs.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?;",
                     (table_name,))
        return curs.fetchone() is not None
