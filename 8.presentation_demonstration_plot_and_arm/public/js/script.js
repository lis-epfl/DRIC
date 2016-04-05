      
$(document).ready(function() 
{
    var ws = new WebSocket(wr_adr);
    var current_x = [0,0,0];

    window.onbeforeunload = function(e) 
    {
        ws.close(1000, "someone left the room");

        if(!e) 
            e = window.event;
        e.stopPropagation();
        e.preventDefault();
    };

    ws.onmessage = function (evt) 
    {
        // console.log(evt.data)
        if (evt.data.substring(0, 4) == "plot" )
        {
            var all_var = (String(evt.data).substring(5)).split(';');

            current_x[0] += 0.1;
            current_x[1] += 0.1;
            current_x[2] += 0.1;

            var trace = {
                x : [[current_x[0]],
                     [current_x[1]],
                     [current_x[2]]],

                y : [[parseFloat(all_var[0])],
                     [parseFloat(all_var[1])],
                     [parseFloat(all_var[2])]]
            };

            // console.log(all_var);

            Plotly.extendTraces('myDiv', trace, [0,1,2], 50);
        }
        else if (evt.data == "server:state:arm")
        {
            document.getElementById("send").childNodes[0].nodeValue="Disarm";
            button_state = "unarm";
        }
        else if (evt.data == "server:state:unarm")
        {
            document.getElementById("send").childNodes[0].nodeValue="Arm";
            button_state = "arm";
        }
    };

    ws.onopen = function() //when the client boot
    {
        ws.send("client:get:arm");

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

        Plotly.newPlot('myDiv', data, {showLink: false});
    };

    ws.onclose = function(evt) //when the client is closing
    {
        // empty
    };

    $("#send").click(function()
    { //when guy click on the button
        ws.send("client:arm:switch");

        // alert("click action");

        return false;
    });

    $('#show_graph').click(function() 
    {
        var $this = $(this);
        // $this will contain a reference to the checkbox   
        if ($this.is(':checked')) 
        {
            document.getElementById('myDiv').style.visibility = 'visible';
        } 
        else 
        {
            document.getElementById('myDiv').style.visibility = 'hidden';
        }
    });
});
