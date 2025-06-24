from flask import Flask


server = Flask(__name__)


@server.route("/hello_world")
def hello_world():
    return "Hello, world!"
