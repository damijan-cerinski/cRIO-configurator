from enum import Enum


class Unit(Enum):


    NOTUSED = 0
    UNIT1 = 1
    UNIT2 = 2
    UNIT3 = 3
    UNIT4 = 4
    UNIT5 = 5
    UNIT6 = 6
    UNIT7 = 7
    UNIT8 = 8
    UNIT9 = 9
    UNIT10 = 10
    UNIT11 = 11
    UNIT12 = 12
    UNIT13 = 13
    UNIT14 = 14
    UNIT15 = 15
    UNIT16 = 16
    UNIT17 = 17
    UNIT18 = 18
    UNIT19 = 19
    UNIT20 = 20
    #This static method returns Unit enum from string in CoDiS configuration file.
    @staticmethod
    def get_unit(str):
        if str.lower() == 'notused':
            return Unit.NOTUSED
        if str.lower()[:4] == 'unit' and str[4:].isdecimal():
            i = int(str[4:])
            if i <= 20:
                return Unit(i)
            else:
                raise ValueError('Unit string name not recognized.')
        raise ValueError('Unit string name not recognized.')

    @staticmethod
    def get_string(unit):
        if unit == Unit.NOTUSED: return "Not used"
        if unit == Unit.UNIT1: return "unit1"
        if unit == Unit.UNIT2: return "unit2"
        if unit == Unit.UNIT3: return "unit3"
        if unit == Unit.UNIT4: return "unit4"
        if unit == Unit.UNIT5: return "unit5"
        if unit == Unit.UNIT6: return "unit6"
        if unit == Unit.UNIT7: return "unit7"
        if unit == Unit.UNIT8: return "unit8"
        if unit == Unit.UNIT9: return "unit9"
        if unit == Unit.UNIT10: return "unit10"
        if unit == Unit.UNIT11: return "unit11"
        if unit == Unit.UNIT12: return "unit12"
        if unit == Unit.UNIT13: return "unit13"
        if unit == Unit.UNIT14: return "unit14"
        if unit == Unit.UNIT15: return "unit15"
        if unit == Unit.UNIT16: return "unit16"
        if unit == Unit.UNIT17: return "unit17"
        if unit == Unit.UNIT18: return "unit18"
        if unit == Unit.UNIT19: return "unit19"
        if unit == Unit.UNIT20: return "unit20"

    
class Source(Enum):


    NOTUSED = 0
    SOURCE0 = 1
    SOURCE1 = 2
    SOURCE2 = 3
    SOURCE3 = 4
    SOURCE4 = 5
    SOURCE5 = 6
    SOURCE6 = 7
    SOURCE7 = 8
    SOURCE8 = 9
    SOURCE9 = 10
    SOURCE10 = 11
    SOURCE11 = 12
    SOURCE12 = 13
    SOURCE13 = 14
    SOURCE14 = 15
    SOURCE15 = 16
    SOURCE16 = 17
    SOURCE17 = 18
    SOURCE18 = 19
    SOURCE19 = 20
    SOURCE20 = 21

    #This static method returns Source enum from string in CoDiS configuration file.
    @staticmethod
    def get_source(str):
        if str.lower() == 'notused':
            return Source.NOTUSED
        if str.lower()[:6] == 'source' and str[6:].isdecimal():
            i = int(str[6:])+1
            if i <= 21:
                return Source(i)
            else:
                raise ValueError('Source string name not recognized.')
        raise ValueError('Source string name not recognized.')

    @staticmethod
    def get_string(source):
        if source == Source.NOTUSED: return "Not used"
        if source == Source.SOURCE0: return "source0"
        if source == Source.SOURCE1: return "source1"
        if source == Source.SOURCE2: return "source2"
        if source == Source.SOURCE3: return "source3"
        if source == Source.SOURCE4: return "source4"
        if source == Source.SOURCE5: return "source5"
        if source == Source.SOURCE6: return "source6"
        if source == Source.SOURCE7: return "source7"
        if source == Source.SOURCE8: return "source8"
        if source == Source.SOURCE9: return "source9"
        if source == Source.SOURCE10: return "source10"
        if source == Source.SOURCE11: return "source11"
        if source == Source.SOURCE12: return "source12"
        if source == Source.SOURCE13: return "source13"
        if source == Source.SOURCE14: return "source14"
        if source == Source.SOURCE15: return "source15"
        if source == Source.SOURCE16: return "source16"
        if source == Source.SOURCE17: return "source17"
        if source == Source.SOURCE18: return "source18"
        if source == Source.SOURCE19: return "source19"
        if source == Source.SOURCE20: return "source20"

class BearingAnalyses(Enum):


    S_MAX = 0
    SP2P_MAX = 1
    
    @staticmethod
    def get_bearing_analysis(str):
        if str == 'Smax': return BearingAnalyses.S_MAX
        if str == 'SP2Pmax': return BearingAnalyses.SP2P_MAX
        raise ValueError('Analysis string name not recognized.')
    
    @staticmethod
    def get_string(bearing_analysis):
        if bearing_analysis == BearingAnalyses.S_MAX: return "Smax"
        if bearing_analysis == BearingAnalyses.SP2P_MAX: return 'SP2Pmax '


class UnitAnalyses(Enum):


    RPM = 0
    ACT_REACT_PWR = 1
    LOAD_ANGLE = 2

    @staticmethod
    def get_unit_analysis(str):
        if str == 'rpm': return UnitAnalyses.RPM
        if str == 'act&reactPowers': return UnitAnalyses.ACT_REACT_PWR
        if str == 'loadAngle': return UnitAnalyses.LOAD_ANGLE
        raise ValueError('Analysis string name not recognized.')
    
    @staticmethod
    def get_string(unit_analysis):
        if unit_analysis == UnitAnalyses.RPM: return "Rotational speed"
        if unit_analysis == UnitAnalyses.ACT_REACT_PWR: return "Active and reactive power"
        if unit_analysis == UnitAnalyses.LOAD_ANGLE: return "Load angle"


class ChannelAnalyses(Enum):


    SNA_PH = 0
    EQ_PEAK = 1
    RMS = 2
    AIR_GAP = 3
    DC = 4
    SIGNAL_FREQUENCY = 5
    THD = 6
    PEAK2PEAK = 7
    REST = 8
    RPM = 9

    @staticmethod
    def get_channel_analysis(str):
        if str == 'snA&Ph': return ChannelAnalyses.SNA_PH
        if str == 'eqPeak': return ChannelAnalyses.EQ_PEAK
        if str == 'airGap': return ChannelAnalyses.AIR_GAP
        if str == 'rms': return ChannelAnalyses.RMS
        if str == 'dc': return ChannelAnalyses.DC
        if str == 'signalFrequency': return ChannelAnalyses.SIGNAL_FREQUENCY
        if str == 'thd': return ChannelAnalyses.THD
        if str == 'peak2peak': return ChannelAnalyses.PEAK2PEAK
        if str == 'rest': return ChannelAnalyses.REST
        if str == 'rpm': return ChannelAnalyses.RPM
        raise ValueError('Analysis string name not recognized.')
    
    @staticmethod
    def get_string(channel_analysis):
        if channel_analysis == ChannelAnalyses.SNA_PH: return "Harmonic"
        if channel_analysis == ChannelAnalyses.EQ_PEAK: return "Equivalent peak"
        if channel_analysis == ChannelAnalyses.RMS: return "Rms"
        if channel_analysis == ChannelAnalyses.AIR_GAP: return "Air gap"
        if channel_analysis == ChannelAnalyses.DC: return "Dc"
        if channel_analysis == ChannelAnalyses.SIGNAL_FREQUENCY: return "Signal frequency"
        if channel_analysis == ChannelAnalyses.THD: return "Thd"
        if channel_analysis == ChannelAnalyses.PEAK2PEAK: return "Peak2Peak"
        if channel_analysis == ChannelAnalyses.REST: return "Rest"
        if channel_analysis == ChannelAnalyses.RPM: return "Rotational speed"


FILTER_TYPE_LABEL_NAME_PAIRS = [
    {'name': 'Lowpass', 'label': 'Lowpass'},
    {'name': 'Highpass', 'label': 'Highpass'},
    {'name': 'Bandpass', 'label': 'Bandpass'},
    {'name': 'Bandstop', 'label': 'Bandstop'}
]

INTEGRATE_TYPE_LABEL_NAME_PAIRS = [
    {'name': 'Do not integrate', 'label': 'Do not integrate'},
    {'name': 'Integrate once', 'label': 'Integrate once'},
    {'name': 'Integrate twice', 'label': 'Integrate twice'}
]

REGISTER_TYPE_LABEL_NAME_PAIRS = [
    {'name': 'holdingRegisters', 'label': 'holdingRegisters'},
    {'name': 'inputRegisters', 'label': 'inputRegisters'}
]

MODBUS_DATA_TYPE_LABEL_NAME_PAIRS = [
    {'name': 'Float-LoHi', 'label': 'floatLoHi'},
    {'name': 'Float-HiLo', 'label': 'floatHiLo'},
    {'name': 'Unsigned integer', 'label': 'unsignedInteger'},
    {'name': 'Signed integer', 'label': 'signedInteger'}
]