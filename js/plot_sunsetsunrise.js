

// // Color shading 
// var color = d3.scale.linear().domain([1,10]).range(['red', 'blue']);

// var circle1 = svg.append(“circle”)
//     .attr("cx", 50)
//     .attr("cy", 100)
//     .attr("r", 20)
//     .style("fill", color(2));

// var circle2 = svg.append("circle")
//     .attr("cx", 50)
//     .attr("cy", 100)
//     .attr("r", 20)
//     .style"fill", color(9));

var parseDate = d3.time.format("%Y-%m-%d").parse;
var parseHour = d3.time.format("%H:%M").parse;

var margin = {top: 20, right: 30, bottom: 40, left: 100},
width = 960 - margin.left - margin.right,
height = 500 - margin.top - margin.bottom;

var x = d3.time.scale()
    .range([0, width]);
    
var y = d3.time.scale()
    .range([height, 0]);

var xAxis = d3.svg.axis()
    .scale(x)
    .tickFormat(d3.time.format("%b"))
    .orient("bottom");

var yAxis = d3.svg.axis()
    .scale(y)
    .ticks(6)
    .tickSubdivide(2)
    .tickFormat(d3.time.format("%I %p"))
    .orient("left");

var areaDawn = d3.svg.area()
    .x(function(d) { return x(d.Date); })
    .y0(height)
    .y1(function(d) { return y(d.Sunrise); });
    // .y1(function(d) { return y(d.Sunrise); });

var areaDay = d3.svg.area()
    .x(function(d) { return x(d.Date); })
    .y0(function(d) { return y(d.Sunrise); })
    .y1(function(d) { return y(d.Sunset); });

var areaDusk = d3.svg.area()
    .x(function(d) { return x(d.Date); })
    .y1(function(d) { return y(d.Sunset); });

var svg = d3.select("body").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

// d3.csv("scripts/data.csv", function(error, data){
dataJSON = JSON.parse(JSONstr);
    dataJSON.forEach( function(d) {
	d.Date = parseDate(d.Date);
	d.Sunrise = parseHour(d.Sunrise);	
	d.Sunset = parseHour(d.Sunset);
    });

    x.domain(d3.extent(dataJSON, function(d) { return d.Date; }));
    y.domain( [new Date(0,0,1,0), new Date(0,0,1,24)] );

    svg.append("path")
	.datum(dataJSON)
	.attr("class", "areaDawn")
	.attr("d", areaDawn);

    svg.append("path")
	.datum(dataJSON)
	.attr("class", "areaDay")
	.attr("d", areaDay);

    svg.append("path")
	.datum(dataJSON)
	.attr("class", "areaDusk")
	.attr("d", areaDusk);

    svg.append("g")
	.attr("class", "x axis")
	.attr("transform", "translate(0," + height + ")")
	.call(xAxis);

    svg.append("g")
	.attr("class", "y axis")
	.call(yAxis)
	.append("text")
	.attr("transform", "rotate(-90)")
	.attr("y", 6)
	.attr("dy", "-5em")   	// move it one text point
	.style("text-anchor", "end")
	.text("Sunset / Sunrise time");
// });
