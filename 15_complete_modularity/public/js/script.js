
function boxClick(object)
{
    var id = 'BOX_' + String(object.id).substring(12);
    console.log(id);
    document.getElementById(id).style.display = 'block';
}

$(document).ready(function() 
{
    var ws = new WebSocket(wr_adr);
    var main = false;

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

        console.log('receive message: ' + reverse_msg_tab[msg.code]);

        switch(msg.code)
        {
            case msg_tab['ARM_STATE']:

                if (msg.data[0] == true) // if armed
                {
                    // changing button 'arm' text and color
                    document.getElementById("arm_btn").className = "btn btn-danger btn-md";
                    document.getElementById("arm_btn").childNodes[0].nodeValue = "Disarm Drone"
                }
                else 
                {
                    // changing button 'arm' text and color
                    document.getElementById("arm_btn").className = "btn btn-success btn-md";
                    document.getElementById("arm_btn").childNodes[0].nodeValue = "Arm Drone"
                }
            break;

            case msg_tab['IP']:
                // idea: we could display it in the margin (in french : marge)
            break;

            case msg_tab['SET_MAIN_CLIENT']:

                main = true;
                document.getElementById("client_status_alert").childNodes[0].nodeValue = "Controller";

                if (msg.data[0] && document.getElementById('checkbox_notif').checked)
                    alert('You can now control the drone')
            break;

            case msg_tab['SET_OBSERVER']:

                main = false;
                document.getElementById("client_status_alert").childNodes[0].nodeValue = "Observer";
                var array = document.getElementsByClassName("input_tab_OP");

                if (msg.data[0] && document.getElementById('checkbox_notif').checked)
                    alert('You are now an observer')
            break;
        }

        if (! (msg.code in reverse_msg_tab) )
            console.log("got unknown message: " + evt.data);

        for (i in call_back_tab[msg.code])
        {   
            call_back_tab[msg.code][i] (reverse_msg_tab[msg.code], msg.data);
        }
    };

    ws.onopen = function() //when the client boot
    {
        var msg = {code : 0, data:[]};

        $.send_data('GET_ARM', []);
        $.send_data('GET_IP', []);

        initMap();        
        $.send_data('GET_LOC', [-1]);

        initAnyChart();
        $.send_data('GET_GRAPH_DATA', []);

        $.send_data('GET_OBP', ['ALL']);
        $.send_data('ASK_CLIENT_STATUS', []);
    };

    ws.onclose = function(evt) //when the client is closing
    {
        // empty
    };

    //password call-back
    $("#client_status_alert").click(function()
    {
        if (!main)
        {
            array =  document.getElementsByClassName('password_prompt');

            for (var i = 0 ; i< array.length ; i++)
                array[i].style.visibility = 'visible';


            document.getElementById('input_password_div').style.visibility = 'visible';
        }
        else
            $.send_data('SWITCH_STATE', ['']);
    });

    //password call-back
    $("#btn_password_cancel").click(function()
    {
        // clear the input 
        document.getElementById('inp_password').value = '';

        // hide all the element
        for (var i = 0 ; i< array.length ; i++)
            array[i].style.visibility = 'hidden';
        document.getElementById('input_password_div').style.visibility = 'hidden';
    });

    //password call-back
    $("#btn_password_ok").click(function()
    {
        $.send_data('SWITCH_STATE', [document.getElementById('inp_password').value]);

        $("#btn_password_cancel").click();
    });

    //password call-back
    $('#inp_password').on('keypress', function (event) {
        if (event.which == 13) //enter pressed
        {
            $("#btn_password_ok").click();
        }
    }); 

    //arm button handle
    $("#arm_btn").click(function()
    {
        if (document.getElementById("arm_btn").childNodes[0].nodeValue == "Arm Drone")
        {
            //send arm command
            $.send_data('SWITCH_ARM', []); //to be change, not a switch arm command but specifically an disarm command

            //change the button's class
            document.getElementById("arm_btn").className = "btn btn-warning btn-md";

            //change the button's name
            document.getElementById("arm_btn").childNodes[0].nodeValue = "Loading"
        }
        else if (document.getElementById("arm_btn").childNodes[0].nodeValue == "Disarm Drone")
        {
            //send Disarm command
            $.send_data('SWITCH_ARM', []); //to be change, not a switch arm command but specifically a arm command

            //change the button's class
            document.getElementById("arm_btn").className = "btn btn-warning btn-md";

            //change the button's name
            document.getElementById("arm_btn").childNodes[0].nodeValue = "Loading"
        }
    });

    window.onresize = function() {
        var width_ = window.innerWidth || 
                     document.documentElement.clientWidth || 
                     document.body.clientWidth;

        var height_ = window.innerHeight || 
                      document.documentElement.clientHeight|| 
                      document.body.clientHeight;
    };

    // one of the most important function: send_data to server!
    jQuery.send_data = function send_data(str_code, arr_data)
    {
        if (typeof(str_code) != 'string')
        {
            console.log('wrong type, code must be a string');
            return;
        }
        else if (! Array.isArray(arr_data))
        {
            console.log('wrong type, data must be an array');
            return;
        }
        else if ( !(str_code in msg_tab))
        {
            console.log('str_code must be in the array');
            return;
        }

        var code_num = msg_tab[str_code];

        msg = {
            code: code_num,
            data: arr_data
        };

        ws.send( JSON.stringify(msg) );

        // executing call back associated to outgoing message
        for (i in call_back_tab[code_num])
        {
            call_back_tab[code_num] [i] (str_code, arr_data);
        }
    }
});
