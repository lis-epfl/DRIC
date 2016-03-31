      
$(document).ready(function() 
{
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

            y : [[parseFloat(all_var[0])],
                 [parseFloat(all_var[1])],
                 [parseFloat(all_var[2])],
                 [parseFloat(all_var[3])]]
        };

        console.log(all_var);

        Plotly.extendTraces('myDiv', trace, [0,1,2,3], 50);
    };

    ws.onopen = function() //when the client boot
    {
        ws.send("someone entered the room");
        var data = [
        {
            x : [[0]],
            y : [[0]],
            type: 'scattergl',
            marker : {color : 'red'}
        },
        {
            x : [[0]],
            y : [[0]],
            type: 'scattergl',
            marker : {color : 'blue'}
        },
        {
            x : [[0]],
            y : [[0]],
            type: 'scattergl',
            marker : {color : 'green'}
        },
        {
            x : [[0]],
            y : [[0]],
            type: 'scattergl',
            marker : {color : 'black'}
        }];

        Plotly.newPlot('myDiv', data);

        // sent default plot values
        ws.send("CLIENT:ASK:TRACE1:BIAS_ACC_X");
        ws.send("CLIENT:ASK:TRACE2:BIAS_ACC_Y");
        ws.send("CLIENT:ASK:TRACE3:BIAS_ACC_Z");
        ws.send("CLIENT:ASK:TRACE4:BIAS_GYRO_X");
    };

    ws.onclose = function(evt) //when the client is closing
    {
        // empty
    };

    $("#trace1_enum").change(function()
    { //new onboard is selected
        console.log($("#trace1_enum").val() + "selected on trace1");

        ws.send("CLIENT:ASK:TRACE1:" + $("#trace1_enum").val());

        return false;
    });

    $("#trace2_enum").change(function()
    { //new onboard is selected
        console.log($("#trace2_enum").val() + "selected on trace2");

        ws.send("CLIENT:ASK:TRACE2:" + $("#trace1_enum").val());

        return false;
    });

    $("#trace3_enum").change(function()
    { //new onboard is selected
        console.log($("#trace3_enum").val() + "selected on trace3");

        ws.send("CLIENT:ASK:TRACE3:" + $("#trace1_enum").val());

        return false;
    });

    $("#trace4_enum").change(function()
    { //new onboard is selected
        console.log($("#trace3_enum").val() + "selected on trace3");

        ws.send("CLIENT:ASK:TRACE4:" + $("#trace1_enum").val());

        return false;

    });
});

// # CLIENT:ASK:TRACENB:THRV_I_PREG
// /CLIENT:ASK:TRACENB:THRV_KP
// /CLIENThxvchxvx:TRACENB:THRV_KD
// /CLIENT:ASK:TRAhxvchxvx:THRV_SOFT
// /CLIENT:ASK:TRACENB:VEL_CLIMBRATE
// /hxvchxvxT:ASKhxvchxvxCENB:VEL_CRUISESPEED
// /CLIENT:ASK:TRACENB:VEL_DIST2VEL
// /CLIENT:ASK:TRACENB:VEL_HOVERPGAIN
// /CLIENT:ASK:TRAChxvchxvxVEL_SOFTZONE
// /CLIhxvchxvxSK:TRACENB:VEL_WPT_PGAIN
// /CLIENT:ASK:TRACENB:VEL_WPT_DGAIN
// /CLIENT:ASK:TRACENB:YAW_R_D_CLIP
// /CLIENT:ASK:TRACENB:YAW_R_I_CLIP
// /CLIENT:ASK:TRACENB:YAW_R_KP
// /CLIENT:ASK:TRACENB:YAW_R_KI
// /CLIENT:ASK:TRACENB:YAW_R_KD
// /CLIENT:ASK:TRACENB:YAW_R_P_CLMN
// /CLIENT:ASK:TRACENB:YAW_R_P_CLM