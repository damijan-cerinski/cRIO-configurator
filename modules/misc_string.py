def get_channel_info_line(table, param):
        #-----------------------------------------------------------
        #table: Label_name_pairs of channels
        #param: channel param dict from main cluster
        #-----------------------------------------------------------
        NAME_LENGTH = 20
        PHYSICAL_CHANNEL_LENGTH = 20
        SLOPE_LENGTH = 20
        INTERCEPT_LENGTH = 20
        FILTER_LENGTH = 20
        FILTER_TYPE_LENGTH = 20
        INTEGRATION_LENGTH = 20

        s = ''
        name = table.get_name(param['label'])[:NAME_LENGTH]
        s = s + name
        for i in range(NAME_LENGTH - len(name)+1):
                s = s + ' '
        ph_ch = str(param['physicalChannel'])[:PHYSICAL_CHANNEL_LENGTH]
        s = s + ph_ch
        for i in range(PHYSICAL_CHANNEL_LENGTH - len(ph_ch)+1):
                s = s + ' '
        slope = str(param['slope'])[:SLOPE_LENGTH]
        s = s + slope
        for i in range(SLOPE_LENGTH - len(slope)+1):
                s = s + ' '
        intercept = str(param['intercept'])[:INTERCEPT_LENGTH]
        s = s + intercept
        for i in range(INTERCEPT_LENGTH - len(intercept)+1):
                s = s + ' '
        if 'filter' in param:
                filter = param['filter']
        else:
                filter = False
        filter_str = "Yes" if filter else "No"
        s = s + filter_str
        for i in range(FILTER_LENGTH - len(filter_str)+1):
                s = s + ' '
        if 'filterType' in param:
                filter_type = param['filterType']
        else:
                filter_type = '-'
        if not filter:
               filter_type = '-'
        s = s + filter_type
        for i in range(FILTER_TYPE_LENGTH - len(filter_type)+1):
                s = s + ' '
        if 'integration' in param:
                if param['integration'] == 'Do not integrate':
                        integration_str = '-'
                else:
                        integration_str = param['integration']
        s = s + integration_str
        s = s + '\n'
        return s

def get_channel_list_info(table, param):
        s = 'Channel              Physical channel     Slope                Intercept            Filter               Filter type          Integration\n\n'
        for i in param:
                s = s + get_channel_info_line(table, i)
        return s


def get_alarm_info_line(table, param):
        ALARM_LENGTH = 40
        DELAY_LENGTH = 20
        PRIORITY_LENGTH = 20

        s = ''
        ls = param['logicalSentence']
        for i in table:
                new_str = "'"+f"{i['name']}"+"'"
                ls = ls.replace(i['label'], new_str)
        ls = ls[:ALARM_LENGTH]
        s = s + ls
        for i in range(ALARM_LENGTH - len(ls)+1):
                s = s + ' '
        delay = str(param['delay'])[:DELAY_LENGTH]
        s = s + delay
        for i in range(DELAY_LENGTH - len(delay)+1):
                s = s + ' '
        priority = str(param['alarmPriority'])[:PRIORITY_LENGTH]
        s = s + priority
        s = s + '\n'
        return s

def get_alarms_list_info(table, param):
        s = 'Alarm                                    Delay [s]            Priority\n\n'
        for i in param:
                s = s + get_alarm_info_line(table, i)
        return s


def get_regime_info_line(table_regimes, table_signals, param):
        NAME_LENGTH = 20
        REGIME_LDF_LENGTH = 80

        s = ''
        name = table_regimes.get_name(param['label'])[:NAME_LENGTH]
        s += name
        for i in range(NAME_LENGTH - len(name)+1):
                s += ' '
        regime_ldf = param['regimeLogicalDefinitionStatement']
        for i in table_signals:
                new_str = "'"+f"{i['name']}"+"'"
                regime_ldf = regime_ldf.replace(i['label'], new_str)
        regime_ldf = regime_ldf[:REGIME_LDF_LENGTH]
        s += regime_ldf
        s += '\n'
        return s

def get_regimes_list_info(table_regimes, table_signals, param):
        s = 'Regime               Regime logical definition statement\n\n'
        for i in param:
                s = s + get_regime_info_line(table_regimes, table_signals, i)
        return s


def get_air_gap_plane_info_line(table_agp, table_sensors, param):
        NAME_LENGTH = 20
        SENSORS_LENGTH = 100

        s = ''
        name = table_agp.get_name(param['label'])[:NAME_LENGTH]
        s += name
        for i in range(NAME_LENGTH - len(name)+1):
                s += ' '
        sensors = param['sensors']
        for i in sensors:
                sensor_name = table_sensors.get_name(i)
                s += f'{sensor_name}, '
        s = s[:-2]
        s = s[:SENSORS_LENGTH]
        s += '\n'
        return s

def get_air_gap_planes_list_info(table_agp, table_sensors, param):
        s = 'Air gap planes       Sensors\n\n'
        for i in param:
                s = s + get_air_gap_plane_info_line(table_agp, table_sensors, i)
        return s


def get_bearing_plane_info_line(table_bearings, table_sensors, param):
        NAME_LENGTH = 20
        X_SENSOR_LENGTH = 20
        Y_SENSOR_LENGTH = 20
        ROTATION_LENGTH = 30
        ANGLE_LENGTH = 20

        s = ''
        name = table_bearings.get_name(param['label'])[:NAME_LENGTH]
        s += name
        for i in range(NAME_LENGTH - len(name)+1):
                s += ' '
        x_sensor = table_sensors.get_name(param['xDirection'])[:X_SENSOR_LENGTH]
        s += x_sensor
        for i in range(X_SENSOR_LENGTH - len(x_sensor)+1):
                s += ' '
        y_sensor = table_sensors.get_name(param['yDirection'])[:Y_SENSOR_LENGTH]
        s += y_sensor
        for i in range(Y_SENSOR_LENGTH - len(y_sensor)+1):
                s += ' '
        if 'rotate' in param:
                rotation = param['rotate']
        else:
                rotation = False
        rotation_str = "Yes" if rotation else "No"
        s += rotation_str
        for i in range(ROTATION_LENGTH - len(rotation_str)+1):
                s += ' '
        angle = str(param['rotationAngle'])[:ANGLE_LENGTH]
        s += angle
        s += '\n'
        return s


def get_bearing_planes_list_info(table_bearings, table_sensors, param):
        s = 'Bearing planes       X-direction Sensor   Y-direction Sensor   Coordinate System Rotation     Angle of rotation\n\n'
        for i in param:
                s = s + get_bearing_plane_info_line(table_bearings, table_sensors, i)
        return s