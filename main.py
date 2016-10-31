#!flask/bin/python
"""`main` is the top level module for your Flask application."""

# Import the Flask Framework
from flask import Flask, jsonify, abort, request, make_response, url_for
import stock_parser

app = Flask(__name__, static_url_path="")
# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.


@app.route('/get_all_companies', methods=['GET'])
def get_all_companies():
    info = None
    while info is None:
        info = stock_parser.get_all_companies()
    return jsonify(info)


@app.route('/get_company_info/<int:stock_code>', methods=['GET'])
def get_company_info(stock_code):
    info = None
    while info is None:
        print info
        info = stock_parser.get_company_info(stock_code)
    return jsonify(info)


@app.route('/get_company_history/<stock_code>/<start_date>/<end_date>', methods=['GET'])
def get_company_history(stock_code, start_date, end_date):
    start_date = start_date.replace("_",  "/")
    end_date = end_date.replace("_", "/")
    history = None
    while history is None:
        history = stock_parser.get_company_history(stock_code, start_date, end_date)
        print history
    return jsonify(history)


@app.errorhandler(404)
def page_not_found(e):
    return "Sorry, nothing at this URL endpoint.", 404


