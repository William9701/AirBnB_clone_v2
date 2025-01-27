#!/usr/bin/python3
""" This is a flask module"""
from flask import Flask

app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello():
    """ returns hello HBNB"""
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def display():
    """ returns HBNB"""
    return "HBNB"


if __name__ == "__main__":
    # if main then run
    app.run()
