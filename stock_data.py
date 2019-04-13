def stock_changes_query(stock_results_df):

    #%matplotlib inline
    import matplotlib.pyplot as plt
    import pandas as pd
    import numpy as np
    import requests
    import sqlite3
    import pymysql
    pymysql.install_as_MySQLdb()

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
return(stock_results_df)