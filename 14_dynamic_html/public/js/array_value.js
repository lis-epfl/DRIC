var msg_tab = {
        //server sending stuff
        'PLOT_DATA'         : 0,    // 4 values for the plot
        'ARM_STATE'         : 1,    // 1 value, arm state
        'IP'                : 2,    // 1 string containing IP adress of server
        'LOC'               : 3,    // 3 value lat, lon, alt
        'OBP_VALUE'         : 4,    // 2 values : first one a string that contain the OBP, second the value (float)
        'OBP_VALUE_ALL'     : 5,    // 57 values: a list of all the float value of the OBP
        'SET_MAIN_CLIENT'   : 6,    // 0 value, set the client as the main client
        'SET_OBSERVER'      : 7,    // 0 value, unset the client as the main client (a client is by default observer)
        'ASK_CHANGE'        : 8,    // 1 value, this message expect an answer type 110, it carry a code that NEED to be transmit back with the answer

        //client sending stuff
        'SWITCH_ARM'        : 100,  // no value
        'GET_ARM'           : 101,  // no value
        'GET_IP'            : 102,  // no value
        'PLOT_RATE'         : 103,  // 1 int value : the rate in seconde, if rate is 0, stop plot
        'PLOT_NEW_DATA'     : 104,  // 4 value, not working for now
        'GET_LOC'           : 105,  // 1 value : if -1, just want to get the coord, if >0, want to get a this period the coord
        'GET_OBP'           : 106,  // 1 value, the OBP (string), if the OBP is 'ALL', then the server will return all the OBP
        'SET_OBP'           : 107,  // 2 values, the OBP (string) and the float value of the OBP to change
        'SWITCH_STATE'      : 108,  // 0 value, client ask to become an observer or a controller
        'ASK_CLIENT_STATUS' : 109,  // 1 value, ask what is the client status, nedd to transmit a code that will be returned
        'ANSW_CHANGE_STATUS': 110,  // 2 values : 1st: code that is transmit back, 2nd: true or false to the answer of 'ASK_CHANGE'
    };

var OBP_tab = [
    'BIAS_ACC_X', 'BIAS_ACC_Y', 'BIAS_ACC_Z',
    'BIAS_GYRO_X', 'BIAS_GYRO_Y','BIAS_GYRO_Z',
    'BIAS_MAG_X','BIAS_MAG_Y','BIAS_MAG_Z',
    'COM_RC_IN_MODE','CTRL_CTRL_SRC','ID_SYSID',
    'PITCH_R_D_CLIP','PITCH_R_I_CLIP',
    'PITCH_R_KD','PITCH_R_KI','PITCH_R_KP',
    'POS_KP_ALT_BARO',
    'POS_KP_POS0','POS_KP_POS1','POS_KP_POS2',
    'POS_KP_VELB',
    'QF_KP_ACC','QF_KP_MAG',
    'ROLL_R_D_CLIP',
    'ROLL_R_I_CLIP',
    'ROLL_R_KP','ROLL_R_KI','ROLL_R_KD',
    'SCALE_ACC_X','SCALE_ACC_Y','SCALE_ACC_Z',
    'SCALE_GYRO_X','SCALE_GYRO_Y','SCALE_GYRO_Z',
    'SCALE_MAG_X','SCALE_MAG_Y','SCALE_MAG_Z',
    'THRV_I_PREG','THRV_KP','THRV_KD','THRV_SOFT',
    'VEL_CLIMBRATE','VEL_CRUISESPEED','VEL_DIST2VEL',
    'VEL_HOVER_PGAIN','VEL_HOVER_DGAIN',
    'VEL_SOFTZONE',
    'VEL_WPT_PGAIN','VEL_WPT_DGAIN',
    'YAW_R_D_CLIP','YAW_R_I_CLIP',
    'YAW_R_KP','YAW_R_KI','YAW_R_KD',
    'YAW_R_P_CLMN','YAW_R_P_CLMX',
]
