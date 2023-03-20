from tkinter import *
from .codis_enums import Unit, Source, ChannelAnalyses
from .codis_enums import UnitAnalyses, BearingAnalyses
from .tree_items import ItemType
from .main_window import Main_window
from .uploading import UploadingProcess

class App():

    def __init__(self):
        self.system_settings = []
        self.main_cluster = []
        self.root = Tk()
        self.main_win = Main_window(
            update_param = self.update_param,
            get_param_value = self.get_param_value,
            add_bearing = self.add_bearing,
            remove_bearing = self.remove_bearing,
            add_air_gap_plane = self.add_air_gap_plane,
            remove_air_gap_plane = self.remove_air_gap_plane,
            get_bearing_analysis_type = self.get_bearing_analysis_type,
            add_bearing_analysis = self.add_bearing_analysis,
            remove_bearing_analysis = self.remove_bearing_analysis,
            add_alarm = self.add_alarm,
            remove_alarm = self.remove_alarm,
            add_regime = self.add_regime,
            remove_regime = self.remove_regime,
            add_regime_to_air_gap = self.add_regime_to_air_gap,
            remove_regime_from_air_gap = self.remove_regime_from_air_gap,
            add_channel = self.add_channel,
            remove_channel = self.remove_channel,
            remove_channel_from_other_items = self.remove_channel_from_other_items,
            get_channel_element = self.get_channel_element,
            get_channel_analysis_type = self.get_channel_analysis_type,
            add_channel_analysis = self.add_channel_analysis,
            get_unit_analysis_type = self.get_unit_analysis_type,
            add_unit_analysis = self.add_unit_analysis,
            remove_channel_analysis = self.remove_channel_analysis,
            remove_unit_analysis = self.remove_unit_analysis,
            add_condition_vector_element = self.add_condition_vector_element,
            get_condition_vector_element = self.get_condition_vector_element,
            remove_condition_vector_element =
            self.remove_condition_vector_element,
            get_bearing_labels_from_mc = self.get_bearing_labels_from_mc,
            get_air_gap_plane_labels_from_mc = self.get_air_gap_plane_labels_from_mc,
            get_sensor_labels_from_mc = self.get_sensor_labels_from_mc,
            get_regime_labels_from_mc = self.get_regime_labels_from_mc,
            get_signal_labels_from_mc = self.get_signal_labels_from_mc,
            get_main_cluster = self.get_main_cluster,
            set_main_cluster = self.set_main_cluster,
            get_main_cluster_index = self.get_main_cluster_index,
            get_system_settings = self.get_system_settings,
            set_system_settings = self.set_system_settings,
            get_main_trigger_sensor = self.get_main_trigger_sensor,
            get_number_of_poles = self.get_number_of_poles,
            master = self.root)

    def run(self):
        self.root.wm_title("cRIO configurator")
        self.root.geometry("640x480")
        self.center(self.root)
        self.root.mainloop()

    def center(self, win):
        """
        centers a tkinter window
        :param win: the main window or Toplevel window to center
        """
        win.update_idletasks()
        width = win.winfo_width()
        frm_width = win.winfo_rootx() - win.winfo_x()
        win_width = width + 2 * frm_width
        height = win.winfo_height()
        titlebar_height = win.winfo_rooty() - win.winfo_y()
        win_height = height + titlebar_height + frm_width
        x = win.winfo_screenwidth() // 2 - win_width // 2
        y = win.winfo_screenheight() // 2 - win_height // 2
        win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        win.deiconify()

    def get_main_cluster(self):
        return list(self.main_cluster)

    def set_main_cluster(self, main_cluster):
        self.main_cluster = main_cluster

    def get_system_settings(self):
        return dict(self.system_settings)

    def set_system_settings(self, system_settings):
        self.system_settings = system_settings

    def get_main_cluster_index(self, unit, source):
        index = 0
        for i in self.get_main_cluster():
            try:
                u = Unit.get_unit(i['unitName'])
                s = Source.get_source(i['sourceName'])
                if u == unit and s == source:
                    return index
            except ValueError:
                print("Unit or Source from m. cluster settings not recognized.")
            index += 1
        return -1

    def get_wav_channel_index(self, unit, source, label):
        index_main = self.get_main_cluster_index(unit, source)
        if index_main != -1:
            index = 0
            wavs = self.main_cluster[index_main]['waveformCluster']['waveforms']
            for i in wavs:
                if i['label'] == label:
                    return index
                index += 1
            return -1
        else:
            return -1

    def get_bearing_index(self, unit, source, label):
        index_main = self.get_main_cluster_index(unit, source)
        if index_main != -1:
            index = 0
            bear = self.main_cluster[index_main]['waveformCluster']['bearings']
            for i in bear:
                if i['label'] == label:
                    return index
                index += 1
            return -1
        else:
            return -1

    def get_regime_index(self, unit, source, label):
        index_main = self.get_main_cluster_index(unit, source)
        if index_main != -1:
            index = 0
            regimes = self.main_cluster[index_main]['conditionVectorCluster']['regimesDefinition']
            for i in regimes:
                if i['label'] == label:
                    return index
                index += 1
            return -1
        else:
            return -1

    def get_air_gap_plane_index(self, unit, source, label):
        index_main = self.get_main_cluster_index(unit, source)
        if index_main != -1:
            index = 0
            agp = self.main_cluster[index_main]['waveformCluster']['airGapPlanes']
            for i in agp:
                if i['label'] == label:
                    return index
                index += 1
            return -1
        else:
            return -1

    def get_sensor_labels_from_mc(self, unit, source):
        index_main = self.get_main_cluster_index(unit, source)
        if index_main != -1:
                labels = []
                w_c = self.main_cluster[index_main]['waveformCluster']
                wavs = w_c['waveforms']
                for j in wavs:
                    labels.append(j['label'])
                return labels
        return []
    
    def get_bearing_labels_from_mc(self, unit, source):
        index_main = self.get_main_cluster_index(unit, source)
        if index_main != -1:
                labels = []
                w_c = self.main_cluster[index_main]['waveformCluster']
                bearings = w_c['bearings']
                for j in bearings:
                    labels.append(j['label'])
                return labels
        return []

    def get_air_gap_plane_labels_from_mc(self, unit, source):
        index_main = self.get_main_cluster_index(unit, source)
        if index_main != -1:
                labels = []
                w_c = self.main_cluster[index_main]['waveformCluster']
                agp = w_c['airGapPlanes']
                for j in agp:
                    labels.append(j['label'])
                return labels
        return []

    def get_regime_labels_from_mc(self, unit, source):
        index_main = self.get_main_cluster_index(unit, source)
        if index_main != -1:
                labels = []
                c_v_c = self.main_cluster[index_main]['conditionVectorCluster']
                regimes = c_v_c['regimesDefinition']
                for j in regimes:
                    labels.append(j['label'])
                return labels
        return []
    
    def get_signal_labels_from_mc(self, unit, source):
        index_main = self.get_main_cluster_index(unit, source)
        if index_main != -1:
                labels = []
                c_v_c = self.main_cluster[index_main]['conditionVectorCluster']
                c_v_e = c_v_c['conditionVectorElements']
                for j in c_v_e:
                    labels.append(j['label'])
                return labels
        return []
    
    def get_main_trigger_sensor(self, unit, source):
        index_main = self.get_main_cluster_index(unit, source)
        if index_main != -1:
            un = self.main_cluster[index_main]['waveformCluster']['unit']
            if 'mainTriggerSensor' in un:
                return un['mainTriggerSensor']
            else:
                return None
        else:
            return None

    def get_number_of_poles(self, unit, source):
        index_main = self.get_main_cluster_index(unit, source)
        if index_main != -1:
            un = self.main_cluster[index_main]['waveformCluster']['unit']
            if 'numberOfPoles' in un:
                return un['numberOfPoles']
            else:
                return None
        else:
            return None

#------------------------------------------------------------------
#              Main cluster handling by tree elements
#------------------------------------------------------------------ 
    def update_param(self, item, new_value):
        unit = item.get_item_data()['unitName']
        source = item.get_item_data()['sourceName']
        t = item.get_item_type()
        index_main = self.get_main_cluster_index(unit, source)
        if index_main == -1: return
        if t == ItemType.UNIT_SOURCE:
            self.main_cluster[index_main]['waveformCluster']['unit'] = new_value
            return
        if t == ItemType.UNIT_ANALYSIS:
            analysis_index = item.get_item_data()['index']
            u = self.main_cluster[index_main]['waveformCluster']['unit']
            u['analyses'][analysis_index] = new_value
            return
        if t == ItemType.ALARM:
            index = item.get_item_data()['index']
            c_v_c = self.main_cluster[index_main]['conditionVectorCluster']
            c_v_c['alarms'][index] = new_value
            return
        if (
            t == ItemType.CHANNEL
            or t == ItemType.PHYSICAL_CHANNEL
            or t ==ItemType.SLOPE
            or t == ItemType.INTERCEPT
            or t == ItemType.CHANNEL_ANALYSIS
        ):
            label = item.get_item_data()['label']
            index_wav = self.get_wav_channel_index(unit, source, label)
            if index_wav == -1: return
            w_c = self.main_cluster[index_main]['waveformCluster']
            wav = w_c['waveforms'][index_wav]
            if t == ItemType.CHANNEL:
                w_c['waveforms'][index_wav] = new_value
            if t == ItemType.PHYSICAL_CHANNEL:
                wav['physicalChannel'] = new_value
            if t == ItemType.SLOPE:
                wav['slope'] = new_value
            if t == ItemType.INTERCEPT:
                wav['intercept'] = new_value
            if t == ItemType.CHANNEL_ANALYSIS:
                analysis_index = item.get_item_data()['index']
                wav['analyses'][analysis_index] = new_value
        if (
            t == ItemType.BEARING
            or t == ItemType.BEARING_ANALYSIS
        ):
            label = item.get_item_data()['label']
            index_bear = self.get_bearing_index(unit, source, label)
            if index_bear == -1: return
            w_c = self.main_cluster[index_main]['waveformCluster']
            bearings = w_c['bearings']
            bearing = bearings[index_bear]
            if t == ItemType.BEARING:
                bearings[index_bear] = new_value
            if t == ItemType.BEARING_ANALYSIS:
                analysis_index = item.get_item_data()['index']
                bearing['analyses'][analysis_index] = new_value
        if t == ItemType.REGIME:
            label = item.get_item_data()['label']
            index_reg = self.get_regime_index(unit, source, label)
            if index_reg == -1: return
            c_v_c = self.main_cluster[index_main]['conditionVectorCluster']
            reg_def = c_v_c['regimesDefinition']
            reg_def[index_reg] = new_value
        if t == ItemType.AIR_GAP_PLANE:
            label = item.get_item_data()['label']
            index_agp = self.get_air_gap_plane_index(unit, source, label)
            if index_agp == -1: return
            w_c = self.main_cluster[index_main]['waveformCluster']
            agp = w_c['airGapPlanes']
            agp[index_agp] = new_value

    def get_param_value(self, item):
        if(
            item.get_item_type() != ItemType.CHANNELS_LIST
            and item.get_item_type() != ItemType.CHANNEL
            and item.get_item_type() != ItemType.UNIT_SOURCE
            and item.get_item_type() != ItemType.CHANNEL_ANALYSES_LIST
            and item.get_item_type() != ItemType.PHYSICAL_CHANNEL
            and item.get_item_type() != ItemType.SLOPE
            and item.get_item_type() != ItemType.INTERCEPT
            and item.get_item_type() != ItemType.UNIT_ANALYSES_LIST
            and item.get_item_type() != ItemType.UNIT_ANALYSIS
            and item.get_item_type() != ItemType.CHANNEL_ANALYSIS
            and item.get_item_type() != ItemType.BEARINGS_LIST
            and item.get_item_type() != ItemType.BEARING_ANALYSES_LIST
            and item.get_item_type() != ItemType.BEARING_ANALYSIS
            and item.get_item_type() != ItemType.BEARING
            and item.get_item_type() != ItemType.REGIMES_LIST
            and item.get_item_type() != ItemType.REGIME
            and item.get_item_type() != ItemType.AIR_GAP_PLANES_LIST
            and item.get_item_type() != ItemType.AIR_GAP_PLANE
            and item.get_item_type() != ItemType.ALARMS_LIST
            and item.get_item_type() != ItemType.ALARM
        ):
            return 'Not yet implemented!'
        unit = item.get_item_data()['unitName']
        source = item.get_item_data()['sourceName']
        index_main = self.get_main_cluster_index(unit, source)
        if index_main != -1:
            if item.get_item_type() == ItemType.UNIT_SOURCE:
                v = self.main_cluster[index_main]['waveformCluster']['unit']
                return dict(v)
            if item.get_item_type() == ItemType.BEARINGS_LIST:
                v = self.main_cluster[index_main]['waveformCluster']['bearings']
                return list(v)
            if item.get_item_type() == ItemType.AIR_GAP_PLANES_LIST:
                v = self.main_cluster[index_main]['waveformCluster']['airGapPlanes']
                return list(v)
            if item.get_item_type() == ItemType.REGIMES_LIST:
                v = self.main_cluster[index_main]['conditionVectorCluster']['regimesDefinition']
                return list(v)
            if item.get_item_type() == ItemType.ALARMS_LIST:
                cv = self.main_cluster[index_main]['conditionVectorCluster']
                if 'alarms' in cv:
                    return list(cv['alarms'])
                else:
                    return []
            if item.get_item_type() == ItemType.ALARM:
                index = item.get_item_data()['index']
                cv = self.main_cluster[index_main]['conditionVectorCluster']
                return dict(cv['alarms'][index])
            if item.get_item_type() == ItemType.CHANNELS_LIST:
                v=self.main_cluster[index_main]['waveformCluster']['waveforms']
                return list(v)
            if item.get_item_type() == ItemType.UNIT_ANALYSES_LIST:
                v=self.main_cluster[index_main]['waveformCluster']['unit']['analyses']
                return list(v)
            if item.get_item_type() == ItemType.UNIT_ANALYSIS:
                analysis_index = item.get_item_data()['index']
                return dict(self.main_cluster[index_main]['waveformCluster']['unit']['analyses'][analysis_index])
            label = item.get_item_data()['label']
            index_wav = self.get_wav_channel_index(unit, source, label)
            if index_wav != -1:
                    w_c = self.main_cluster[index_main]['waveformCluster']
                    wav = w_c['waveforms'][index_wav]
                    if item.get_item_type() == ItemType.CHANNEL:
                        return dict(wav)
                    if item.get_item_type() == ItemType.CHANNEL_ANALYSES_LIST:
                        return list(wav['analyses'])
                    if item.get_item_type() == ItemType.PHYSICAL_CHANNEL:
                        return wav['physicalChannel']
                    if item.get_item_type() == ItemType.SLOPE:
                        return wav['slope']
                    if item.get_item_type() == ItemType.INTERCEPT:
                        return wav['intercept']
                    if item.get_item_type() == ItemType.CHANNEL_ANALYSIS:
                        analysis_index = item.get_item_data()['index']
                        return dict(wav['analyses'][analysis_index])
            index_bear = self.get_bearing_index(unit, source, label)
            if index_bear != -1:
                w_c = self.main_cluster[index_main]['waveformCluster']
                bearing = w_c['bearings'][index_bear]
                if item.get_item_type() == ItemType.BEARING:
                    return dict(bearing)
                if item.get_item_type() == ItemType.BEARING_ANALYSES_LIST:
                    return list(bearing['analyses'])
                if item.get_item_type() == ItemType.BEARING_ANALYSIS:
                    analysis_index = item.get_item_data()['index']
                    return dict(bearing['analyses'][analysis_index])
            index_reg = self.get_regime_index(unit, source, label)
            if index_reg != -1:
                c_v_c = self.main_cluster[index_main]['conditionVectorCluster']
                regime = c_v_c['regimesDefinition'][index_reg]
                if item.get_item_type() == ItemType.REGIME:
                    return dict(regime)
            index_agp = self.get_air_gap_plane_index(unit, source, label)
            if index_agp != -1:
                w_c = self.main_cluster[index_main]['waveformCluster']
                agp = w_c['airGapPlanes'][index_agp]
                if item.get_item_type() == ItemType.AIR_GAP_PLANE:
                    return dict(agp)
            else:
                return None
        else:
            return None


#------------------------------------------------------------------
#                              Bearings
#------------------------------------------------------------------

    def add_bearing(self, unit, source, value):
        #-----------------------------------------------------------
        #unit: codis_enums.Unit
        #source: codis_enums.Source
        #value: dict
        #index: int
        #-----------------------------------------------------------
        index_main = self.get_main_cluster_index(unit, source)
        if index_main != -1:
            bearings = self.main_cluster[index_main]['waveformCluster']['bearings']
            bearings.append(value)

    def remove_bearing(self, unit, source, label):
        index_main = self.get_main_cluster_index(unit, source)
        if index_main != -1:
            bearings = self.main_cluster[index_main]['waveformCluster']['bearings']
            index = 0
            for i in bearings:
                if i['label'] == label:
                    bearings.pop(index)
                index += 1
    
#------------------------------------------------------------------
#                              Alarms
#------------------------------------------------------------------
    def add_alarm(self, unit, source, value):
        index_main = self.get_main_cluster_index(unit, source)
        if index_main == -1: return
        c_v = self.main_cluster[index_main]['conditionVectorCluster']
        alarms = c_v['alarms']
        alarms.append(value)

    def remove_alarm(self, unit, source, index):
        index_main = self.get_main_cluster_index(unit, source)
        if index_main == -1: return
        c_v = self.main_cluster[index_main]['conditionVectorCluster']
        c_v['alarms'].pop(index)

#------------------------------------------------------------------
#                              Regimes
#------------------------------------------------------------------

    def add_regime(self, unit, source, value):
        index_main = self.get_main_cluster_index(unit, source)
        if index_main != -1:
            reg_def = self.main_cluster[index_main]['conditionVectorCluster']['regimesDefinition']
            reg_def.append(value)
    
    def remove_regime(self, unit, source, label):
        index_main = self.get_main_cluster_index(unit, source)
        if index_main != -1:
            reg_def = self.main_cluster[index_main]['conditionVectorCluster']['regimesDefinition']
            index = 0
            for i in reg_def:
                if i['label'] == label:
                    reg_def.pop(index)
                index += 1

    def remove_regime_from_air_gap(self, unit, source, channel_label, regime_label):
        index_main = self.get_main_cluster_index(unit, source)
        if index_main != -1:
            index_wav = self.get_wav_channel_index(unit, source, channel_label)
            if index_wav != -1:
                waveform = self.main_cluster[index_main]['waveformCluster']['waveforms'][index_wav]
                for analysis in waveform['analyses']:
                    if ChannelAnalyses.get_channel_analysis(analysis['analysis']) == ChannelAnalyses.AIR_GAP:
                        index = 0
                        for param in analysis['parameters']:
                            if param['regime'] == regime_label:
                                analysis['parameters'].pop(index)
                                index -= 1
                            index += 1

    def add_regime_to_air_gap(self, unit, source, channel_label, regime_label):
        index_main = self.get_main_cluster_index(unit, source)
        if index_main != -1:
            index_wav = self.get_wav_channel_index(unit, source, channel_label)
            if index_wav != -1:
                waveform = self.main_cluster[index_main]['waveformCluster']['waveforms'][index_wav]
                for analysis in waveform['analyses']:
                    ca = ChannelAnalyses.get_channel_analysis(
                            analysis['analysis']
                        )
                    if ca == ChannelAnalyses.AIR_GAP:
                        regime_labels = []
                        for param in analysis['param']['regimeParam']:
                            regime_labels.append(param['regime'])
                        if regime_label not in regime_labels:
                            analysis['param']['regimeParam'].append({
                                'regime': regime_label,
                                'firstPoleAfterTrigger': 0,
                                'poleNumbersAscending': True
                            })



#------------------------------------------------------------------
#                       Bearing analysis
#------------------------------------------------------------------ 
    def add_bearing_analysis(self, unit, source, label, analysis):
        #-----------------------------------------------------------
        #unit: codis_enums.Unit
        #source: codis_enums.Source
        #label: str
        #index: int
        #analysis: dict 
        #-----------------------------------------------------------
        index_main = self.get_main_cluster_index(unit, source)
        if index_main != -1:
            index_bearing = self.get_bearing_index(unit, source, label)
            if index_bearing != -1:
                w_c = self.main_cluster[index_main]['waveformCluster']
                bearing = w_c['bearings'][index_bearing]
                if 'analyses' in bearing:
                    bearing['analyses'].append(analysis)
                else:
                    bearing['analyses'] = [analysis]

    def remove_bearing_analysis(self, unit, source, label, index):
        #-----------------------------------------------------------
        #unit: codis_enums.Unit
        #source: codis_enums.Source
        #label: str
        #index: int
        #-----------------------------------------------------------
        index_main = self.get_main_cluster_index(unit, source)
        if index_main != -1:
            index_bearing = self.get_bearing_index(unit, source, label)
            if index_bearing != -1:
                w_c = self.main_cluster[index_main]['waveformCluster']
                bearing = w_c['bearings'][index_bearing]
                if 'analyses' in bearing:
                    bearing['analyses'].pop(index)

    def get_bearing_analysis_type(self, item):
        type = item.get_item_type()
        if type != ItemType.BEARING_ANALYSIS: return None
        params = self.get_param_value(item)
        if 'analysis' not in params: return None
        try:
            analysis = BearingAnalyses.get_bearing_analysis(params['analysis'])
        except ValueError:
            print("No such bearing analysis type!")
            return None
        return analysis

    
#------------------------------------------------------------------
#                          Air gap planes
#------------------------------------------------------------------ 
    def add_air_gap_plane(self, unit, source, value):
        #-----------------------------------------------------------
        #unit: codis_enums.Unit
        #source: codis_enums.Source
        #value: dict
        #index: int
        #-----------------------------------------------------------
        index_main = self.get_main_cluster_index(unit, source)
        if index_main != -1:
            agps = self.main_cluster[index_main]['waveformCluster']['airGapPlanes']
            agps.append(value)

    def remove_air_gap_plane(self, unit, source, label):
        index_main = self.get_main_cluster_index(unit, source)
        if index_main != -1:
            agps = self.main_cluster[index_main]['waveformCluster']['airGapPlanes']
            index = 0
            for i in agps:
                if i['label'] == label:
                    agps.pop(index)
                index += 1

#------------------------------------------------------------------
#                          Channels
#------------------------------------------------------------------ 
    def get_channel(self, unit, source, label):
        #-----------------------------------------------------------
        #This method returns a reference.
        #unit: codis_enums.Unit
        #source: codis_enums.Source
        #label: str
        #-----------------------------------------------------------
        index_main = self.get_main_cluster_index(unit, source)
        if index_main != -1:
            index = 0
            wavs = self.main_cluster[index_main]['waveformCluster']['waveforms']
            for i in wavs:
                if i['label'] == label:
                    return dict(wavs[index])
                index += 1
            return None
        else:
            return None

    def add_channel(self, unit, source, value):
        #-----------------------------------------------------------
        #unit: codis_enums.Unit
        #source: codis_enums.Source
        #value: dict
        #index: int
        #-----------------------------------------------------------
        index_main = self.get_main_cluster_index(unit, source)
        if index_main != -1:
            wavs = self.main_cluster[index_main]['waveformCluster']['waveforms']
            wavs.append(value)

    def get_channel_element(self, unit, source, label):
        index_main = self.get_main_cluster_index(unit, source)
        if index_main != -1:
            wavs = self.main_cluster[index_main]['waveformCluster']['waveforms']
            for i in wavs:
                if label == i['label']:
                    return dict(i)
            return None
        else:
            return None

    def remove_channel(self, unit, source, label):
        index_main = self.get_main_cluster_index(unit, source)
        if index_main != -1:
            wavs = self.main_cluster[index_main]['waveformCluster']['waveforms']
            index = 0
            for i in wavs:
                if i['label'] == label:
                    wavs.pop(index)
                index += 1

    def remove_channel_from_other_items(self, unit, source, ch_label):
        index_main = self.get_main_cluster_index(unit, source)
        if index_main != -1:
            agps = self.main_cluster[index_main]['waveformCluster']['airGapPlanes']
            for i in agps:
                index = 0
                for j in i['sensors']:
                    if j['label'] == ch_label:
                        i['sensors'].pop(index)
                    index += 1
            bearings = self.main_cluster[index_main]['waveformCluster']['bearings']
            for i in bearings:
                if i['xDirection'] == ch_label:
                    i['xDirection'] = ''
                if i['yDirection'] == ch_label:
                    i['yDirection'] = ''
            un = self.main_cluster[index_main]['waveformCluster']['unit']
            if 'analyses' in un:
                unit_analyses = un['analyses']
                for i in unit_analyses:
                    analysis_type = UnitAnalyses.get_unit_analysis(i['analysis'])
                    if analysis_type == UnitAnalyses.RPM:
                        if 'param' in i:
                            if 'mainTriggerSensor' in i['param']:
                                if i['param']['mainTriggerSensor'] == ch_label:
                                    i['param']['mainTriggerSensor'] = ''
                    if analysis_type == UnitAnalyses.ACT_REACT_PWR:
                        if 'param' in i:
                            if 'voltageSensors' in i['param']:
                                counter = 0
                                for j in i['param']['voltageSensors']:
                                    if j == ch_label:
                                        i['param']['voltageSensors'][counter] = ''
                                    counter += 1
                            if 'currentSensors' in i['param']:
                                counter = 0
                                for j in i['param']['currentSensors']:
                                    if j == ch_label:
                                        i['param']['currentSensors'][counter] = ''
                                    counter += 1


#------------------------------------------------------------------
#                       Channel analyses
#------------------------------------------------------------------ 
    def add_channel_analysis(self, unit, source, label, analysis):
        #-----------------------------------------------------------
        #unit: codis_enums.Unit
        #source: codis_enums.Source
        #label: str
        #index: int
        #analysis: dict 
        #-----------------------------------------------------------
        index_main = self.get_main_cluster_index(unit, source)
        if index_main != -1:
            index_wav = self.get_wav_channel_index(unit, source, label)
            if index_wav != -1:
                w_c = self.main_cluster[index_main]['waveformCluster']
                wav = w_c['waveforms'][index_wav]
                if 'analyses' in wav:
                    wav['analyses'].append(analysis)
                else:
                    wav['analyses'] = [analysis]
    
    def remove_channel_analysis(self, unit, source, label, index):
        #-----------------------------------------------------------
        #unit: codis_enums.Unit
        #source: codis_enums.Source
        #label: str
        #index: int
        #-----------------------------------------------------------
        index_main = self.get_main_cluster_index(unit, source)
        if index_main != -1:
            index_wav = self.get_wav_channel_index(unit, source, label)
            if index_wav != -1:
                w_c = self.main_cluster[index_main]['waveformCluster']
                wav = w_c['waveforms'][index_wav]
                if 'analyses' in wav:
                    wav['analyses'].pop(index)

    
    def get_channel_analysis_type(self, item):
        type = item.get_item_type()
        if type != ItemType.CHANNEL_ANALYSIS: return None
        params = self.get_param_value(item)
        if 'analysis' not in params: return None
        try:
            analysis = ChannelAnalyses.get_channel_analysis(params['analysis'])
        except ValueError:
            print("No such channel analysis type!")
            return None
        return analysis

#------------------------------------------------------------------
#                            Unit analyses
#------------------------------------------------------------------ 
    def add_unit_analysis(self, unit, source, analysis):
        index_main = self.get_main_cluster_index(unit, source)
        if index_main != -1:
            un = self.main_cluster[index_main]['waveformCluster']['unit']
            if 'analyses' in un:
                un['analyses'].append(analysis)
            else:
                un['analyses'] = [analysis]

    def get_unit_analysis_type(self, item):
        type = item.get_item_type()
        if type != ItemType.UNIT_ANALYSIS: return None
        params = self.get_param_value(item)
        if 'analysis' not in params: return None
        try:
            analysis = UnitAnalyses.get_unit_analysis(params['analysis'])
        except ValueError:
            print("No such unit analysis type!")
            return None
        return analysis

    def remove_unit_analysis(self, unit, source, index):
        index_main = self.get_main_cluster_index(unit, source)
        if index_main != -1:
            un = self.main_cluster[index_main]['waveformCluster']['unit']
            if 'analyses' in un:
                un['analyses'].pop(index)



#------------------------------------------------------------------
#                          Condition vectors
#------------------------------------------------------------------ 
    def add_condition_vector_element(
        self, unit, source, label, saveTodBase = True
    ):
        index_main = self.get_main_cluster_index(unit, source)
        if index_main != -1:
            found = False
            cond_vect = self.main_cluster[index_main]['conditionVectorCluster']
            c_v_elements = cond_vect['conditionVectorElements']
            for i in c_v_elements:
                if i['label'] == label:
                    found = True
                    break
            if found:
                i['saveTodBase'] = saveTodBase
            else:
                c_v_elements.append(
                    {
                        'label': label,
                        'saveTodBase': saveTodBase
                    }
                )
    def get_condition_vector_element(self, unit, source, label):
        index_main = self.get_main_cluster_index(unit, source)
        if index_main != -1:
            cond_vect = self.main_cluster[index_main]['conditionVectorCluster']
            c_v_elements = cond_vect['conditionVectorElements']
            for i in c_v_elements:
                if label == i['label']:
                    return dict(i)
            return None
        else:
            return None

    def remove_condition_vector_element(self, unit, source, label):
        index_main = self.get_main_cluster_index(unit, source)
        if index_main != -1:
            cond_vect = self.main_cluster[index_main]['conditionVectorCluster']
            c_v_elements = cond_vect['conditionVectorElements']
            i = 0
            while i < len(c_v_elements):
                element = c_v_elements[i]
                if element['label'] == label:
                    c_v_elements.pop(i)
                    i -= 1
                i += 1