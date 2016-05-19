
$(document).ready(function() 
{

    var ws = new WebSocket(wr_adr);

    var main = false;
    var test = 0;

    // var plot_visible = false;
    // var plot_rate = 80; //in ms
    // var time_start = new Date().getTime();
    // var plotDiv = document.getElementById('myDiv');

    var plot_data = 
    {
        number      : 0,
        dataSet     : anychart.data.set([]), // x, y1,y2,y3,y4
        visible     : false,
        rate        : 2000, // in ms
        time_start  : new Date().getTime()
    }

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

                console.log(msg.data);



                // plot_data.dataSet.append([String(inSeconds), (msg.data[0]), 
                //                                              (msg.data[1]), 
                //                                              (msg.data[2]),
                //                                              (msg.data[3])]);

                // console.log(plot_data.dataSet);

                // plot_data.dataSet.append([String(inSeconds), msg.data[0]]);
                // plot_data.dataSet.append({x : inSeconds,
                //                           value: msg.data[0]});
            }
            break;

            case msg_tab['ARM_STATE']:
                console.log("receive arm state");

                if (msg.data[0] == true) // if armed
                {
                    document.getElementById("arm_btn").className = "btn btn-danger btn-md";
                    document.getElementById("arm_btn").childNodes[0].nodeValue = "Disarm Drone"
                }
                else 
                {
                    document.getElementById("arm_btn").className = "btn btn-success btn-md";
                    document.getElementById("arm_btn").childNodes[0].nodeValue = "Arm Drone"
                }

            break;

            case msg_tab['IP']:
                console.log("got IP adress");

                // document.getElementById("IP_label").innerHTML = msg.data[0];
            break;

            case msg_tab['LOC']:
                console.log("got drone location")
                set_drone_pos(msg.data[0], msg.data[1]);
            break;

            case msg_tab['OBP_VALUE']:
                console.log('got value of' + msg.data[0]);

                // document.getElementById('inp_' + msg.data[0]).value = String(msg.data[1]).substring(0,6);
                change_input_value(String(msg.data[1]).substring(0,6), 'inp_' + String(msg.data[0]))

                document.getElementById('change_alert').style.visibility = 'visible';
                setTimeout(remove_alert, 800, 'change_alert');
            break;

            case msg_tab['OBP_VALUE_ALL']:
                console.log('got all OBP values');
                console.log(msg.data);

                $('#OBparam_body').html('')
                for ( hash in msg.data )
                {
                    console.log('hash:' + String(msg.data[hash]));
                    var OBP = Object.keys(msg.data[hash])[0];
                    var value = msg.data[hash][OBP];

                    console.log(OBP);
                    console.log(value);

                    $('#OBparam_body').append('<tr><td>\n' + OBP + '</td><td><input type="text" class="input_tab_OP" value="'+
                                               parseFloat(value).toFixed(2) + '" id="inp_' +
                                               OBP + '">\n<div class="alert alert-success pull-right" id="alert_' +
                                               OBP + '"><i class="icon fa fa-check"></i> Sent!</div>\n</td></tr>\n')

                }

                // document.getElementById('inp_' + OBP_tab[i]).value = String(msg.data[i]).substring(0,6);

                document.getElementById('change_alert').style.visibility = 'visible';
                setTimeout(remove_alert, 800, 'change_alert');
            break;

            case msg_tab['SET_MAIN_CLIENT']:
                main = true;

                //console.log(msg.data);
                document.getElementById("client_status_alert").childNodes[0].nodeValue = "Controller";

                change_status();

                if (msg.data[0] && document.getElementById('checkbox_notif').checked)
                    alert('You can now control the drone')
                
            break;

            case msg_tab['SET_OBSERVER']:
                main = false;

                document.getElementById("client_status_alert").childNodes[0].nodeValue = "Observer";
                
                var array = document.getElementsByClassName("input_tab_OP");

                change_status();

                if (msg.data[0] && document.getElementById('checkbox_notif').checked)
                    alert('You are now an observer')
                
            break;

            case msg_tab['ASK_CHANGE']:
                if (main) //otherwise I don't know..
                {
                    // if notif not activated answer is no
                    var answer = false;

                    if (document.getElementById('checkbox_notif').checked)
                        answer = confirm('Client number ' + String(msg.data[0]) + ' ask to become the controler, do you want to become an observer?' );

                    sendData('ANSW_CHANGE_STATUS', [ msg.data[0], answer ]);
                }

            case msg_tab['GRAPH_DATA']:
                console.log('receive the big dictionnary of the graph data');

                var keys = Object.keys(msg.data[0]).sort();

                for (var element in keys)
                {
                    element = keys[element];
                    var id = 'graph_data_' + element;
                    var value = String(Math.round(msg.data[0][element][1]*10)/10);

                    if (document.getElementById(id) == null) // if the line of the tab dosesn't exist
                    {  
                        $('#Graph_data_id').append('<tr><td>\n'+
                                                   element + '</td><td><div class="some_random_things" id ="'+ 
                                                   id + '">'+
                                                   value + ' Hz</div>\n</td></tr>');
                    }
                    else
                    {
                        document.getElementById(id).childNodes[0].nodeValue = value + ' Hz';
                    }
                }

            break;

            default:
                console.log("got unknown message: " + evt.data);
            break;
        }
    };

    ws.onopen = function() //when the client boot
    {
        var msg = {code : 0, data:[]};

        sendData('GET_ARM', []);
        sendData('GET_IP', []);

        initMap();        
        sendData('GET_LOC', [-1]); //TODO: change -1 to 1.0

        initAnyChart();

        // sendData('GET_OBP', ['NAMES']);
        sendData('GET_OBP', ['ALL']);
        sendData('ASK_CLIENT_STATUS', []);
        sendData('GET_GRAPH_DATA', []);
        
    };

    ws.onclose = function(evt) //when the client is closing
    {
        // empty
    };

    function change_input_value(val, id)
    {
        var element = document.getElementById(id);

        element.readOnly = false;
        element.value = val;
        element.readOnly = !main;
    }

    function remove_alert(id)
    {
        document.getElementById(id).style.visibility = 'hidden';
    }

    function change_status()
    {
        //onboard parameter
        var array = document.getElementsByClassName("input_tab_OP");

        for (var i = 0 ; i< array.length ; i++)
            array[i].readOnly = !main;

        //...
    }

    $(".input_tab_OP").change(function()
    {
        var id = String(this.id).substring(4);

        console.log('sent new value for OBP:' + id );
        sendData('SET_OBP', [ id, document.getElementById(this.id).value ] );

        document.getElementById('alert_'+id).style.visibility = 'visible';

        setTimeout(remove_alert, 800, 'alert_'+id);
    })

    $("#send").click(function()
    {
        if (document.getElementById("send").childNodes[0].nodeValue != "Loading")
        {
            // var msg = {
            //     code : msg_tab['SWITCH_ARM'],
            //     data : []
            // }

            // ws.send( JSON.stringify(msg) );
            sendData('SWITCH_ARM', []);
            console.log("sent data " + 'SWITCH_ARM');

            document.getElementById("send").childNodes[0].nodeValue = "Loading";
        }
    });

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
            sendData('SWITCH_STATE', ['']);
    })

    $("#btn_password_cancel").click(function()
    {
        // clear the input 
        document.getElementById('inp_password').value = '';

        // hide all the element
        for (var i = 0 ; i< array.length ; i++)
            array[i].style.visibility = 'hidden';
        document.getElementById('input_password_div').style.visibility = 'hidden';
    })

    $("#btn_password_ok").click(function()
    {
        sendData('SWITCH_STATE', [document.getElementById('inp_password').value]);

        $("#btn_password_cancel").click();
    })

    $('#inp_password').on('keypress', function (event) {
        if (event.which == 13) //enter pressed
        {
            $("#btn_password_ok").click();
        }
    }); 

    $("#rate_id").change(function()
    { //new onboard is selected
        plot_data.rate = parseInt(String($("#rate_id").val()).substring(0, 3));

        console.log('change plot rate to:' + String(plot_data.rate));

        if (plot_data.visible)
        {
            // var msg = {
            //         code : msg_tab['PLOT_RATE'],
            //         data : [plot_data.rate / 1000.0]
            //     };

            console.log(plot_data.rate / 1000.0);

            // ws.send( JSON.stringify(msg) );
            sendData('PLOT_RATE', [plot_data.rate / 1000.0] );
        }
    });

    $("#get_loc").click(function()
    {
        // var msg = {
        //         code : msg_tab['GET_LOC'],
        //         data : [0]
        //     };

        // ws.send( JSON.stringify(msg) );

        sendData('GET_LOC', [0]);

    });

    $("#follow_drone_btn").click(function()
    {
        // alert(1);
        if (document.getElementById("follow_drone_btn").childNodes[0].nodeValue == "follow drone")
        {
            // alert(2);
            sendData('GET_LOC', [1.0]);
            document.getElementById("follow_drone_btn").childNodes[0].nodeValue = "stop following drone";
        }
        else if (document.getElementById("follow_drone_btn").childNodes[0].nodeValue == "stop following drone")
        {
            // alert(3);
            sendData('GET_LOC', [-1]);
            document.getElementById("follow_drone_btn").childNodes[0].nodeValue = "follow drone";
        }
    })

    $("#arm_btn").click(function()
    {
        console.log('arm ok');
        test();

        if (document.getElementById("arm_btn").childNodes[0].nodeValue == "Arm Drone")
        {
            //send arm command
            sendData('SWITCH_ARM', []); //to be change, not a switch arm command but specifically an disarm command

            //change the button's class
            document.getElementById("arm_btn").className = "btn btn-warning btn-md";

            //change the button's name
            document.getElementById("arm_btn").childNodes[0].nodeValue = "Loading"
        }
        else if (document.getElementById("arm_btn").childNodes[0].nodeValue == "Disarm Drone")
        {
            //send Disarm command
            sendData('SWITCH_ARM', []); //to be change, not a switch arm command but specifically a arm command

            //change the button's class
            document.getElementById("arm_btn").className = "btn btn-warning btn-md";

            //change the button's name
            document.getElementById("arm_btn").childNodes[0].nodeValue = "Loading"
        }
    })

    $("#disarm_btn").click(function()
    {
        document.getElementById('arm_btn').style.visibility = 'visible';
        document.getElementById('disarm_btn').style.visibility = 'hidden';
    })

    $("#show_plot").click(function()
    {
        // $this will contain a reference to the checkbox   
        if (plot_data.visible) 
        {
            // document.getElementById('plot').style.visibility = 'hidden';
            // document.getElementById('show_plot').name = 'pause';
            document.getElementById("show_plot").childNodes[0].nodeValue = "Play"
            plot_data.visible = false;

            // var msg = {
            //     code : msg_tab['PLOT_RATE'],
            //     data : [-1]                   // order to server : stop sending data
            // };

            // ws.send( JSON.stringify(msg) );
            sendData('PLOT_RATE', [-1]);

            console.log('sent stop sending data');
        } 
        else 
        {
            document.getElementById("show_plot").childNodes[0].nodeValue = "Pause"
            plot_data.visible = true;

            sendData('PLOT_RATE', [plot_data.rate / 1000.0] );
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

    window.onresize = function() {
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

    };

    function sendData(str_code, arr_data)
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

        msg = {
            code: msg_tab[str_code],
            data: arr_data
        };

        // console.log(str_code);
        console.log(msg)
        // console.log("sent: " + JSON.stringify(msg));
        ws.send( JSON.stringify(msg) );
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
    }


});
