#!/usr/bin/python3
""" This is a flask module"""
from flask import Flask

app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello():
    """ a tipical hello world"""
    return "Hello HBNB!"


if __name__ == "__main__":
    # if main then run
    app.run()
