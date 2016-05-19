

msg_tab = {
    #server sending stuff
    'PLOT_DATA'         : 0, # in data: 4 values for the plot
    'ARM_STATE'         : 1, # 1 value, arm state
    'IP'                : 2, # 1 string containing IP adress of server
    'LOC'               : 3, # 3 values lat, lon, alt
    'OBP_VALUE'         : 4, # 2 values : first one a string that contain the OBP, second the value (float)
    'OBP_VALUE_ALL'     : 5, # 57 values: a list of all the float value of the OBP
    'SET_MAIN_CLIENT'   : 6, # 1 value, set the client as the main client, if value is true, an alert is launch in the client
    'SET_OBSERVER'      : 7, # 1 value, unset the client as the main client (a client is by default observer), if data is true:alert
    'ASK_CHANGE'        : 8, # 1 value, this message expect an answer type 110, it carry a code that NEED to be transmit back with the answer
    'GRAPH_DATA'        : 9, # 1 value : the entire dictionnary msg_listenner

    #client sending stuff
    'SWITCH_ARM'        : 100, # no value
    'GET_ARM'           : 101, # no value
    'GET_IP'            : 102, # no value
    'PLOT_RATE'         : 103, # 1 int value : the rate in seconde, if rate=0, it means 'stop sending data'
    'PLOT_NEW_DATA'     : 104, # 4 values, no working for now
    'GET_LOC'           : 105, # 1 value : if -1, just want to get the coord, is >0, want to get a this period the coord
    'GET_OBP'           : 106, # 1 value, the OBP (string), if the OBP is 'ALL', then the server will return all the OBP
    'SET_OBP'           : 107, # 2 values, the OBP (string) and the float value of the OBP to change
    'SWITCH_STATE'      : 108, # 0 value, client ask to become an observer or a controller
    'ASK_CLIENT_STATUS' : 109, # 1 value, ask what is the client status, nedd to transmit a code that will be returned
    'ANSW_CHANGE_STATUS': 110, # 2 values : 1st: code that is transmit back, 2nd: true or false to the answer of 'ASK_CHANGE'
    'MAVLINK_MESSAGE'   : 111,  #11 values of the mavlink message (see .message_factory.command_long_send? dronekit doc)
}

msg_tab_inv = {v: k for (k, v) in msg_tab.items()}

#list of the onboard parameter (OBP) :

OBP_tab = [
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

msg_listener = {
    # initialize to empty but filled during the program, it contain the following structur:
    # name : [value, frequency, time of the last message received]
}

# typicall tab msg_listener when sent will be like :

# {
#     "code": 0,
#     "data": [{
#         "VFR_HUD": [{
#             "throttle": 0,
#             "groundspeed": 1.872008965619898e-06,
#             "airspeed": 1.872008965619898e-06,
#             "heading": 0,
#             "mavpackettype": "VFR_HUD",
#             "climb": -6.59714032735792e-07,
#             "alt": 400.0
#         }, 1.98, 1463486205.414974], #freq, last_time_update
#         "LOCAL_POSITION_NED_COV": [{
#             "x": 0.0,
#             "mavpackettype": "LOCAL_POSITION_NED_COV",
#             "z": 0.2000005543231964,
#             "y": 0.0,
#             "time_utc": 0,
#             "time_boot_ms": 208957,
#             "covariance": [0.0008942768326960504, 0.054922640323638916, 0.01213605236262083, 0.0, -9.494671758147888e-06, 0.0, 0.0, 0.0, 0.0, 0.0, 1.2587477613124065e-05, 0.0, -6.692879196634749e-06, 0.0, 0.0, 0.0, 5.147848030893931e-16, 0.0, 5.406287417741851e-09, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0005891678738407791, 0.0, -0.0003132660349365324, 0.0, 0.0, 0.0, 8.813163393517343e-11, 0.0, 0.0009255614131689072, 0.0, 0.0, 0.0, 0.0, 0.0, -0.001273766509257257, 0.0, 0.0006772735505364835, 0.0, 0.0, 0.0, 1.0],
#             "ax": 0.0,
#             "ay": 0.0,
#             "estimator_type": 0,
#             "vx": 0.0,
#             "vy": 0.0,
#             "vz": 3.3744698157534e-05,
#             "az": 0.0002698793832678348
#         }, 9.95, 1463486205.768147],
#         "RC_CHANNELS_SCALED": [{
#             "chan8_scaled": 32767,
#             "chan3_scaled": 0,
#             "chan7_scaled": 32767,
#             "time_boot_ms": 208593,
#             "chan4_scaled": 0,
#             "chan5_scaled": 0,
#             "chan2_scaled": 0,
#             "chan6_scaled": 0,
#             "mavpackettype": "RC_CHANNELS_SCALED",
#             "port": 1,
#             "chan1_scaled": 0,
#             "rssi": 64
#         }, 16710.37, 1463486205.414846],
#         "AUTOPILOT_VERSION": [{
#             "os_custom_version": [76, 69, 81, 117, 97, 100, 76, 73],
#             "product_id": 0,
#             "os_sw_version": 0,
#             "middleware_sw_version": 17104896,
#             "vendor_id": 0,
#             "capabilities": 0,
#             "flight_sw_version": 0,
#             "board_version": 0,
#             "middleware_custom_version": [100, 98, 102, 52, 48, 52, 48, 0],
#             "flight_custom_version": [100, 98, 102, 52, 48, 52, 48, 0],
#             "mavpackettype": "AUTOPILOT_VERSION",
#             "uid": 0
#         }, 0.99, 1463486192.688938],
#         "LOCAL_POSITION_NED": [{
#             "x": -9.322438927483745e-07,
#             "time_boot_ms": 208585,
#             "y": 0.0,
#             "mavpackettype": "LOCAL_POSITION_NED",
#             "vx": -1.8795071810018271e-06,
#             "vy": 0.0,
#             "vz": 6.690700047329301e-07,
#             "z": 3.3186370274052024e-07
#         }, 1.98, 1463486205.414644],
#         "ATTITUDE": [{
#             "pitchspeed": -7.267267343458172e-11,
#             "yaw": 0.0,
#             "rollspeed": 0.0,
#             "time_boot_ms": 208765,
#             "pitch": 1.9075002910540206e-07,
#             "mavpackettype": "ATTITUDE",
#             "yawspeed": 0.0,
#             "roll": 0.0
#         }, 4.93, 1463486205.616496],
#         "COMMAND_ACK": [{
#             "mavpackettype": "COMMAND_ACK",
#             "command": 520,
#             "result": 0
#         }, 0.99, 1463486192.689013],
#         "NAMED_VALUE_FLOAT": [{
#             "mavpackettype": "NAMED_VALUE_FLOAT",
#             "time_boot_ms": 208821,
#             "value": 5.0,
#             "name": "stabExTime"
#         }, 18558.87, 1463486205.616865],
#         "ATTITUDE_QUATERNION": [{
#             "q1": 1.0000044107437134,
#             "q3": 9.537977518903062e-08,
#             "q2": 0.0,
#             "q4": 0.0,
#             "pitchspeed": -7.268816104577525e-11,
#             "rollspeed": 0.0,
#             "time_boot_ms": 208589,
#             "mavpackettype": "ATTITUDE_QUATERNION",
#             "yawspeed": 0.0
#         }, 1.98, 1463486205.414718],
#         "SCALED_PRESSURE": [{
#             "mavpackettype": "SCALED_PRESSURE",
#             "press_abs": 400.0,
#             "time_boot_ms": 208605,
#             "temperature": 24,
#             "press_diff": -0.0
#         }, 1.98, 1463486205.415032],
#         "RC_CHANNELS_RAW": [{
#             "chan4_raw": 1024,
#             "chan2_raw": 1024,
#             "chan6_raw": 1024,
#             "time_boot_ms": 208829,
#             "chan1_raw": 1024,
#             "chan5_raw": 1024,
#             "chan3_raw": 1024,
#             "mavpackettype": "RC_CHANNELS_RAW",
#             "chan7_raw": 65535,
#             "chan8_raw": 65535,
#             "port": 1,
#             "rssi": 0
#         }, 11214.72, 1463486205.61714],
#         "SERVO_OUTPUT_RAW": [{
#             "servo4_raw": 950,
#             "servo2_raw": 950,
#             "servo6_raw": 0,
#             "time_usec": 208609170,
#             "servo1_raw": 950,
#             "servo8_raw": 0,
#             "servo5_raw": 0,
#             "mavpackettype": "SERVO_OUTPUT_RAW",
#             "servo3_raw": 950,
#             "port": 0,
#             "servo7_raw": 0
#         }, 0.99, 1463486205.415095],
#         "GPS_RAW_INT": [{
#             "fix_type": 3,
#             "cog": 0,
#             "epv": 300,
#             "lon": 65660448,
#             "time_usec": 208551584,
#             "eph": 100,
#             "satellites_visible": 5,
#             "lat": 465185241,
#             "mavpackettype": "GPS_RAW_INT",
#             "alt": 400000,
#             "vel": 0
#         }, 0.99, 1463486205.415369],
#         "DISTANCE_SENSOR": [{
#             "orientation": 0,
#             "covariance": 0,
#             "time_boot_ms": 208597,
#             "current_distance": 20,
#             "max_distance": 0,
#             "mavpackettype": "DISTANCE_SENSOR",
#             "type": 1,
#             "id": 0,
#             "min_distance": 0
#         }, 1.98, 1463486205.414907],
#         "HEARTBEAT": [{
#             "base_mode": 96,
#             "system_status": 3,
#             "custom_mode": 0,
#             "autopilot": 18,
#             "mavpackettype": "HEARTBEAT",
#             "type": 2,
#             "mavlink_version": 3
#         }, 1.04, 1463486205.617332],
#         "SCALED_IMU": [{
#             "xgyro": 0,
#             "ygyro": 0,
#             "xmag": 469,
#             "time_boot_ms": 208833,
#             "xacc": 0,
#             "zacc": -999,
#             "yacc": 0,
#             "zgyro": 0,
#             "mavpackettype": "SCALED_IMU",
#             "ymag": 0,
#             "zmag": 882
#         }, 4.93, 1463486205.617206],
#         "GLOBAL_POSITION_INT": [{
#             "lat": 465185241,
#             "lon": 65660448,
#             "time_boot_ms": 208825,
#             "hdg": 0,
#             "relative_alt": 0,
#             "mavpackettype": "GLOBAL_POSITION_INT",
#             "vx": 0,
#             "vy": 0,
#             "alt": 400000,
#             "vz": 0
#         }, 4.93, 1463486205.616953],
#         "SYS_STATUS": [{
#             "onboard_control_sensors_present": 64551,
#             "load": 0,
#             "battery_remaining": 91,
#             "errors_count4": 0,
#             "drop_rate_comm": 0,
#             "errors_count2": 0,
#             "errors_count3": 0,
#             "errors_comm": 0,
#             "current_battery": 0,
#             "errors_count1": 0,
#             "onboard_control_sensors_health": 64551,
#             "mavpackettype": "SYS_STATUS",
#             "onboard_control_sensors_enabled": 64551,
#             "voltage_battery": 12340
#         }, 0.99, 1463486205.415198]
#     }]
# }