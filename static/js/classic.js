
var e = d3.select("#stock_menu");

// Function to handle input change
function handleChange(event) {
  var pick = document.getElementById("stock_menu");
  var stock = pick.options[pick.selectedIndex].value;
  buildMetadata(stock);
  d3.select("company_info").attr("class","panel-body table table-sm");
  buildCharts(stock);
}

e.on("change", handleChange);

function buildMetadata(ticker) {

  // Build the metadata panel
  const url = "/api/company_detail/" + ticker;
  let tbody = d3.select("#company_info");
  
  tbody.html("");
  tbody.html('<a><img src="static/img/'+ ticker +'.png"></a><br/>');
    d3.json(url).then(function(data) {
      Object.entries(data).forEach(function([key, value]) {
        tbody.append("tr");
        tbody.append("td").text( key + ":  ");
        tbody.append("td").text(value);
      });
    });
}

function buildCharts(ticker) {

    const url = "/api/master12/" + ticker;

    d3.json(url).then(function(data) {
    // Build a Chart
  
    var trace1 = {
        x: data.map(d => d.Date),
        y: data.map(d => d.Close),
        type: 'scatter'
      };
        
      var data1 = [trace1];

    Plotly.newPlot("twelve_months_performance", data1);

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



var doc = new jsPDF()
var creat_pdf = d3.select("#pdf")

creat_pdf.on('click', function() {
  var source = window.document.getElementsByTagName("div")[0];
  doc.text(20, 20, 'Stock information');

  doc.fromHTML(
    source,
    15,
    15
    );
  doc.save("your_stock");
  });
