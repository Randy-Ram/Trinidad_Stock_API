#!flask/bin/python

from flask import Flask, jsonify, abort, request, make_response, url_for


def start():
    """
    Create your application. Files outside the app directory can import
    this function and use it to recreate your application -- both
    bootstrap.py and the `tests` directory do this.
    """
    app = Flask(__name__)
    #Do stuff
    return app