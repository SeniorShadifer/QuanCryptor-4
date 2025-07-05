import sqlite3
from sqlite3 import Connection, Cursor

import server.crypto, server.var
from common import crypto_utils

CONNECT_STR = "database.db"


connection: Connection
cursor: Cursor


def prepare_database():
    global connection, cursor

    connection = sqlite3.connect(CONNECT_STR)
    cursor = connection.cursor()

    cursor.execute(
        """CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY NOT NULL,
            nickname TEXT(50) NOT NULL,
            color TEXT(7) DEFAULT '#FFF',

            server_url TEXT(200),
            server_hash VARCHAR(64),

            password_hash VARCHAR(64),
            password_salt VARCHAR(128),
            iterations INTEGER
        )"""
    )

    cursor.execute(
        """INSERT OR IGNORE INTO users (id, nickname, color) VALUES (0, 'SERVER', '#F0F')"""
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
        """INSERT OR IGNORE INTO chats 
        (id, chat_name, description, salt, checksum_salt, checksum_hash, iterations)
        VALUES
        (0, 
        'Shared server chat', 
        'Chat available to all server users. The key is identical to the server key.',
        ?, ?, ?, ?)
        """,
        (
            server.crypto.salt,
            server.crypto.checksum_salt,
            server.crypto.checksum_hash,
            server.crypto.iterations,
        ),
    )

    cursor.execute(
        """CREATE TABLE IF NOT EXISTS messages (
                   id INTEGER PRIMARY KEY NOT NULL,
                   chat_id INTEGER NOT NULL,
                   sender_id INTEGER NOT NULL,

                   message VARCHAR(50000),
                   timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )"""
    )

    cursor.execute(
        """INSERT OR IGNORE INTO messages (id, chat_id, sender_id, message) 
        VALUES
        (0, 0, 0, ?)
        """,
        (
            server.crypto.fernet.encrypt(
                server.var.configuration["shared_chat_hello_message"].encode()
            ),
        ),
    )

    connection.commit()

    """  print(
        f"TEMP TEST: {cursor.execute("SELECT * FROM messages WHERE chat_id = 0 ORDER BY id DESC LIMIT 3").fetchall()}"
    ) """
