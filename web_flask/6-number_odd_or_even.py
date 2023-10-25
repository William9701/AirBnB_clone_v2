#!/usr/bin/python3
""" This is a flask module"""
from flask import Flask, render_template

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


@app.route("/number/<int:n>", strict_slashes=False)
def display_number(n):
    """ returns n only if its an integer"""
    return f"{n} is a number"


@app.route("/number_template/<int:n>", strict_slashes=False)
def display_number_template(n):
    """ renders the html page with the number included"""
    return render_template('5-number.html', n=n)


@app.route("/number_odd_or_even/<int:n>", strict_slashes=False)
def display_number_odd_or_even(n):
    """ renders the html page with either the odd or even clause"""
    return render_template('6-number_odd_or_even.html', n=n)


if __name__ == "__main__":
    # if main then run
    app.run()
