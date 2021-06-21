#!/usr/bin/python3
from flask import *
import flask

monitor = Flask(__name__)


@monitor.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    monitor.run(port=13337)