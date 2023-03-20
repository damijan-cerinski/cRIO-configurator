from enum import Enum

class ItemType(Enum):
    UNIT_SOURCE = 0
    BEARINGS_LIST = 1
    BEARING = 2
    BEARING_ANALYSES_LIST = 3
    BEARING_ANALYSIS = 4
    REGIMES_LIST = 5
    REGIME = 6
    UNIT_ANALYSES_LIST = 7
    UNIT_ANALYSIS = 8
    CHANNELS_LIST = 9
    CHANNEL = 10
    CHANNEL_ANALYSES_LIST = 11
    CHANNEL_ANALYSIS = 12
    PHYSICAL_CHANNEL = 13
    SLOPE = 14
    INTERCEPT = 15
    AIR_GAP_PLANES_LIST = 16
    AIR_GAP_PLANE = 17
    ALARMS_LIST = 18
    ALARM = 19
    MODBUS_LIST = 20


class Item:
    def __init__(self, item_type, item_data, item_id = ''):
        self.item_id = item_id
        self.item_type = item_type
        self.item_data = item_data

    def get_item_type(self):
        return self.item_type

    def get_item_data(self):
        return self.item_data
    
    def get_item_id(self):
        return self.item_id

    def set_item_id(self, item_id):
        self.item_id = item_id
