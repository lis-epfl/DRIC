var plot_data = 
{
    number      : 0,
    dataSet     : anychart.data.set([]), // x, y1,y2,y3,y4
    visible     : false,
    rate        : 100, // in ms
    time_start  : new Date().getTime(),
    trace       : [ ['ATTITUDE', 'pitch'], 
                    ['ATTITUDE', 'roll'], 
                    ['ATTITUDE', 'yaw'], 
                    ['GLOBAL_POSITION_INT', 'alt'] ],
    trace_num   : 0,
}

var series_1 = 0;
var series_2 = 0;
var series_3 = 0;
var series_4 = 0;

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

// onclick callback
function graph_data_click(object)
{
    id = 'Graph_data_tree_view_id_' + String(object.id).substring(14);
    element = document.getElementById(id);

    if (element.style.display == 'none')
        element.style.display = 'block';
    else
        element.style.display = 'none';
}

function graph_data_treeview_click(object, event_)
{
    // stop event propagation to graph_data_click()
    event_.stopPropagation();

    //get names of msg and msg_type
    msg = String(object.getAttribute('class')).substring(26);
    msg_type = String(object.id).substring(21 + msg.length);

    //override trace 
    plot_data.trace[plot_data.trace_num][0] = msg;
    plot_data.trace[plot_data.trace_num][1] = msg_type;

    switch (plot_data.trace_num)
    {
        case 0: series_1.name(msg_type); break;
        case 1: series_2.name(msg_type); break;
        case 2: series_3.name(msg_type); break;
        case 3: series_4.name(msg_type); break;
    }

    // increment trace selectionner
    plot_data.trace_num++;
    if (plot_data.trace_num>3) plot_data.trace_num=0;

    // sending order to change DATA PLOT
    $.send_data('PLOT_NEW_DATA', plot_data.trace);
}

// call back:
function refresh_data_frequency(code, data)
{
    var msg = Object.keys(data[0]).sort();

    for (var element in msg)
    {
        element = msg[element];
        // var element = key[element_i];
        var id = 'graph_data_' + element;
        var value = String(Math.round(data[0][element][1]*10)/10);

        if (document.getElementById(id) == null) // if the line of the tab dosesn't exist
        {  
            // console.log('..........' + element);
            // console.log(Object.keys(data[0][element][0]).sort());
            // var array = Object.keys(element[0]).sort();
            var array = Object.keys(data[0][element][0]).sort();

            var tree_view = '<ul class="treeview-menu graph_data_treeview" style="display:none;" '+ 
                            'id="Graph_data_tree_view_id_' + element + '">\n';
            for (el in array)
            {
                if (typeof data[0][element][0][array[el]] == 'number')
                {
                    // console.log(array[el] + ':' + data[0][element][0][array[el]]);
                    //
                    tree_view += '  <li id="graph_data_treeview_' + element + '_' + array[el] + 
                                 '" class="graph_data_treeview_class_' + element +
                                 '" onmouseover="this.style.textDecoration=\'underline\'" ' + 
                                 'onmouseout="this.style.textDecoration=\'none\'" style="textDecoration:none;" ' + 
                                 'onclick="graph_data_treeview_click(this, event)">' + array[el] + '</li>\n';
                }
                else
                {
                    // console.log(array[el] + ' is a ' + typeof data[0][element][0][array[el]]);
                }
            }

            tree_view += '</ul>\n';

            $('#Graph_data_id').append('<tr><td onclick="graph_data_click(this)" style="cursor:pointer;" id="Graph_data_id_' + 
                                       element + '">\n'+
                                       element + '\n' + tree_view + 
                                       '</td><td><div class="some_random_things" id ="'+ 
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
    series_1 = chart.line(plot_data.dataSet.mapAs({x: [0], value: [1]}));
    series_1.name('pitch');
    series_1.hoverMarkers().enabled(true).type('circle').size(4);
    series_1.tooltip().position('right').anchor('left').offsetX(5).offsetY(5);

    // create second series with mapped data
    series_2 = chart.line(plot_data.dataSet.mapAs({x: [0], value: [2]}));
    series_2.name('roll');
    series_2.hoverMarkers().enabled(true).type('circle').size(4);
    series_2.tooltip().position('right').anchor('left').offsetX(5).offsetY(5);

    // create third series with mapped data
    series_3 = chart.line(plot_data.dataSet.mapAs({x: [0], value: [3]}));
    series_3.name('yaw');
    series_3.hoverMarkers().enabled(true).type('circle').size(4);
    series_3.tooltip().position('right').anchor('left').offsetX(5).offsetY(5);

    // create fourth series with mapped data
    series_4 = chart.line(plot_data.dataSet.mapAs({x: [0], value: [4]}));
    series_4.name('alt');
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