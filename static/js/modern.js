
var e = d3.select("#stock_menu");

function handleChange(event) {
  var pick = document.getElementById("stock_menu");
  var stock = pick.options[pick.selectedIndex].value;
  buildMetadata(stock);
  buildCharts(stock);
}

e.on("change", handleChange);


function buildMetadata(ticker) {

  // Build the metadata panel
   const url = "/api/company_detail/" + ticker;
    // const url = "/api/company_detail/INTC";

    let tbody = d3.select("#company_info");

    tbody.html("");
    
    d3.json(url).then(function(data) {
      console.log(data)
      Object.entries(data).forEach(function([key, value]) {
        tbody.append("tr");
         tbody.append("td").text(key + ":  ");
        tbody.append("td").text(value);
      });
    });
}

function buildCharts(ticker) {

    const url = "/api/companies_details/";

    d3.json(url).then(function(data) {
      console.log(data);
    // Build a Chart
  
    var trace1 = {
      x: [1, 2, 3, 4, 5],
      y: [1, 6, 3, 6, 1],
      mode: 'markers+text',
      type: 'scatter',
      name: 'Team A',
      text: ['A-1', 'A-2', 'A-3', 'A-4', 'A-5'],
      textposition: 'top center',
      textfont: {
        family:  'Raleway, sans-serif'
      },
      marker: { size: 12 }
    };
    
    var trace2 = {
      x: [1.5, 2.5, 3.5, 4.5, 5.5],
      y: [4, 1, 7, 1, 4],
      mode: 'markers+text',
      type: 'scatter',
      name: 'Team B',
      text: ['B-a', 'B-b', 'B-c', 'B-d', 'B-e'],
      textfont : {
        family:'Times New Roman'
      },
      textposition: 'bottom center',
      marker: { size: 12 }
    };
    
    var data = [ trace1, trace2 ];
    
    var layout = {
      xaxis: {
        range: [ 0.75, 5.25 ]
      },
      yaxis: {
        range: [0, 8]
      },
      legend: {
        y: 0.5,
        yref: 'paper',
        font: {
          family: 'Arial, sans-serif',
          size: 20,
          color: 'grey',
        }
      },
      title:'Data Labels on the Plot'
    };
    
    Plotly.newPlot('scatter_plot', data, layout);

});

const url2 = "/api/master/" + ticker;

d3.json(url2).then(function(data) {

    // Build a Chart
  
    var trace1 = {
        x: data.map(d => d.Date),
        y: data.map(d => d.Volume),
        type: 'bar'
      };
        
      var data1 = [trace1];

    Plotly.newPlot("stock_volume_chart", data1);

});

const url3 = "/api/master/" + ticker;

d3.json(url3).then(function(data) {
    
    // Build a Chart
  
    var trace1 = {
        x: data.map(d => d.Date),
        y: data.map(d => d.Close),
        type: 'scatter'
      };
        
      var data1 = [trace1];

    Plotly.newPlot("increase_over_time", data1);

});

}
