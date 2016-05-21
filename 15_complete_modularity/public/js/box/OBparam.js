
// call back:
function change_OBP_value(code, data)
{
    var val = data[1]
    var OBP = String(data[0])
    var value = 0.0;

    if (typeof val == "number")
    {
        value = String(val.toFixed(2));
    }
    else if (typeof val == "string")
    {
        value = parseFloat(val).toFixed(2);
    }
    else
    {
        return
    }

    var element = document.getElementById('inp_' + OBP);

    if (element == null)
    {
        add_OBP_to_list(val, OBP);
    }

    element.readOnly = false;
    element.value = value;
    element.readOnly = !main;

    document.getElementById('change_alert').style.visibility = 'visible';
    setTimeout(remove_OBP_alert, 800, 'change_alert');
}

//call back:
function reset_OBP(code, data)
{
    $('#OBparam_body').html('');

    for ( hash in data )
    {
        var OBP = Object.keys(data[hash])[0];
        var value = data[hash][OBP];

        add_OBP_to_list(value, OBP);
    }

    document.getElementById('change_alert').style.visibility = 'visible';
    setTimeout(remove_OBP_alert, 800, 'change_alert');
}

function add_OBP_to_list(val, OBP)
{
    var value = 0.0;

    if (typeof val == "number")
    {

        value = val.toFixed(2);
    }
    else if (typeof val == "string")
    {
        value = parseFloat(val).toFixed(2);
    }
    else
    {
        return
    }

    $('#OBparam_body').append('<tr><td>\n' + OBP + '</td><td><input type="text" class="input_tab_OBP" value="'+
                              value + '" id="inp_' +
                              OBP + '" onchange="change_OBP_detected(this)">\n<div class="alert alert-success pull-right" id="alert_' +
                              OBP + '"><i class="icon fa fa-check"></i> Sent!</div>\n</td></tr>\n')
}

function change_OBP_detected(self)
{
    var id = String(self.id).substring(4); //substring because we remove the 'inp_'

    $.send_data('SET_OBP', [ id, document.getElementById(self.id).value ] );

    document.getElementById('alert_' + id).style.visibility = 'visible';

    setTimeout(remove_OBP_alert, 800, 'alert_' + id);
}

function remove_OBP_alert(id)
{
    document.getElementById(id).style.visibility = 'hidden';
}

