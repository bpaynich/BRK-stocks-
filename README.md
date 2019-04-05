# BRK-stocks

<strong>Summary</strong>

We are analyzing stock data using 30 stocks from Dow Jones.  We want the user to be able to choose a stock and see visualizations about that stock (i.e. rate of change btw open and close, best day of the week/year to trade, top 5 days of the year to trade, changes in volume)

<strong>Current Tasks</strong>

Roman - Put CSVs into database (MySQL)<br/>
Bryan - create flask app skeleton<br/>
Katherine - Take CSV files and experiment with charting (use matplotlib, plotly.js, d3, etc)<br/>


<strong>Links used:</strong>

DOW stocks - https://www.investopedia.com/terms/d/dow-30.asp<br/>
Client side PDF gen - https://github.com/MrRio/jsPDF<br/>
Trading Data - www.worldtradingdata.com<br/>

Things to do:

Scrape lat/long data for list of headquarters
Scrape general information from wikipedia?  or some database for company information
Display All headquarter markers on main page
Display filtered headquarters on company page
Chart Stock Historical Chart price per stock
Chart Stock Price over last 12 months
Chart Historical Stock Volume
Chart Average percentage change over year, but Day of year
SVG showing largest 1 day increase and Day
SVG showing largest 1 day decrease and Day
SVG showing Day of year that stock closes higher during the year and by what percentage
SVG showing Day of year that stock closes lower during the eyar and what percentage
Install PDF.js and create PDF displaying information
