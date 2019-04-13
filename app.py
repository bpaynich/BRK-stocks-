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
#from newsapi import NewsApiClient    

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

@app.route("/news")
def news_query():
    # # Init
    # newsapi = NewsApiClient(api_key='88414c712b5841f28b13a86369d03b40')
    # # /v2/top-headlines
    # top_headlines = newsapi.get_top_headlines(q='bitcoin',
    #                                         sources='bbc-news,the-verge',
    #                                         category='business',
    #                                         language='en',
    #                                         country='us')
    # # /v2/sources
    # sources = newsapi.get_sources()
    return render_template("news.html")

@app.route("/API")
def api_query():
    return render_template("api.html")

# @app.route("/pdf")
# def pdf_query():
#     return render_template("writepdf.html")

# @app.route("/api/locations")
# def locations_query():
#     sqlite_conn = sqlite3.connect('db/stock.sqlite')
#     cursor = sqlite_conn.cursor()
#     rows = cursor.execute('SELECT latitude, longitude FROM address_api_table').fetchall()
#     sqlite_conn.close()
#     return jsonify([member[0] for member in cursor.description], rows)
#     #return jsonify(rows)

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
    addresses = {}
    addresses_df = []
    num_rows = len(rows)
    for x in range(num_rows):
        addresses["Company_name"] = rows[x][0]
        addresses["Address"] = rows[x][1]
        addresses["City"] = rows[x][2]
        addresses["State"] = rows[x][3]
        addresses["Latitude"] = rows[x][4]
        addresses["Longitude"] = rows[x][5]
        addresses["Company"] = rows[x][6]
        addresses_df.append(addresses.copy())
    sqlite_conn.close()
    return jsonify(addresses_df)

@app.route("/api/companies_details")
def companies_details_query():
    sqlite_conn = sqlite3.connect('db/stock.sqlite')
    cursor = sqlite_conn.cursor()
    rows = cursor.execute('SELECT * FROM company_details').fetchall()
    comp_details = {}
    comp_details_df = []
    num_rows = len(rows)
    for x in range(num_rows):
        comp_details["Index"] = rows[x][0]
        comp_details["m_ticker"] = rows[x][1]
        comp_details["ticker"] = rows[x][2]
        comp_details["comp_name"] = rows[x][3]
        comp_details["comp_name_2"] = rows[x][4]
        comp_details["exchange"] = rows[x][5]
        comp_details["currency_code"] = rows[x][6]
        comp_details["comp_desc"] = rows[x][7]
        comp_details["address_line_1"] = rows[x][8]
        comp_details["address_line_2"] = rows[x][9]
        comp_details["city"] = rows[x][10]
        comp_details["state_code"] = rows[x][11]
        comp_details["country_code"] = rows[x][12]
        comp_details["post_code"] = rows[x][13]
        comp_details["phone_nbr"] = rows[x][14]
        comp_details["fax_nbr"] = rows[x][15]
        comp_details["email"] = rows[x][16]
        comp_details["comp_url"] = rows[x][17]
        comp_details["per_end_month_nbr"] = rows[x][19]
        comp_details["zacks_x_ind_code"] = rows[x][20]
        comp_details["zacks_x_ind_desc"] = rows[x][21]
        comp_details["zacks_x_sector_code"] = rows[x][22]
        comp_details["zacks_x_section_desc"] = rows[x][23]
        comp_details["zacks_m_ind_code"] = rows[x][24]
        comp_details["zacks_m_ind_desc"] = rows[x][25]
        comp_details["emp_cnt"] = rows[x][28]
        comp_details["market_val"] = rows[x][29]
        comp_details["tot_revenue_f0"] = rows[x][30]
        comp_details["net_income_f0"] = rows[x][31]
        comp_details["pe_ratio_f1"] = rows[x][32]
        comp_details["pe_ratio_12m"] = rows[x][33]
        comp_details["peg_ratio"] = rows[x][34]
        comp_details["price_per_sales"] = rows[x][35]
        comp_details["price_book"] = rows[x][36]
        comp_details["price_cash"] = rows[x][37]
        comp_details["roe_q0"] = rows[x][38]
        comp_details["roa_q0"] = rows[x][39]
        comp_details["pre_tax_margin_q0"] = rows[x][40]
        comp_details["net_margin_q0"] = rows[x][41]
        comp_details["zacks_oper_margin"] = rows[x][42]
        comp_details["inv_turnover"] = rows[x][43]
        comp_details["curr_ratio_q0"] = rows[x][44]
        comp_details["quick_ratio_q0"] = rows[x][45]
        comp_details["debt_to_comm_equ"] = rows[x][46]
        comp_details["iad"] = rows[x][47]
        comp_details["div_yield"] = rows[x][48]
        comp_details["shares_out"] = rows[x][49]
        comp_details["avg_vol_20d"] = rows[x][50]
        comp_details["bvps_f0"] = rows[x][51]
        comp_details["deliuted_eps_net_4q"] = rows[x][52]
        comp_details["per_end_date_qr0"] = rows[x][53]
        comp_details["eps_mean_est"] = rows[x][54]
        comp_details["eps_act_qr0"] = rows[x][55]
        comp_details["eps_amt_diff_surp_qr0"] = rows[x][56]
        comp_details["eps_pct_diff_surp_qr0"] = rows[x][57]
        comp_details["per_end_date"] = rows[x][58]
        comp_details["eps_mean_est_fr1"] = rows[x][59]
        comp_details["per_end_date_fr2"] = rows[x][60]
        comp_details["esp_mean_est_fr2"] = rows[x][61]
        comp_details["eps_act_fr0"] = rows[x][62]
        comp_details["rating_cnt_strong_buys"] = rows[x][63]
        comp_details["rating_cnt_buys"] = rows[x][64]
        comp_details["rating_cnt_holds"] = rows[x][65]
        comp_details["rating_cnt_sells"] = rows[x][66]
        comp_details["rating_cnt_strong_sells"] = rows[x][67]
        comp_details["cont_recom_curr"] = rows[x][68]
        comp_details["const_recom_7d_ago"] = rows[x][69]
        comp_details["held_by_insiders_pct"] = rows[x][70]
        comp_details["held_by_instutitions_pct"] = rows[x][71]
        comp_details["free_float"] = rows[x][72]
        comp_details_df.append(comp_details.copy())
    sqlite_conn.close()
    return jsonify(comp_details_df)

@app.route("/api/company_detail/<ticker_name>")
def company_detail_query(ticker_name):
    sqlite_conn = sqlite3.connect('db/stock.sqlite')
    cursor = sqlite_conn.cursor()
    rows = cursor.execute("SELECT * FROM company_details WHERE ticker = ?", (ticker_name,)).fetchone()
    comp_details_one = {}
    comp_details_one_df = []
    num_rows = len(rows)
    for y in range(num_rows):
        comp_details_one["Index"] = rows[y][0]
        comp_details_one["m_ticker"] = rows[y][1]
        comp_details_one["ticker"] = rows[y][2]
        comp_details_one["comp_name"] = rows[y][3]
        comp_details_one["comp_name_2"] = rows[y][4]
        comp_details_one["exchange"] = rows[y][5]
        comp_details_one["currency_code"] = rows[y][6]
        comp_details_one["comp_desc"] = rows[y][7]
        comp_details_one["address_line_1"] = rows[y][8]
        comp_details_one["address_line_2"] = rows[y][9]
        comp_details_one["city"] = rows[y][10]
        comp_details_one["state_code"] = rows[y][11]
        comp_details_one["country_code"] = rows[y][12]
        comp_details_one["post_code"] = rows[y][13]
        comp_details_one["phone_nbr"] = rows[y][14]
        comp_details_one["fax_nbr"] = rows[y][15]
        comp_details_one["email"] = rows[y][16]
        comp_details_one["comp_url"] = rows[y][17]
        comp_details_one["per_end_month_nbr"] = rows[y][19]
        comp_details_one["zacks_x_ind_code"] = rows[y][20]
        comp_details_one["zacks_x_ind_desc"] = rows[y][21]
        comp_details_one["zacks_x_sector_code"] = rows[y][22]
        comp_details_one["zacks_x_section_desc"] = rows[y][23]
        comp_details_one["zacks_m_ind_code"] = rows[y][24]
        comp_details_one["zacks_m_ind_desc"] = rows[y][25]
        comp_details_one["emp_cnt"] = rows[y][28]
        comp_details_one["market_val"] = rows[y][29]
        comp_details_one["tot_revenue_f0"] = rows[y][30]
        comp_details_one["net_income_f0"] = rows[y][31]
        comp_details_one["pe_ratio_f1"] = rows[y][32]
        comp_details_one["pe_ratio_12m"] = rows[y][33]
        comp_details_one["peg_ratio"] = rows[y][34]
        comp_details_one["price_per_sales"] = rows[y][35]
        comp_details_one["price_book"] = rows[y][36]
        comp_details_one["price_cash"] = rows[y][37]
        comp_details_one["roe_q0"] = rows[y][38]
        comp_details_one["roa_q0"] = rows[y][39]
        comp_details_one["pre_tax_margin_q0"] = rows[y][40]
        comp_details_one["net_margin_q0"] = rows[y][41]
        comp_details_one["zacks_oper_margin"] = rows[y][42]
        comp_details_one["inv_turnover"] = rows[y][43]
        comp_details_one["curr_ratio_q0"] = rows[y][44]
        comp_details_one["quick_ratio_q0"] = rows[y][45]
        comp_details_one["debt_to_comm_equ"] = rows[y][46]
        comp_details_one["iad"] = rows[y][47]
        comp_details_one["div_yield"] = rows[y][48]
        comp_details_one["shares_out"] = rows[y][49]
        comp_details_one["avg_vol_20d"] = rows[y][50]
        comp_details_one["bvps_f0"] = rows[y][51]
        comp_details_one["deliuted_eps_net_4q"] = rows[y][52]
        comp_details_one["per_end_date_qr0"] = rows[y][53]
        comp_details_one["eps_mean_est"] = rows[y][54]
        comp_details_one["eps_act_qr0"] = rows[y][55]
        comp_details_one["eps_amt_diff_surp_qr0"] = rows[y][56]
        comp_details_one["eps_pct_diff_surp_qr0"] = rows[y][57]
        comp_details_one["per_end_date"] = rows[y][58]
        comp_details_one["eps_mean_est_fr1"] = rows[y][59]
        comp_details_one["per_end_date_fr2"] = rows[y][60]
        comp_details_one["esp_mean_est_fr2"] = rows[y][61]
        comp_details_one["eps_act_fr0"] = rows[y][62]
        comp_details_one["rating_cnt_strong_buys"] = rows[y][63]
        comp_details_one["rating_cnt_buys"] = rows[y][64]
        comp_details_one["rating_cnt_holds"] = rows[y][65]
        comp_details_one["rating_cnt_sells"] = rows[y][66]
        comp_details_one["rating_cnt_strong_sells"] = rows[y][67]
        comp_details_one["cont_recom_curr"] = rows[y][68]
        comp_details_one["const_recom_7d_ago"] = rows[y][69]
        comp_details_one["held_by_insiders_pct"] = rows[y][70]
        comp_details_one["held_by_instutitions_pct"] = rows[y][71]
        comp_details_one["free_float"] = rows[y][72]
        comp_details_one_df.append(comp_details_one.copy())
    sqlite_conn.close()
    return jsonify(comp_details_df)

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
