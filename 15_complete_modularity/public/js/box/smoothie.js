
$(document).ready(function() 
{
	smoothie.streamTo(document.getElementById("mycanvas"));
	var width = document.getElementById("BOX_Smoothie plot").offsetWidth;

	document.getElementById("mycanvas").width = width -10;
});

	var smoothie = new SmoothieChart();



	// Data
	var line1 = new TimeSeries();
	// var line2 = new TimeSeries();
	// var line3 = new TimeSeries();
	// var line4 = new TimeSeries();

	smoothie.addTimeSeries(line1, {strokeStyle:'rgb(255, 0,   0)', lineWidth:5});
	// smoothie.addTimeSeries(line2, {strokeStyle:'rgb(0, 	 255, 0)', lineWidth:5});
	// smoothie.addTimeSeries(line3, {strokeStyle:'rgb(0, 	 0,   255)', lineWidth:5});
	// smoothie.addTimeSeries(line4, {strokeStyle:'rgb(0, 	 255, 255)', lineWidth:5});


//call back
function smoothie_set_state(code, data)
{
	// console.log(data[0]);
	if (data[0] < 0)
		smoothie.stop();

	else
		smoothie.start();
}

//call back
function add_point_graph_smoothie(code, data)
{
	var now = new Date().getTime();

	line1.append(now, data[0]);
	// line2.append(now, data[1]);
	// line3.append(now, data[2]);
	// line4.append(now, data[3]);
}

