import sqlite3
from sqlite3 import Connection, Cursor

import client.path


connection: Connection
cursor: Cursor


def prepare_database():
    global connection, cursor

    connection = sqlite3.connect(
        f"{client.path.user_data_dir}/database.db", check_same_thread=False
    )
    cursor = connection.cursor()

    cursor.execute(
        """CREATE TABLE IF NOT EXISTS servers (
                   address TEXT(1000) NOT NULL PRIMARY KEY,
                   key BYTEA(64)
                   )"""
    )
    connection.commit()
