      
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
        var all_var = String(evt.data).split(';');

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

        console.log(all_var);

        Plotly.extendTraces('myDiv', trace, [0,1,2], 50);
    };

    ws.onopen = function() //when the client boot
    {
        ws.send("someone entered the room");
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

        Plotly.newPlot('myDiv', data);
    };

    ws.onclose = function(evt) //when the client is closing
    {
        // empty
    };

    
});
