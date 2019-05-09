const url = "api/companies_details";
var x = '';
var y = '';
var xtext = '';
var ytext = '';

d3.json(url).then(function (data) {
  // Function to build charts
  function buildCharts() {
    if (x && y ) {
    var trace1 = {
      x: data.map(d => d[x]),
      y: data.map(d => d[y]),
      mode: 'markers',
      type: 'bubble',
      text: data.map(d => d.comp_name_2),
      textposition: 'top center',
      textfont: {
        family: 'Raleway, sans-serif'
      },
      marker: { size: 12 }
    };
    var data1 = [trace1];

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
      title: `${xtext} vs ${ytext}`,
      xaxis: {
        title: {
          text: `${xtext}`,
          font: {
            family: 'Arial',
            size: 18,
            color: '#000000'
          }
        },
      },
      yaxis: {
        title: {
          text: `${ytext}`,
          font: {
            family: 'Arial',
            size: 18,
            color: '#000000'
          }
        }
      }

    };

    Plotly.newPlot('adaptive_plot', data1, layout);
    };

  };

  // Function to handle input change
  function handleChange() {
    x = xPick.options[xPick.selectedIndex].value;
    y = yPick.options[yPick.selectedIndex].value;
    xtext = xPick.options[xPick.selectedIndex].text;
    ytext = yPick.options[yPick.selectedIndex].text;
    console.log(x, y);
    // d3.select("adaptive_plot").attr("class","panel-body table table-sm");
    buildCharts();
  };

  var xPick = document.getElementById("stock_parameters_x");
  var yPick = document.getElementById("stock_parameters_y");

  xPick.onchange = handleChange;
  yPick.onchange = handleChange;

  buildCharts();
});