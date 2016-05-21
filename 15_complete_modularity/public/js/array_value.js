

var msg_tab = {
    //server sending stuff
    'PLOT_DATA'         : 0, // in data: 4 values for the plot
    'ARM_STATE'         : 1, // 1 value, arm state
    'IP'                : 2, // 1 string containing IP adress of server
    'LOC'               : 3, // 3 values lat, lon, alt
    'OBP_VALUE'         : 4, // 2 values : first one a string that contain the OBP, second the value (float)
    'OBP_VALUE_ALL'     : 5, // ~57 dictionnary: a list of all the float value. The array looks like: [{'OBP1' : value}, {'OBP2' : value}, ...]
    'SET_MAIN_CLIENT'   : 6, // 1 value, set the client as the main client, if value is true, an alert is launch in the client
    'SET_OBSERVER'      : 7, // 1 value, unset the client as the main client (a client is by default observer), if data is true:alert
    'GRAPH_DATA'        : 8, // 1 value : the entire dictionnary msg_listenner
    'MAV_MSG_CONF'      : 9, // 0 value : confirm that the drone receive the order

    //client sending stuff
    'SWITCH_ARM'        : 100, // no value
    'GET_ARM'           : 101, // no value
    'GET_IP'            : 102, // no value
    'PLOT_RATE'         : 103, // 1 int value : the rate in seconde, if rate=0, it means 'stop sending data'
    'PLOT_NEW_DATA'     : 104, // 4 values, no working for now
    'GET_LOC'           : 105, // 1 value : if -1, just want to get the coord, is >0, want to get a this period the coord
    'GET_OBP'           : 106, // 1 value, the OBP (string), if the OBP is 'ALL', then the server will send 'OBP_VALUE_ALL' 
    'SET_OBP'           : 107, // 2 values, the OBP (string) and the float value of the OBP to change
    'SWITCH_STATE'      : 108, // 1 value password if client want to become controller, or '' if client want to become observer
    'ASK_CLIENT_STATUS' : 109, // 1 value, ask what is the client status, nedd to transmit a code that will be returned
    'MAVLINK_MESSAGE'   : 110, //11 values of the mavlink message (see .message_factory.command_long_send? dronekit doc)
    'GET_GRAPH_DATA'    : 111, // no value

    };

var reverse_msg_tab = {};
for (element in msg_tab)
    reverse_msg_tab[ msg_tab[element] ] = element;