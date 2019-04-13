
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

d3.json(url, function(response) {
  // console.log(response);
  // Create a new marker cluster group
  var markers = L.markerClusterGroup();
  
  // Loop through data
  for (var i = 0; i < response.length; i++) {
    var location = response[i].location;

    // Set the data location property to a variable
    var lat = response.map(d => d.Latitude)[i];  
    var lng = response.map(d => d.Longitude)[i];
    var name = response.map(d => d.Company)[i];
    var city = response.map(d => d.City)[i];
    var state = response.map(d => d.State)[i];
    var address = response.map(d => d.Address)[i];
    console.log(lat,lng,name,city,state,address);
    // Check for location property
   
      // Add a new marker to the cluster group and bind a pop-up
      map.addLayer(L.marker([lat,lng])
        .bindPopup(name + '<br/>' + address + '<br/>' + city + ", " + state)
        );
    

  }
  
});

 