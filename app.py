import pandas as pd
import numpy as np
import sqlite3
import pprint
import googlemaps
import gmaps
import json
import warnings
import gmaps.geojson_geometries
import functions    

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
app.config['JSON_SORT_KEYS'] = False

#################################################
# Flask Routes
#################################################

@app.route("/")
def index_query():
    return render_template("index.html")

@app.route("/classic")
def classic_query():
    return render_template("classic.html")

@app.route("/company")
def company_query():
    return render_template("company.html")

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
    return jsonify([member[0] for member in cursor.description], rows)
    #return jsonify(rows)

@app.route("/api/names")
def names_query():
    sqlite_conn = sqlite3.connect('db/stock.sqlite')
    cursor = sqlite_conn.cursor()
    rows = cursor.execute('SELECT comp_name_2, ticker FROM company_details').fetchall()
    names = {}
    names_df = []
    num_rows = len(rows)
    for x in range(num_rows):
        names["Company"] = rows[x][0]
        names["Ticker"] = rows[x][1]
        names_df.append(names.copy())
    sqlite_conn.close()
    return jsonify(names_df)

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

@app.route("/api/company_detail/<ticker_name>")
def company_detail_query(ticker_name):
    sqlite_conn = sqlite3.connect('db/stock.sqlite')
    cursor = sqlite_conn.cursor()
    rows = cursor.execute("SELECT * FROM company_details WHERE ticker = ?", (ticker_name,)).fetchone()
    dict = {}
    dict["Company"] = rows[4]
    dict["Address"] = rows[8]
    dict["City"] = rows[10]
    dict["State"] = rows[11]
    dict["Zip"] = rows[13]
    # dict["phone_nbr"] = rows[14]
    # dict["fax_nbr"] = rows[15]
    dict["Country"] = rows[12]
    dict["Site"] = rows[17]
    dict["Industry"] = rows[21]
    dict["Employees"] = rows[28]
    dict["Market Value"] = rows[29]
    dict["P/E"] = rows[33]
    dict["Outstanding Share"] = rows[49]
    dict["Ticker"] = rows[2]
    # dict["Insider Held"] = rows[79]
    # dict["Insitutional Holding"] = rows[80]
    dict["Exchange"] = rows[5]
    dict["Currency"] = rows[6]
    # dict["comp_desc"] = rows[7]
    sqlite_conn.close()
    return jsonify(dict)

@app.route("/api/stock_quarter_close")
def stock_quarter_close_query():
    sqlite_conn = sqlite3.connect('db/stock.sqlite')
    cursor = sqlite_conn.cursor()
    rows = cursor.execute('SELECT * FROM stock_quarter_close').fetchall()
    quarter = {}
    quarter_df = []
    num_rows = len(rows)
    for x in range(num_rows):
        quarter["Index"] = rows[x][0]
        quarter["Ticker"] = rows[x][7]
        quarter["Date"] = rows[x][1]
        quarter["Open"] = rows[x][2]
        quarter["Close"] = rows[x][3]
        quarter["High"] = rows[x][4]
        quarter["Low"] = rows[x][5]
        quarter["Volume"] = rows[x][6]
        quarter_df.append(quarter.copy())
    sqlite_conn.close()
    return jsonify(quarter_df)

@app.route("/api/master/<ticker_name_master>")
def master_query(ticker_name_master):
    sqlite_conn = sqlite3.connect('db/stock.sqlite')
    cursor = sqlite_conn.cursor()
    rows = cursor.execute("SELECT * FROM master WHERE Name = ?", (ticker_name_master,)).fetchall()
    dates = {}
    df = []
    num_rows = len(rows)
    for x in range(num_rows):
        dates["Index"] = rows[x][0]
        dates["Ticker"] = rows[x][7]
        dates["Date"] = rows[x][1]
        dates["Open"] = rows[x][2]
        dates["Close"] = rows[x][3]
        dates["High"] = rows[x][4]
        dates["Low"] = rows[x][5]
        dates["Volume"] = rows[x][6]
        df.append(dates.copy())
    sqlite_conn.close()
    return jsonify(df)

@app.route("/api/master12/<ticker_name_master12>")
def master12_query(ticker_name_master12):
    sqlite_conn = sqlite3.connect('db/stock.sqlite')
    cursor = sqlite_conn.cursor()
    rows = cursor.execute("SELECT * FROM master WHERE Date like '2018%' AND Name = ?", (ticker_name_master12,)).fetchall()
    dates = {}
    df = []
    num_rows = len(rows)
    for x in range(num_rows):
        dates["Index"] = rows[x][0]
        dates["Ticker"] = rows[x][7]
        dates["Date"] = rows[x][1]
        dates["Open"] = rows[x][2]
        dates["Close"] = rows[x][3]
        dates["High"] = rows[x][4]
        dates["Low"] = rows[x][5]
        dates["Volume"] = rows[x][6]
        df.append(dates.copy())
    sqlite_conn.close()
    return jsonify(df)

if __name__ == "__main__":
    app.run(debug=True)
