
$(document).ready(function() 
{
    var ws = new WebSocket(wr_adr);
    var current_x = [0,0,0];
    var plot_visible = false;

    var msg_tab = {
        //server sending stuff

        'PLOT_DATA' : 0,    // 4 values for the plot
        'ARM_STATE' : 1,    // 1 value, arm state
        'IP'        : 2,    // 1 string containing IP adress of server

        //client sending stuff
        'SWITCH_ARM' : 100, // no value
        'GET_ARM'    : 101, // no value
        'GET_IP'     : 102  // no value
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

                current_x[0] += 0.1;
                current_x[1] += 0.1;
                current_x[2] += 0.1;

                var trace = 
                {
                    x : [[current_x[0]],
                         [current_x[1]],
                         [current_x[2]]],

                    y : [[ msg.data[0] ],
                         [ msg.data[1] ],
                         [ msg.data[2] ]]
                };

                Plotly.extendTraces('myDiv', trace, [0,1,2], 50);
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


        var data = [
        {
            x : [[0]],
            y : [[0]],
            type: 'scattergl',
            marker : {color : 'red'},
            name : 'Pitch'
        },
        {
            x : [[0]],
            y : [[0]],
            type: 'scattergl',
            marker : {color : 'blue'},
            name : 'Roll'
        },
        {
            x : [[0]],
            y : [[0]],
            type: 'scattergl',
            marker : {color : 'green'},
            name : 'Yaw'
        }];

        layout = 
        {
            showLink: false,
            showlegend: true,
        };

        Plotly.newPlot('myDiv', data, layout);
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

    $("#show_plot").click(function()
    {

        // $this will contain a reference to the checkbox   
        if (plot_visible) 
        {
            document.getElementById('myDiv').style.visibility = 'hidden';
            plot_visible = false;
        } 
        else 
        {
            document.getElementById('myDiv').style.visibility = 'visible';
            plot_visible = true;
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

        var update = 
        {
            width: width_ * 0.80 //20% free on each side of the graph
        };

        Plotly.relayout('myDiv', update);

    };
});
