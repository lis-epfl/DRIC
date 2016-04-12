
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
        var msg      = JSON.parse(evt.data);
        Plotly.newPlot('myDiv', msg.data, msg.layout);
    };

    ws.onopen = function() //when the client boot
    {
        ws.send("someone entered the room");
    };

    ws.onclose = function(evt) //when the client is closing
    {
        // empty
    };


});
