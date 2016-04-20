
$(document).ready(function() 
{
    var ws = new WebSocket(wr_adr);
    // var plot_visible = false;
    // var plot_rate = 80; //in ms
    // var time_start = new Date().getTime();
    // var plotDiv = document.getElementById('myDiv');

    var plot_data = 
    {
        number      : 1,
        dataSet     : anychart.data.set([]), // x, y1,y2,y3,y4
        visible     : false,
        rate        : 80, // in ms
        time_start  : new Date().getTime()
    }

    var msg_tab = {
        //server sending stuff

        'PLOT_DATA'     : 0,    // 4 values for the plot
        'ARM_STATE'     : 1,    // 1 value, arm state
        'IP'            : 2,    // 1 string containing IP adress of server

        //client sending stuff
        'SWITCH_ARM'    : 100, // no value
        'GET_ARM'       : 101, // no value
        'GET_IP'        : 102, // no value
        'PLOT_RATE'     : 103, // 1 int value : the rate in seconde, if rate is 0, stop plot
        'PLOT_NEW_DATA' : 104  // 4 value, not working for now
    };

    window.onbeforeunload = function(e) 
    {
        ws.close(1000, "someone left the room");

        if(!e) e = window.event;
        e.stopPropagation();
        e.preventDefault();
    };

    ws.onmessage = function (evt)
    {
        var msg = JSON.parse(evt.data);

        switch(msg.code)
        {
            case msg_tab['PLOT_DATA']:
            {
                // console.log("receive data to plot");

                var current = new Date().getTime();

                var inSeconds = Math.round((current - plot_data.time_start) /100) /10 ;

                if (plot_data.number >= 50)
                    plot_data.dataSet.remove(0);
                else
                    plot_data.number += 1;

                plot_data.dataSet.append([String(inSeconds), (msg.data[0]), 
                                                             (msg.data[1]), 
                                                             (msg.data[2]),
                                                             (msg.data[3])]);
                // Plotly.extendTraces('myDiv', trace, [0,1,2], 50);
            }
            break;

            case msg_tab['ARM_STATE']:
                console.log("receive arm state");

                if (msg.data[0] == true) // if armed
                    document.getElementById("send").childNodes[0].nodeValue="Disarm";
                else 
                    document.getElementById("send").childNodes[0].nodeValue="Arm";
            break;

            case msg_tab['IP']:
                console.log("receive IP adress");

                document.getElementById("IP_label").innerHTML = msg.data[0];
            break;

            default:
                console.log("got unknown message: " + evt.data);
            break;
        }
    };

    ws.onopen = function() //when the client boot
    {
        var msg = {
            code : msg_tab['GET_ARM'],
            data : []
        }

        ws.send( JSON.stringify(msg) );

        var msg2 = {
            code : msg_tab['GET_IP'],
            data : []
        }

        ws.send( JSON.stringify(msg2) );




        // create line chart
        chart = anychart.line();

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

    };

    ws.onclose = function(evt) //when the client is closing
    {
        // empty
    };

    $("#send").click(function()
    {
        if (document.getElementById("send").childNodes[0].nodeValue != "Loading")
        {
            var msg = {
                code : msg_tab['SWITCH_ARM'],
                data : []
            }

            ws.send( JSON.stringify(msg) );
            console.log("sent data " + JSON.stringify(msg));

            document.getElementById("send").childNodes[0].nodeValue = "Loading";
        }
    });

    $("#rate_id").change(function()
    { //new onboard is selected
        plot_data.rate = parseInt(String($("#rate_id").val()).substring(0, 3));

        console.log('change plot rate to:' + String(plot_data.rate));

        // ws.send("CLIENT:ASK:TRACE1:" + $("#trace1_enum").val());
        if (plot_data.visible)
        {
            var msg = {
                    code : msg_tab['PLOT_RATE'],
                    data : [plot_data.rate / 1000.0]
                };

            console.log(msg.data[0]);

            ws.send( JSON.stringify(msg) );
        }
    });

    $("#show_plot").click(function()
    {
        // $this will contain a reference to the checkbox   
        if (plot_data.visible) 
        {

            document.getElementById('plot').style.visibility = 'hidden';
            plot_data.visible = false;

            var msg = {
                code : msg_tab['PLOT_RATE'],
                data : [-1]                   // order to server : stop sending data
            };

            ws.send( JSON.stringify(msg) );

            console.log('sent stop sending data');
        } 
        else 
        {
            document.getElementById('plot').style.visibility = 'visible';
            plot_data.visible = true;

            var msg = {
                code : msg_tab['PLOT_RATE'],
                data : [plot_data.rate / 1000.0]               // order to server : start sending data at a rate of 0.080
            };

            ws.send( JSON.stringify(msg) );
            console.log('sent start sending data');

            // time_start = new Date().getTime();

            

            //clear plot data here !!

            // plotDiv.data.push ( { x: [], y: [] } );
            // Plotly.redraw(plotDiv);
        }
    });

    window.onresize = function() {
        // Plotly.Plots.resize('myDiv');
        var width_ = window.innerWidth || 
                     document.documentElement.clientWidth || 
                     document.body.clientWidth;

        var height_ = window.innerHeight || 
                      document.documentElement.clientHeight|| 
                      document.body.clientHeight;

        // var update = 
        // {
        //     width: width_ * 0.80 //20% free on each side of the graph
        // };

        // Plotly.relayout('myDiv', update);

    };


});
