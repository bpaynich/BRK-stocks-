// Store API query variables
var name = 'MMM'
var url = "/api/company_detail/" + name;

d3.json(url, function (data) {
console.log(data);
  //function tabulate(data) {
		//var table = d3.select('#company_table').append('table')
		//var	tbody = table.append('tbody');

		// create a row for each object in the data
		var rows = [data];
	d3.select("tbody")
		.selectAll("tr")
	  .data(rows)
	  .enter()
	  .append("tr")
		.html(function(d) {
			return `<td>${d.city}</td>`
		});
		
		// create a cell in each row for each column
		// rows.selectAll('tr')
		//   .data(data)
		//   .enter()
		//   .append('td')
		// 	.text(data['comp_desc']);
		// console.log(data['comp_desc']);

	  //return table;
	//}

	// render the table(s)
	//tabulate(data); // 2 column table

});
