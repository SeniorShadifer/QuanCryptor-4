from flask import Flask

import server.crypto
import server.var


flaskapp = Flask(__name__)


@flaskapp.route("/cert")
def hello_world():
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
