import pandas as pd
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, func
import sqlite3
import pprint
import googlemaps
import gmaps
import json
import warnings
import gmaps.geojson_geometries

# Hide warning messages
from ipywidgets.embed import embed_minimal_html
warnings.filterwarnings('ignore')

import pymysql
pymysql.install_as_MySQLdb()

from flask import Flask, jsonify, render_template, request

#################################################
# Database Setup
#################################################
#engine = create_engine("mysql://root:Batman!99@localhost:3306/stock_db")

# Create our session (link) from Python to the DB
#session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def index_query():
    sqlite_conn = sqlite3.connect('../db/stock.sqlite')
    cursor = sqlite_conn.cursor()
    rows = cursor.execute('SELECT * FROM address_api_table').fetchall()
    return render_template("index.html", rows=rows)
    sqlite_conn.close()
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

@app.route("/api/address_api")
def address_api_query():
    sqlite_conn = sqlite3.connect('../db/stock.sqlite')
    cursor = sqlite_conn.cursor()
    rows = cursor.execute('SELECT * FROM address_api_table').fetchall()
    sqlite_conn.close()
    return json.dumps(rows)

@app.route("/api/company_details")
def company_details_query():
    sqlite_conn = sqlite3.connect('../db/stock.sqlite')
    cursor = sqlite_conn.cursor()
    rows = cursor.execute('SELECT * FROM company_details').fetchall()
    sqlite_conn.close()
    return json.dumps(rows)

@app.route("/api/stock_quarter_close")
def stock_quarter_close_query():
    sqlite_conn = sqlite3.connect('../db/stock.sqlite')
    cursor = sqlite_conn.cursor()
    rows = cursor.execute('SELECT * FROM stock_quarter_close').fetchall()
    sqlite_conn.close()
    return json.dumps(rows)

@app.route("/api/master")
def master_query():
    sqlite_conn = sqlite3.connect('../db/stock.sqlite')
    cursor = sqlite_conn.cursor()
    rows = cursor.execute('SELECT * FROM master').fetchall()
    sqlite_conn.close()
    return json.dumps(rows)





if __name__ == "__main__":
    app.run(debug=True)
