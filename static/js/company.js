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

    let tbody = d3.select("#company_table");

    tbody.html("");
    
    d3.json(url).then(function(data) {
      console.log(data)
      Object.entries(data).forEach(function([key, value]) {
        tbody.append("tr");
         tbody.append("td").text(key);
        tbody.append("td").text(value);
      });
    });
}

function buildCharts(sample) {

    const url = "/samples/" + sample;

    d3.json(url).then(function(data) {
      
    // Build a Pie Chart
  
    var trace1 = {
      values: data.sample_values.slice(0, 10),
      labels: data.otu_ids.slice(0, 10),
      //hoverinfo: data.otu_labels.slice(0, 10)
      type: 'pie'
    };

    // data
    var data1 = [trace1];

    
    var layout1 = {
      title: 'Belly Button Bacteria Types',
      showlegend: true,
      height: 400,
      width: 400
    };

    Plotly.newPlot("pie", data1, layout1);

// Bubble Chart using the sample data

    var trace2 = {
      x: data.otu_ids,
      y: data.sample_values,
      mode: 'markers',
      marker: {
        size: data.sample_values,
        color: data.otu_ids,
        text: data.otu_labels
      }
    };
    
    var data1 = [trace2];
    
    var layout = {
      title: 'Belly Button Bacteria',
      showlegend: true,
      height: 600,
      width: 1200
    };
    
    Plotly.newPlot('bubble', data1, layout);
});

}

function init() {
  // Grab a reference to the dropdown select element
  var selector = d3.select("#selDataset");

  // Use the list of sample names to populate the select options
  d3.json("/names").then((sampleNames) => {
    sampleNames.forEach((sample) => {
      selector
        .append("option")
        .text(sample)
        .property("value", sample);
    });

    // Use the first sample from the list to build the initial plots
    const firstSample = sampleNames[0];
    buildCharts(firstSample);
    buildMetadata(firstSample);
  });
}

function optionChanged(newSample) {
  // Fetch new data each time a new sample is selected
  buildCharts(newSample);
  buildMetadata(newSample);
}