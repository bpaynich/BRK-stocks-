function buildTable() {

  // Build the stock data table
  const stockUrl = "api/stock_changes";
 
  let tbody = d3.select("#stock_data");
  tbody.html("");
    
    d3.json(stockUrl).then(function(stockData) {
      console.log(stockData)
      tbody.append("thead")
      Object.keys(stockData[0]).forEach(function(key) {
        //tbody.append("th");
        tbody.append("th").text(key);
      });
      Object.entries(stockData).forEach(function([key, value]) {
        console.log(key);
        console.log(value);
        tbody.append("tr");
        //tbody.append("td").text(`${key}`);
        tbody.append("td").text(value["index"]);
        tbody.append("td").text(value["Stock Name"]);
        tbody.append("td").text(value["Highest Percent Change"]);
        tbody.append("td").text(value["Date of Highest Percent Change"]);
        tbody.append("td").text(value["Lowest Percent Change"]);
        tbody.append("td").text(value["Date of Lowest Percent Change"]);
        tbody.append("td").text(value["Highest Average Change for a Specific Date"]);
        tbody.append("td").text(value["Date of Highest Average Change"]);
        tbody.append("td").text(value["Lowest Average Change for a Specific Date"]);
        tbody.append("td").text(value["Date of Lowest Average Change"]);
        
      });
    });
 };
 
 buildTable();

const url = "/api/companies_details";

d3.json(url).then(function(data) {
    
      // Build a Chart
    var trace1 = {
      x: data.map(d=>d.market_val * 1000),
      y: data.map(d=>d.emp_cnt),
      mode: 'markers',
      type: 'bubble',
      text: data.map(d=>d.comp_name_2),
      textposition: 'top center',
      textfont: {
        family:  'Raleway, sans-serif'
      },
      marker: { size: 12 }
    };
    
    var data = [ trace1 ];
    
    var layout = {
      legend: {
        y: 0.5,
        yref: 'paper',
        font: {
          family: 'Arial, sans-serif',
          size: 20,
          color: 'grey',
        }
      },
      title:'Market Cap Vs. Employee Count',
      xaxis: {
        title: {
          text: 'Market Cap',
          font: {
            family: 'Arial',
            size: 18,
            color: '#000000'
          }
        },
      },
      yaxis: {
        title: {
          text: 'Employee Count',
          font: {
            family: 'Arial',
            size: 18,
            color: '#000000'
          }
        }
      }
      
    };
    
    Plotly.newPlot('scatter_plot1', data, layout);

});




// const url = "/api/companies_details";

d3.json(url).then(function(data) {

 // Build a Chart
var trace1 = {
 x: data.map(d=>d.price_per_sales),
 y: data.map(d=>d.price_cash),
 mode: 'markers',
 type: 'scatter',
 text: data.map(d=>d.comp_name_2),
 textposition: 'top center',
 textfont: {
   family:  'Raleway, sans-serif'
 },
 marker: { size: 12 }
};

var data = [ trace1 ];

var layout2 = {
 legend: {
   y: 0.5,
   yref: 'paper',
   font: {
     family: 'Arial, sans-serif',
     size: 20,
     color: 'grey',
   }
 },
 title:'Sales vs. Cash Ratio',
 xaxis: {
   title: {
     text: 'Sales',
     font: {
       family: 'Arial',
       size: 18,
       color: '#000000'
     }
   },
 },
 yaxis: {
   title: {
     text: 'Cash',
     font: {
       family: 'Arial',
       size: 18,
       color: '#000000'
     }
   }
 }
 
};

Plotly.newPlot('scatter_plot2', data, layout2);

});




// const url = "/api/companies_details";

d3.json(url).then(function(data) {

 // Build a Chart
var trace1 = {
 x: data.map(d=>d.market_val * 1000),
 y: data.map(d=>d.tot_revenue_f0),
 mode: 'markers',
 type: 'bubble',
 text: data.map(d=>d.comp_name_2),
 textposition: 'top center',
 textfont: {
   family:  'Raleway, sans-serif'
 },
 marker: { size: 12 }
};

var data = [ trace1 ];

var layout = {
 legend: {
   y: 0.5,
   yref: 'paper',
   font: {
     family: 'Arial, sans-serif',
     size: 20,
     color: 'grey',
   }
 },
 title:'Market Cap Vs. Total Revenue',
 xaxis: {
   title: {
     text: 'Market Cap',
     font: {
       family: 'Arial',
       size: 18,
       color: '#000000'
     }
   },
 },
 yaxis: {
   title: {
     text: 'Total Revenue',
     font: {
       family: 'Arial',
       size: 18,
       color: '#000000'
     }
   }
 }
 
};

Plotly.newPlot('scatter_plot3', data, layout);

});