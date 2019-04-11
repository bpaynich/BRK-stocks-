import pandas as pd
import numpy as np
import sqlite3
import pprint
import googlemaps
import gmaps
import json
import warnings
import gmaps.geojson_geometries
import data_extract

from flask import Flask, jsonify, render_template, request

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy

# Hide warning messages
from ipywidgets.embed import embed_minimal_html
warnings.filterwarnings('ignore')

#################################################
# Flask Setup
#################################################

app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def index_query():
    sqlite_conn = sqlite3.connect('db/stock.sqlite')
    cursor = sqlite_conn.cursor()
    rows = cursor.execute('SELECT * FROM address_api_table').fetchall()
    sqlite_conn.close()
    return render_template("index.html")

@app.route("/company")
def company_query():
    return render_template("company.html")

@app.route("/classic")
def classic_query():
    return render_template("classic.html")

@app.route("/modern")
def modern_query():
    return render_template("modern.html")

@app.route("/pdf")
def pdf_query():
    return render_template("writepdf.html")

@app.route("/api/locations")
def locations_query():
    sqlite_conn = sqlite3.connect('db/stock.sqlite')
    cursor = sqlite_conn.cursor()
    rows = cursor.execute('SELECT latitude, longitude FROM address_api_table').fetchall()
    sqlite_conn.close()
    #return jsonify([member[0] for member in cursor.description], rows)
    return jsonify(rows)

@app.route("/api/names")
def names_query():
    sqlite_conn = sqlite3.connect('db/stock.sqlite')
    cursor = sqlite_conn.cursor()
    rows = cursor.execute('SELECT comp_name_2, ticker FROM company_details').fetchall()
    sqlite_conn.close()
    #return jsonify([member[0] for member in cursor.description])
    return jsonify(rows)

@app.route("/api/addresses")
def address_api_query():
    sqlite_conn = sqlite3.connect('db/stock.sqlite')
    cursor = sqlite_conn.cursor()
    rows = cursor.execute('SELECT a.Company, a.Address, a.City, a.State, a.latitude, a.longitude, b.comp_name_2 FROM address_api_table as a INNER JOIN company_details as b ON a.Company = b.comp_name').fetchall()
    sqlite_conn.close()
    return jsonify(rows)

@app.route("/api/companies_details")
def companies_details_query():
    sqlite_conn = sqlite3.connect('db/stock.sqlite')
    cursor = sqlite_conn.cursor()
    rows = cursor.execute('SELECT * FROM company_details').fetchall()
    sqlite_conn.close()
    return jsonify(rows)

@app.route("/api/company_detail")
def company_detail_query():
    sqlite_conn = sqlite3.connect('db/stock.sqlite')
    cursor = sqlite_conn.cursor()
    rows = cursor.execute('SELECT * FROM company_details WHERE ticker = "INTC"').fetchall()
    sqlite_conn.close()
    return jsonify(rows)


# @app.route("/api/company_details")
# def company_details_query():
#     ticker = request.args.get('ticker')
#     if not ticker:
#         return "There is no ticker query parameter"
#     return jsonify(data_extract.company_details(ticker))


# @app.route("/api/company_details/<ticker>")
# def sample_metadata(ticker):
    
#     sel = [
#         company_details.ticker,
#         company_details.comp_name_2,
#         company_details.comp_desc,
#         company_details.exchange,
#         company_details.address_line_1,
#         company_details.city,
#         company_details.state_code,
#     ]

#     results = db.session.query(*sel).filter(company_details.ticker == ticker).all()

#     # Create a dictionary entry for each row of metadata information
#     company_details = {}
#     for result in results:
#         company_details["ticker"] = result[2]
#         company_details["comp_name_2"] = result[4]
#         company_details["comp_desc"] = result[7]
#         company_details["exchange"] = result[5]
#         company_details["address_line_1"] = result[8]
#         company_details["city"] = result[10]
#         company_details["state_code"] = result[11]

#     print(company_details)
#     return jsonify(company_details)
























@app.route("/api/stock_quarter_close")
def stock_quarter_close_query():
    sqlite_conn = sqlite3.connect('db/stock.sqlite')
    cursor = sqlite_conn.cursor()
    rows = cursor.execute('SELECT * FROM stock_quarter_close').fetchall()
    sqlite_conn.close()
    return jsonify(rows)

@app.route("/api/master")
def master_query():
    sqlite_conn = sqlite3.connect('db/stock.sqlite')
    cursor = sqlite_conn.cursor()
    rows = cursor.execute('SELECT * FROM master WHERE Name = "AAPL"').fetchall()
    sqlite_conn.close()
    return jsonify(rows)

if __name__ == "__main__":
    app.run(debug=True)
