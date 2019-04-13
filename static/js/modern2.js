
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
            color: '#ffffff'
          }
        },
      },
      yaxis: {
        title: {
          text: 'Employee Count',
          font: {
            family: 'Arial',
            size: 18,
            color: '#ffffff'
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
       color: '#ffffff'
     }
   },
 },
 yaxis: {
   title: {
     text: 'Cash',
     font: {
       family: 'Arial',
       size: 18,
       color: '#ffffff'
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
       color: '#ffffff'
     }
   },
 },
 yaxis: {
   title: {
     text: 'Total Revenue',
     font: {
       family: 'Arial',
       size: 18,
       color: '#ffffff'
     }
   }
 }
 
};

Plotly.newPlot('scatter_plot3', data, layout);

});