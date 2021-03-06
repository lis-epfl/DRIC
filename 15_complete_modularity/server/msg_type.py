

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
    'PLOT_RATE'         : 103, # 1 int value : the rate in seconde, if rate=-1, it means 'stop sending data'
    'PLOT_NEW_DATA'     : 104, # 4 tab of 2 values each, 4 tab for each trace and first value for msg (e.g : 'ATTITUDE') 2nd for type (e.g : 'pitch')
    'GET_LOC'           : 105, # 1 value : if -1, just want to get the coord, is >0, want to get a this period the coord
    'GET_OBP'           : 106, # 1 value, the OBP (string), if the OBP is 'ALL', then the server will send 'OBP_VALUE_ALL'
    'SET_OBP'           : 107, # 2 values, the OBP (string) and the float value of the OBP to change
    'SWITCH_STATE'      : 108, # 1 value password if client want to become controller, or '' if client want to become observer
    'ASK_CLIENT_STATUS' : 109, # 1 value, ask what is the client status, nedd to transmit a code that will be returned
    'MAVLINK_MESSAGE'   : 110, # see with julien
    'MAVLINK_COMMAND'   : 111, # 9 values to send a mavlink command (see vehicle.message_factory.command_long_send? or dronekit doc or below)
    'GET_GRAPH_DATA'    : 112, # no value
}

# MAVLINK_COMMAND parameter:
#  1: Command:              (it's a MAV_CMD enum, see below)
#  2: Confirmation
#  3: Parameter 1
#  4: Parameter 2
#  5: Parameter 3
#  6: Parameter 4
#  7: Parameter 5
#  8: Parameter 6
#  9: Parameter 7

# MAVLINK_MESSAGE parameter:

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

# typicall tab msg_listener value, look at the appendix of the report.

###
# filename : msg_type.py
#
# description: declar many array very usefull
#
# Work made at the Labotory of Inteligent System at EPFL.
#
# Autor : Stephane Ballmer
#
# Last change: 15/06/2016
###
