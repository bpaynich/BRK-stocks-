from pprint import pformat
import json
import sqlite3

def locations_query():
    sqlite_conn = sqlite3.connect('db/stock.sqlite')
    cursor = sqlite_conn.cursor()
    rows = cursor.execute('SELECT latitude, longitude FROM address_api_table').fetchall()
    sqlite_conn.close()
    return json.dumps(rows)

def address_api_query():
    sqlite_conn = sqlite3.connect('db/stock.sqlite')
    cursor = sqlite_conn.cursor()
    rows = cursor.execute('SELECT * FROM address_api_table').fetchall()
    sqlite_conn.close()

def companies_detail_query():
    sqlite_conn = sqlite3.connect('db/stock.sqlite')
    cursor = sqlite_conn.cursor()
    rows = cursor.execute('SELECT * FROM company_details').fetchall()
    sqlite_conn.close()
    return json.dumps(rows)

def company_details(ticker):
    sqlite_conn = sqlite3.connect('db/stock.sqlite')
    cursor = sqlite_conn.cursor()
    rows = cursor.execute('SELECT * FROM company_details WHERE ticker = ?',(ticker)).fetchall()
    sqlite_conn.close()

    for row in rows:
        return row[0]

    return None

    # return json.dumps(rows)


def stock_quarter_close_query():
    sqlite_conn = sqlite3.connect('db/stock.sqlite')
    cursor = sqlite_conn.cursor()
    rows = cursor.execute('SELECT * FROM stock_quarter_close').fetchall()
    sqlite_conn.close()
    return json.dumps(rows)

def master_query():
    sqlite_conn = sqlite3.connect('db/stock.sqlite')
    cursor = sqlite_conn.cursor()
    rows = cursor.execute('SELECT * FROM master').fetchall()
    sqlite_conn.close()
    return json.dumps(rows)