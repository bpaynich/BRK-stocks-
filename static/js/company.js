var e = d3.select("#stock_menu");

function handleChange(event) {
  var pick = document.getElementById("stock_menu");
  var stock = pick.options[pick.selectedIndex].value;
  buildMetadata(stock);
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

// Creating map object
var map = L.map("map", {
  center: [39.8283,-98.5795],
  zoom: 4
});


// Adding tile layer to the map
L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
  attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
  maxZoom: 18,
  id: "mapbox.streets",
  accessToken: API_KEY
}).addTo(map);

// Store API query variables
var url = "/api/addresses";

// Grab the data with d3

d3.json(url, function(data) {
  
  // Create a new marker cluster group
  var markers = L.markerClusterGroup();

  // Loop through data
  for (var i = 0; i < response.length; i++) {
    
    // Set the data location property to a variable
    var lat = data.map(d => d.Latitude);
    var lng = data.map(d => d.Longitude);
    var name = data.map(d => d.Company);
    var city = data.map(d => d.City);
    var state = data.map(d => d.State);
    var address = data.map(d => d.Address);
    
    // Check for location property
    if (location) {
      // Add a new marker to the cluster group and bind a pop-up
      markers.addLayer(L.marker([lat,lng])
        .bindPopup(name + '<br/>' + address + '<br/>' + city + ", " + state)
        );
    }

  }
  // Add our marker cluster layer to the map
  map.addLayer(markers);
});