import pandas as pd
import numpy as np
import sqlite3
import pprint
import googlemaps
import gmaps
import json
import math
import warnings
import gmaps.geojson_geometries
import functions
import stock_data
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

@app.route("/modern30")
def modern30_query():
    return render_template("modern2.html")

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


@app.route("/api/stock_changes")
def stock_changes_query():

    # Connect to the database and create a dataframe
    conn = sqlite3.connect("db/stock.sqlite")
    stock_df = pd.read_sql_query("SELECT Name, Date, Open, Close FROM master", conn)

    split_date = stock_df["Date"].str.split("-", n = 1, expand = True)
    open = stock_df["Open"]
    close = stock_df["Close"]
    percent_change = ((close - open)/open)*100

    # Create a dataframe with additional columns
    ticker_df = pd.DataFrame({
        "Name": stock_df["Name"],
        "Date": stock_df["Date"],
        "Year": split_date[0],
        "Month-Day": split_date[1],
        "Open": stock_df["Open"],
        "Close": stock_df["Close"],
        "Percent Change": percent_change
        })

    # Create a list of ticker names
    unique_tickers = stock_df["Name"].unique()

    # Create empty lists
    name = []
    max_overall = []
    max_overall_date = []
    min_overall = []
    min_overall_date = []
    max_avg = []
    max_avg_date = []
    min_avg = []
    min_avg_date = []

    # For loop over the ticker names
    for x in unique_tickers:
        
        ticker_data = ticker_df.loc[ticker_df['Name'] == x]
        
        name.append(ticker_data['Name'].unique()[0])
        
        # Find the maximum percent change for all dates
        max_change = ticker_data["Percent Change"].max()

        max_overall.append(max_change)
        
        # Find the minimum percent change for all dates
        min_change = ticker_data["Percent Change"].min()
        
        min_overall.append(min_change)
        
        # Find the date of the maximum percent change
        max_change_date = ticker_data.loc[ticker_data["Percent Change"] == max_change]["Date"]
        
        max_overall_date.append(max_change_date.max())
        
        # Find the date of the minimum percent change
        min_change_date = ticker_data.loc[ticker_data["Percent Change"] == min_change]["Date"]
        
        min_overall_date.append(min_change_date.min())
        
        # Find the average daily change for each date
        date_change_avg = ticker_data.groupby(["Month-Day"]).agg(
        {
            "Percent Change":"mean"
        
        })["Percent Change"]
        
        date_change_avg_df = pd.DataFrame({
            "Average Daily Percent Change": date_change_avg
        })
        
        date_change_avg_final = date_change_avg.reset_index(drop=False)
        
        # Find the max average change
        max_avg_change = date_change_avg.max()
        
        max_avg.append(max_avg_change.max())
        
        # Find the month and day for the max average change
        max_average_date = date_change_avg_final.loc[date_change_avg_final["Percent Change"] == max_avg_change]["Month-Day"]
        
        max_avg_date.append(max_average_date.min())
        
        # Find the min average change
        min_avg_change = date_change_avg.min()
        
        min_avg.append(min_avg_change.min())

        # Find the month and day for the max average change
        min_average_date = date_change_avg_final.loc[date_change_avg_final["Percent Change"] == min_avg_change]["Month-Day"]
        
        min_avg_date.append(min_average_date.min())

    # Round
    def round_up(n, decimals=0):
        multiplier = 10 ** decimals
        return math.ceil(n * multiplier) / multiplier
    max_overall = [round_up(n, 1) for n in max_overall]
    min_overall = [round_up(n, 1) for n in min_overall]
    max_avg = [round_up(n, 1) for n in max_avg]
    min_avg = [round_up(n, 1) for n in min_avg]

    # Zip frame together with the appended lists
    stock_results_df = pd.DataFrame(list(zip(name, max_overall, max_overall_date, \
                                            min_overall, min_overall_date, max_avg, \
                                            max_avg_date, min_avg, min_avg_date)))

    # Rename the columns in the dataframe
    stock_results_df  = stock_results_df.rename(columns={stock_results_df.columns[0]: "Stock Name", \
                                                        stock_results_df.columns[1]: "Highest Percent Change", \
                                                        stock_results_df.columns[2]: "Date of Highest Percent Change", \
                                                        stock_results_df.columns[3]: "Lowest Percent Change", \
                                                        stock_results_df.columns[4]: "Date of Lowest Percent Change", \
                                                        stock_results_df.columns[5]: "Highest Average Change for a Specific Date", \
                                                        stock_results_df.columns[6]: "Date of Highest Average Change", \
                                                        stock_results_df.columns[7]: "Lowest Average Change for a Specific Date", \
                                                        stock_results_df.columns[8]: "Date of Lowest Average Change"})

    out = json.loads(stock_results_df.reset_index().to_json(orient='records'))
    return jsonify(out)

@app.route("/API")
def api_query():
    return render_template("api.html")

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
def addresses_api_query():
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

@app.route("/api/address/<ticker_name>")
def address_api_query(ticker_name):
    sqlite_conn = sqlite3.connect('db/stock.sqlite')
    cursor = sqlite_conn.cursor()
    rows = cursor.execute("SELECT a.Company, a.Address, a.City, a.State, a.latitude, a.longitude, b.comp_name_2 FROM address_api_table as a INNER JOIN company_details as b ON a.Company = b.comp_name WHERE ticker = ?", (ticker_name,)).fetchone()
    address = {}
    address_df = []
    address["Company_name"] = rows[0]
    address["Address"] = rows[1]
    address["City"] = rows[2]
    address["State"] = rows[3]
    address["Latitude"] = rows[4]
    address["Longitude"] = rows[5]
    address["Company"] = rows[6]
    address_df.append(address.copy())
    sqlite_conn.close()
    return jsonify(address_df)

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
