import sqlite3
from flask import Flask, request, g

import server.const, server.crypto, server.var, server.db


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
    return str(server.var.configuration["iterations"])


@flaskapp.route("/checksum")
def receive_checksum():
    return server.crypto.checksum


""" @flaskapp.route("/register", methods=["POST"])
def register():
    data = request """


@flaskapp.route("/test")
def test():
    return f"{get_db().execute("SELECT * FROM messages").fetchall()}"
