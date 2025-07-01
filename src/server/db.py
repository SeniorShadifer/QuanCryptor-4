import sqlite3
from sqlite3 import Connection, Cursor


connection: Connection
cursor: Cursor


def prepare_database():
    global connection, cursor

    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    cursor.execute(
        """CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY NOT NULL,
            nickname TEXT(50) NOT NULL,

            hash VARCHAR(64) NOT NULL,
            salt VARCHAR(128) NOT NULL
        )"""
    )

    cursor.execute(
        """CREATE TABLE IF NOT EXISTS chats (
                   id INTEGER PRIMARY KEY NOT NULL,

                   chat_name TEXT(50) DEFAULT 'untitled_chat',
                   description TEXT(1000),

                   salt VARCHAR(128) NOT NULL,
                   checksum_salt VARCHAR(128) NOT NULL,
                   checksum_hash VARCHAR(128) NOT NULL,
                   iterations INTEGER NOT NULL DEFAULT 200000
                   )"""
    )

    cursor.execute(
        """CREATE TABLE IF NOT EXISTS messages (
                   id INTEGER PRIMARY KEY NOT NULL,
                   chat_id INTEGER NOT NULL,

                   message TEXT(10000),
                   timestamp DATETIME DEFAULT CURRENT_TIMASTAMP
        )"""
    )

    connection.commit()

    """ print(
        f"TEMP TEST: {cursor.execute("SELECT * FROM messages WHERE chat_id = 0 ORDER BY id DESC LIMIT 3").fetchall()}"
    ) """
