from threading import enumerate
from tkinter import *
from tkinter import ttk, messagebox, filedialog
from json import dumps, dump, loads, load
from typing import ItemsView
from .loading import LoadingProcess, OpenProcess
from .uploading import UploadingProcess
from .interfaces import AirGapPlaneInterface, BearingInterface, ChannelAnalysisAirGap, ChannelAnalysisRpm, UnsignedIntegerInterface, ChannelInterface, FloatInterface
from .interfaces import TempJsonEditor, UnitInterface, ChannelAnalysisDC
from .interfaces import ChannelAnalysisRms, NoParameterAnalysis, ChannelAnalysisRest
from .interfaces import ChannelAnalysisHarmonic, UnitAnalysisRpm, UnitAnalysisPowers
from .interfaces import PeakAnalysis, RegimeInterface, AlarmInterface, IpFrame
from .interfaces import Progress, ModbusSentInterface
from .label_name_pairs import Label_name_pairs, TableType
from .codis_enums import BearingAnalyses, Unit, Source, UnitAnalyses, ChannelAnalyses
from .tree_items import Item, ItemType
from requests import get, codes
from .simple_input_widgets import IpIntegerEntry
from .misc_string import get_channel_list_info, get_alarms_list_info, get_regimes_list_info
from .misc_string import get_air_gap_planes_list_info, get_bearing_planes_list_info

class Main_window(Frame):

    def __init__(
        self,
        update_param,
        get_param_value,
        add_bearing,
        remove_bearing,
        get_bearing_analysis_type,
        add_bearing_analysis,
        remove_bearing_analysis,
        add_alarm,
        remove_alarm,
        add_regime,
        remove_regime,
        add_air_gap_plane,
        remove_air_gap_plane,
        add_regime_to_air_gap,
        remove_regime_from_air_gap,
        add_channel,
        remove_channel,
        remove_channel_from_other_items,
        get_channel_element,
        get_channel_analysis_type,
        add_channel_analysis,
        get_unit_analysis_type,
        add_unit_analysis,
        remove_channel_analysis,
        remove_unit_analysis,
        add_condition_vector_element,
        get_condition_vector_element,
        remove_condition_vector_element,
        get_bearing_labels_from_mc,
        get_air_gap_plane_labels_from_mc,
        get_sensor_labels_from_mc,
        get_regime_labels_from_mc,
        get_signal_labels_from_mc,
        get_main_cluster,
        set_main_cluster,
        get_main_cluster_index,
        get_system_settings,
        set_system_settings,
        get_main_trigger_sensor,
        get_number_of_poles,
        master = None
    ):
        Frame.__init__(self, master)
        #self.app = app
        self.items = []
        #This variable has all label-name pairs
        # modified by the application.
        self.tables = []
        self.running_threads = []
        self.update_param = update_param
        self.get_param_value = get_param_value
        self.add_bearing = add_bearing
        self.remove_bearing = remove_bearing
        self.get_bearing_analysis_type = get_bearing_analysis_type
        self.add_bearing_analysis = add_bearing_analysis
        self.remove_bearing_analysis = remove_bearing_analysis
        self.add_alarm = add_alarm
        self.remove_alarm = remove_alarm
        self.add_regime = add_regime
        self.remove_regime = remove_regime
        self.add_air_gap_plane = add_air_gap_plane
        self.remove_air_gap_plane = remove_air_gap_plane
        self.add_regime_to_air_gap = add_regime_to_air_gap
        self.remove_regime_from_air_gap = remove_regime_from_air_gap
        self.add_channel = add_channel
        self.remove_channel = remove_channel
        self.remove_channel_from_other_items = remove_channel_from_other_items
        self.get_channel_element = get_channel_element
        self.get_channel_analysis_type = get_channel_analysis_type
        self.add_channel_analysis = add_channel_analysis
        self.get_unit_analysis_type = get_unit_analysis_type
        self.add_unit_analysis = add_unit_analysis
        self.remove_channel_analysis = remove_channel_analysis
        self.remove_unit_analysis = remove_unit_analysis
        self.add_condition_vector_element = add_condition_vector_element
        self.get_condition_vector_element = get_condition_vector_element
        self.remove_condition_vector_element = remove_condition_vector_element
        self.get_bearing_labels_from_mc = get_bearing_labels_from_mc
        self.get_air_gap_plane_labels_from_mc = get_air_gap_plane_labels_from_mc
        self.get_sensor_labels_from_mc = get_sensor_labels_from_mc
        self.get_regime_labels_from_mc = get_regime_labels_from_mc
        self.get_signal_labels_from_mc = get_signal_labels_from_mc
        self.get_main_cluster = get_main_cluster
        self.set_main_cluster = set_main_cluster
        self.get_main_cluster_index = get_main_cluster_index
        self.get_system_settings = get_system_settings
        self.set_system_settings = set_system_settings
        self.get_main_trigger_sensor = get_main_trigger_sensor
        self.get_number_of_poles = get_number_of_poles

        #Menu bar
        self.menubar = Menu(master, tearoff = 0)
        # File menu
        self.filemenu = Menu(self.menubar, tearoff = 0)
        self.filemenu.add_command(
            label = 'Open',
            command = self.run_open_data
        )
        self.filemenu.add_command(
            label = 'Save',
            command = self.run_save_data
        )
        self.filemenu.add_separator()
        self.filemenu.add_command(
            label = 'Exit',
            command = self.master.quit
        )
        self.menubar.add_cascade(
            label = 'File',
            menu = self.filemenu
        )
        # Help menu
        self.helpmenu = Menu(self.menubar, tearoff = 0)
        self.helpmenu.add_command(
            label = 'About',
            command = self.run_about
        )
        self.menubar.add_cascade(
            label = 'Help',
            menu = self.helpmenu
        )

        master.config(menu = self.menubar)

        #Frame for IP entry and command buttons
        self.controls_frame = Frame(self)

        #Widget for entering IP adress
        self.ip = IpFrame(self.controls_frame)

        #create Frame for Tree and info widgets
        self.tree_info_frame = Frame(self)
        self.tree_info_paned_window = PanedWindow(self.tree_info_frame)
        

        #create Treeview element
        self.tree = ttk.Treeview(self.tree_info_paned_window)
        self.tree.bind('<<TreeviewSelect>>', self.item_selected_event)
        self.tree.bind('<Double-Button-1>',self.doubleclick_event)
        self.tree.bind('<Button-3>',self.right_click_event)

        #create info element
        self.info = Text(
            self.tree_info_paned_window,
            bg = 'white',
            wrap = NONE
            )
        self.tree_info_paned_window.add(self.tree)
        self.tree_info_paned_window.add(self.info)

        # create button, link it to load_settings()
        self.load_button = ttk.Button(
            self.controls_frame,
            text="Load",
            command = self.load_settings_event
        )

        # create button, link it to upload_settings()
        self.upload_botton = Button(
            self.controls_frame,
            text = "Upload",
            command = self.upload_settings_event
        )
        
        #Temp test button
        self.test_button = ttk.Button(
            self.controls_frame,
            text="Test",
            command = self.test
        )

        #Bearings list right click menu
        self.bearings_list_menu = Menu(tearoff = 0)
        self.bearings_list_menu.add_cascade(
            label = 'Add bearing',
            command = self.add_new_bearing
        )

        #Bearing right click menu
        self.bearing_menu = Menu(tearoff = 0)
        self.bearing_menu.add_cascade(
            label = 'Remove bearing',
            command = self.remove_bearing_event
        )

        #Add bearing analysis menu
        self.add_bearing_analysis_menu = Menu(tearoff = 0)
        self.add_bearing_analysis_menu.add_command(
            label = "Smax",
            command = self.add_Smax
        )
        self.add_bearing_analysis_menu.add_command(
            label = "SP2Pmax",
            command = self.add_SP2Pmax
        )

        #Bearing analyses list right click menu
        self.bearing_analyses_list_menu = Menu(self, tearoff = 0)
        self.bearing_analyses_list_menu.add_cascade(
            label = "Add analysis",
            menu = self.add_bearing_analysis_menu
        )

        #Bearing analysis right click menu
        self.bearing_analysis_menu = Menu(self, tearoff = 0)
        self.bearing_analysis_menu.add_cascade(
            label = 'Remove analysis',
            command = self.remove_bearing_analysis_event
        )

        #Add channel list menu
        self.add_channel_list_menu = Menu(tearoff = 0)
        self.add_channel_list_menu.add_command(
            label = "Trigger",
            command = self.add_trigger
        )        
        self.add_channel_list_menu.add_command(
            label = "Relative vibrations",
            command = self.add_relative_vib
        )
        self.add_channel_list_menu.add_command(
            label = "Absolute vibrations - velometer",
            command = self.add_velometer
        )
        self.add_channel_list_menu.add_command(
            label = "Absolute vibrations - accelerometer",
            command = self.add_accelerometer
        )
        self.add_channel_list_menu.add_command(
            label = "Absolute vibrations - stator core",
            command = self.add_absolute_vibration_stator_core
        )
        self.add_channel_list_menu.add_command(
            label = "Air gap",
            command = self.add_air_gap
        )

        #Channels list menu
        self.ch_list_menu = Menu(tearoff = 0)
        self.ch_list_menu.add_cascade(
            label = "Add channel",
            menu = self.add_channel_list_menu
        )

        #Channel right click menu
        self.channel_menu = Menu(tearoff = 0)
        self.channel_menu.add_cascade(
            label = 'Remove channel',
            command = self.remove_channel_event
        )

        #Add channel analysis menu
        self.add_ch_analysis_menu = Menu(tearoff = 0)
        self.add_ch_analysis_menu.add_command(
            label = "Dc",
            command = self.add_dc
        )
        self.add_ch_analysis_menu.add_command(
            label = "Rms",
            command = self.add_rms
        )
        self.add_ch_analysis_menu.add_command(
            label = "Eq. peak",
            command = self.add_eq_peak
        )
        self.add_ch_analysis_menu.add_command(
            label = "Signal Frequency",
            command = self.add_sig_freq
        )
        self.add_ch_analysis_menu.add_command(
            label = "Thd",
            command = self.add_thd
        )
        self.add_ch_analysis_menu.add_command(
            label = "Harmonic",
            command = self.add_harmonic
        )
        self.add_ch_analysis_menu.add_command(
            label = "Peak2Peak",
            command = self.add_peak2peak
        )
        self.add_ch_analysis_menu.add_command(
            label = "Rest",
            command = self.add_rest
        )
        self.add_ch_analysis_menu.add_command(
            label = "Air gap",
            command = self.add_air_gap_analysis
        )
        self.add_ch_analysis_menu.add_command(
            label = "Rotational speed",
            command = self.add_channel_rpm
        )
        

        #Channel analyses list right click menu
        self.ch_analyses_list_menu = Menu(self, tearoff = 0)
        self.ch_analyses_list_menu.add_cascade(
            label = "Add analysis",
            menu = self.add_ch_analysis_menu
        )

        #Channel analysis right click menu
        self.ch_analysis_menu = Menu(self, tearoff = 0)
        self.ch_analysis_menu.add_cascade(
            label = "Remove analysis",
            command = self.remove_channel_analysis_event
        )

        #Add unit analysis list menu
        self.add_unit_analysis_list_menu = Menu(self, tearoff = 0)
        self.add_unit_analysis_list_menu.add_command(
            label = 'Rotational speed',
            command = self.add_rpm
        )
        self.add_unit_analysis_list_menu.add_command(
            label = 'Active and reactive powers',
            command = self.add_powers
        )
        
        #Unit analyses list right click menu
        self.unit_analysis_list_menu = Menu(self, tearoff = 0)
        self.unit_analysis_list_menu.add_cascade(
            label = 'Add analysis',
            menu = self.add_unit_analysis_list_menu
        )

        #Unit analyses right click menu
        self.unit_analysis_menu = Menu(self, tearoff = 0)
        self.unit_analysis_menu.add_cascade(
            label = 'Remove analysis',
            command = self.remove_unit_analysis_event
        )

        #Regimes list right click menu
        self.regimes_list_menu = Menu(tearoff = 0)
        self.regimes_list_menu.add_cascade(
            label = 'Add regime',
            command = self.add_new_regime
        )

        # Regime right click menu
        self.regime_menu = Menu(self, tearoff = 0)
        self.regime_menu.add_cascade(
            label = 'Remove regime',
            command = self.remove_regime_event
        )

        #Alarms list right click menu
        self.alarms_list_menu = Menu(tearoff = 0)
        self.alarms_list_menu.add_cascade(
            label = 'Add alarm',
            command = self.add_new_alarm
        )

        #Alarm right click menu
        self.alarm_menu = Menu(tearoff = 0)
        self.alarm_menu.add_cascade(
            label = 'Remove alarm',
            command = self.remove_alarm_event
        )

        #Air gap planes list right click menu
        self.air_gap_planes_list_menu = Menu(tearoff = 0)
        self.air_gap_planes_list_menu.add_cascade(
            label = 'Add air gap plane',
            command = self.add_new_air_gap_plane
        )

        #Air gap plane right click menu
        self.air_gap_plane_menu = Menu(self, tearoff = 0)
        self.air_gap_plane_menu.add_cascade(
            label = 'Remove air gap plane',
            command = self.remove_air_gap_plane_event
        )

        #Modbus list right click menu
        self.modbus_list_menu = Menu(self, tearoff = 0)
        self.modbus_list_menu.add_cascade(
            label = "Add send group",
            command = self.add_sent_to_modbus
        )

        self.pack(fill = BOTH, expand = 1)
        self.controls_frame.pack(side = TOP, fill = X)
        self.upload_botton.pack(side = RIGHT)
        self.load_button.pack(side = RIGHT)
        self.ip.pack(side = RIGHT, fill= BOTH)
        self.tree_info_frame.pack(fill = BOTH, expand = 1)
        self.tree_info_paned_window.pack(fill=BOTH, expand = 1)
        #self.tree.pack(side = LEFT, fill = BOTH, expand = 0)
        #self.info.pack(side = LEFT, fill = BOTH, expand = 1)
        self.test_button.pack(side = LEFT)

#------------------------------------------------------------------
#                           Menu bar functions
#------------------------------------------------------------------
    def do_nothing(self):
        pass

    def run_save_data(self):
        folder_name = filedialog.askdirectory()
        if folder_name != '':
            main_settings_filename = f'{folder_name}/main_settings.json'
            system_settings_filename = f'{folder_name}/system_settings.json'
            main_cluster = self.get_main_cluster()
            system_settings = self.get_system_settings()
            for i in self.tables:
                if i.get_table_type() == TableType.SIGNALS:
                    unit_string = Unit.get_string(i.get_unit())
                    filename = f'{folder_name}/tsignal_{unit_string}.json'
                    pairs = i.get_pairs()
                    with open(filename, 'w') as f:
                        dump(pairs, f, indent = 2)
                if i.get_table_type() == TableType.SENSORS:
                    unit_string = Unit.get_string(i.get_unit())
                    filename = f'{folder_name}/tsensor_{unit_string}.json'
                    pairs = i.get_pairs()
                    with open(filename, 'w') as f:
                        dump(pairs, f, indent = 2)
                if i.get_table_type() == TableType.REGIMES:
                    unit_string = Unit.get_string(i.get_unit())
                    filename = f'{folder_name}/tregime_{unit_string}.json'
                    pairs = i.get_pairs()
                    with open(filename, 'w') as f:
                        dump(pairs, f, indent = 2)
                if i.get_table_type() == TableType.BEARINGS:
                    unit_string = Unit.get_string(i.get_unit())
                    filename = f'{folder_name}/tbearing_{unit_string}.json'
                    pairs = i.get_pairs()
                    with open(filename, 'w') as f:
                        dump(pairs, f, indent = 2)
                if i.get_table_type() == TableType.AIR_GAP_PLANES:
                    unit_string = Unit.get_string(i.get_unit())
                    filename = f'{folder_name}/air_gap_plane_{unit_string}.json'
                    pairs = i.get_pairs()
                    with open(filename, 'w') as f:
                        dump(pairs, f, indent = 2)
            with open(main_settings_filename, 'w') as f:
                dump(main_cluster, f, indent = 2)
            with open(system_settings_filename, 'w') as f:
                dump(system_settings, f, indent = 2)

    def run_open_data(self):
        #following line disables root window, which prevents
        #opening of additional subinterfaces
        self.master.wm_attributes("-disabled", True)
        folder_name = filedialog.askdirectory()
        if folder_name == '':
            self.master.wm_attributes("-disabled", False)
            return
        self.pb = Progress(
            title = 'Loading progress:',
            cancel_callback = self.cancel_load_settings_process)
        self.temp_system_settings = self.get_system_settings()
        self.temp_main_cluster = self.get_main_cluster()
        self.temp_tables = self.tables
        self.tables = []
        op = OpenProcess(
            folder_name = folder_name,
            load_settings_process_ok = self.load_settings_process_ok,
            load_settings_process_failed = self.load_settings_process_failed,
            set_num_iteration = self.pb.set_num_iteration,
            update_interface = self.pb.progress,
            canceled = self.get_and_update_thread_status
        )
        self.current_thread_name = op.name
        self.add_thread(op.name)

    def run_about(self):
        
        self.win = Toplevel()
        self.win.title('About:')
        label = Label(self.win, text="CompactRio configurator was developed within VESKi Ltd.\nFor all information about the product feel free to contact us:\nSenior developer: Tihomir Tonković - tihomir.tonkovic@veski.hr\nJunior developer: Damijan Cerinski - damijan.cerinski@4-cube.hr", bg='white')
        label.pack(ipadx=50, ipady=10, fill='both', expand=True)
        
        self.ok_butt = Button(self.win, text="Ok", command=self.win.destroy)
        self.ok_butt.pack(pady=10, padx=10, ipadx=20)

#------------------------------------------------------------------
#                               Events
#------------------------------------------------------------------
    def item_selected_event(self, event):
        item_id = self.tree.selection()[0]
        self.item_selected(item_id)

    def item_selected(self, item_id):
        item = self.find_item(item_id = item_id)
        if item.get_item_type() == ItemType.CHANNELS_LIST:
            param = self.get_param_value(item)
            table = self.get_table(
                unit = item.get_item_data()['unitName'],
                table_type = TableType.SENSORS
            )
            s = get_channel_list_info(table, param)
            self.set_info_text(s)
        elif item.get_item_type() == ItemType.ALARMS_LIST:
            param = self.get_param_value(item)
            table = self.get_table(
                unit = item.get_item_data()['unitName'],
                table_type = TableType.SIGNALS
            )
            s = get_alarms_list_info(table, param)
            self.set_info_text(s)
        elif item.get_item_type() == ItemType.REGIMES_LIST:
            param = self.get_param_value(item)
            table_regimes = self.get_table(
                unit = item.get_item_data()['unitName'],
                table_type = TableType.REGIMES
            )
            table_signals = self.get_table(
                unit = item.get_item_data()['unitName'],
                table_type = TableType.SIGNALS
            )
            s = get_regimes_list_info(table_regimes, table_signals, param)
            self.set_info_text(s)
        elif item.get_item_type() == ItemType.AIR_GAP_PLANES_LIST:
            param = self.get_param_value(item)
            table_agp = self.get_table(
                unit = item.get_item_data()['unitName'],
                table_type = TableType.AIR_GAP_PLANES
            )
            table_sensors = self.get_table(
                unit = item.get_item_data()['unitName'],
                table_type = TableType.SENSORS
            )
            s = get_air_gap_planes_list_info(table_agp, table_sensors, param)
            self.set_info_text(s)
        elif item.get_item_type() == ItemType.BEARINGS_LIST:
            param = self.get_param_value(item)
            table_bearings = self.get_table(
                unit = item.get_item_data()['unitName'],
                table_type = TableType.BEARINGS
            )
            table_sensors = self.get_table(
                unit = item.get_item_data()['unitName'],
                table_type = TableType.SENSORS
            )
            s = get_bearing_planes_list_info(table_bearings, table_sensors, param)
            self.set_info_text(s)
        else:
            self.set_info_text(
                dumps(self.get_param_value(item))
            )

    def load_settings_event(self):
        #following line disables root window, which prevents
        #opening of additional subinterfaces
        self.master.wm_attributes("-disabled", True)
        self.pb = Progress(
            title = 'Loading progress:',
            cancel_callback = self.cancel_load_settings_process)
        self.temp_system_settings = self.get_system_settings()
        self.temp_main_cluster = self.get_main_cluster()
        self.temp_tables = self.tables
        self.tables = []
        lp = LoadingProcess(
            ip = self.ip.get(),
            load_settings_process_ok = self.load_settings_process_ok,
            load_settings_process_failed = self.load_settings_process_failed,
            set_num_iteration = self.pb.set_num_iteration,
            update_interface = self.pb.progress,
            canceled = self.get_and_update_thread_status
        )
        self.current_thread_name = lp.name
        self.add_thread(lp.name)
        
    def load_settings_process_ok(
        self,
        system_settings,
        main_cluster,
        tables
    ):
        self.set_system_settings(system_settings)
        self.set_main_cluster(main_cluster)
        self.tables = tables
        self.clear_tree()
        self.fill_tree()
        self.remove_thread(self.current_thread_name)
        #Enable main window after it was disabled.
        self.master.wm_attributes("-disabled", False)

    def load_settings_process_failed(self, name):
        self.pb.destroy()
        self.remove_thread(name)
        #Enable main window after it was disabled.
        self.master.wm_attributes("-disabled", False)

    def cancel_load_settings_process(self):
        self.cancel_thread(self.current_thread_name)
        #Enable main window after it was disabled.
        self.master.wm_attributes("-disabled", False)

    def upload_settings_event(self):
        up = UploadingProcess(
            ip = self.ip.get(),
            get_main_cluster = self.get_main_cluster,
            get_system_settings = self.get_system_settings,
            get_table = self.get_table
        )
        up.execute()

    def doubleclick_event(self, event):
        item_id = self.tree.identify('item', event.x, event.y)
        if item_id !='':
            item = self.find_item(item_id)
            #last item that was doubleclicked
            #is stored to self.doubleclicked_item
            self.doubleclicked_item = item
            if item.get_item_type() == ItemType.UNIT_SOURCE:
                #following line disables root window, which prevents
                #opening of additional subinterfaces
                self.master.wm_attributes("-disabled", True)
                unit = item.get_item_data()['unitName']
                source = item.get_item_data()['sourceName']
                UnitInterface(
                    init_value = self.get_param_value(item),
                    callback = self.subinterface_callback,
                    cancel_callback = self.cancel_callback,
                    x = self.tree.winfo_pointerx(),
                    y = self.tree.winfo_pointery()
                )
            elif item.get_item_type() == ItemType.BEARING:
                #following line disables root window, which prevents
                #opening of additional subinterfaces
                self.master.wm_attributes("-disabled", True)
                unit = item.get_item_data()['unitName']
                source = item.get_item_data()['sourceName']
                init_value = self.get_param_value(item)
                pairs = []
                for i in self.get_sensor_labels_from_mc(unit, source):
                    pairs.append(
                        {
                            'label': i,
                            'name': self.get_name_from_table(unit, i, TableType.SENSORS)
                        }
                    )
                table = Label_name_pairs(pairs)
                bearing_name = self.get_name_from_table(
                    unit = unit,
                    label = init_value['label'],
                    table_type = TableType.BEARINGS
                )
                BearingInterface(
                    init_value = init_value,
                    bearing_name = bearing_name,
                    callback = self.subinterface_callback,
                    cancel_callback = self.cancel_callback,
                    ch_pairs = table,
                    x = self.tree.winfo_pointerx(),
                    y = self.tree.winfo_pointery()
                )
            elif item.get_item_type() == ItemType.BEARING_ANALYSIS:
                #following line disables root window, which prevents
                #opening of additional subinterfaces
                self.master.wm_attributes("-disabled", True)
                analysis_type = self.get_bearing_analysis_type(item)
                if analysis_type == BearingAnalyses.S_MAX:
                    unit = item.get_item_data()['unitName']
                    bearing_label = item.get_item_data()['label']
                    l_a = self.get_param_value(item)['param']['labelAddition']
                    signal_label = f'{bearing_label}.Smax{l_a}'
                    name = self.get_name_from_table(
                        unit = unit,
                        label = signal_label,
                        table_type = TableType.SIGNALS
                        )
                    PeakAnalysis(
                        title = 'Smax',
                        init_value = self.get_param_value(item),
                        signal_label = signal_label,
                        signal_name = name,
                        callback = self.subinterface_callback,
                        cancel_callback = self.cancel_callback,
                        x = self.tree.winfo_pointerx(),
                        y = self.tree.winfo_pointery()
                    )
                if analysis_type == BearingAnalyses.SP2P_MAX:
                    unit = item.get_item_data()['unitName']
                    bearing_label = item.get_item_data()['label']
                    l_a = self.get_param_value(item)['param']['labelAddition']
                    signal_label = f'{bearing_label}.SP2Pmax{l_a}'
                    name = self.get_name_from_table(
                        unit = unit,
                        label = signal_label,
                        table_type = TableType.SIGNALS
                        )
                    PeakAnalysis(
                        title = 'SP2Pmax',
                        init_value = self.get_param_value(item),
                        signal_label = signal_label,
                        signal_name = name,
                        callback = self.subinterface_callback,
                        cancel_callback = self.cancel_callback,
                        x = self.tree.winfo_pointerx(),
                        y = self.tree.winfo_pointery()
                    )
            elif item.get_item_type() == ItemType.AIR_GAP_PLANE:
                #following line disables root window, which prevents
                #opening of additional subinterfaces
                self.master.wm_attributes("-disabled", True)
                unit = item.get_item_data()['unitName']
                source = item.get_item_data()['sourceName']
                init_value = self.get_param_value(item)
                agp_name = self.get_name_from_table(
                    unit = unit,
                    label = init_value['label'],
                    table_type = TableType.AIR_GAP_PLANES
                )
                pairs = []
                for i in self.get_sensor_labels_from_mc(unit, source):
                    pairs.append(
                        {
                            'label': i,
                            'name': self.get_name_from_table(unit, i, TableType.SENSORS)
                        }
                    )
                table = Label_name_pairs(pairs)
                AirGapPlaneInterface(
                    init_value = init_value,
                    agp_name = agp_name,
                    ch_pairs = table,
                    cancel_callback = self.cancel_callback,
                    callback = self.subinterface_callback,
                    x = self.tree.winfo_pointerx(),
                    y = self.tree.winfo_pointery()
                )
            elif item.get_item_type() == ItemType.ALARM:
                #following line disables root window, which prevents
                #opening of additional subinterfaces
                self.master.wm_attributes("-disabled", True)
                unit = item.get_item_data()['unitName']
                source = item.get_item_data()['sourceName']
                init_value = self.get_param_value(item)
                sig_pairs = []
                for i in self.get_signal_labels_from_mc(unit, source):
                    sig_pairs.append(
                        {
                            'label': i,
                            'name': self.get_name_from_table(unit, i, TableType.SIGNALS)
                        }
                    )
                definitions = init_value['logicalSentence']
                for i in sig_pairs:
                    new_str = "'"+f"{i['name']}"+"'"
                    definitions = definitions.replace(i['label'], new_str)
                init_value['logicalSentence'] = definitions
                AlarmInterface(
                    init_value = init_value,
                    sig_pairs = sig_pairs,
                    callback = self.subinterface_callback,
                    cancel_callback = self.cancel_callback,
                    x = self.tree.winfo_pointerx(),
                    y = self.tree.winfo_pointery() 
                )

            elif item.get_item_type() == ItemType.REGIME:
                #following line disables root window, which prevents
                #opening of additional subinterfaces
                self.master.wm_attributes("-disabled", True)
                unit = item.get_item_data()['unitName']
                source = item.get_item_data()['sourceName']
                init_value = self.get_param_value(item)
                regime_name = self.get_name_from_table(
                    unit = unit,
                    label = init_value['label'],
                    table_type = TableType.REGIMES
                )
                sig_pairs = []
                for i in self.get_signal_labels_from_mc(unit, source):
                    sig_pairs.append(
                        {
                            'label': i,
                            'name': self.get_name_from_table(unit, i, TableType.SIGNALS)
                        }
                    )
                definitions = init_value['regimeLogicalDefinitionStatement']
                for i in sig_pairs:
                    new_str = "'"+f"{i['name']}"+"'"
                    definitions = definitions.replace(i['label'], new_str)
                init_value['regimeLogicalDefinitionStatement'] = definitions
                RegimeInterface(
                    init_value = init_value,
                    regime_name = regime_name,
                    sig_pairs = sig_pairs,
                    callback = self.subinterface_callback,
                    cancel_callback = self.cancel_callback,
                    x = self.tree.winfo_pointerx(),
                    y = self.tree.winfo_pointery() 
                )
            elif item.get_item_type() == ItemType.PHYSICAL_CHANNEL:
                #following line disables root window, which prevents
                #opening of additional subinterfaces
                self.master.wm_attributes("-disabled", True)
                UnsignedIntegerInterface(
                    title = "Physical channel:",
                    callback = self.subinterface_callback,
                    cancel_callback = self.cancel_callback,
                    init_value = self.get_param_value(item),
                    x = self.tree.winfo_pointerx(),
                    y = self.tree.winfo_pointery()
                )
            elif item.get_item_type() == ItemType.SLOPE:
                #following line disables root window, which prevents
                #opening of additional subinterfaces
                self.master.wm_attributes("-disabled", True)
                FloatInterface(
                    title = "Slope:",
                    callback = self.subinterface_callback,
                    cancel_callback = self.cancel_callback,
                    init_value = self.get_param_value(item),
                    x = self.tree.winfo_pointerx(),
                    y = self.tree.winfo_pointery()
                )
            elif item.get_item_type() == ItemType.INTERCEPT:
                #following line disables root window, which prevents
                #opening of additional subinterfaces
                self.master.wm_attributes("-disabled", True)
                FloatInterface(
                    title = "Intercept:",
                    callback = self.subinterface_callback,
                    cancel_callback = self.cancel_callback,
                    init_value = self.get_param_value(item),
                    x = self.tree.winfo_pointerx(),
                    y = self.tree.winfo_pointery()
                )
            elif item.get_item_type() == ItemType.CHANNEL:
                #following line disables root window, which prevents
                #opening of additional subinterfaces
                self.master.wm_attributes("-disabled", True)
                unit = item.get_item_data()['unitName']
                label = item.get_item_data()['label']
                ChannelInterface(
                    init_value = self.get_param_value(item),
                    ch_name = self.get_name_from_table(unit, label, TableType.SENSORS),
                    callback = self.subinterface_callback,
                    cancel_callback = self.cancel_callback,
                    x = self.tree.winfo_pointerx(),
                    y = self.tree.winfo_pointery()   
                )
            elif item.get_item_type() == ItemType.CHANNEL_ANALYSIS:
                #following line disables root window, which prevents
                #opening of additional subinterfaces
                self.master.wm_attributes("-disabled", True)
                analysis_type = self.get_channel_analysis_type(item)
                if analysis_type == ChannelAnalyses.SNA_PH:
                    unit = item.get_item_data()['unitName']
                    ch_label = item.get_item_data()['label']
                    source = item.get_item_data()['sourceName']
                    harmonic = str(self.get_param_value(item)['param']['harmonic'])
                    sig_label_A = f'{ch_label}.s{harmonic}.00A'
                    sig_label_Ph = f'{ch_label}.s{harmonic}.00Ph'
                    name_A = self.get_name_from_table(
                        unit = unit,
                        label = sig_label_A,
                        table_type = TableType.SIGNALS
                        )
                    name_Ph = self.get_name_from_table(
                        unit = unit,
                        label = sig_label_Ph,
                        table_type = TableType.SIGNALS
                        )
                    ChannelAnalysisHarmonic(
                        init_value = self.get_param_value(item),
                        channel_label = ch_label,
                        signal_name_A = name_A,
                        signal_name_Ph = name_Ph,
                        signal_label_A_old = sig_label_A,
                        signal_label_Ph_old = sig_label_Ph,
                        callback = self.subinterface_callback,
                        cancel_callback = self.cancel_callback,
                        x = self.tree.winfo_pointerx(),
                        y = self.tree.winfo_pointery()
                    )
                elif analysis_type == ChannelAnalyses.RMS:
                    unit = item.get_item_data()['unitName']
                    ch_label = item.get_item_data()['label']
                    l_a = self.get_param_value(item)['param']['labelAddition']
                    sig_label = f'{ch_label}.RMS{l_a}'
                    name = self.get_name_from_table(
                        unit = unit,
                        label = sig_label,
                        table_type = TableType.SIGNALS
                        )
                    ChannelAnalysisRms(
                        init_value = self.get_param_value(item),
                        signal_label = sig_label,
                        signal_name = name,
                        callback = self.subinterface_callback,
                        cancel_callback = self.cancel_callback,
                        x = self.tree.winfo_pointerx(),
                        y = self.tree.winfo_pointery()
                    )
                elif analysis_type == ChannelAnalyses.EQ_PEAK:
                    unit = item.get_item_data()['unitName']
                    ch_label = item.get_item_data()['label']
                    l_a = self.get_param_value(item)['param']['labelAddition']
                    sig_label = f'{ch_label}.EqPeak{l_a}'
                    name = self.get_name_from_table(
                        unit = unit,
                        label = sig_label,
                        table_type = TableType.SIGNALS
                        )
                    PeakAnalysis(
                        title = 'EqPeak',
                        init_value = self.get_param_value(item),
                        signal_label = sig_label,
                        signal_name = name,
                        callback = self.subinterface_callback,
                        cancel_callback = self.cancel_callback,
                        x = self.tree.winfo_pointerx(),
                        y = self.tree.winfo_pointery()
                    )
                elif analysis_type == ChannelAnalyses.DC:
                    unit = item.get_item_data()['unitName']
                    ch_label = item.get_item_data()['label']
                    sig_label = f'{ch_label}.DC'
                    name = self.get_name_from_table(
                        unit = unit,
                        label = sig_label,
                        table_type = TableType.SIGNALS
                        )
                    ChannelAnalysisDC(
                        init_value = self.get_param_value(item),
                        signal_label = sig_label,
                        signal_name = name,
                        callback = self.subinterface_callback,
                        cancel_callback = self.cancel_callback,
                        x = self.tree.winfo_pointerx(),
                        y = self.tree.winfo_pointery()
                    )
                elif analysis_type == ChannelAnalyses.SIGNAL_FREQUENCY:
                    unit = item.get_item_data()['unitName']
                    ch_label = item.get_item_data()['label']
                    sig_label = f'{ch_label}.SignalFrequency'
                    name = self.get_name_from_table(
                        unit = unit,
                        label = sig_label,
                        table_type = TableType.SIGNALS
                        )
                    if name == None:
                        name = f'{ch_label} Signal frequency'
                    else:
                        pass
                    NoParameterAnalysis(
                        title = 'sigfreq',
                        init_value = self.get_param_value(item),
                        signal_label = sig_label,
                        signal_name = name,
                        callback = self.subinterface_callback,
                        cancel_callback = self.cancel_callback,
                        x = self.tree.winfo_pointerx(),
                        y = self.tree.winfo_pointery()
                    )
                elif analysis_type == ChannelAnalyses.THD:
                    unit = item.get_item_data()['unitName']
                    ch_label = item.get_item_data()['label']
                    sig_label = f'{ch_label}.THD'
                    name = self.get_name_from_table(
                        unit = unit,
                        label = sig_label,
                        table_type = TableType.SIGNALS
                    )
                    if name == None:
                        name = f'{ch_label} Thd'
                    else:
                        pass
                    NoParameterAnalysis(
                        title = 'thd',
                        init_value = self.get_param_value(item),
                        signal_label = sig_label,
                        signal_name = name,
                        callback = self.subinterface_callback,
                        cancel_callback = self.cancel_callback,
                        x = self.tree.winfo_pointerx(),
                        y = self.tree.winfo_pointery()
                    )
                elif analysis_type == ChannelAnalyses.PEAK2PEAK:
                    unit = item.get_item_data()['unitName']
                    ch_label = item.get_item_data()['label']
                    l_a = self.get_param_value(item)['param']['labelAddition']
                    sig_label = f'{ch_label}.Peak2Peak{l_a}'
                    name = self.get_name_from_table(
                        unit = unit,
                        label = sig_label,
                        table_type = TableType.SIGNALS
                        )
                    PeakAnalysis(
                        title = 'Peak2Peak',
                        init_value = self.get_param_value(item),
                        signal_label = sig_label,
                        signal_name = name,
                        callback = self.subinterface_callback,
                        cancel_callback = self.cancel_callback,
                        x = self.tree.winfo_pointerx(),
                        y = self.tree.winfo_pointery()
                    )
                elif analysis_type == ChannelAnalyses.REST:
                    unit = item.get_item_data()['unitName']
                    ch_label = item.get_item_data()['label']
                    sig_label = f'{ch_label}.Rest'
                    name = self.get_name_from_table(
                        unit = unit,
                        label = sig_label,
                        table_type = TableType.SIGNALS
                    )
                    if name == None:
                        name = f'{ch_label} Rest'
                    else:
                        pass
                    ChannelAnalysisRest(
                        init_value = self.get_param_value(item),
                        signal_label = sig_label,
                        signal_name = name,
                        callback = self.subinterface_callback,
                        cancel_callback = self.cancel_callback,
                        x = self.tree.winfo_pointerx(),
                        y = self.tree.winfo_pointery()
                    )
                elif analysis_type == ChannelAnalyses.AIR_GAP:
                    unit = item.get_item_data()['unitName']
                    source = item.get_item_data()['sourceName']
                    num_of_poles = self.get_number_of_poles(unit, source)
                    ch_label = item.get_item_data()['label']
                    sensor_name = self.get_name_from_table(
                        unit = unit,
                        label = ch_label,
                        table_type = TableType.SENSORS)
                    pairs = []
                    regime_labels = self.get_regime_labels_from_mc(unit, source)
                    if regime_labels == []:
                        messagebox.showinfo("Error:", "There is no regimes defined.")
                        self.master.wm_attributes("-disabled", False)
                    else:
                        for i in regime_labels:
                            pairs.append(
                                {
                                    'label': i,
                                    'name': self.get_name_from_table(unit, i, TableType.REGIMES)
                                }
                            )
                        reg_pairs = Label_name_pairs(pairs)
                        init_value = self.get_param_value(item)
                        ChannelAnalysisAirGap(
                            init_value = init_value,
                            channel_label = ch_label,
                            sensor_name = sensor_name,
                            reg_pairs = reg_pairs,
                            number_of_poles = num_of_poles,
                            callback = self.subinterface_callback,
                            cancel_callback = self.cancel_callback,
                            x = self.tree.winfo_pointerx(),
                            y = self.tree.winfo_pointery()
                    )
                elif analysis_type == ChannelAnalyses.RPM:
                    unit = item.get_item_data()['unitName']
                    ch_label = item.get_item_data()['label']
                    sig_label = f'{ch_label}.RotSpeed'
                    name = self.get_name_from_table(
                        unit = unit,
                        label = sig_label,
                        table_type = TableType.SIGNALS
                    )
                    if name == None:
                        name = f'{ch_label} rotational speed'
                    else:
                        pass
                    ChannelAnalysisRpm(
                        init_value = self.get_param_value(item),
                        signal_label = sig_label,
                        signal_name = name,
                        callback = self.subinterface_callback,
                        cancel_callback = self.cancel_callback,
                        x = self.tree.winfo_pointerx(),
                        y = self.tree.winfo_pointery()
                    )
                else:
                    TempJsonEditor(
                        init_value = self.get_param_value(item),
                        callback = self.subinterface_callback,
                        cancel_callback = self.cancel_callback,
                        x = self.tree.winfo_pointerx(),
                        y = self.tree.winfo_pointery()
                    )
            elif item.get_item_type() == ItemType.UNIT_ANALYSIS:
                #following line disables root window, which prevents
                #opening of additional subinterfaces
                self.master.wm_attributes("-disabled", True)
                analysis_type = self.get_unit_analysis_type(item)
                if analysis_type == UnitAnalyses.RPM:
                    unit = item.get_item_data()['unitName']
                    source = item.get_item_data()['sourceName']
                    unit_name = Unit.get_string(unit)
                    source_name = Source.get_string(source)
                    sig_label = f'{unit_name}.{source_name}.RotSpeed'
                    name = self.get_name_from_table(
                        unit = unit,
                        label = sig_label,
                        table_type = TableType.SIGNALS
                    )
                    pairs = []
                    for i in self.get_sensor_labels_from_mc(unit, source):
                        pairs.append(
                            {
                                'label': i,
                                'name': self.get_name_from_table(unit, i, TableType.SENSORS)
                            }
                        )
                    table = Label_name_pairs(pairs)
                    UnitAnalysisRpm(
                        init_value = self.get_param_value(item),
                        ch_pairs = table,
                        signal_label = sig_label,
                        signal_name = name,
                        callback = self.subinterface_callback,
                        cancel_callback = self.cancel_callback,
                        x = self.tree.winfo_pointerx(),
                        y = self.tree.winfo_pointery()
                    )
                elif analysis_type == UnitAnalyses.ACT_REACT_PWR:
                    unit = item.get_item_data()['unitName']
                    source = item.get_item_data()['sourceName']
                    unit_name = Unit.get_string(unit)
                    source_name = Source.get_string(source)
                    signal_label_act = f'{unit_name}.{source_name}.activePower'
                    signal_label_react = f'{unit_name}.{source_name}.reactivePower'
                    name_act = self.get_name_from_table(
                        unit = unit,
                        label = signal_label_act,
                        table_type = TableType.SIGNALS
                    )
                    name_react = self.get_name_from_table(
                        unit = unit,
                        label = signal_label_react,
                        table_type = TableType.SIGNALS
                    )
                    pairs = []
                    for i in self.get_sensor_labels_from_mc(unit, source):
                        pairs.append(
                            {
                                'label': i,
                                'name': self.get_name_from_table(unit, i, TableType.SENSORS)
                            }
                        )
                    table = Label_name_pairs(pairs)
                    UnitAnalysisPowers(
                        init_value = self.get_param_value(item),
                        ch_pairs = table,
                        signal_label_act = signal_label_act,
                        signal_name_act = name_act,
                        signal_label_react = signal_label_react,
                        signal_name_react = name_react,
                        callback = self.subinterface_callback,
                        cancel_callback = self.cancel_callback,
                        x = self.tree.winfo_pointerx(),
                        y = self.tree.winfo_pointery()
                    )
                else:
                    TempJsonEditor(
                    init_value = self.get_param_value(item),
                    callback = self.subinterface_callback,
                    cancel_callback = self.cancel_callback,
                    x = self.tree.winfo_pointerx(),
                    y = self.tree.winfo_pointery()
                )
                    
                
            #return 'break' prevents item expansion or collapse
            # on doubleclick.
            return 'break'

    def right_click_event(self, event):
        item_id = self.tree.identify('item', event.x, event.y)
        if item_id !='':
            item = self.find_item(item_id)
            self.rightclicked_item = item
            if item.get_item_type() == ItemType.CHANNEL_ANALYSES_LIST:
                self.tree.focus(item_id)
                #<<TreeviewSelect>> event is fired 
                # by the selection_set method.
                self.tree.selection_set(item_id)
                self.ch_analyses_list_menu.tk_popup(
                    self.tree.winfo_pointerx(),
                    self.tree.winfo_pointery()
                )
            if item.get_item_type() == ItemType.CHANNEL_ANALYSIS:
                self.tree.focus(item_id)
                #<<TreeviewSelect>> event is fired 
                # by the selection_set method.
                self.tree.selection_set(item_id)
                self.ch_analysis_menu.tk_popup(
                    self.tree.winfo_pointerx(),
                    self.tree.winfo_pointery()
                )
            if item.get_item_type() == ItemType.CHANNELS_LIST:
                self.tree.focus(item_id)
                #<<TreeviewSelect>> event is fired 
                # by the selection_set method.
                self.tree.selection_set(item_id)
                self.ch_list_menu.tk_popup(
                    self.tree.winfo_pointerx(),
                    self.tree.winfo_pointery()
                )
            if item.get_item_type() == ItemType.UNIT_ANALYSES_LIST:
                self.tree.focus(item_id)
                self.tree.selection_set(item_id)
                self.unit_analysis_list_menu.tk_popup(
                    self.tree.winfo_pointerx(),
                    self.tree.winfo_pointery()
                )
            if item.get_item_type() == ItemType.UNIT_ANALYSIS:
                self.tree.focus(item_id)
                self.tree.selection_set(item_id)
                self.unit_analysis_menu.tk_popup(
                    self.tree.winfo_pointerx(),
                    self.tree.winfo_pointery()
                )
            if item.get_item_type() == ItemType.CHANNEL:
                self.tree.focus(item_id)
                self.tree.selection_set(item_id)
                self.channel_menu.tk_popup(
                    self.tree.winfo_pointerx(),
                    self.tree.winfo_pointery()
                )
            if item.get_item_type() == ItemType.BEARINGS_LIST:
                self.tree.focus(item_id)
                self.tree.selection_set(item_id)
                self.bearings_list_menu.tk_popup(
                    self.tree.winfo_pointerx(),
                    self.tree.winfo_pointery()
                )
            if item.get_item_type() == ItemType.BEARING:
                self.tree.focus(item_id)
                self.tree.selection_set(item_id)
                self.bearing_menu.tk_popup(
                    self.tree.winfo_pointerx(),
                    self.tree.winfo_pointery()
                )
            if item.get_item_type() == ItemType.BEARING_ANALYSES_LIST:
                self.tree.focus(item_id)
                #<<TreeviewSelect>> event is fired 
                # by the selection_set method.
                self.tree.selection_set(item_id)
                self.bearing_analyses_list_menu.tk_popup(
                    self.tree.winfo_pointerx(),
                    self.tree.winfo_pointery()
                )
            if item.get_item_type() == ItemType.BEARING_ANALYSIS:
                self.tree.focus(item_id)
                self.tree.selection_set(item_id)
                self.bearing_analysis_menu.tk_popup(
                    self.tree.winfo_pointerx(),
                    self.tree.winfo_pointery()
                )
            if item.get_item_type() == ItemType.REGIMES_LIST:
                self.tree.focus(item_id)
                self.tree.selection_set(item_id)
                self.regimes_list_menu.tk_popup(
                    self.tree.winfo_pointerx(),
                    self.tree.winfo_pointery()
                )
            if item.get_item_type() == ItemType.REGIME:
                self.tree.focus(item_id)
                self.tree.selection_set(item_id)
                self.regime_menu.tk_popup(
                    self.tree.winfo_pointerx(),
                    self.tree.winfo_pointery()
                )
            if item.get_item_type() == ItemType.ALARMS_LIST:
                self.tree.focus(item_id)
                self.tree.selection_set(item_id)
                self.alarms_list_menu.tk_popup(
                    self.tree.winfo_pointerx(),
                    self.tree.winfo_pointery()
                )
            if item.get_item_type() == ItemType.ALARM:
                self.tree.focus(item_id)
                self.tree.selection_set(item_id)
                self.alarm_menu.tk_popup(
                    self.tree.winfo_pointerx(),
                    self.tree.winfo_pointery()
                )
            if item.get_item_type() == ItemType.AIR_GAP_PLANES_LIST:
                self.tree.focus(item_id)
                self.tree.selection_set(item_id)
                self.air_gap_planes_list_menu.tk_popup(
                    self.tree.winfo_pointerx(),
                    self.tree.winfo_pointery()
                )
            if item.get_item_type() == ItemType.AIR_GAP_PLANE:
                self.tree.focus(item_id)
                self.tree.selection_set(item_id)
                self.air_gap_plane_menu.tk_popup(
                    self.tree.winfo_pointerx(),
                    self.tree.winfo_pointery()
                )
            if item.get_item_type() == ItemType.MODBUS_LIST:
                self.tree.focus(item_id)
                self.tree.selection_set(item_id)
                self.modbus_list_menu.tk_popup(
                    self.tree.winfo_pointerx(),
                    self.tree.winfo_pointery()
                )


    def subinterface_callback(
        self, new_value, sensor_updates = [], signal_updates = [], signal_remove = [],
        condition_vector_add = [], bearing_updates = [], table = None, x = None, y = None,
        name = '', regime_updates = [], air_gap_plane_updates = []
    ):
        #-----------------------------------------------------------
        #sensor_updates: list of dicts [{"name":name,"label":label}]
        #signal_updates: list of dicts [{"name":name,"label":label}] 
        #-----------------------------------------------------------
        #Enable main window after it was disabled.
        self.master.wm_attributes("-disabled", False)
        self.update_param(self.doubleclicked_item, new_value)
        for i in sensor_updates:
            self.update_name_in_table(
                unit = self.doubleclicked_item.get_item_data()['unitName'],
                label = i['label'],
                name = i['name'],
                table_type = TableType.SENSORS
                )
        for i in bearing_updates:
            self.update_name_in_table(
                unit = self.doubleclicked_item.get_item_data()['unitName'],
                label = i['label'],
                name = i['name'],
                table_type = TableType.BEARINGS
                )
        for i in regime_updates:
            self.update_name_in_table(
                unit = self.doubleclicked_item.get_item_data()['unitName'],
                label = i['label'],
                name = i['name'],
                table_type = TableType.REGIMES
                )
        for i in air_gap_plane_updates:
            self.update_name_in_table(
                unit = self.doubleclicked_item.get_item_data()['unitName'],
                label = i['label'],
                name = i['name'],
                table_type = TableType.AIR_GAP_PLANES
                )
        for i in signal_updates:
            self.update_name_in_table(
                unit = self.doubleclicked_item.get_item_data()['unitName'],
                label = i['label'],
                name = i['name'],
                table_type = TableType.SIGNALS)
        for i in condition_vector_add:
            self.add_condition_vector_element(
                unit = self.doubleclicked_item.get_item_data()['unitName'],
                source = self.doubleclicked_item.get_item_data()['sourceName'],
                label = i['label']
            )
        for i in signal_remove:
            self.remove(
                unit = self.doubleclicked_item.get_item_data()['unitName'],
                label = i['label'],
                table_type = TableType.SIGNALS
            )
            self.remove_condition_vector_element(
                unit = self.doubleclicked_item.get_item_data()['unitName'],
                source = self.doubleclicked_item.get_item_data()['sourceName'],
                label = i['label']
            )
        self.update_tree()
        #update info text after param has been modified.
        item = self.find_item(item_id = self.doubleclicked_item.get_item_id())
        self.set_info_text(dumps(self.get_param_value(item)))

    def cancel_callback(self):
        #Enable main window after it was disabled.
        self.master.wm_attributes("-disabled", False)


#------------------------------------------------------------------
#                      Channels analysis
#------------------------------------------------------------------ 

    def add_dc(self):
        self.master.wm_attributes("-disabled", True)
        item = self.rightclicked_item
        unit = item.get_item_data()['unitName']
        ch_label = item.get_item_data()['label']
        sensor_name = self.get_name_from_table(
            unit = unit,
            label = ch_label,
            table_type = TableType.SENSORS)
        signal_label = f'{ch_label}.DC'
        signal_name = f'{sensor_name} Dc'

        ChannelAnalysisDC(
            init_value = {
                'analysis': 'dc',
                'param':{
                    'triggerToTrigger': True
                },
                'performOnServer': False    
            },
            signal_label = signal_label,
            signal_name = signal_name,
            callback = self.add_channel_analysis_callback,
            cancel_callback = self.cancel_callback,
            x = self.tree.winfo_pointerx(),
            y = self.tree.winfo_pointery()
        )

    def add_sig_freq(self):
        self.master.wm_attributes("-disabled", True)
        item = self.rightclicked_item
        unit = item.get_item_data()['unitName']
        ch_label = item.get_item_data()['label']
        sensor_name = self.get_name_from_table(
            unit = unit,
            label = ch_label,
            table_type = TableType.SENSORS)
        signal_label = f'{ch_label}.SignalFrequency'
        signal_name = f'{sensor_name} Signal Frequency'

        NoParameterAnalysis(
            title = 'sigfreq',
            init_value = {
                'analysis': 'signalFrequency',
                'performOnServer': False
            },
            signal_label = signal_label,
            signal_name = signal_name,
            callback = self.add_channel_analysis_callback,
            cancel_callback = self.cancel_callback,
            x = self.tree.winfo_pointerx(),
            y = self.tree.winfo_pointery()
        )

    def add_thd(self):
        self.master.wm_attributes("-disabled", True)
        item = self.rightclicked_item
        unit = item.get_item_data()['unitName']
        ch_label = item.get_item_data()['label']
        sensor_name = self.get_name_from_table(unit = unit,
        label = ch_label,
        table_type = TableType.SENSORS)
        signal_label = f'{ch_label}.THD'
        signal_name = f'{sensor_name} Thd'

        NoParameterAnalysis(
            title = 'thd',
            init_value = {
                'analysis': 'thd',
                'performOnServer': False
            },
            signal_label = signal_label,
            signal_name = signal_name,
            callback = self.add_channel_analysis_callback,
            cancel_callback = self.cancel_callback,
            x = self.tree.winfo_pointerx(),
            y = self.tree.winfo_pointery()
        )

    def add_rms(self):
        self.master.wm_attributes("-disabled", True)
        item = self.rightclicked_item
        unit = item.get_item_data()['unitName']
        source = item.get_item_data()['sourceName']
        ch_label = item.get_item_data()['label']
        sig_label = f'{ch_label}.RMS'
        c_v = self.get_condition_vector_element(unit, source, sig_label)
        labelAddition = ''
        if c_v != None:
            suffix = 0
            labelAddition = str(suffix)
            sig_label = f'{ch_label}.RMS{suffix}'
            c_v = self.get_condition_vector_element(unit, source, sig_label)
            while c_v != None:
                sig_label = f'{ch_label}.RMS{suffix}'
                labelAddition = str(suffix)
                c_v = self.get_condition_vector_element(unit, source, sig_label)
                suffix += 1
        sensor_name = self.get_name_from_table(
            unit = unit,
            label = ch_label,
            table_type = TableType.SENSORS)
        sig_name = f'{sensor_name} Rms'
        ChannelAnalysisRms(
            init_value = {
                'analysis': 'rms',
                'param':{
                    'averagePerRevolution':False,
                    'filterParam':{
                        'f1':0,
                        'f2':0,
                        'filter':False,
                        'order':0,
                        'type':'Lowpass'
                    },
                    'glide':False,
                    'labelAddition':'',
                    'numOfPoints':0,
                    'substractDc':False,
                    'triggerToTrigger':False,
                    'labelAddition': labelAddition
                },
                'performOnServer': False    
            },
            signal_label = sig_label,
            signal_name = sig_name,
            callback = self.add_channel_analysis_callback,
            cancel_callback = self.cancel_callback,
            x = self.tree.winfo_pointerx(),
            y = self.tree.winfo_pointery()
        )

    def add_eq_peak(self):
        self.master.wm_attributes("-disabled", True)
        item = self.rightclicked_item
        unit = item.get_item_data()['unitName']
        source = item.get_item_data()['sourceName']
        ch_label = item.get_item_data()['label']
        sig_label = f'{ch_label}.EqPeak'
        c_v = self.get_condition_vector_element(unit, source, sig_label)
        labelAddition = ''
        if c_v != None:
            suffix = 0
            labelAddition = str(suffix)
            sig_label = f'{ch_label}.EqPeak{suffix}'
            c_v = self.get_condition_vector_element(unit, source, sig_label)
            while c_v != None:
                sig_label = f'{ch_label}.EqPeak{suffix}'
                labelAddition = str(suffix)
                c_v = self.get_condition_vector_element(unit, source, sig_label)
                suffix += 1
        sensor_name = self.get_name_from_table(
            unit = unit,
            label = ch_label,
            table_type = TableType.SENSORS
            )
        sig_name = f'{sensor_name} Eq. Peak'
        PeakAnalysis(
            title = 'EqPeak',
            init_value = {
                'analysis': 'eqPeak',
                'param':{
                    'averagePerRevolution':False,
                    'filterParam':{
                        'f1':0,
                        'f2':0,
                        'filter':False,
                        'order':0,
                        'type':'Lowpass'
                    },
                    'glide':False,
                    'labelAddition':'',
                    'numOfPoints':0,
                    'substractDc':False,
                    'triggerToTrigger':False,
                    'labelAddition': labelAddition
                },
                'performOnServer': False    
            },
            signal_label = sig_label,
            signal_name = sig_name,
            callback = self.add_channel_analysis_callback,
            cancel_callback = self.cancel_callback,
            x = self.tree.winfo_pointerx(),
            y = self.tree.winfo_pointery()
        )

    def add_harmonic(self):
        self.master.wm_attributes("-disabled", True)
        item = self.rightclicked_item
        unit = item.get_item_data()['unitName']
        source = item.get_item_data()['sourceName']
        ch_label = item.get_item_data()['label']
        sensor_name = self.get_name_from_table(
            unit = unit,
            label = ch_label,
            table_type = TableType.SENSORS
            )
        found = False
        if '[' and ']' in sensor_name:
            found = True
            bracket_position_start = sensor_name.find('[')
            bracket_position_end = sensor_name.find(']')+1
            measuring_unit = sensor_name[bracket_position_start:bracket_position_end]
        if found:
            sensor_name_reduced = sensor_name[:bracket_position_start]
            sig_name_A = f'{sensor_name_reduced} 1x Ampl {measuring_unit}'
            sig_name_Ph = f'{sensor_name_reduced} 1x Phase [deg]'
        else:
            sig_name_A = f'{sensor_name} 1x Ampl'
            sig_name_Ph = f'{sensor_name} 1x Phase [deg]'
        ChannelAnalysisHarmonic(
            init_value = {
                'analysis': 'snA&Ph',
                'param':{
                    'amplitude':True,
                    'harmonic':1, 
                },
                'performOnServer': False    
            },
            channel_label = ch_label,
            signal_name_A = sig_name_A,
            signal_name_Ph = sig_name_Ph,
            callback = self.add_channel_analysis_callback,
            cancel_callback = self.cancel_callback,
            x = self.tree.winfo_pointerx(),
            y = self.tree.winfo_pointery()
        )

    def add_peak2peak(self):
        self.master.wm_attributes("-disabled", True)
        item = self.rightclicked_item
        unit = item.get_item_data()['unitName']
        source = item.get_item_data()['sourceName']
        ch_label = item.get_item_data()['label']
        sig_label = f'{ch_label}.Peak2Peak'
        c_v = self.get_condition_vector_element(unit, source, sig_label)
        labelAddition = ''
        if c_v != None:
            suffix = 0
            labelAddition = str(suffix)
            sig_label = f'{ch_label}.Peak2Peak{suffix}'
            c_v = self.get_condition_vector_element(unit, source, sig_label)
            while c_v != None:
                sig_label = f'{ch_label}.Peak2Peak{suffix}'
                labelAddition = str(suffix)
                c_v = self.get_condition_vector_element(unit, source, sig_label)
                suffix += 1
        sensor_name = self.get_name_from_table(
            unit = unit,
            label = ch_label,
            table_type = TableType.SENSORS
            )
        sig_name = f'{sensor_name} Peak2Peak'
        PeakAnalysis(
            title = 'Peak2Peak',
            init_value = {
                "analysis": "peak2peak",
                "param": {
                    "filterParam": {
                    "f1": 100,
                    "f2": 0,
                    "filter": False,
                    "order": 0,
                    "type": "Lowpass"
                    },
                    "averagePerRevolution": False,
                    "glide": False,
                    "labelAddition": labelAddition,
                    "numOfPoints": 5,
                    "triggerToTrigger": False
                },
                "performOnServer": False
            },
            signal_label = sig_label,
            signal_name = sig_name,
            callback = self.add_channel_analysis_callback,
            cancel_callback = self.cancel_callback,
            x = self.tree.winfo_pointerx(),
            y = self.tree.winfo_pointery()
        )

    def add_rest(self):
        self.master.wm_attributes("-disabled", True)
        item = self.rightclicked_item
        unit = item.get_item_data()['unitName']
        ch_label = item.get_item_data()['label']
        sensor_name = self.get_name_from_table(
            unit = unit,
            label = ch_label,
            table_type = TableType.SENSORS)
        signal_label = f'{ch_label}.Rest'
        signal_name = f'{sensor_name} Rest'
        ChannelAnalysisRest(
            init_value = {
                'analysis': 'rest',
                'param':{
                    'amplitude': True
                },
                'performOnServer': False
            },
            signal_label = signal_label,
            signal_name = signal_name,
            callback = self.add_channel_analysis_callback,
            cancel_callback = self.cancel_callback,
            x = self.tree.winfo_pointerx(),
            y = self.tree.winfo_pointery()
        )       

    def add_air_gap_analysis(self):
        self.master.wm_attributes("-disabled", True)
        item = self.rightclicked_item
        unit = item.get_item_data()['unitName']
        source = item.get_item_data()['sourceName']
        num_of_poles = self.get_number_of_poles(unit, source)
        ch_label = item.get_item_data()['label']
        sensor_name = self.get_name_from_table(
            unit = unit,
            label = ch_label,
            table_type = TableType.SENSORS)
        init_value = {
            'analysis':'airGap',
            'param':{
                'threshold': 10,
                'regimeParam': []
            },
            'performOnServer': False
        }
        pairs = []
        regime_labels = self.get_regime_labels_from_mc(unit, source)
        if regime_labels == []:
            messagebox.showinfo("Error:", "There is no regimes defined.")
            self.master.wm_attributes("-disabled", False)
        elif num_of_poles == None or num_of_poles == 0:
            messagebox.showinfo("Error:", "The number of poles is equal to 0 or not determined.")
            self.master.wm_attributes("-disabled", False)
        else:
            for i in regime_labels:
                pairs.append(
                    {
                        'label': i,
                        'name': self.get_name_from_table(unit, i, TableType.REGIMES)
                    }
                )
                init_value['param']['regimeParam'].append({
                    'regime': i,
                    'firstPoleAfterTrigger': 0,
                    'poleNumbersAscending': True
                })
            reg_pairs = Label_name_pairs(pairs)
            ChannelAnalysisAirGap(
                init_value = init_value,
                channel_label = ch_label,
                sensor_name = sensor_name,
                reg_pairs = reg_pairs,
                number_of_poles = num_of_poles,
                callback = self.add_channel_analysis_callback,
                cancel_callback = self.cancel_callback,
                x = self.tree.winfo_pointerx(),
                y = self.tree.winfo_pointery()
            )

    def add_channel_rpm(self):
        self.master.wm_attributes("-disabled", True)
        item = self.rightclicked_item
        unit = item.get_item_data()['unitName']
        source = item.get_item_data()['sourceName']
        ch_label = item.get_item_data()['label']
        sensor_name = self.get_name_from_table(
            unit = unit,
            label = ch_label,
            table_type = TableType.SENSORS)
        signal_label = f'{ch_label}.RotSpeed'
        signal_name = f'{sensor_name} rotational speed [rpm]'
        ChannelAnalysisRpm(
            init_value = {
                'analysis': 'rpm',
                'param':{
                    'onRising': True,
                    'pulseWidth': 2,
                    'treshold': 9
                 },
                'performOnServer': False
            },
            signal_label = signal_label,
            signal_name = signal_name,
            callback = self.add_channel_analysis_callback,
            cancel_callback = self.cancel_callback,
            x = self.tree.winfo_pointerx(),
            y = self.tree.winfo_pointery()
        )


    def add_channel_analysis_callback(self, new_value, signal_updates):
        self.master.wm_attributes("-disabled", False)
        item = self.rightclicked_item
        unit = item.get_item_data()['unitName']
        source = item.get_item_data()['sourceName']
        label = item.get_item_data()['label']
        self.add_channel_analysis(unit, source, label, new_value)
        for i in signal_updates:
            self.update_name_in_table(
                unit = unit,
                label = i['label'],
                name = i['name'],
                table_type = TableType.SIGNALS
            )
            self.add_condition_vector_element(
                unit = unit,
                source = source,
                label = i['label']
            )
        self.reindex_channel_analyses_items(unit, source, label)

    def remove_channel_analysis_event(self):
        item = self.rightclicked_item
        unit = item.get_item_data()['unitName']
        source = item.get_item_data()['sourceName']
        ch_label = item.get_item_data()['label']
        ch_name = self.get_name_from_table(
            unit = unit,
            label = ch_label,
            table_type = TableType.SENSORS
        )
        index = item.get_item_data()['index']
        analysis_data = self.get_param_value(item)
        signal_updates = self.get_channel_signal_data(
            unit = unit,
            source = source,
            channel_label = ch_label,
            channel_name = ch_name,
            analysis_data = analysis_data
        )
        c_v_labels = []
        for i in signal_updates:
            c_v_labels.append(i['label'])
        for c_v_label in c_v_labels:
            self.remove_condition_vector_element(unit, source, c_v_label)
            self.remove(unit, c_v_label, TableType.SIGNALS)
        self.remove_channel_analysis(unit, source, ch_label, index)
        self.reindex_channel_analyses_items(unit, source, ch_label)

#------------------------------------------------------------------
#                        Channels
#------------------------------------------------------------------

    def add_trigger(self):
        self.master.wm_attributes("-disabled", True)
        item = self.rightclicked_item
        unit = item.get_item_data()['unitName']
        source = item.get_item_data()['sourceName']
        init_value = self.get_initial_configuration('trigger')
        m_c = self.get_main_cluster()
        labels = []
        for i in m_c:
            if Unit.get_unit(i['unitName']) == unit:
                labels.extend(self.get_sensor_labels_from_mc(
                    unit = unit,
                    source = Source.get_source(i['sourceName'])
                ))
        u = Unit.get_string(unit)
        s = Source.get_string(source)
        label_root = f'{u}.{s}.SEN'
        counter = 0
        while label_root+str(counter) in labels:
            counter += 1
        init_value['label'] = label_root+str(counter)
        ChannelInterface(
                    init_value = init_value,
                    ch_name = "Trigger",
                    callback = self.add_channel_callback,
                    cancel_callback = self.cancel_callback,
                    x = self.tree.winfo_pointerx(),
                    y = self.tree.winfo_pointery()   
                )

    def add_relative_vib(self):
        self.master.wm_attributes("-disabled", True)
        item = self.rightclicked_item
        unit = item.get_item_data()['unitName']
        source = item.get_item_data()['sourceName']
        init_value = self.get_initial_configuration('relative_vibration')
        m_c = self.get_main_cluster()
        labels = []
        for i in m_c:
            if Unit.get_unit(i['unitName']) == unit:
                labels.extend(self.get_sensor_labels_from_mc(
                    unit = unit,
                    source = Source.get_source(i['sourceName'])
                ))
        u = Unit.get_string(unit)
        s = Source.get_string(source)
        label_root = f'{u}.{s}.SEN'
        counter = 0
        while label_root+str(counter) in labels:
            counter += 1
        init_value['label'] = label_root+str(counter)
        ChannelInterface(
                    init_value = init_value,
                    ch_name = "Relative vibrations",
                    callback = self.add_channel_callback,
                    cancel_callback = self.cancel_callback,
                    x = self.tree.winfo_pointerx(),
                    y = self.tree.winfo_pointery()   
                )

    def add_velometer(self):
        self.master.wm_attributes("-disabled", True)
        item = self.rightclicked_item
        unit = item.get_item_data()['unitName']
        source = item.get_item_data()['sourceName']
        init_value = self.get_initial_configuration('velometer')
        m_c = self.get_main_cluster()
        labels = []
        for i in m_c:
            if Unit.get_unit(i['unitName']) == unit:
                labels.extend(self.get_sensor_labels_from_mc(
                    unit = unit,
                    source = Source.get_source(i['sourceName'])
                ))
        u = Unit.get_string(unit)
        s = Source.get_string(source)
        label_root = f'{u}.{s}.SEN'
        counter = 0
        while label_root+str(counter) in labels:
            counter += 1
        init_value['label'] = label_root+str(counter)
        ChannelInterface(
                    init_value = init_value,
                    ch_name = "Absolute vibrations - velometer",
                    callback = self.add_channel_callback,
                    cancel_callback = self.cancel_callback,
                    x = self.tree.winfo_pointerx(),
                    y = self.tree.winfo_pointery()   
                )
        
    def add_accelerometer(self):
        self.master.wm_attributes("-disabled", True)
        item = self.rightclicked_item
        unit = item.get_item_data()['unitName']
        source = item.get_item_data()['sourceName']
        init_value = self.get_initial_configuration('accelerometer')
        m_c = self.get_main_cluster()
        labels = []
        for i in m_c:
            if Unit.get_unit(i['unitName']) == unit:
                labels.extend(self.get_sensor_labels_from_mc(
                    unit = unit,
                    source = Source.get_source(i['sourceName'])
                ))
        u = Unit.get_string(unit)
        s = Source.get_string(source)
        label_root = f'{u}.{s}.SEN'
        counter = 0
        while label_root+str(counter) in labels:
            counter += 1
        init_value['label'] = label_root+str(counter)
        ChannelInterface(
                    init_value = init_value,
                    ch_name = "Absolute vibrations - accelerometer",
                    callback = self.add_channel_callback,
                    cancel_callback = self.cancel_callback,
                    x = self.tree.winfo_pointerx(),
                    y = self.tree.winfo_pointery()   
                )

    def add_absolute_vibration_stator_core(self):
        self.master.wm_attributes("-disabled", True)
        item = self.rightclicked_item
        unit = item.get_item_data()['unitName']
        source = item.get_item_data()['sourceName']
        init_value = self.get_initial_configuration('stator_core')
        m_c = self.get_main_cluster()
        labels = []
        for i in m_c:
            if Unit.get_unit(i['unitName']) == unit:
                labels.extend(self.get_sensor_labels_from_mc(
                    unit = unit,
                    source = Source.get_source(i['sourceName'])
                ))
        u = Unit.get_string(unit)
        s = Source.get_string(source)
        label_root = f'{u}.{s}.SEN'
        counter = 0
        while label_root+str(counter) in labels:
            counter += 1
        init_value['label'] = label_root+str(counter)
        num_of_poles = self.get_number_of_poles(unit, source)
        for i in range(1,4):
            parameters = init_value['analyses'][i-1]['param']
            parameters['harmonic'] = num_of_poles*i
        ChannelInterface(
                    init_value = init_value,
                    ch_name = "Absolute vibrations - stator core",
                    callback = self.add_channel_callback,
                    cancel_callback = self.cancel_callback,
                    x = self.tree.winfo_pointerx(),
                    y = self.tree.winfo_pointery()   
                )
    
    def add_air_gap(self):
        self.master.wm_attributes("-disabled", True)
        item = self.rightclicked_item
        unit = item.get_item_data()['unitName']
        source = item.get_item_data()['sourceName']
        init_value = self.get_initial_configuration('air_gap')
        m_c = self.get_main_cluster()
        labels = []
        for i in m_c:
            if Unit.get_unit(i['unitName']) == unit:
                labels.extend(self.get_sensor_labels_from_mc(
                    unit = unit,
                    source = Source.get_source(i['sourceName'])
                ))
        u = Unit.get_string(unit)
        s = Source.get_string(source)
        label_root = f'{u}.{s}.SEN'
        counter = 0
        while label_root+str(counter) in labels:
            counter += 1
        init_value['label'] = label_root+str(counter)
        ChannelInterface(
                    init_value = init_value,
                    ch_name = "Air gap",
                    callback = self.add_channel_callback,
                    cancel_callback = self.cancel_callback,
                    x = self.tree.winfo_pointerx(),
                    y = self.tree.winfo_pointery()   
                )
    
    def add_channel_callback(self, new_value, sensor_updates):
        self.master.wm_attributes("-disabled", False)
        item = self.rightclicked_item
        unit = item.get_item_data()['unitName']
        source = item.get_item_data()['sourceName']
        parent_id = item.get_item_id()
        self.add_channel(unit, source, new_value)
        for i in sensor_updates:
            self.update_name_in_table(
                unit = unit,
                label = i['label'],
                name = i['name'],
                table_type = TableType.SENSORS
            )
        channel_id = self.append_item(
                    parent_id = parent_id,
                    item_type =ItemType.CHANNEL,
                    item_data = {
                        'unitName': unit,
                        'sourceName': source,
                        'label': new_value['label']
                    }
        )
        channel_analyses_list_id = self.append_item(
            parent_id = channel_id,
            item_type =ItemType.CHANNEL_ANALYSES_LIST,
            item_data = {
                'unitName': unit,
                'sourceName': source,
                'label': new_value['label']
            }
        )
        index = 0
        for k in new_value['analyses']:
            signal_updates = self.get_channel_signal_data(
                unit = unit,
                source = source,
                channel_label = new_value['label'],
                channel_name = sensor_updates[0]['name'],
                analysis_data = k
            )
            if signal_updates != None:
                for i in signal_updates:
                    self.update_name_in_table(
                    unit = unit,
                    label = i['label'],
                    name = i['name'],
                    table_type = TableType.SIGNALS
                    )
                    self.add_condition_vector_element(
                        unit = unit,
                        source = source,
                        label = i['label']
                    )
            self.append_item(
                parent_id = channel_analyses_list_id,
                item_type =ItemType.CHANNEL_ANALYSIS,
                item_data = {
                'unitName': unit,
                'sourceName': source,
                'label': new_value['label'],
                'index': index
                }
            )
            index += 1
        self.append_item(
            parent_id = channel_id,
            item_type =ItemType.PHYSICAL_CHANNEL,
            value = new_value['physicalChannel'],
            item_data = {
                'unitName': unit,
                'sourceName': source,
                'label': new_value['label']
            }
        )
        self.append_item(
            parent_id = channel_id,
            item_type =ItemType.SLOPE,
            value = new_value['slope'],
            item_data = {
                'unitName': unit,
                'sourceName': source,
                'label': new_value['label']
            }
        )
        self.append_item(
            parent_id = channel_id,
            item_type =ItemType.INTERCEPT,
            value = new_value['intercept'],
            item_data = {
                'unitName': unit,
                'sourceName': source,
                'label': new_value['label']
            }
        )
        item_id = self.tree.selection()[0]
        self.item_selected(item_id)

    def remove_channel_event(self):
        item = self.rightclicked_item
        unit = item.get_item_data()['unitName']
        source = item.get_item_data()['sourceName']
        ch_label = item.get_item_data()['label']
        self.remove_analyses_from_channel(unit, source, ch_label)
        self.remove_channel_item(unit, source, ch_label)
        self.remove_channel(unit, source, ch_label)
        self.remove(
            unit = unit,
            label = ch_label,
            table_type = TableType.SENSORS)
        self.remove_channel_from_other_items(unit, source, ch_label)

#------------------------------------------------------------------
#                        Bearings
#------------------------------------------------------------------

    def add_new_bearing(self):
        self.master.wm_attributes("-disabled", True)
        item = self.rightclicked_item
        unit = item.get_item_data()['unitName']
        source = item.get_item_data()['sourceName']
        init_value = self.get_initial_configuration('bearing')
        m_c = self.get_main_cluster()
        labels = []
        for i in m_c:
            if Unit.get_unit(i['unitName']) == unit:
                labels.extend(self.get_bearing_labels_from_mc(
                    unit = unit,
                    source = Source.get_source(i['sourceName'])
                ))
        u = Unit.get_string(unit)
        s = Source.get_string(source)
        label_root = f'{u}.{s}.BRG'
        counter = 0
        while label_root+str(counter) in labels:
            counter += 1
        init_value['label'] = label_root+str(counter)
        pairs = []
        for i in self.get_sensor_labels_from_mc(unit, source):
            pairs.append(
                {
                    'label': i,
                    'name': self.get_name_from_table(unit, i, TableType.SENSORS)
                }
            )
        table = Label_name_pairs(pairs)
        BearingInterface(
            init_value = init_value,
            bearing_name = 'Bearing',
            ch_pairs = table,
            callback = self.add_bearing_callback,
            cancel_callback = self.cancel_callback,
            x = self.tree.winfo_pointerx(),
            y = self.tree.winfo_pointery()
        )

    def add_bearing_callback(
        self,
        new_value,
        bearing_updates,
        x = None,
        y = None,
        table = None,
        name = ''):
        if 'xDirection' not in new_value or 'yDirection' not in new_value:
            messagebox.showinfo("Error:", "Please select X and/or Y direction Sensors.")
            BearingInterface(
            init_value = new_value,
            bearing_name = name,
            ch_pairs = table,
            callback = self.add_bearing_callback,
            cancel_callback = self.cancel_callback,
            x = x,
            y = y
        )
        else:
            self.master.wm_attributes("-disabled", False)
            item = self.rightclicked_item
            unit = item.get_item_data()['unitName']
            source = item.get_item_data()['sourceName']
            parent_id = item.get_item_id()
            self.add_bearing(unit, source, new_value)
            for i in bearing_updates:
                self.update_name_in_table(
                    unit = unit,
                    label = i['label'],
                    name = i['name'],
                    table_type = TableType.BEARINGS
                )
            bearing_id = self.append_item(
                    parent_id = parent_id,
                    item_type = ItemType.BEARING,
                    item_data = {
                            'unitName': unit,
                            'sourceName': source,
                            'label': new_value['label']
                    }
            )
            bearing_analyses_list_id = self.append_item(
                parent_id = bearing_id,
                item_type = ItemType.BEARING_ANALYSES_LIST,
                item_data = {
                    'unitName': unit,
                    'sourceName': source,
                    'label': new_value['label']
                }
            )
            index = 0
            for k in new_value['analyses']:
                signal_updates = self.get_bearing_signal_data(
                    bearing_label = new_value['label'],
                    bearing_name = bearing_updates[0]['name'],
                    analysis_data = k                
                )
                if signal_updates != None:
                    for i in signal_updates:
                        self.update_name_in_table(
                        unit = unit,
                        label = i['label'],
                        name = i['name'],
                        table_type = TableType.SIGNALS
                        )
                        self.add_condition_vector_element(
                            unit = unit,
                            source = source,
                            label = i['label']
                        )
                self.append_item(
                    parent_id = bearing_analyses_list_id,
                    item_type = ItemType.BEARING_ANALYSIS,
                    item_data = {
                    'unitName': unit,
                    'sourceName': source,
                    'label': new_value['label'],
                    'index': index
                    }
                )
                index +=1
        item_id = self.tree.selection()[0]
        self.item_selected(item_id)

    def remove_bearing_event(self):
        item = self.rightclicked_item
        unit = item.get_item_data()['unitName']
        source = item.get_item_data()['sourceName']
        bearing_label = item.get_item_data()['label']
        self.remove_analyses_from_bearing(unit, source, bearing_label)
        self.remove_bearing_item(unit, source, bearing_label)
        self.remove_bearing(unit, source, bearing_label)
        self.remove(
            unit = unit,
            label = bearing_label,
            table_type = TableType.BEARINGS)
        

#------------------------------------------------------------------
#                      Bearing analysis
#------------------------------------------------------------------

    def add_Smax(self):
        self.master.wm_attributes("-disabled", True)
        item = self.rightclicked_item
        unit = item.get_item_data()['unitName']
        source = item.get_item_data()['sourceName']
        bearing_label = item.get_item_data()['label']
        signal_label = f'{bearing_label}.Smax'
        c_v = self.get_condition_vector_element(unit, source, signal_label)
        labelAddition = ''
        if c_v != None:
            suffix = 0
            labelAddition = str(suffix)
            signal_label = f'{bearing_label}.Smax{suffix}'
            c_v = self.get_condition_vector_element(unit, source, signal_label)
            while c_v != None:
                signal_label = f'{bearing_label}.Smax{suffix}'
                labelAddition = str(suffix)
                c_v = self.get_condition_vector_element(unit, source, signal_label)
                suffix += 1
        bearing_name = self.get_name_from_table(
            unit = unit,
            label = bearing_label,
            table_type = TableType.BEARINGS
            )
        signal_name = f'{bearing_name} Smax'
        PeakAnalysis(
            title = 'Smax',
            init_value = {
                "analysis": "Smax",
                "param": {
                    "filterParam": {
                    "f1": 100,
                    "f2": 0,
                    "filter": False,
                    "order": 0,
                    "type": "Lowpass"
                    },
                    "averagePerRevolution": False,
                    "glide": False,
                    "labelAddition": labelAddition,
                    "numOfPoints": 5,
                    "triggerToTrigger": False
                },
                "performOnServer": False
            },
            signal_label = signal_label,
            signal_name = signal_name,
            callback = self.add_bearing_analysis_callback,
            cancel_callback = self.cancel_callback,
            x = self.tree.winfo_pointerx(),
            y = self.tree.winfo_pointery()
        )

    def add_SP2Pmax(self):
        self.master.wm_attributes("-disabled", True)
        item = self.rightclicked_item
        unit = item.get_item_data()['unitName']
        source = item.get_item_data()['sourceName']
        bearing_label = item.get_item_data()['label']
        signal_label = f'{bearing_label}.SP2Pmax'
        c_v = self.get_condition_vector_element(unit, source, signal_label)
        labelAddition = ''
        if c_v != None:
            suffix = 0
            labelAddition = str(suffix)
            signal_label = f'{bearing_label}.SP2Pmax{suffix}'
            c_v = self.get_condition_vector_element(unit, source, signal_label)
            while c_v != None:
                signal_label = f'{bearing_label}.SP2Pmax{suffix}'
                labelAddition = str(suffix)
                c_v = self.get_condition_vector_element(unit, source, signal_label)
                suffix += 1
        bearing_name = self.get_name_from_table(
            unit = unit,
            label = bearing_label,
            table_type = TableType.BEARINGS
            )
        signal_name = f'{bearing_name} SP2Pmax'
        PeakAnalysis(
            title = 'SP2Pmax',
            init_value = {
                "analysis": "SP2Pmax",
                "param": {
                    "filterParam": {
                    "f1": 100,
                    "f2": 0,
                    "filter": False,
                    "order": 0,
                    "type": "Lowpass"
                    },
                    "averagePerRevolution": False,
                    "glide": False,
                    "labelAddition": labelAddition,
                    "numOfPoints": 5,
                    "triggerToTrigger": False
                },
                "performOnServer": False
            },
            signal_label = signal_label,
            signal_name = signal_name,
            callback = self.add_bearing_analysis_callback,
            cancel_callback = self.cancel_callback,
            x = self.tree.winfo_pointerx(),
            y = self.tree.winfo_pointery()
        )

    def add_bearing_analysis_callback(self, new_value, signal_updates):
        self.master.wm_attributes("-disabled", False)
        item = self.rightclicked_item
        unit = item.get_item_data()['unitName']
        source = item.get_item_data()['sourceName']
        bearing_label = item.get_item_data()['label']
        self.add_bearing_analysis(unit, source, bearing_label, new_value)
        for i in signal_updates:
            self.update_name_in_table(
                unit = unit,
                label = i['label'],
                name = i['name'],
                table_type = TableType.SIGNALS
            )
            self.add_condition_vector_element(
                unit = unit,
                source = source,
                label = i['label']
            )
        self.reindex_bearing_analyses_items(unit, source, bearing_label)

    def remove_bearing_analysis_event(self):
        item = self.rightclicked_item
        unit = item.get_item_data()['unitName']
        source = item.get_item_data()['sourceName']
        bearing_label = item.get_item_data()['label']
        bearing_name = self.get_name_from_table(
            unit = unit,
            label = bearing_label,
            table_type = TableType.BEARINGS
        )
        index = item.get_item_data()['index']
        analysis_data = self.get_param_value(item)
        signal_updates = self.get_bearing_signal_data(
            bearing_label = bearing_label,
            bearing_name = bearing_name,
            analysis_data = analysis_data
        )
        c_v_labels = []
        for i in signal_updates:
            c_v_labels.append(i['label'])
        for c_v_label in c_v_labels:
            self.remove_condition_vector_element(unit, source, c_v_label)
            self.remove(unit, c_v_label, TableType.SIGNALS)
        self.remove_bearing_analysis(unit, source, bearing_label, index)
        self.reindex_bearing_analyses_items(unit, source, bearing_label)

#------------------------------------------------------------------
#                      Air gap planes
#------------------------------------------------------------------

    def add_new_air_gap_plane(self):
        self.master.wm_attributes("-disabled", True)
        item = self.rightclicked_item
        unit = item.get_item_data()['unitName']
        source = item.get_item_data()['sourceName']
        init_value = {
            'label': 'AGP000',
            'sensors': []
        }
        m_c = self.get_main_cluster()
        labels = []
        for i in m_c:
            if Unit.get_unit(i['unitName']) == unit:
                labels.extend(self.get_air_gap_plane_labels_from_mc(
                    unit = unit,
                    source = Source.get_source(i['sourceName'])
                ))

        u = Unit.get_string(unit)
        s = Source.get_string(source)
        label_root = f'{u}.{s}.AGP'
        counter = 0
        while label_root+str(counter) in labels:
            counter += 1
        init_value['label'] = label_root+str(counter)
        pairs = []
        for i in self.get_sensor_labels_from_mc(unit, source):
            pairs.append(
                {
                    'label': i,
                    'name': self.get_name_from_table(unit, i, TableType.SENSORS)
                }
            )
        table = Label_name_pairs(pairs)
        AirGapPlaneInterface(
            init_value = init_value,
            agp_name = 'Air gap plane',
            ch_pairs = table,
            cancel_callback = self.cancel_callback,
            callback = self.add_air_gap_plane_callback,
            x = self.tree.winfo_pointerx(),
            y = self.tree.winfo_pointery()
        )

    def add_air_gap_plane_callback(self, new_value, signal_updates, air_gap_plane_updates):
        self.master.wm_attributes("-disabled", False)
        item = self.rightclicked_item
        unit = item.get_item_data()['unitName']
        source = item.get_item_data()['sourceName']
        parent_id = item.get_item_id()
        self.add_air_gap_plane(unit, source, new_value)
        for i in air_gap_plane_updates:
            self.update_name_in_table(
                unit = unit,
                label = i['label'],
                name = i['name'],
                table_type = TableType.AIR_GAP_PLANES
            )
        air_gap_plane_id = self.append_item(
                    parent_id = parent_id,
                    item_type =ItemType.AIR_GAP_PLANE,
                    item_data = {
                        'unitName': unit,
                        'sourceName': source,
                        'label': new_value['label']
                    }
        )
        for i in signal_updates:
            self.update_name_in_table(
            unit = unit,
            label = i['label'],
            name = i['name'],
            table_type = TableType.SIGNALS
            )
            self.add_condition_vector_element(
                unit = unit,
                source = source,
                label = i['label']
            )
        item_id = self.tree.selection()[0]
        self.item_selected(item_id)

    def remove_air_gap_plane_event(self):
        item = self.rightclicked_item
        unit = item.get_item_data()['unitName']
        source = item.get_item_data()['sourceName']
        agp_label = item.get_item_data()['label']
        self.remove_item(item)
        self.remove_air_gap_plane(unit, source, agp_label)
        self.remove(
            unit = unit,
            label = agp_label,
            table_type = TableType.AIR_GAP_PLANES
        )
        c_v_labels = []
        c_v_labels.append(f'{agp_label}.MinExtremaMin')
        c_v_labels.append(f'{agp_label}.MinExtremaMinPoleNum')
        c_v_labels.append(f'{agp_label}.MaxDiff')
        c_v_labels.append(f'{agp_label}.MaxDiffPoleNum')
        for c_v_label in c_v_labels:
            self.remove_condition_vector_element(unit, source, c_v_label)


#------------------------------------------------------------------
#                      Unit analysis
#------------------------------------------------------------------

    def add_rpm(self):
        self.master.wm_attributes("-disabled", True)
        item = self.rightclicked_item
        unit = item.get_item_data()['unitName']
        source = item.get_item_data()['sourceName']
        unit_name = Unit.get_string(unit)
        source_name = Source.get_string(source)
        signal_label = f'{unit_name}.{source_name}.RotSpeed'
        signal_name = "Rotational speed [rpm]"
        pairs = []
        for i in self.get_sensor_labels_from_mc(unit, source):
            pairs.append(
                {
                    'label': i,
                    'name': self.get_name_from_table(unit, i, TableType.SENSORS)
                }
            )
        table = Label_name_pairs(pairs)
        UnitAnalysisRpm(
            init_value = {
                'analysis': 'rpm',
                 'param':{
                    'mainTriggerSensor': '',
                    'onRising': True,
                    'pulseWidth': 2,
                    'treshold': 9
                 },
                 'performOnServer': False
            },
            ch_pairs = table,
            signal_label = signal_label,
            signal_name = signal_name,
            callback = self.add_unit_analysis_callback,
            cancel_callback = self.cancel_callback,
            x = self.tree.winfo_pointerx(),
            y = self.tree.winfo_pointery()
        )

    def add_powers(self):
        self.master.wm_attributes("-disabled", True)
        item = self.rightclicked_item
        unit = item.get_item_data()['unitName']
        source = item.get_item_data()['sourceName']
        unit_name = Unit.get_string(unit)
        source_name = Source.get_string(source)
        signal_label_act = f'{unit_name}.{source_name}.activePower'
        signal_label_react = f'{unit_name}.{source_name}.reactivePower'
        signal_name_act = 'Unit active power'
        signal_name_react = 'Unit reactive power'
        pairs = []
        for i in self.get_sensor_labels_from_mc(unit, source):
            pairs.append(
                {
                    'label': i,
                    'name': self.get_name_from_table(unit, i, TableType.SENSORS)
                }
            )
        table = Label_name_pairs(pairs)
        UnitAnalysisPowers(
            init_value = {
                'analysis': 'act&reactPowers',
                'param': {
                    'voltageSensors': ['','',''],
                    'currentSensors': ['','',''],
                    'lineVoltage': False
                },
                'performOnServer': False
            },
            ch_pairs = table,
            signal_label_act = signal_label_act,
            signal_name_act = signal_name_act,
            signal_label_react = signal_label_react,
            signal_name_react = signal_name_react,
            callback = self.add_unit_analysis_callback,
            cancel_callback = self.cancel_callback,
            x = self.tree.winfo_pointerx(),
            y = self.tree.winfo_pointery()
        )


    def add_unit_analysis_callback(self, new_value, signal_updates):
        self.master.wm_attributes("-disabled", False)
        item = self.rightclicked_item
        unit = item.get_item_data()['unitName']
        source = item.get_item_data()['sourceName']
        self.add_unit_analysis(unit, source, new_value)
        for i in signal_updates:
            self.update_name_in_table(
                unit = unit,
                label = i['label'],
                name = i['name'],
                table_type = TableType.SIGNALS
            )
            self.add_condition_vector_element(
                unit = unit,
                source = source,
                label = i['label']
            )
        self.reindex_unit_analyses_items(unit, source)

    def remove_unit_analysis_event(self):
        item = self.rightclicked_item
        unit = item.get_item_data()['unitName']
        source = item.get_item_data()['sourceName']
        unit_name = Unit.get_string(unit)
        source_name = Source.get_string(source)
        index = item.get_item_data()['index']
        analysis_type = self.get_unit_analysis_type(item)
        if analysis_type == UnitAnalyses.RPM:
            c_v_labels = [f'{unit_name}.{source_name}.RotSpeed']
        if analysis_type == UnitAnalyses.ACT_REACT_PWR:
            c_v_labels = [
                f'{unit_name}.{source_name}.activePower',
                f'{unit_name}.{source_name}.reactivePower'
            ]
        for c_v_label in c_v_labels:
            self.remove_condition_vector_element(unit, source, c_v_label)
            self.remove(unit, c_v_label, TableType.SIGNALS)
        self.remove_unit_analysis(unit, source, index)
        self.reindex_unit_analyses_items(unit, source)

#------------------------------------------------------------------
#                            Alarms
#------------------------------------------------------------------

    def add_new_alarm(self):
        self.master.wm_attributes("-disabled", True)
        item = self.rightclicked_item
        unit = item.get_item_data()['unitName']
        source = item.get_item_data()['sourceName']
        init_value = {'delay': 2, 'alarmPriority': 0, 'logicalSentence':''}
        sig_pairs = []
        for i in self.get_signal_labels_from_mc(unit, source):
            sig_pairs.append(
                {
                    'label': i,
                    'name': self.get_name_from_table(unit, i, TableType.SIGNALS)
                }
            )
        AlarmInterface(
                    init_value = init_value,
                    sig_pairs = sig_pairs,
                    callback = self.add_alarm_callback,
                    cancel_callback = self.cancel_callback,
                    x = self.tree.winfo_pointerx(),
                    y = self.tree.winfo_pointery() 
                )

    def add_alarm_callback(self, new_value):
        self.master.wm_attributes("-disabled", False)
        item = self.rightclicked_item
        unit = item.get_item_data()['unitName']
        source = item.get_item_data()['sourceName']
        self.add_alarm(unit, source, new_value)
        self.reindex_alarm_items(unit, source)
        item_id = self.tree.selection()[0]
        self.item_selected(item_id)
        
    
    def reindex_alarm_items(self, unit, source):
        #-----------------------------------------------------------
        #unit: codis_enums.Unit
        #source: codis_enums.Source
        #-----------------------------------------------------------
        #This method updates alarms list after a new
        #alarm has been added or one was removed.
        #-----------------------------------------------------------
        i = 0
        while i < len(self.items):
            item = self.items[i]
            if (
                item.get_item_type() == ItemType.ALARM
                and item.get_item_data()['unitName'] == unit
                and item.get_item_data()['sourceName'] == source
            ):
                self.remove_item(item)
                i -= 1
            i += 1
        index_main = self.get_main_cluster_index(unit, source)
        if index_main == -1: return
        #Following loop finds parent id
        # of ALARMS_LIST element.
        for i in self.items:
            if i.get_item_type() == ItemType.ALARMS_LIST:
                if(
                    i.get_item_data()['unitName'] == unit
                    and i.get_item_data()['sourceName'] == source
                ):
                    parent_id = i.get_item_id()
                    break
        cv = self.get_main_cluster()[index_main]['conditionVectorCluster']
        a = cv['alarms']
        index_alarm = 0
        for i in a:
            self.append_item(
                parent_id = parent_id,
                item_type =ItemType.ALARM,
                item_data = {
                'unitName': unit,
                'sourceName': source,
                'index': index_alarm
                }
            )
            index_alarm += 1
    
    def remove_alarm_event(self):
        item = self.rightclicked_item
        unit = item.get_item_data()['unitName']
        source = item.get_item_data()['sourceName']
        index = item.get_item_data()['index']
        self.remove_alarm(unit, source, index)
        i = 0
        while i < len(self.items):
            item = self.items[i]
            if (
                item.get_item_type() == ItemType.ALARM
                and item.get_item_data()['unitName'] == unit
                and item.get_item_data()['sourceName'] == source
            ):
                if item.get_item_data()['index'] == index:
                    self.remove_item(item)
                    break
            i += 1
        self.reindex_alarm_items(unit, source)

#------------------------------------------------------------------
#                            Regimes
#------------------------------------------------------------------

    def add_new_regime(self):
        self.master.wm_attributes("-disabled", True)
        item = self.rightclicked_item
        unit = item.get_item_data()['unitName']
        source = item.get_item_data()['sourceName']
        init_value = {
            'label': 'REG000',
            'regimeLogicalDefinitionStatement': ''
        }
        m_c = self.get_main_cluster()
        labels = []
        for i in m_c:
            if Unit.get_unit(i['unitName']) == unit:
                labels.extend(self.get_regime_labels_from_mc(
                    unit = unit,
                    source = Source.get_source(i['sourceName'])
                ))
        regime_label = init_value['label']
        new_label = regime_label
        if new_label in labels:
            counter = 1
            label_addition = str(counter)
            label = regime_label[:-1]
            new_label = label+label_addition
            while new_label in labels:
                counter += 1
                if counter < 10:
                    label_addition = str(counter)
                    new_label = label+label_addition
                elif counter < 100 and counter > 9:
                    label = regime_label[:-2]
                    label_addition = str(counter)
                    new_label = label+label_addition
                else:
                    label = regime_label[:-3]
                    label_addition = str(counter)
                    new_label = label+label_addition
        init_value['label'] = new_label
        pairs = []
        for i in self.get_signal_labels_from_mc(unit, source):
            pairs.append(
                {
                    'label': i,
                    'name': self.get_name_from_table(unit, i, TableType.SIGNALS)
                }
            )
        RegimeInterface(
            init_value = init_value,
            regime_name = '',
            sig_pairs = pairs,
            callback = self.add_regime_callback,
            cancel_callback = self.cancel_callback,
            x = self.tree.winfo_pointerx(),
            y = self.tree.winfo_pointery() 
        )


    def add_regime_callback(self, new_value, regime_updates):
        self.master.wm_attributes("-disabled", False)
        item = self.rightclicked_item
        unit = item.get_item_data()['unitName']
        source = item.get_item_data()['sourceName']
        parent_id = item.get_item_id()
        self.add_regime(unit, source, new_value)
        for i in regime_updates:
            self.update_name_in_table(
                unit = unit,
                label = i['label'],
                name = i['name'],
                table_type = TableType.REGIMES
            )
        regime_id = self.append_item(
            parent_id = parent_id,
            item_type = ItemType.REGIME,
            item_data = {
                'unitName': unit,
                'sourceName': source,
                'label': new_value['label']
            }
        )
        self.add_regime_data_to_air_gap(unit, source, new_value['label'])
        item_id = self.tree.selection()[0]
        self.item_selected(item_id)

    def remove_regime_event(self):
        item = self.rightclicked_item
        unit = item.get_item_data()['unitName']
        source = item.get_item_data()['sourceName']
        regime_label = item.get_item_data()['label']
        self.remove_regime_item(unit, source, regime_label) # vjerojatno nepotrebno, dovoljno bi bilo self.remove_item(item)
        self.remove_regime(unit, source, regime_label)
        self.remove(
            unit = unit,
            label = regime_label,
            table_type = TableType.REGIMES
        )
        # deleting regimes data from air gap analysis
        self.remove_regime_data_from_air_gap(
            unit = unit,
            source = source,
            regime_label = regime_label
        )

    def remove_regime_data_from_air_gap(self, unit, source, regime_label):
        i = 0
        while i < len(self.items):
            item = self.items[i]
            if (
                item.get_item_type() == ItemType.CHANNEL_ANALYSIS
                and item.get_item_data()['unitName'] == unit
                and item.get_item_data()['sourceName'] == source
            ):
                analysis_data = self.get_param_value(item)
                channel_label = item.get_item_data()['label']
                analysis = ChannelAnalyses.get_channel_analysis(analysis_data['analysis'])
                if analysis == ChannelAnalyses.AIR_GAP:
                    self.remove_regime_from_air_gap(
                        unit = unit,
                        source = source,
                        channel_label = channel_label,
                        regime_label = regime_label
                    )
            i += 1

    def add_regime_data_to_air_gap(self, unit, source, regime_label):
        i = 0
        while i < len(self.items):
            item = self.items[i]
            if (
                item.get_item_type() == ItemType.CHANNEL_ANALYSIS
                and item.get_item_data()['unitName'] == unit
                and item.get_item_data()['sourceName'] == source
            ):
                analysis_data = self.get_param_value(item)
                channel_label = item.get_item_data()['label']
                analysis = ChannelAnalyses.get_channel_analysis(analysis_data['analysis'])
                if analysis == ChannelAnalyses.AIR_GAP:
                    self.add_regime_to_air_gap(
                        unit = unit,
                        source = source,
                        channel_label = channel_label,
                        regime_label = regime_label
                    )
            i += 1

    def set_info_text(self, text):
        self.info['state'] = 'normal'
        self.info.delete(1.0, END)
        self.info.insert(END, text)
        self.info['state'] = 'disabled'
                
    def exit_event(self):
        exit()


#------------------------------------------------------------------
#                              Modbus
#------------------------------------------------------------------

    def add_sent_to_modbus(self):
        self.master.wm_attributes("-disabled", True)
        item = self.rightclicked_item
        unit = item.get_item_data()['unitName']
        source = item.get_item_data()['sourceName']
        init_value = {
            'dataSource': 'value',
            'labels': ['', '', '','', '', '','', '', '',''],
            'dataTypes': ['floatLoHi','floatLoHi','floatLoHi','floatLoHi','floatLoHi','floatLoHi','floatLoHi','floatLoHi','floatLoHi','floatLoHi'],
            'scaleFactors': 10*[int(1)],
            'registerType': 'holdingRegisters',
            'adress': 16000
        }
        name = f"Modbus{init_value['adress']}"
        pairs = []
        for i in self.get_signal_labels_from_mc(unit, source):
            pairs.append(
                {
                    'label': i,
                    'name': self.get_name_from_table(unit, i, TableType.SIGNALS)
                }
            )
        labels = self.get_signal_labels_from_mc(unit, source)
        ModbusSentInterface(
            init_value = init_value,
            sig_pairs = pairs,
            callback = self.add_sent_to_modbus_callback,
            cancel_callback = self.cancel_callback,
            x = self.tree.winfo_pointerx(),
            y = self.tree.winfo_pointery(),
            labels = labels
        )

    def add_sent_to_modbus_callback(self):
        pass



        
#------------------------------------------------------------------
#                       Tree handling methods
#------------------------------------------------------------------
    #This method fills the tree and items array
    # from main_cluster and system_settings.
    #It is called after main_cluster and system_settings
    #are fetched by a LoadingProcess.
    def fill_tree(self):
        self.items = []
        for i in self.get_main_cluster():
            try:
                unit = Unit.get_unit(i['unitName'])
                source = Source.get_source(i['sourceName'])
            except ValueError:
                print("Unit or Source from m. cluster settings not recognized.")
                continue    #If there is ValueError exception in either Unit or Source string continue to the following Main cluster element.

            #Add UNIT_SOURCE element to the tree
            unit_source_item_id = self.append_item(
                item_type =ItemType.UNIT_SOURCE,
                item_data = {
                    'unitName': unit,
                    'sourceName': source
                }
            )
    
            #Add BEARINGS_LIST element to the tree
            bearings_list_item_id = self.append_item(
                parent_id = unit_source_item_id,
                item_type =ItemType.BEARINGS_LIST,
                item_data = {
                    'unitName': unit,
                    'sourceName': source
                }
            )

            #Add BEARING elements to the tree and their children elements.
            for j in i['waveformCluster']['bearings']:
                bearing_id = self.append_item(
                    parent_id = bearings_list_item_id,
                    item_type =ItemType.BEARING,
                    item_data = {
                        'unitName': unit,
                        'sourceName': source,
                        'label': j['label']
                    }
                )
                bearing_analyses_list_id = self.append_item(
                    parent_id = bearing_id,
                    item_type = ItemType.BEARING_ANALYSES_LIST,
                    item_data = {
                        'unitName': unit,
                        'sourceName': source,
                        'label': j['label']
                    }
                )

            
                #Add BEARING_ANALYSES elements to the tree
                index = 0
                for k in j['analyses']:
                    self.append_item(
                        parent_id = bearing_analyses_list_id,
                        item_type =ItemType.BEARING_ANALYSIS,
                        item_data = {
                        'unitName': unit,
                        'sourceName': source,
                        'label': j['label'],
                        'index': index
                        }
                    )
                    index += 1

            #Add AIR_GAP_PLANES_LIST element to the tree
            air_gap_planes_list_item_id = self.append_item(
                parent_id = unit_source_item_id,
                item_type =ItemType.AIR_GAP_PLANES_LIST,
                item_data = {
                    'unitName': unit,
                    'sourceName': source
                }
            )

            #Add AIR_GAP_PLANES elements to the tree
            for j in i['waveformCluster']['airGapPlanes']:
                self.append_item(
                    parent_id = air_gap_planes_list_item_id,
                    item_type = ItemType.AIR_GAP_PLANE,
                    item_data = {
                        'unitName': unit,
                        'sourceName': source,
                        'label': j['label']
                    }
                )

            #Add REGIMES_LIST element to the tree
            regimes_list_item_id = self.append_item(
                parent_id = unit_source_item_id,
                item_type =ItemType.REGIMES_LIST,
                item_data = {
                    'unitName': unit,
                    'sourceName': source
                }
            )

            #Add REGIMES elements to the tree
            index = 0
            for j in i['conditionVectorCluster']['regimesDefinition']:
                self.append_item(
                    parent_id = regimes_list_item_id,
                    item_type = ItemType.REGIME,
                    item_data = {
                        'unitName': unit,
                        'sourceName': source,
                        'label': j['label'],
                        'index': index
                    }
                )
                index += 1

            #Add ALARMS_LIST element to the tree
            alarms_list_id = self.append_item(
                parent_id = unit_source_item_id,
                item_type =ItemType.ALARMS_LIST,
                item_data = {
                    'unitName': unit,
                    'sourceName': source
                }
            )

            #Add ALARM elements to the tree
            if 'alarms' in i['conditionVectorCluster']:
                index = 0
                for j in i['conditionVectorCluster']['alarms']:
                    self.append_item(
                        parent_id = alarms_list_id,
                        item_type =ItemType.ALARM,
                        item_data = {
                            'unitName': unit,
                            'sourceName': source,
                            'index': index
                        }
                    )
                    index += 1

            #Add MODBUS_LIST to the tree
            modbus_list_id = self.append_item(
                parent_id = unit_source_item_id,
                item_type =ItemType.MODBUS_LIST,
                item_data = {
                    'unitName': unit,
                    'sourceName': source
                }
            )

            #Add UNIT_ANALYSES_LIST element to the tree
            unit_analyses_list_item_id = self.append_item(
                parent_id = unit_source_item_id,
                item_type =ItemType.UNIT_ANALYSES_LIST,
                item_data = {
                    'unitName': unit,
                    'sourceName': source
                }
            )

            #Add UNIT_ANALYSES elements to the tree
            index = 0
            for j in i['waveformCluster']['unit']['analyses']:
                self.append_item(
                    parent_id = unit_analyses_list_item_id,
                    item_type =ItemType.UNIT_ANALYSIS,
                    item_data = {
                        'unitName': unit,
                        'sourceName': source,
                        'index': index
                    }
                )
                index += 1

            #Add CHANNELS_LIST element to the tree
            channels_list_item_id = self.append_item(
                parent_id = unit_source_item_id,
                item_type =ItemType.CHANNELS_LIST,
                item_data = {
                    'unitName': unit,
                    'sourceName': source
                }
            )

            #Add CHANNEL elements to the tree and their children elements.
            for j in i['waveformCluster']['waveforms']:
                channel_id = self.append_item(
                    parent_id = channels_list_item_id,
                    item_type =ItemType.CHANNEL,
                    item_data = {
                        'unitName': unit,
                        'sourceName': source,
                        'label': j['label']
                    }
                )
                channel_analyses_list_id = self.append_item(
                    parent_id = channel_id,
                    item_type =ItemType.CHANNEL_ANALYSES_LIST,
                    item_data = {
                        'unitName': unit,
                        'sourceName': source,
                        'label': j['label']
                    }
                )
                #Add CHANNEL_ANALYSES elements to the tree
                index = 0
                for k in j['analyses']:
                    self.append_item(
                        parent_id = channel_analyses_list_id,
                        item_type =ItemType.CHANNEL_ANALYSIS,
                        item_data = {
                        'unitName': unit,
                        'sourceName': source,
                        'label': j['label'],
                        'index': index
                        }
                    )
                    index += 1
                self.append_item(
                    parent_id = channel_id,
                    item_type =ItemType.PHYSICAL_CHANNEL,
                    value = j['physicalChannel'],
                    item_data = {
                        'unitName': unit,
                        'sourceName': source,
                        'label': j['label']
                    }
                )
                self.append_item(
                    parent_id = channel_id,
                    item_type =ItemType.SLOPE,
                    value = j['slope'],
                    item_data = {
                        'unitName': unit,
                        'sourceName': source,
                        'label': j['label']
                    }
                )
                self.append_item(
                    parent_id = channel_id,
                    item_type =ItemType.INTERCEPT,
                    value = j['intercept'],
                    item_data = {
                        'unitName': unit,
                        'sourceName': source,
                        'label': j['label']
                    }
                )


    #this method is used for adding a single item to the tree
    def insert_item_into_tree(self, parent_id = '', index = 'end', text = ''):
        return self.tree.insert(parent = parent_id, index = index, text = text)

    #this method is called after an item has been modified.
    #Ex. channel name has been changed.
    def update_tree_item(self, item, new_value):
        self.tree.item(
            item = item.get_item_id(),
            text = self.create_tree_string(item = item, value = new_value)
        )

    #this method is called after an item has been modified
    # and multiple items are affected by it.
    #Ex. Slope has been changed in the channel interface,
    #so slope item in the tree has to be modified.
    def update_tree(self):
        for i in self.items:
            value = self.get_param_value(i)
            self.update_tree_item(item = i, new_value = value)

    def clear_tree(self):
        self.items = []
        for i in self.tree.get_children():
            self.tree.delete(i)
    
    #This function creates a string corresponding to an item to be displayed on the tree
    def create_tree_string(self, item, value):
        if item.get_item_type() == ItemType.UNIT_SOURCE:
            unit = item.get_item_data()['unitName']
            source = item.get_item_data()['sourceName']
            return f'{source} : {unit}'
        if item.get_item_type() == ItemType.BEARINGS_LIST:
            return "Bearing planes"
        if item.get_item_type() == ItemType.BEARING:
            return self.get_name_from_table(
                unit = item.get_item_data()['unitName'],
                label = item.get_item_data()['label'],
                table_type = TableType.BEARINGS
            )
        if item.get_item_type() == ItemType.BEARING_ANALYSES_LIST:
            return 'Analyses'
        if item.get_item_type() == ItemType.BEARING_ANALYSIS:
            try:
                analysis = BearingAnalyses.get_bearing_analysis(
                self.get_param_value(item)['analysis']
            )
            except ValueError:
                return 'Not recognized'
            return BearingAnalyses.get_string(analysis)
        if item.get_item_type() == ItemType.AIR_GAP_PLANES_LIST:
            return "Air gap planes"
        if item.get_item_type() == ItemType.AIR_GAP_PLANE:
            return self.get_name_from_table(
                unit = item.get_item_data()['unitName'],
                label = item.get_item_data()['label'],
                table_type = TableType.AIR_GAP_PLANES
            )
        if item.get_item_type() == ItemType.REGIMES_LIST:
            return "Regimes"
        if item.get_item_type() == ItemType.ALARMS_LIST:
            return "Alarms"
        if item.get_item_type() == ItemType.ALARM:
            
            unit = item.get_item_data()['unitName']
            source = item.get_item_data()['sourceName']
            sig_pairs = []
            for i in self.get_signal_labels_from_mc(unit, source):
                sig_pairs.append(
                    {
                        'label': i,
                        'name': self.get_name_from_table(unit, i, TableType.SIGNALS)
                    }
                )
            l_s = self.get_param_value(item)['logicalSentence']
            for i in sig_pairs:
                new_str = "'"+f"{i['name']}"+"'"
                l_s = l_s.replace(i['label'], new_str)
            return l_s
        if item.get_item_type() == ItemType.MODBUS_LIST:
            return "Modbus"
        if item.get_item_type() == ItemType.REGIME:
            return self.get_name_from_table(
                unit = item.get_item_data()['unitName'],
                label = item.get_item_data()['label'],
                table_type = TableType.REGIMES
            )
        if item.get_item_type() == ItemType.UNIT_ANALYSES_LIST:
            return "Analyses"
        if item.get_item_type() == ItemType.CHANNELS_LIST:
            return "Channels"
        if item.get_item_type() == ItemType.CHANNEL:
            return self.get_name_from_table(
                unit = item.get_item_data()['unitName'],
                label = item.get_item_data()['label'],
                table_type = TableType.SENSORS
            )
        if item.get_item_type() == ItemType.PHYSICAL_CHANNEL:
            return f"Physical channel: {value}"
        if item.get_item_type() == ItemType.SLOPE:
            return f"Slope: {value}"
        if item.get_item_type() == ItemType.INTERCEPT:
            return f"Intercept: {value}"
        if item.get_item_type() == ItemType.CHANNEL_ANALYSES_LIST:
            return "Analyses"
        if item.get_item_type() == ItemType.UNIT_ANALYSIS:
            analysis = UnitAnalyses.get_unit_analysis(
                self.get_param_value(item)['analysis']
            )
            return UnitAnalyses.get_string(analysis)
        if item.get_item_type() == ItemType.CHANNEL_ANALYSIS:
            try:
                analysis = ChannelAnalyses.get_channel_analysis(
                    self.get_param_value(item)['analysis']
                )
            except ValueError:
                return 'Not recognized'
            return ChannelAnalyses.get_string(analysis)

    #append_item is a function that creates an item, appends it to the items list and inserts it into the tree. 
    def append_item(self, item_type, item_data, parent_id = '', value = ''):
        item = Item(
                item_type = item_type,
                item_data = item_data
            )
        id = self.insert_item_into_tree(
            parent_id = parent_id,
            text = self.create_tree_string(item, value))
        item.set_item_id(id)    #item_id can be set only after it was inserted into the tree.
        self.items.append(item)
        return id

    def remove_item(self, item):
        self.items.remove(item)
        self.tree.delete(item.get_item_id())

    def find_item(self, item_id):
        for i in self.items:
            if i.get_item_id() == item_id:
                return i
                break
        return


    def remove_channel_item(self, unit, source, ch_label):
        i = 0
        while i < len(self.items):
            item = self.items[i]
            if (
                item.get_item_type() == ItemType.CHANNEL_ANALYSES_LIST
                and item.get_item_data()['unitName'] == unit
                and item.get_item_data()['sourceName'] == source
            ):
                if item.get_item_data()['label'] == ch_label:
                    self.remove_item(item)
                    i -= 1
            if (
                item.get_item_type() == ItemType.SLOPE
                and item.get_item_data()['unitName'] == unit
                and item.get_item_data()['sourceName'] == source
            ):
                if item.get_item_data()['label'] == ch_label:
                    self.remove_item(item)
                    i -= 1
            if (
                item.get_item_type() == ItemType.INTERCEPT
                and item.get_item_data()['unitName'] == unit
                and item.get_item_data()['sourceName'] == source
            ):
                if item.get_item_data()['label'] == ch_label:
                    self.remove_item(item)
                    i -= 1
            if (
                item.get_item_type() == ItemType.PHYSICAL_CHANNEL
                and item.get_item_data()['unitName'] == unit
                and item.get_item_data()['sourceName'] == source
            ):
                if item.get_item_data()['label'] == ch_label:
                    self.remove_item(item)
                    i -= 1
            i += 1
        i = 0
        while i < len(self.items):
            item = self.items[i]
            if (
                item.get_item_type() == ItemType.CHANNEL
                and item.get_item_data()['unitName'] == unit
                and item.get_item_data()['sourceName'] == source
            ):
                if item.get_item_data()['label'] == ch_label:
                    self.remove_item(item)
                    i -= 1
            i += 1

    def remove_analyses_from_channel(self, unit, source, ch_label):
        i = 0
        while i < len(self.items):
            item = self.items[i]
            if (
                item.get_item_type() == ItemType.CHANNEL_ANALYSIS
                and item.get_item_data()['unitName'] == unit
                and item.get_item_data()['sourceName'] == source
            ):
                if item.get_item_data()['label'] == ch_label:
                    ch_name = self.get_name_from_table(
                    unit = unit,
                    label = ch_label,
                    table_type = TableType.SENSORS
                )
                    analysis_data = self.get_param_value(item)
                    signal_updates = self.get_channel_signal_data(
                        unit = unit,
                        source = source,
                        channel_label = ch_label,
                        channel_name = ch_name,
                        analysis_data = analysis_data
                    )
                    c_v_labels = []
                    for j in signal_updates:
                        c_v_labels.append(j['label'])
                    for c_v_label in c_v_labels:
                        self.remove_condition_vector_element(unit, source, c_v_label)
                        self.remove(unit, c_v_label, TableType.SIGNALS)
                    self.remove_item(item)
                    i -= 1
            i += 1


    def remove_bearing_item(self, unit, source, bearing_label):
        i = 0
        while i < len(self.items):
            item = self.items[i]
            if (
                item.get_item_type() == ItemType.BEARING_ANALYSES_LIST
                and item.get_item_data()['unitName'] == unit
                and item.get_item_data()['sourceName'] == source
            ):
                if item.get_item_data()['label'] == bearing_label:
                    self.remove_item(item)
                    i -= 1
            i += 1
        i = 0
        while i < len(self.items):
            item = self.items[i]
            if (
                item.get_item_type() == ItemType.BEARING
                and item.get_item_data()['unitName'] == unit
                and item.get_item_data()['sourceName'] == source
            ):
                if item.get_item_data()['label'] == bearing_label:
                    self.remove_item(item)
                    i -= 1
            i += 1

    def remove_analyses_from_bearing(self, unit, source, bearing_label):
        i = 0
        while i < len(self.items):
            item = self.items[i]
            if (
                item.get_item_type() == ItemType.BEARING_ANALYSIS
                and item.get_item_data()['unitName'] == unit
                and item.get_item_data()['sourceName'] == source
            ):
                if item.get_item_data()['label'] == bearing_label:
                    bearing_name = self.get_name_from_table(
                    unit = unit,
                    label = bearing_label,
                    table_type = TableType.BEARINGS
                )
                    analysis_data = self.get_param_value(item)
                    signal_updates = self.get_bearing_signal_data(
                        bearing_label = bearing_label,
                        bearing_name = bearing_name,
                        analysis_data = analysis_data
                    )
                    c_v_labels = []
                    for j in signal_updates:
                        c_v_labels.append(j['label'])
                    for c_v_label in c_v_labels:
                        self.remove_condition_vector_element(unit, source, c_v_label)
                        self.remove(unit, c_v_label, TableType.SIGNALS)
                    self.remove_item(item)
                    i -= 1
            i += 1

    def remove_regime_item(self, unit, source, regime_label):
        i = 0
        while i < len(self.items):
            item = self.items[i]
            if (
                item.get_item_type() == ItemType.REGIME
                and item.get_item_data()['unitName'] == unit
                and item.get_item_data()['sourceName'] == source
            ):
                if item.get_item_data()['label'] == regime_label:
                    self.remove_item(item)
                    i -= 1
            i += 1


    def reindex_channel_analyses_items(self, unit, source, ch_label):
        #-----------------------------------------------------------
        #unit: codis_enums.Unit
        #source: codis_enums.Source
        #ch_label: str
        #-----------------------------------------------------------
        #This method updates channel analyses list after a new
        #analysis has been added or one was removed.
        #-----------------------------------------------------------
        i = 0
        while i < len(self.items):
            item = self.items[i]
            if (
                item.get_item_type() == ItemType.CHANNEL_ANALYSIS
                and item.get_item_data()['unitName'] == unit
                and item.get_item_data()['sourceName'] == source
            ):
                if item.get_item_data()['label'] == ch_label:
                    self.remove_item(item)
                    i -= 1
            i += 1
        index_main = self.get_main_cluster_index(unit, source)
        if index_main == -1: return
        #Following loop finds parent id
        # of CHANNEL_ANALYSES_LIST element.
        for i in self.items:
            if i.get_item_type() == ItemType.CHANNEL_ANALYSES_LIST:
                if(
                    i.get_item_data()['unitName'] == unit
                    and i.get_item_data()['sourceName'] == source
                    and i.get_item_data()['label'] == ch_label
                ):
                    parent_id = i.get_item_id()
                    break
        w_c = self.get_main_cluster()[index_main]['waveformCluster']
        index_wav = 0
        found = False
        for i in w_c['waveforms']:
            if i['label'] == ch_label:
                found = True
                break
            index_wav += 1
        if found:
            index_analysis = 0
            for i in w_c['waveforms'][index_wav]['analyses']:
                self.append_item(
                    parent_id = parent_id,
                    item_type =ItemType.CHANNEL_ANALYSIS,
                    item_data = {
                    'unitName': unit,
                    'sourceName': source,
                    'label': ch_label,
                    'index': index_analysis
                    }
                )
                index_analysis += 1

    def reindex_unit_analyses_items(self, unit, source):
        #-----------------------------------------------------------
        #unit: codis_enums.Unit
        #source: codis_enums.Source
        #-----------------------------------------------------------
        #This method updates unit analyses list after a new
        #analysis has been added or one was removed.
        #-----------------------------------------------------------
        i = 0
        while i < len(self.items):
            item = self.items[i]
            if (
                item.get_item_type() == ItemType.UNIT_ANALYSIS
                and item.get_item_data()['unitName'] == unit
                and item.get_item_data()['sourceName'] == source
            ):
                self.remove_item(item)
                i -= 1
            i += 1
        index_main = self.get_main_cluster_index(unit, source)
        if index_main == -1: return
        #Following loop finds parent id
        # of UNIT_ANALYSES_LIST element.
        for i in self.items:
            if i.get_item_type() == ItemType.UNIT_ANALYSES_LIST:
                if(
                    i.get_item_data()['unitName'] == unit
                    and i.get_item_data()['sourceName'] == source
                ):
                    parent_id = i.get_item_id()
                    break
        un = self.get_main_cluster()[index_main]['waveformCluster']['unit']
        index_analysis = 0
        for i in un['analyses']:
            self.append_item(
                parent_id = parent_id,
                item_type =ItemType.UNIT_ANALYSIS,
                item_data = {
                'unitName': unit,
                'sourceName': source,
                'index': index_analysis
                }
            )
            index_analysis += 1

    def reindex_bearing_analyses_items(self, unit, source, bearing_label):
        #-----------------------------------------------------------
        #unit: codis_enums.Unit
        #source: codis_enums.Source
        #bearing_label: str
        #-----------------------------------------------------------
        #This method updates bearing analyses list after a new
        #analysis has been added or one was removed.
        #-----------------------------------------------------------
        i = 0
        while i < len(self.items):
            item = self.items[i]
            if (
                item.get_item_type() == ItemType.BEARING_ANALYSIS
                and item.get_item_data()['unitName'] == unit
                and item.get_item_data()['sourceName'] == source
            ):
                if item.get_item_data()['label'] == bearing_label:
                    self.remove_item(item)
                    i -= 1
            i += 1
        index_main = self.get_main_cluster_index(unit, source)
        if index_main == -1: return
        #Following loop finds parent id
        # of BEARING_ANALYSES_LIST element.
        for i in self.items:
            if i.get_item_type() == ItemType.BEARING_ANALYSES_LIST:
                if(
                    i.get_item_data()['unitName'] == unit
                    and i.get_item_data()['sourceName'] == source
                    and i.get_item_data()['label'] == bearing_label
                ):
                    parent_id = i.get_item_id()
                    break
                
        w_c = self.get_main_cluster()[index_main]['waveformCluster']
        index_wav = 0
        found = False
        for i in w_c['bearings']:
            if i['label'] == bearing_label:
                found = True
                break
            index_wav += 1
        if found:
            index_analysis = 0
            for i in w_c['bearings'][index_wav]['analyses']:
                self.append_item(
                    parent_id = parent_id,
                    item_type =ItemType.BEARING_ANALYSIS,
                    item_data = {
                    'unitName': unit,
                    'sourceName': source,
                    'label': bearing_label,
                    'index': index_analysis
                    }
                )
                index_analysis += 1

#------------------------------------------------------------------
#                   Tables handling methods
#------------------------------------------------------------------
    def get_table(self, unit, table_type):
        for i in self.tables:
            if unit == i.get_unit() and table_type == i.get_table_type():
                return i
        return

    def append_table(self, unit, labels_names, table_type):
        self.tables.append(Label_name_pairs(labels_names, unit, table_type))
    
    def get_name_from_table(self, unit, label, table_type):
        table = self.get_table(unit, table_type)
        if table != None:
            return table.get_name(label)
        else:
            return
    
    def get_label_from_table(self, unit, name, table_type):
        table = self.get_table(unit, table_type)
        if table != None:
            return table.get_label(name)
        else:
            return None
    
    def update_name_in_table(self, unit, label, name, table_type):
        table = self.get_table(unit, table_type)
        if table != None:
            table.update_name(label = label, name = name)
        return

    def remove(self, unit, label, table_type):
        table = self.get_table(unit, table_type)
        if table != None:
            table.remove(label)
    
#------------------------------------------------------------------


        #-----------------------------------------------------------
        #item: tree_items.ItemType
        #-----------------------------------------------------------

    def get_initial_configuration(self, name):
        file_name = f'{name}_initial_configuration.json'
        f = open(f'init_configuration/{file_name}')
        return load(f)

    def get_channel_signal_data(
        self, channel_label, channel_name, analysis_data, unit = None, source = None
    ):
        #-----------------------------------------------------------
        # channel_label: sensor label string
        # channel_name: sensor name string
        # analysis_data: dictionary with analysis data
        #-----------------------------------------------------------
        # This method return signal_updates list for adding or removing 
        # signals data from tsignal_table and condition vector elements. 
        #-----------------------------------------------------------  
        analysis = ChannelAnalyses.get_channel_analysis(analysis_data['analysis'])
        if analysis == ChannelAnalyses.SNA_PH:
            harmonic = analysis_data['param']['harmonic']
            signal_label_A = f'{channel_label}.s{harmonic}.00A'
            signal_label_Ph = f'{channel_label}.s{harmonic}.00Ph'
            found = False
            if '[' and ']' in channel_name:
                found = True
                bracket_start = channel_name.find('[')
                bracket_end = channel_name.find(']')+1
                measuring_unit = channel_name[bracket_start:bracket_end]
            if found:
                channel_name_reduced = channel_name[:bracket_start]
                signal_name_A = f'{channel_name_reduced} {harmonic}x Ampl {measuring_unit}'
                signal_name_Ph = f'{channel_name_reduced} {harmonic}x Phase [deg]'
            else:
                signal_name_A = f'{channel_name} {harmonic}x Ampl'
                signal_name_Ph = f'{channel_name} {harmonic}x Phase [deg]'
            signal_updates = [{
                'label': signal_label_A,
                'name': signal_name_A
            }, {
                'label': signal_label_Ph,
                'name': signal_name_Ph
            }]
            return signal_updates
        elif analysis == ChannelAnalyses.DC:
            signal_label = f'{channel_label}.DC'
            found = False
            if '[' and ']' in channel_name:
                found = True
                bracket_start = channel_name.find('[')
                bracket_end = channel_name.find(']')+1
                measuring_unit = channel_name[bracket_start:bracket_end]
            if found:
                channel_name_reduced = channel_name[:bracket_start]
                signal_name = f'{channel_name_reduced} Dc {measuring_unit}'
            else:
                signal_name = f'{channel_name} Dc'
            signal_updates =[{
                'label': signal_label,
                'name': signal_name
            }]
            return signal_updates
        elif analysis == ChannelAnalyses.EQ_PEAK:
            l_a = analysis_data['param']['labelAddition']
            signal_label = f'{channel_label}.EqPeak{l_a}'
            found = False
            if '[' and ']' in channel_name:
                found = True
                bracket_start = channel_name.find('[')
                bracket_end = channel_name.find(']')+1
                measuring_unit = channel_name[bracket_start:bracket_end]
            if found:
                channel_name_reduced = channel_name[:bracket_start]
                signal_name = f'{channel_name_reduced} Eq. Peak {measuring_unit}'
            else:
                signal_name = f'{channel_name} Eq. Peak'
            signal_updates =[{
                'label': signal_label,
                'name': signal_name
            }]
            return signal_updates
        elif analysis == ChannelAnalyses.RMS:
            l_a = analysis_data['param']['labelAddition']
            signal_label = f'{channel_label}.RMS{l_a}'
            found = False
            if '[' and ']' in channel_name:
                found = True
                bracket_start = channel_name.find('[')
                bracket_end = channel_name.find(']')+1
                measuring_unit = channel_name[bracket_start:bracket_end]
            if found:
                channel_name_reduced = channel_name[:bracket_start]
                signal_name = f'{channel_name_reduced} Rms {measuring_unit}'
            else:
                signal_name = f'{channel_name} Rms'
            signal_updates =[{
                'label': signal_label,
                'name': signal_name
            }]
            return signal_updates
        elif analysis == ChannelAnalyses.SIGNAL_FREQUENCY:
            signal_label = f'{channel_label}.SignalFrequency'
            found = False
            if '[' and ']' in channel_name:
                found = True
                bracket_start = channel_name.find('[')
                bracket_end = channel_name.find(']')+1
                measuring_unit = channel_name[bracket_start:bracket_end]
            if found:
                channel_name_reduced = channel_name[:bracket_start]
                signal_name = f'{channel_name_reduced} Signal Frequency {measuring_unit}'
            else:
                signal_name = f'{channel_name} Signal Frequency'
            signal_updates =[{
                'label': signal_label,
                'name': signal_name
            }]
            return signal_updates
        elif analysis == ChannelAnalyses.THD:
            signal_label = f'{channel_label}.THD'
            found = False
            if '[' and ']' in channel_name:
                found = True 
                bracket_start = channel_name.find('[')
                bracket_end = channel_name.find(']')+1
                measuring_unit = channel_name[bracket_start:bracket_end]
            if found:
                channel_name_reduced = channel_name[:bracket_start]
                signal_name = f'{channel_name_reduced} Thd {measuring_unit}'
            else:
                signal_name = f'{channel_name} Thd'
            signal_updates =[{
                'label': signal_label,
                'name': signal_name
            }]
            return signal_updates
        elif analysis == ChannelAnalyses.PEAK2PEAK:
            l_a = analysis_data['param']['labelAddition']
            signal_label = f'{channel_label}.Peak2Peak{l_a}'
            found = False
            if '[' and ']' in channel_name:
                found = True
                bracket_start = channel_name.find('[')
                bracket_end = channel_name.find(']')+1
                measuring_unit = channel_name[bracket_start:bracket_end]
            if found:
                channel_name_reduced = channel_name[:bracket_start]
                signal_name = f'{channel_name_reduced} Peak2Peak {measuring_unit}'
            else:
                signal_name = f'{channel_name} Peak2Peak'
            signal_updates =[{
                'label': signal_label,
                'name': signal_name
            }]
            return signal_updates
        elif analysis == ChannelAnalyses.REST:
            signal_label = f'{channel_label}.Rest'
            found = False
            if '[' and ']' in channel_name:
                found = True 
                bracket_start = channel_name.find('[')
                bracket_end = channel_name.find(']')+1
                measuring_unit = channel_name[bracket_start:bracket_end]
            if found:
                channel_name_reduced = channel_name[:bracket_start]
                signal_name = f'{channel_name_reduced} Rest {measuring_unit}'
            else:
                signal_name = f'{channel_name} Rest'
            signal_updates =[{
                'label': signal_label,
                'name': signal_name
            }]
            return signal_updates
        elif analysis == ChannelAnalyses.AIR_GAP:
            signal_name_reduced = ''
            measuring_unit = ''
            name = channel_name
            signal_updates = []
            for i in range(1, self.get_number_of_poles(unit, source)+1):
                if i < 10:
                    num = '0'+str(i)
                else:
                    num = str(i)
                label = f'{channel_label}.MinPole{num}'
                found = False
                if '[' and ']' in name:
                    found = True
                    bracket_start = name.find('[')
                    bracket_end = name.find(']')+1
                    mu = name[bracket_start:bracket_end]
                    measuring_unit = f' {mu}'
                if found:
                    signal_name_reduced = name[:bracket_start]
                    signal_name = f'{signal_name_reduced} min pole{num}{measuring_unit}'
                else:
                    signal_name = f'{name} min pole{num}'
                signal_updates.append({
                    'label': label,
                    'name': signal_name
                })
            if signal_name_reduced != '':
                signal_name = signal_name_reduced
            else:
                signal_name = name
            signal_updates.append({
            'label': f'{channel_label}.s1.00A',
            'name': f'{signal_name} 1x Ampl{measuring_unit}'
            })
            signal_updates.append({
            'label': f'{channel_label}.s2.00A',
            'name': f'{signal_name} 2x Ampl{measuring_unit}'
            })
            signal_updates.append({
            'label': f'{channel_label}.s1.00Ph',
            'name': f'{signal_name} 1x Phase [deg]'
            })
            signal_updates.append({
            'label': f'{channel_label}.s2.00Ph',
            'name': f'{signal_name} 2x Phase [deg]'
            })
            signal_updates.append({
            'label': f'{channel_label}.DCExtremaMin',
            'name': f'{signal_name} average air gap{measuring_unit}'
            })
            signal_updates.append({
            'label': f'{channel_label}.MaxExtremaMin',
            'name': f'{signal_name} max air gap{measuring_unit}'
            })
            signal_updates.append({
            'label': f'{channel_label}.MinExtremaMin',
            'name': f'{signal_name} min air gap{measuring_unit}'
            })
            signal_updates.append({
            'label': f'{channel_label}.MaxDiffPoleNum',
            'name': f'{signal_name} max diff pole num'
            })
            signal_updates.append({
            'label': f'{channel_label}.MaxPoleDiff',
            'name': f'{signal_name} max pole diff{measuring_unit}'
            })
            return signal_updates
        elif analysis == ChannelAnalyses.RPM:
            signal_label = f'{channel_label}.RotSpeed'
            found = False
            if '[' and ']' in channel_name:
                found = True 
                bracket_start = channel_name.find('[')
                bracket_end = channel_name.find(']')+1
                measuring_unit = channel_name[bracket_start:bracket_end]
            if found:
                channel_name_reduced = channel_name[:bracket_start]
                signal_name = f'{channel_name_reduced} Rotational speed {measuring_unit}'
            else:
                signal_name = f'{channel_name} Rotational speed'
            signal_updates =[{
                'label': signal_label,
                'name': signal_name
            }]
            return signal_updates
        else:
            return []

    def get_bearing_signal_data(self, bearing_label, bearing_name, analysis_data):
        #-----------------------------------------------------------
        # bearing_label: bearing label string
        # bearing_name: bearing name string
        # analysis_data: dictionary with analysis data
        #-----------------------------------------------------------
        # This method return signal_updates list for adding or removing 
        # signals data from tsignal_table and condition vector elements. 
        #-----------------------------------------------------------
        analysis = BearingAnalyses.get_bearing_analysis(analysis_data['analysis'])
        if analysis == BearingAnalyses.S_MAX:
            l_a = analysis_data['param']['labelAddition']
            signal_label = f'{bearing_label}.Smax{l_a}'
            found = False
            if '[' and ']' in bearing_name:
                found = True
                bracket_start = bearing_name.find('[')
                bracket_end = bearing_name.find(']')+1
                measuring_unit = bearing_name[bracket_start:bracket_end]
            if found:
                bearing_name_reduced = bearing_name[:bracket_start]
                signal_name = f'{bearing_name_reduced} Smax {measuring_unit}'
            else:
                signal_name = f'{bearing_name} Smax'
            signal_updates =[{
                'label': signal_label,
                'name': signal_name
            }]
            return signal_updates
        elif analysis == BearingAnalyses.SP2P_MAX:
            l_a = analysis_data['param']['labelAddition']
            signal_label = f'{bearing_label}.SP2Pmax{l_a}'
            found = False
            if '[' and ']' in bearing_name:
                found = True
                bracket_start = bearing_name.find('[')
                bracket_end = bearing_name.find(']')+1
                measuring_unit = bearing_name[bracket_start:bracket_end]
            if found:
                bearing_name_reduced = bearing_name[:bracket_start]
                signal_name = f'{bearing_name_reduced} SP2Pmax {measuring_unit}'
            else:
                signal_name = f'{bearing_name} SP2Pmax'
            signal_updates =[{
                'label': signal_label,
                'name': signal_name
            }]
            return signal_updates
        else:
            return None  

    def add_thread(self, name):
        self.running_threads.append(
            {
                'name': name,
                'canceled': False
            }
        )
    #Mark thread in the list as canceled.
    def cancel_thread(self, name):
        for i in self.running_threads:
            if i['name'] == name:
                i['canceled'] = True
                return

    def get_thread_cancel_status(self, name):
        for i in self.running_threads:
            if i['name'] == name:
                return i['canceled']

    #Remove thread from the list.
    def remove_thread(self, name):
        for i in range(len(self.running_threads)):
            if self.running_threads[i]['name'] == name:
                self.running_threads.pop(i)
                return
    
    def get_and_update_thread_status(self, name):
        r = self.get_thread_cancel_status(name)
        if r: self.remove_thread(name)
        return r

    def test(self):
        #print(self.pb.winfo_exists())
        """print(self.running_threads)
        print(enumerate())"""
        #print(self.app.main_cluster[0]['waveformCluster']['waveforms'])
        #print(self.doubleclicked_item)
        # print(self.get_main_cluster()[0]['waveformCluster']['waveforms'])
        #self.update_tree()
        #for i in self.tsensor_tables:
            #print(i.get_unit())
        #print(len(self.items))
        for i in self.tables:
            if i.get_table_type() == TableType.SENSORS:
                for j in i:
                    print(j)
        # print(self.get_main_cluster()[0]['waveformCluster']['airGapPlanes'])
        # print(self.get_main_cluster()[0]['waveformCluster']['bearings'])
        #print(self.get_sensor_labels_from_main_cluster(
            #Unit.UNIT1,
            #Source.SOURCE11
        #))
        # print(self.tables)
        #print(self.get_channel_analysis_type(self.doubleclicked_item))
        #pass
        #print(self.doubleclicked_item.get_item_data())
        #self.reindex_channel_analyses_items(
        #    unit = Unit.UNIT1,
        #    source = Source.SOURCE0,
        #    ch_label = 'RV000'
        #)
        # for i in self.tables:
        #     print(i.get_unit())
        #     print(i.get_table_type())
        #     print(i.get_pairs())
        #print(self.get_main_cluster()[0]['conditionVectorCluster']['conditionVectorElements'])
        #id = self.get_channel_tree_element(
        #    unit = Unit.UNIT1,
        #    source = Source.SOURCE0,
        #    ch_label = 'RV000')
        #print(id)
        # print(self.get_number_of_poles(Unit.UNIT1,
        #     Source.SOURCE0))
        # print(self.get_main_cluster()[0]['waveformCluster']['unit'])
        # print(self.get_main_cluster()[0]['waveformCluster']['waveforms'][0])
        #print(self.get_main_cluster()[0]['conditionVectorCluster']['conditionVectorElements'])
        # print(self.get_label_from_table(
        #     unit = Unit.UNIT1,
        #     name = 'UGB',
        #     table_type = TableType.BEARINGS
        #     ))
        #print(self.get_main_cluster()[0]['waveformCluster']['waveforms'])

        # waveformcluster = self.get_main_cluster()[0]['waveformCluster']['waveforms'][0]

        # print(dumps(waveformcluster, indent = 2, sort_keys=True))
        # print(self.get_main_cluster()[0]['waveformCluster']['unit']['analyses'])
        # main_trigger = self.get_main_trigger_sensor(unit = Unit.UNIT1,
        #         source = Source.SOURCE0)
        # print(main_trigger)
        """print(
            self.get_channel_element(
                unit = Unit.UNIT1,
                source = Source.SOURCE0,
                label = 'TRG000'
            )
        )"""
        """print(self.get_condition_vector_element(
            unit = Unit.UNIT1,
            source = Source.SOURCE0,
            label = 'TRG000.DC'
        ))"""
        # counter = 0
        # for item in self.items:
        #     counter +=1
        #     print(item.get_item_id())
        # print(counter)
