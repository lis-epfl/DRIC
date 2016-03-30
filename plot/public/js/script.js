      
$(document).ready(function() {
    var ws = new WebSocket(wr_adr);
    var current_x = [0,0,0,0];

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
        current_x[3] += 0.1;

        var trace = {
            x : [[current_x[0]],
                 [current_x[1]],
                 [current_x[2]],
                 [current_x[3]]],

            y : [[parseFloat(all_var[0].substring(2))],
                 [parseFloat(all_var[1].substring(2))],
                 [parseFloat(all_var[2].substring(2))],
                 [parseFloat(all_var[3].substring(2))]]
        };

        Plotly.extendTraces('myDiv', trace, [0,1,2,3], 50);
    };

    ws.onopen = function() //when the client boot
    {
        ws.send("someone entered the room");
        var data = [
        {
            x : [[0]],
            y : [[0]],
            type: 'scatter',
            marker : {color : 'red'}
        },
        {
            x : [[0]],
            y : [[0]],
            type: 'scatter',
            marker : {color : 'blue'}
        },
        {
            x : [[0]],
            y : [[0]],
            type: 'scatter',
            marker : {color : 'green'}
        },
        {
            x : [[0]],
            y : [[0]],
            type: 'scatter',
            marker : {color : 'black'}
        }];

        Plotly.newPlot('myDiv', data);
    };

    ws.onclose = function(evt) //when the client is closing
    {
        // empty
    };
});