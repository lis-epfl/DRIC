// JQuery call_back inside (not accessible from anaywhere else)
$(document).ready(function() 
{
	$("#send_mav_btn").click(function()
	{
	    $.send_data('MAVLINK_MESSAGE', [
	        document.getElementById('inp_mav_target_system').value,
	        document.getElementById('inp_mav_target_component').value,
	        document.getElementById('inp_mav_command').value,
	        document.getElementById('inp_mav_confirmation').value,
	        document.getElementById('inp_mav_param1').value,
	        document.getElementById('inp_mav_param2').value,
	        document.getElementById('inp_mav_param3').value,
	        document.getElementById('inp_mav_param4').value,
	        document.getElementById('inp_mav_param5').value,
	        document.getElementById('inp_mav_param6').value,
	        document.getElementById('inp_mav_param7').value ]);
	});
});

//call back
function show_conf_receive_mav(code, data)
{
	document.getElementById('alert_receive_mav').style.visibility = 'visible';
    setTimeout(remove_mav_alert, 800, 'change_alert');
}

function remove_mav_alert()
{
	document.getElementById('alert_receive_mav').style.visibility = 'hidden';
}
