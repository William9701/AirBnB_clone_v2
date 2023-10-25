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


@app.route("/c/<text>", strict_slashes=False)
def display_c_text(text):
    """ returns c + what ever passed as the 'text' """
    text = text.replace('_', ' ')
    return f"C {text}"


@app.route("/python/<text>", strict_slashes=False)
@app.route("/python/", defaults={"text": "is cool"}, strict_slashes=False)
def display_python_text(text):
    """ returns python + what ever passed as the 'text' """
    text = text.replace('_', ' ')
    return f"Python {text}"


if __name__ == "__main__":
    # if main then run
    app.run()
