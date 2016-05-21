var plot_data = 
{
    number      : 0,
    dataSet     : anychart.data.set([]), // x, y1,y2,y3,y4
    visible     : false,
    rate        : 100, // in ms
    time_start  : new Date().getTime()
}

var test = 0;

//call back:
function add_point_graph(code, data)
{
    // console.log("receive data to plot");

    //if (plot_data.visible)

    var current = new Date().getTime();

    var inSeconds = Math.round((current - plot_data.time_start) /100) /10 ;

    if (plot_data.number >= 50)
        plot_data.dataSet.remove(0);
    else
        plot_data.number += 1;

    // console.log(msg.data);

    // plot_data.dataSet.append([String(inSeconds), (data[0]), 
    //                                              (data[1]), 
    //                                              (data[2]),
    //                                              (data[3])]);

    // console.log(plot_data.dataSet);
}

// call back:
function refresh_data_frequency(code, data)
{
    var keys = Object.keys(data[0]).sort();

    for (var element in keys)
    {
        element = keys[element];
        var id = 'graph_data_' + element;
        var value = String(Math.round(data[0][element][1]*10)/10);

        if (document.getElementById(id) == null) // if the line of the tab dosesn't exist
        {  
            $('#Graph_data_id').append('<tr><td>\n'+
                                       element + '</td><td><div class="some_random_things" id ="'+ 
                                       id + '">'+
                                       value + ' Hz</div>\n</td></tr>');
        }
        else
        {
            document.getElementById(id).childNodes[0].nodeValue = value + ' Hz';
        }
    }
}

function initAnyChart()
{
    // create line chart
    chart = anychart.line();

    // chart.height(400);

    // turn on chart animation
    chart.animation(true);

    // set plot id for the chart
    chart.container('plot');
    chart.padding([10,20,5,20]);

    // turn on the crosshair
    chart.crosshair().enabled(true).yLabel().enabled(false);
    chart.crosshair().yStroke(null);

    // set tooltip mode to point
    chart.tooltip().positionMode('point');

    // set chart title text settings
    // chart.title('Trend of Sales of the Most Popular Products of ACME Corp.');
    chart.title().padding([0,0,5,0]);
    // set yAxis title

    // chart.yAxis().title('Average Number of Bottles Sold per Hour');
    chart.xAxis().labels().padding([5]);

    // create first series with mapped data
    var series_1 = chart.line(plot_data.dataSet.mapAs({x: [0], value: [1]}));
    series_1.name('Pitch');
    series_1.hoverMarkers().enabled(true).type('circle').size(4);
    series_1.tooltip().position('right').anchor('left').offsetX(5).offsetY(5);

    // create second series with mapped data
    var series_2 = chart.line(plot_data.dataSet.mapAs({x: [0], value: [2]}));
    series_2.name('Roll');
    series_2.hoverMarkers().enabled(true).type('circle').size(4);
    series_2.tooltip().position('right').anchor('left').offsetX(5).offsetY(5);

    // create third series with mapped data
    var series_3 = chart.line(plot_data.dataSet.mapAs({x: [0], value: [3]}));
    series_3.name('Yaw');
    series_3.hoverMarkers().enabled(true).type('circle').size(4);
    series_3.tooltip().position('right').anchor('left').offsetX(5).offsetY(5);

    // create fourth series with mapped data
    var series_4 = chart.line(plot_data.dataSet.mapAs({x: [0], value: [4]}));
    series_4.name('Altitude');
    series_4.hoverMarkers().enabled(true).type('circle').size(4);
    series_4.tooltip().position('right').anchor('left').offsetX(5).offsetY(5);

    // turn the legend on
    chart.legend().enabled(true).fontSize(13).padding([0,0,10,0]);

    // initiate chart drawing
    chart.draw();
}

$(document).ready(function() 
{
	$("#show_plot_btn").click(function()
    {
        // $this will contain a reference to the checkbox   
        if (plot_data.visible) 
        {
            // document.getElementById('plot').style.visibility = 'hidden';
            // document.getElementById('show_plot').name = 'pause';
            document.getElementById("show_plot_btn").childNodes[0].nodeValue = "Play"
            plot_data.visible = false;

            // var msg = {
            //     code : msg_tab['PLOT_RATE'],
            //     data : [-1]                   // order to server : stop sending data
            // };

            // ws.send( JSON.stringify(msg) );
            $.send_data('PLOT_RATE', [-1]);

            console.log('sent stop sending data');
        } 
        else 
        {
            document.getElementById("show_plot_btn").childNodes[0].nodeValue = "Pause"
            plot_data.visible = true;

            $.send_data('PLOT_RATE', [plot_data.rate / 1000.0] );
            console.log('sent start sending data');
        }

        if (plot_data.number >= 5)
            plot_data.dataSet.remove(0);
        else
            plot_data.number += 1;

        plot_data.dataSet.append([String(test), (test), 
                                                (test), 
                                                (test),
                                                (test)]);
        test +=1;

    });
});