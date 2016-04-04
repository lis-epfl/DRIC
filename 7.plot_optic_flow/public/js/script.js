
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
        var msg     = JSON.parse(evt.data);

        // Plotly.redraw('myDiv', msg.data, msg.layout);
        Plotly.newPlot('myDiv', msg.data, msg.layout);
        // Plotly.reDraw('myDiv', msg.data);

    };

    ws.onopen = function() //when the client boot
    {
        ws.send("someone entered the room");
        var data = [
        {
            x : [[0]],
            y : [[0]],
            type: 'scatter',
            marker : {color : 'red'},
            name : 'OF'
        }];

        // Plotly.newPlot('myDiv', data);
    };

    ws.onclose = function(evt) //when the client is closing
    {
        // empty
    };


});
