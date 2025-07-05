import sqlite3
import json
import os
from flask import Flask, request, g

import server.const, server.crypto, server.var, server.db
from common import crypto_utils


flaskapp = Flask(server.const.APP_NAME)


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(server.db.CONNECT_STR)

    return g.db


@flaskapp.teardown_appcontext
def close_db(e):
    db = g.pop("db", None)
    if db is not None:
        db.close()


@flaskapp.route("/cert")
def receive_cert():
    return server.var.cert


@flaskapp.route("/salt")
def receive_salt():
    return server.crypto.salt


@flaskapp.route("/iterations")
def receive_iterations():
    return str(server.crypto.iterations)


@flaskapp.route("/checksum")
def receive_checksum():
    return server.crypto.checksum


@flaskapp.route("/register", methods=["POST"])
def register():
    data = json.loads(server.crypto.fernet.decrypt(request.get_data()))
    print(data)

    db = get_db()

    if (
        db.cursor()
        .execute(
            "SELECT EXISTS(SELECT 1 FROM users WHERE nickname = ?)", (data["nickname"],)
        )
        .fetchone()[0]
        == 1
    ):
        raise Exception("Account already exists")

    password_salt = os.urandom(16)
    password_hash = crypto_utils.hash_with_salt(
        data["password"], password_salt, server.crypto.iterations
    )

    db.cursor().execute(
        """
        INSERT INTO users (nickname, password_hash, password_salt, iterations) VALUES (?, ?, ?, ?)
        """,
        (
            data["nickname"],
            password_hash,
            password_salt,
            server.crypto.iterations,
        ),
    )

    db.commit()

    return "true"


@flaskapp.route("/test")
def test():
    return f"{get_db().execute("SELECT * FROM messages").fetchall()}"
