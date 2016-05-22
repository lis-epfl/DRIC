

msg_tab = {
    # server sending stuff
    'PLOT_DATA'         : 0, # in data: 4 values for the plot
    'ARM_STATE'         : 1, # 1 value, arm state
    'IP'                : 2, # 1 string containing IP adress of server
    'LOC'               : 3, # 3 values lat, lon, alt
    'OBP_VALUE'         : 4, # 2 values : first one a string that contain the OBP, second the value (float)
    'OBP_VALUE_ALL'     : 5, # ~57 dictionnary: a list of all the float value. The array looks like: [{'OBP1' : value}, {'OBP2' : value}, ...]
    'SET_MAIN_CLIENT'   : 6, # 1 value, set the client as the main client, if value is true, an alert is launch in the client
    'SET_OBSERVER'      : 7, # 1 value, unset the client as the main client (a client is by default observer), if data is true:alert
    'GRAPH_DATA'        : 8, # 1 value : the entire dictionnary msg_listenner
    'MAV_MSG_CONF'      : 9, # 0 value : confirm that the drone receive the order

    # client sending stuff
    'SWITCH_ARM'        : 100, # no value
    'GET_ARM'           : 101, # no value
    'GET_IP'            : 102, # no value
    'PLOT_RATE'         : 103, # 1 int value : the rate in seconde, if rate=0, it means 'stop sending data'
    'PLOT_NEW_DATA'     : 104, # 4 tab of 2 values each, 4 tab for each trace and first value for msg (e.g : 'ATTITUDE') 2nd for type (e.g : 'pitch') 
    'GET_LOC'           : 105, # 1 value : if -1, just want to get the coord, is >0, want to get a this period the coord
    'GET_OBP'           : 106, # 1 value, the OBP (string), if the OBP is 'ALL', then the server will send 'OBP_VALUE_ALL' 
    'SET_OBP'           : 107, # 2 values, the OBP (string) and the float value of the OBP to change
    'SWITCH_STATE'      : 108, # 1 value password if client want to become controller, or '' if client want to become observer
    'ASK_CLIENT_STATUS' : 109, # 1 value, ask what is the client status, nedd to transmit a code that will be returned
    'MAVLINK_MESSAGE'   : 110, # 11 values of the mavlink message (see .message_factory.command_long_send? dronekit doc or below)
    'MAVLINK_MSG_SHORT' : 111, # 9 values same as MAVLINK_MESSAGE but no need to specified the 2 first parameter, they are automatically set, see below
    'GET_GRAPH_DATA'    : 112, # no value 
}

# MAVLINK_MESSAGE parameter:
#  1: Target_system         (with MAVLINK_MSG_SHORT : set to the drone ID automatically)
#  2: Target_component      (with MAVLINK_MSG_SHORT : set to 0 automatically)
#  3: Command:              (it's a MAV_CMD enum, see below)
#  4: Confirmation
#  5: Parameter 1
#  6: Parameter 2
#  7: Parameter 3
#  8: Parameter 4
#  9: Parameter 5
#  10: Parameter 6
#  11: Parameter 7

# MAVLINK_MSG parameter:
#  Target_system is set to the drone ID automatically
#  Target_component is set to 0 automatically
#  1: Command:              (it's a MAV_CMD enum, see below)
#  2: Confirmation
#  3: Parameter 1
#  4: Parameter 2
#  5: Parameter 3
#  6: Parameter 4
#  7: Parameter 5
#  8: Parameter 6
#  9: Parameter 7

# MAV_CMD enum:
# see complete list at  https://pixhawk.ethz.ch/mavlink/ 
MAV_CMD = {
    'MAV_CMD_NAV_WAYPOINT'                  : 16,   
    'MAV_CMD_NAV_LOITER_UNLIM'              : 17,   
    'MAV_CMD_NAV_LOITER_TURNS'              : 18,   
    'MAV_CMD_NAV_LOITER_TIME'               : 19,   
    'MAV_CMD_NAV_RETURN_TO_LAUNCH'          : 20,   
    'MAV_CMD_NAV_LAND'                      : 21,   
    'MAV_CMD_NAV_TAKEOFF'                   : 22,   
    'MAV_CMD_NAV_LAND_LOCAL'                : 23,   
    'MAV_CMD_NAV_TAKEOFF_LOCAL'             : 24,   
    'MAV_CMD_NAV_FOLLOW'                    : 25,   
    'MAV_CMD_NAV_CONTINUE_AND_CHANGE_ALT'   : 30,   
    'MAV_CMD_NAV_LOITER_TO_ALT'             : 31,   
    'MAV_CMD_DO_FOLLOW'                     : 32,   
    'MAV_CMD_DO_FOLLOW_REPOSITION'          : 33,   
    'MAV_CMD_NAV_ROI'                       : 80,   
    'MAV_CMD_NAV_PATHPLANNING'              : 81,   
    'MAV_CMD_NAV_SPLINE_WAYPOINT'           : 82,   
    'MAV_CMD_NAV_VTOL_TAKEOFF'              : 84,   
    'MAV_CMD_NAV_VTOL_LAND'                 : 85,   
    'MAV_CMD_NAV_GUIDED_ENABLE'             : 92,   
    'MAV_CMD_NAV_DELAY'                     : 93,   
    'MAV_CMD_NAV_LAST'                      : 95,   
    'MAV_CMD_CONDITION_DELAY'               : 112,  
    'MAV_CMD_CONDITION_CHANGE_ALT'          : 113,  
    'MAV_CMD_CONDITION_DISTANCE'            : 114,  
    'MAV_CMD_CONDITION_YAW'                 : 115,  
    'MAV_CMD_CONDITION_LAST'                : 159,  
    'MAV_CMD_DO_SET_MODE'                   : 176,  
    'MAV_CMD_DO_JUMP'                       : 177,  
    'MAV_CMD_DO_CHANGE_SPEED'               : 178,  
    'MAV_CMD_DO_SET_HOME'                   : 179,  
    'MAV_CMD_DO_SET_PARAMETER'              : 180,  
    'MAV_CMD_DO_SET_RELAY'                  : 181,  
    'MAV_CMD_DO_REPEAT_RELAY'               : 182,  
    'MAV_CMD_DO_SET_SERVO'                  : 183,  
    'MAV_CMD_DO_REPEAT_SERVO'               : 184,  
    'MAV_CMD_DO_FLIGHTTERMINATION'          : 185,  
    'MAV_CMD_DO_LAND_START'                 : 189,  
    'MAV_CMD_DO_RALLY_LAND'                 : 190,  
    'MAV_CMD_DO_GO_AROUND'                  : 191,  
    'MAV_CMD_DO_REPOSITION'                 : 192,  
    'MAV_CMD_DO_PAUSE_CONTINUE'             : 193,  
    'MAV_CMD_DO_CONTROL_VIDEO'              : 200,  
    'MAV_CMD_DO_SET_ROI'                    : 201,  
    'MAV_CMD_DO_DIGICAM_CONFIGURE'          : 202,  
    'MAV_CMD_DO_DIGICAM_CONTROL'            : 203,  
    'MAV_CMD_DO_MOUNT_CONFIGURE'            : 204,  
    'MAV_CMD_DO_MOUNT_CONTROL'              : 205,  
    'MAV_CMD_DO_SET_CAM_TRIGG_DIST'         : 206,  
    'MAV_CMD_DO_FENCE_ENABLE'               : 207,  
    'MAV_CMD_DO_PARACHUTE'                  : 208,  
    'MAV_CMD_DO_INVERTED_FLIGHT'            : 210,  
    'MAV_CMD_DO_MOUNT_CONTROL_QUAT'         : 220,  
    'MAV_CMD_DO_GUIDED_MASTER'              : 221,  
    'MAV_CMD_DO_GUIDED_LIMITS'              : 222,  
    'MAV_CMD_DO_LAST'                       : 240,  
    'MAV_CMD_PREFLIGHT_CALIBRATION'         : 241,  
    'MAV_CMD_PREFLIGHT_SET_SENSOR_OFFSETS'  : 242,  
    'MAV_CMD_PREFLIGHT_UAVCAN'              : 243,  
    'MAV_CMD_PREFLIGHT_STORAGE'             : 245,  
    'MAV_CMD_PREFLIGHT_REBOOT_SHUTDOWN'     : 246,  
    'MAV_CMD_OVERRIDE_GOTO'                 : 252,  
    'MAV_CMD_MISSION_START'                 : 300,  
    'MAV_CMD_COMPONENT_ARM_DISARM'          : 400,  
    'MAV_CMD_GET_HOME_POSITION'             : 410,  
    'MAV_CMD_START_RX_PAIR'                 : 500,  
    'MAV_CMD_GET_MESSAGE_INTERVAL'          : 510,  
    'MAV_CMD_SET_MESSAGE_INTERVAL'          : 511,  
    'MAV_CMD_REQUEST_AUTOPILOT_CAPABILITIE' : 520,  
    'MAV_CMD_IMAGE_START_CAPTURE'           : 2000, 
    'MAV_CMD_IMAGE_STOP_CAPTURE'            : 2001, 
    'MAV_CMD_DO_TRIGGER_CONTROL'            : 2003, 
    'MAV_CMD_VIDEO_START_CAPTURE'           : 2500, 
    'MAV_CMD_VIDEO_STOP_CAPTURE'            : 2501, 
    'MAV_CMD_PANORAMA_CREATE'               : 2800, 
    'MAV_CMD_DO_VTOL_TRANSITION'            : 3000, 
    'MAV_CMD_PAYLOAD_PREPARE_DEPLOY'        : 30001,        
    'MAV_CMD_PAYLOAD_CONTROL_DEPLOY'        : 30002,        
    'MAV_CMD_WAYPOINT_USER_1'               : 31000,        
    'MAV_CMD_WAYPOINT_USER_2'               : 31001,        
    'MAV_CMD_WAYPOINT_USER_3'               : 31002,        
    'MAV_CMD_WAYPOINT_USER_4'               : 31003,        
    'MAV_CMD_WAYPOINT_USER_5'               : 31004,        
    'MAV_CMD_SPATIAL_USER_1'                : 31005,        
    'MAV_CMD_SPATIAL_USER_2'                : 31006,        
    'MAV_CMD_SPATIAL_USER_3'                : 31007,        
    'MAV_CMD_SPATIAL_USER_4'                : 31008,        
    'MAV_CMD_SPATIAL_USER_5'                : 31009,        
    'MAV_CMD_USER_1'                        : 31010,        
    'MAV_CMD_USER_2'                        : 31011,        
    'MAV_CMD_USER_3'                        : 31012,        
    'MAV_CMD_USER_4'                        : 31013,        
    'MAV_CMD_USER_5'                        : 31014
    }


msg_tab_inv = {v: k for (k, v) in msg_tab.items()}

# list of all the password that allow a client to become Controller
password = ['LISLIS', 'MavRic4Ever']


msg_listener = {
    # initialize to empty but filled during the program, it contain the following structur:
    # name : [value, frequency, time of the last message received]
}

# typicall tab msg_listener when sent will be like :

# {
#     "VFR_HUD": [{
#         "throttle": 0,
#         "groundspeed": 1.872008965619898e-06,
#         "airspeed": 1.872008965619898e-06,
#         "heading": 0,
#         "mavpackettype": "VFR_HUD",
#         "climb": -6.59714032735792e-07,
#         "alt": 400.0
#     }, 1.98, 1463486205.414974], #freq, last_time_update
#     "LOCAL_POSITION_NED_COV": [{
#         "x": 0.0,
#         "mavpackettype": "LOCAL_POSITION_NED_COV",
#         "z": 0.2000005543231964,
#         "y": 0.0,
#         "time_utc": 0,
#         "time_boot_ms": 208957,
#         "covariance":[0.000894,       0.054922,       0.012136,       0.0,            -9.49467-06, 
#                       0.0,            0.0,            0.0,            0.0,            0.0, 
#                       1.25874e-05,    0.0,            -6.69287e-06,   0.0,            0.0, 
#                       0.0,            5.14784e-16,    0.0,            5.40628e-09,    0.0, 
#                       0.0,            0.0,            0.0,            0.0,            0.0005891, 
#                       0.0,            -0.000313,      0.0,            0.0,            0.0, 
#                       8.8131e-11,     0.0,            0.000925,       0.0,            0.0, 
#                       0.0,            0.0,            0.0,            -0.001273,      0.0, 
#                       0.000677,       0.0,            0.0,            0.0,            1.0],
#         "ax": 0.0,
#         "ay": 0.0,
#         "estimator_type": 0,
#         "vx": 0.0,
#         "vy": 0.0,
#         "vz": 3.3744698157534e-05,
#         "az": 0.0002698793832678348
#     }, 9.95, 1463486205.768147],
#     "RC_CHANNELS_SCALED": [{
#         "chan8_scaled": 32767,
#         "chan3_scaled": 0,
#         "chan7_scaled": 32767,
#         "time_boot_ms": 208593,
#         "chan4_scaled": 0,
#         "chan5_scaled": 0,
#         "chan2_scaled": 0,
#         "chan6_scaled": 0,
#         "mavpackettype": "RC_CHANNELS_SCALED",
#         "port": 1,
#         "chan1_scaled": 0,
#         "rssi": 64
#     }, 16710.37, 1463486205.414846],
#     "AUTOPILOT_VERSION": [{
#         "os_custom_version": [76, 69, 81, 117, 97, 100, 76, 73],
#         "product_id": 0,
#         "os_sw_version": 0,
#         "middleware_sw_version": 17104896,
#         "vendor_id": 0,
#         "capabilities": 0,
#         "flight_sw_version": 0,
#         "board_version": 0,
#         "middleware_custom_version": [100, 98, 102, 52, 48, 52, 48, 0],
#         "flight_custom_version": [100, 98, 102, 52, 48, 52, 48, 0],
#         "mavpackettype": "AUTOPILOT_VERSION",
#         "uid": 0
#     }, 0.99, 1463486192.688938],
#     "LOCAL_POSITION_NED": [{
#         "x": -9.322438927483745e-07,
#         "time_boot_ms": 208585,
#         "y": 0.0,
#         "mavpackettype": "LOCAL_POSITION_NED",
#         "vx": -1.8795071810018271e-06,
#         "vy": 0.0,
#         "vz": 6.690700047329301e-07,
#         "z": 3.3186370274052024e-07
#     }, 1.98, 1463486205.414644],
#     "ATTITUDE": [{
#         "pitchspeed": -7.267267343458172e-11,
#         "yaw": 0.0,
#         "rollspeed": 0.0,
#         "time_boot_ms": 208765,
#         "pitch": 1.9075002910540206e-07,
#         "mavpackettype": "ATTITUDE",
#         "yawspeed": 0.0,
#         "roll": 0.0
#     }, 4.93, 1463486205.616496],
#     "COMMAND_ACK": [{
#         "mavpackettype": "COMMAND_ACK",
#         "command": 520,
#         "result": 0
#     }, 0.99, 1463486192.689013],
#     "NAMED_VALUE_FLOAT": [{
#         "mavpackettype": "NAMED_VALUE_FLOAT",
#         "time_boot_ms": 208821,
#         "value": 5.0,
#         "name": "stabExTime"
#     }, 18558.87, 1463486205.616865],
#     "ATTITUDE_QUATERNION": [{
#         "q1": 1.0000044107437134,
#         "q3": 9.537977518903062e-08,
#         "q2": 0.0,
#         "q4": 0.0,
#         "pitchspeed": -7.268816104577525e-11,
#         "rollspeed": 0.0,
#         "time_boot_ms": 208589,
#         "mavpackettype": "ATTITUDE_QUATERNION",
#         "yawspeed": 0.0
#     }, 1.98, 1463486205.414718],
#     "SCALED_PRESSURE": [{
#         "mavpackettype": "SCALED_PRESSURE",
#         "press_abs": 400.0,
#         "time_boot_ms": 208605,
#         "temperature": 24,
#         "press_diff": -0.0
#     }, 1.98, 1463486205.415032],
#     "RC_CHANNELS_RAW": [{
#         "chan4_raw": 1024,
#         "chan2_raw": 1024,
#         "chan6_raw": 1024,
#         "time_boot_ms": 208829,
#         "chan1_raw": 1024,
#         "chan5_raw": 1024,
#         "chan3_raw": 1024,
#         "mavpackettype": "RC_CHANNELS_RAW",
#         "chan7_raw": 65535,
#         "chan8_raw": 65535,
#         "port": 1,
#         "rssi": 0
#     }, 11214.72, 1463486205.61714],
#     "SERVO_OUTPUT_RAW": [{
#         "servo4_raw": 950,
#         "servo2_raw": 950,
#         "servo6_raw": 0,
#         "time_usec": 208609170,
#         "servo1_raw": 950,
#         "servo8_raw": 0,
#         "servo5_raw": 0,
#         "mavpackettype": "SERVO_OUTPUT_RAW",
#         "servo3_raw": 950,
#         "port": 0,
#         "servo7_raw": 0
#     }, 0.99, 1463486205.415095],
#     "GPS_RAW_INT": [{
#         "fix_type": 3,
#         "cog": 0,
#         "epv": 300,
#         "lon": 65660448,
#         "time_usec": 208551584,
#         "eph": 100,
#         "satellites_visible": 5,
#         "lat": 465185241,
#         "mavpackettype": "GPS_RAW_INT",
#         "alt": 400000,
#         "vel": 0
#     }, 0.99, 1463486205.415369],
#     "DISTANCE_SENSOR": [{
#         "orientation": 0,
#         "covariance": 0,
#         "time_boot_ms": 208597,
#         "current_distance": 20,
#         "max_distance": 0,
#         "mavpackettype": "DISTANCE_SENSOR",
#         "type": 1,
#         "id": 0,
#         "min_distance": 0
#     }, 1.98, 1463486205.414907],
#     "HEARTBEAT": [{
#         "base_mode": 96,
#         "system_status": 3,
#         "custom_mode": 0,
#         "autopilot": 18,
#         "mavpackettype": "HEARTBEAT",
#         "type": 2,
#         "mavlink_version": 3
#     }, 1.04, 1463486205.617332],
#     "SCALED_IMU": [{
#         "xgyro": 0,
#         "ygyro": 0,
#         "xmag": 469,
#         "time_boot_ms": 208833,
#         "xacc": 0,
#         "zacc": -999,
#         "yacc": 0,
#         "zgyro": 0,
#         "mavpackettype": "SCALED_IMU",
#         "ymag": 0,
#         "zmag": 882
#     }, 4.93, 1463486205.617206],
#     "GLOBAL_POSITION_INT": [{
#         "lat": 465185241,
#         "lon": 65660448,
#         "time_boot_ms": 208825,
#         "hdg": 0,
#         "relative_alt": 0,
#         "mavpackettype": "GLOBAL_POSITION_INT",
#         "vx": 0,
#         "vy": 0,
#         "alt": 400000,
#         "vz": 0
#     }, 4.93, 1463486205.616953],
#     "SYS_STATUS": [{
#         "onboard_control_sensors_present": 64551,
#         "load": 0,
#         "battery_remaining": 91,
#         "errors_count4": 0,
#         "drop_rate_comm": 0,
#         "errors_count2": 0,
#         "errors_count3": 0,
#         "errors_comm": 0,
#         "current_battery": 0,
#         "errors_count1": 0,
#         "onboard_control_sensors_health": 64551,
#         "mavpackettype": "SYS_STATUS",
#         "onboard_control_sensors_enabled": 64551,
#         "voltage_battery": 12340
#     }, 0.99, 1463486205.415198]
# }