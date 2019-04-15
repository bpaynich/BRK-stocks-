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

var e = d3.select("#stock_menu");

function handleChange(event) {
  var pick = document.getElementById("stock_menu");
  var stock = pick.options[pick.selectedIndex].value;
  var index = pick.options[pick.selectedIndex].id;
  buildMetadata(stock);
  buildMap(index);
  buildDescription(index);
}

e.on("change", handleChange);

function buildMetadata(ticker) {

  // Build the metadata panel
  const url = "/api/company_detail/" + ticker;
 
  let tbody = d3.select("#company_table");

    tbody.html("");

    d3.json(url).then(function(data) {
      console.log(data);
      tbody.html('<a><img src="static/img/'+ ticker +'.png"></a><br/>');
      Object.entries(data).forEach(function([key, value]) {
        tbody.append("tr");
         tbody.append("td").text(key);
        tbody.append("td").text(value);
      });
    });
  };   

function buildMap(index) { 

  // Store API query variables
  var url2 = "/api/addresses" 
  console.log('im working at this point')
  // Grab the data with d3
  //d3.json(url2, function(response) {  
  d3.json(url2).then(function(response) {
    // Set the data location property to a variable
    console.log('hi you suck')
    var lat = response.map(d => d.Latitude)[index];  
    var lng = response.map(d => d.Longitude)[index];
    var name = response.map(d => d.Company)[index];
    var city = response.map(d => d.City)[index];
    var state = response.map(d => d.State)[index];
    var address = response.map(d => d.Address)[index];


      //     // Creating map object
      // var map = L.map("map", {
      //   center: [39.8283,-98.5795],
      //   zoom: 4
      // }); 


      // Adding tile layer to the map
      L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
        attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
        maxZoom: 18,
        id: "mapbox.streets",
        accessToken: API_KEY
      }).addTo(map);

      // Add a new marker to the cluster group and bind a pop-up
      map.addLayer(L.marker([lat,lng])
        .bindPopup(name + '<br/>' + address + '<br/>' + city + ", " + state)
      );

    // add a marker
    var marker = L.marker([lat, lng],{}).addTo(map);
    // console.log("IS THIS WORKING??")
    // set the view
    map.setView([lat, lng], 12);
  });
};

function buildDescription(index) {

  // Build the metadata panel
  const url = "/api/companies_details"
 
  let body = d3.select("#company_desc");
  body.html("");
    
    d3.json(url).then(function(data) {
      console.log(index)
      body.html('<h3>Company Description</h3>');
      body.append('p').text(data[index].comp_desc)
      // Object.entries(data).forEach(function([key, value]) {
      //   tbody.append("tr");
      //    tbody.append("td").text(key);
      //   tbody.append("td").text(value);
      // });
    });
  };  
  
