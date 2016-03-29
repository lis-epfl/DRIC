// Single plot
var plotDiv = document.getElementById('plotDiv');

var data = [{
	x: [ new Date().getTime() / 1000 ],
	y: [0]
}];

Plotly.plot(plotDiv, data, { title: 'extendTraces on single trace'});

setInterval(function(){
	var t = new Date().getTime() / 1000;

  var update = {
		x: [[ t ]],
		y: [[ Math.sin(2*t) ]]
	};

    Plotly.extendTraces(plotDiv, update, [0], 50);
}, 80);

// -----------------------------------------------------------------------------

// Mutiple plots
var plotDivMulti = document.getElementById('plotDivMulti');

var dataMulti = [
  {
  	x: [ new Date().getTime() / 1000 ],
  	y: [0]
  },
  {
  	x: [ new Date().getTime() / 1000 ],
  	y: [0]
  }];

Plotly.plot(plotDivMulti, dataMulti, { title: 'extendTraces on multiple traces'});

setInterval(function(){
	var t = new Date().getTime() / 1000;

  var update = {
		x: [[ t ],
        [ t ]],
		y: [[ Math.sin(2*t) ],
        [ Math.sin(2*t) + 0.5 ]]
	};

  Plotly.extendTraces(plotDivMulti, update, [0, 1], 50);

}, 80);
