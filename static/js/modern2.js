// function buildTable() {

//   // Build the stock data table
//   const stockUrl = "api/stock_changes";
 
//   let tbody = d3.select("#stock_data");
//   tbody.html("");
    
//     d3.json(stockUrl).then(function(stockData) {
//       console.log(stockData)
//       tbody.append("thead")
//       Object.keys(stockData[0]).forEach(function(key) {
//         //tbody.append("th");
//         tbody.append("th").text(key);
//       });
//       Object.entries(stockData).forEach(function([key, value]) {
//         console.log(key);
//         console.log(value);
//         tbody.append("tr");
//         //tbody.append("td").text(`${key}`);
//         tbody.append("td").text(value["index"]);
//         tbody.append("td").text(value["Stock Name"]);
//         tbody.append("td").text(value["Highest Percent Change"] + "%");
//         tbody.append("td").text(value["Date of Highest Percent Change"]);
//         tbody.append("td").text(value["Lowest Percent Change"] + "%");
//         tbody.append("td").text(value["Date of Lowest Percent Change"]);
//         tbody.append("td").text(value["Highest Average Change for a Specific Date"] + "%");
//         tbody.append("td").text(value["Date of Highest Average Change"]);
//         tbody.append("td").text(value["Lowest Average Change for a Specific Date"] + "%");
//         tbody.append("td").text(value["Date of Lowest Average Change"]);
//       });
//     });
//  };
 
//  buildTable();

const url = "/api/companies_details";

d3.json(url).then(function(data) {
    
      // Build a Chart
    var trace1 = {
      x: data.map(d=>d.market_val),
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
      title:'Market Value (Millions) Vs. Employee Count',
      xaxis: {
        title: {
          text: 'Market Value (Millions)',
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
var trace2 = {
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

var data = [ trace2 ];

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
 title:'Price-Sales Ratio vs. Price-to-Cash Flow Ratio',
 xaxis: {
   title: {
     text: 'Price-Sales Ratio',
     font: {
       family: 'Arial',
       size: 18,
       color: '#000000'
     }
   },
 },
 yaxis: {
   title: {
     text: 'Price-to-Cash Flow Ratio',
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
var trace3 = {
 x: data.map(d=>d.market_val),
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

var data = [ trace3 ];

var layout3 = {
 legend: {
   y: 0.5,
   yref: 'paper',
   font: {
     family: 'Arial, sans-serif',
     size: 20,
     color: 'grey',
   }
 },
 title:'Market Value (Millions) Vs. Total Revenue (Millions)',
 xaxis: {
   title: {
     text: 'Market Value (Millions)',
     font: {
       family: 'Arial',
       size: 18,
       color: '#000000'
     }
   },
 },
 yaxis: {
   title: {
     text: 'Total Revenue (Millions)',
     font: {
       family: 'Arial',
       size: 18,
       color: '#000000'
     }
   }
 }
 
};

Plotly.newPlot('scatter_plot3', data, layout3);

});

// const url = "/api/companies_details";

d3.json(url).then(function(data) {
var trace4 = {
  x: data.map(d=>d.zacks_m_ind_desc),
  y: data.map(d=>d.tot_revenue_f0),
  type: 'bar',
  text: data.map(d=>d.comp_name_2),
  textposition: 'top center',
  textfont: {
    family:  'Raleway, sans-serif'
  },
  marker: { size: 12 }
 };
 var data = [ trace4 ];

 var layout4 = {
  legend: {
    y: 0.5,
    yref: 'paper',
    font: {
      family: 'Arial, sans-serif',
      size: 20,
      color: 'grey',
    }
  },
  title:'Industry Type Vs. Total Revenue (Millions)',
  xaxis: {
    title: {
      text: 'Industry Type',
      font: {
        family: 'Arial',
        size: 18,
        color: '#000000'
      }
    },
  },
  yaxis: {
    title: {
      text: 'Total Revenue (Millions)',
      font: {
        family: 'Arial',
        size: 18,
        color: '#000000'
      }
    }
  }
  
 };
Plotly.newPlot('bar_graph1', data, layout4);
});

d3.json(url).then(function(data) {
  var trace5 = {
    x: data.map(d=>d.state_code),
    y: data.map(d=>d.market_val),
    type: 'bar',
    text: data.map(d=>d.comp_name_2),
    textposition: 'top center',
    textfont: {
      family:  'Raleway, sans-serif'
    },
    marker: { size: 12 }
   };
var data = [ trace5 ];

var layout5 = {
 legend: {
   y: 0.5,
   yref: 'paper',
   font: {
     family: 'Arial, sans-serif',
     size: 20,
     color: 'grey',
   }
 },
 title:'State Vs. Market Value (Millions)',
 xaxis: {
   title: {
     text: 'State',
     font: {
       family: 'Arial',
       size: 18,
       color: '#000000'
     }
   },
 },
 yaxis: {
   title: {
     text: 'Market Value (Millions)',
     font: {
       family: 'Arial',
       size: 18,
       color: '#000000'
     }
   }
 }
 
};
Plotly.newPlot('bar_graph2', data, layout5);
});