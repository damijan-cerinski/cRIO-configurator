from tkinter import *
from json import dumps, loads, JSONDecodeError
from tkinter import messagebox
from tkinter.messagebox import showerror
from tkinter.scrolledtext import ScrolledText
from tkinter.ttk import Progressbar

#from modules.label_name_pairs import Label_name_pairs
from .simple_input_widgets import UnsignedIntegerEntry, SelectorCombo
from .simple_input_widgets import FloatEntry, IntegerEntry, IpIntegerEntry
from .simple_input_widgets import SelectorList, Unsigned16bitIntegerEntry
from .simple_input_widgets import AutocompleteEntry
from .label_name_pairs import Label_name_pairs
from .codis_enums import FILTER_TYPE_LABEL_NAME_PAIRS, INTEGRATE_TYPE_LABEL_NAME_PAIRS
from .codis_enums import REGISTER_TYPE_LABEL_NAME_PAIRS, MODBUS_DATA_TYPE_LABEL_NAME_PAIRS

"""from simple_input_widgets import UnsignedIntegerEntry, SelectorCombo
from simple_input_widgets import FloatEntry
from label_name_pairs import Label_name_pairs
from codis_enums import FILTER_TYPE_LABEL_NAME_PAIRS"""
import time


class UnsignedIntegerInterface(Toplevel):

    def __init__(
        self,
        x,
        y,
        init_value = '',
        title = '',
        callback = None,
        cancel_callback = None
    ):
        Toplevel.__init__(self)
        self.callback = callback
        self.cancel_callback = cancel_callback
        self.protocol('WM_DELETE_WINDOW', self.x_button)
        #This line removes title bar. It is OS dependent.
        self.wm_overrideredirect(True)
        self.border_frame = Frame(
            self,
            borderwidth = 2,
            relief = FLAT,
            bg = 'gray'
        )
        self.content_frame = Frame(self.border_frame)
        self.label = Label(self.content_frame, text = title)
        self.num = UnsignedIntegerEntry(self.content_frame)
        self.num.bind('<Key-Return>', self.return_pressed)
        self.num.insert(0, init_value)
        self.buttons_frame = Frame(self.content_frame)
        self.ok_button = Button(
            self.buttons_frame, text='Ok', command = self.ok_event
        )
        self.cancel_button = Button(
            self.buttons_frame, text='Cancel', command = self.cancel_event
        )
        self.border_frame.pack(fill = BOTH, expand = 1)
        self.content_frame.pack(fill = BOTH, expand = 1)
        self.geometry(f'120x80+{x}+{y}')
        self.resizable(False, False)
        self.label.pack(side = TOP, anchor = 'w')
        self.num.pack(side = TOP, fill = X, expand = 1)
        self.buttons_frame.pack(side = TOP, fill = X)
        self.ok_button.pack(side = RIGHT, expand = 1)
        self.cancel_button.pack(side = RIGHT, expand = 1)
        self.num.focus_set()

    #Button command callback method doesn't have event param.
    def ok_event(self):
        if self.callback != None:
            self.callback(self.num.get())
            self.destroy()

    def return_pressed(self, e):
        if self.callback != None:
            self.callback(self.num.get())
            self.destroy()

    def cancel_event(self):
        self.cancel_callback()
        self.destroy()
    
    def x_button(self):
        self.cancel_callback()
        self.destroy()


class FloatInterface(Toplevel):

    def __init__(
        self,
        x,
        y,
        init_value = '',
        title = '',
        callback = None,
        cancel_callback = None
    ):
        Toplevel.__init__(self)
        self.callback = callback
        self.cancel_callback = cancel_callback
        self.protocol('WM_DELETE_WINDOW', self.x_button)
        #This line removes title bar. It is OS dependent.
        self.wm_overrideredirect(True)
        self.border_frame = Frame(
            self,
            borderwidth = 2,
            relief = FLAT,
            bg = 'gray'
        )
        self.content_frame = Frame(self.border_frame)
        self.label = Label(self.content_frame, text = title)
        self.num = FloatEntry(self.content_frame)
        self.num.bind('<Key-Return>', self.return_pressed)
        self.num.insert(0, init_value)
        self.buttons_frame = Frame(self.content_frame)
        self.ok_button = Button(
            self.buttons_frame, text='Ok', command = self.ok_event
        )
        self.cancel_button = Button(
            self.buttons_frame, text='Cancel', command = self.cancel_event
        )
        self.border_frame.pack(fill = BOTH, expand = 1)
        self.content_frame.pack(fill = BOTH, expand = 1)
        self.geometry(f'120x80+{x}+{y}')
        self.resizable(False, False)
        self.label.pack(side = TOP, anchor = 'w')
        self.num.pack(side = TOP, fill = X, expand = 1)
        self.buttons_frame.pack(side = TOP, fill = X)
        self.ok_button.pack(side = RIGHT, expand = 1)
        self.cancel_button.pack(side = RIGHT, expand = 1)
        self.num.focus_set()

    #Button command callback method doesn't have event param.
    def ok_event(self):
        if self.callback != None:
            self.callback(self.num.get())
            self.destroy()

    def return_pressed(self, e):
        if self.callback != None:
            self.callback(self.num.get())
            self.destroy()

    def cancel_event(self):
        self.cancel_callback()
        self.destroy()
    
    def x_button(self):
        self.cancel_callback()
        self.destroy()


class BearingInterface(Toplevel):
    
    def __init__(
        self,
        init_value,
        bearing_name,
        x,
        y,
        ch_pairs,
        callback = None,
        cancel_callback = None
    ):
        Toplevel.__init__(self)
        self.title("Bearing:")
        self.value = init_value
        self.callback = callback
        self.cancel_callback = cancel_callback
        self.ch_pairs = ch_pairs
        self.x = x
        self.y = y
        self.protocol('WM_DELETE_WINDOW', self.x_button)
        self.content_frame = Frame(self, borderwidth = 5)
        self.bearing_name_label = Label(
            self.content_frame,
            text = "Bearing Plane Name:")
        self.bearing_name = Entry(self.content_frame)
        self.bearing_name.insert(0, bearing_name)
        self.bearing_pl_conf_label = Label(
            self.content_frame,
            text = "Bearing Plane Configuration:")
        self.x_direction_label = Label(
            self.content_frame,
            text = "X - direction Sensor")
        
        if 'xDirection' in init_value:
            found = False
            for i in ch_pairs:
                if init_value['xDirection'] == i['label']:
                    found = True
            if found:
                x_dir = ch_pairs.get_name(init_value['xDirection'])
            else:
                x_dir = ''
        else:
            x_dir = ''

        self.x_direction = SelectorCombo(
            self.content_frame,
            pairs = ch_pairs,
            init_name = x_dir
        )
        self.y_direction_label = Label(
            self.content_frame,
            text = "Y - direction Sensor")

        if 'yDirection' in init_value:
            found = False
            for i in ch_pairs:
                if init_value['yDirection'] == i['label']:
                    found = True
            if found:
                y_dir = ch_pairs.get_name(init_value['yDirection'])
            else:
                y_dir = ''
        else:
            y_dir = ''

        self.y_direction = SelectorCombo(
            self.content_frame,
            pairs = ch_pairs,
            init_name = y_dir
        )
        self.rotate_var = BooleanVar()
        if 'rotate' in self.value:
            val = self.value['rotate']
            self.rotate_var.set(val)
        self.rotate = Checkbutton(
            self.content_frame,
            text = 'Coordinate System Rotation',
            variable = self.rotate_var,
            onvalue = True,
            offvalue = False,
            command = self.rotation_pressed
        )
        self.rotation_frame = Frame(self.content_frame, border = 5)
        self.angle_rotation_label = Label(
            self.rotation_frame,
            text = "Angle of Rotation"
        )
        self.angle_rotation = IntegerEntry(self.rotation_frame)
        if 'rotationAngle' in self.value:
            val = self.value['rotationAngle']
            self.angle_rotation.insert(0, val)
        else:
            self.angle_rotation.insert(0, '0')
        
        self.buttons_frame = Frame(self.content_frame)
        self.ok_button = Button(
            self.buttons_frame, text='Ok', command = self.ok_event
        )
        self.cancel_button = Button(
            self.buttons_frame, text='Cancel', command = self.cancel_event
        )
        #self.border_frame.pack(fill = BOTH, expand = 1)
        self.content_frame.pack(fill = BOTH, expand = 1)
        self.geometry(f'280x300+{x}+{y}')
        self.resizable(False, False)
        self.bearing_name_label.pack(side = TOP, anchor = 'w')
        self.bearing_name.pack(side = TOP, fill = X, expand = 1)
        self.bearing_pl_conf_label.pack(side = TOP, anchor = 'w')
        self.x_direction_label.pack(side = TOP, anchor = 'w')
        self.x_direction.pack(side = TOP, fill = X, expand = 1)
        self.y_direction_label.pack(side = TOP, anchor = 'w')
        self.y_direction.pack(side = TOP, fill = X, expand = 1)
        self.rotate.pack(side = TOP, expand = 1, anchor = 'w')
        self.rotation_frame.pack(fill = BOTH, expand = 1)
        self.angle_rotation_label.pack(side = TOP, anchor = 'w')
        self.angle_rotation.pack(side = TOP, fill = X, expand = 1)

        self.buttons_frame.pack(side = TOP, fill = X)
        self.ok_button.pack(side = RIGHT, expand = 1)
        self.cancel_button.pack(side = RIGHT, expand = 1)

        self.rotation_pressed()

    def call_callback(self):
        if self.callback != None:
            if self.x_direction.get() != '':
                self.value['xDirection'] = self.x_direction.get()
            if self.y_direction.get() != '':
                self.value['yDirection'] = self.y_direction.get()
            self.value['rotate'] = self.rotate_var.get()
            self.value['rotationAngle'] = int(self.angle_rotation.get())
            bearing_name = self.bearing_name.get()
            self.callback(
                new_value = self.value,
                bearing_updates = [{
                    "label": self.value['label'],
                    "name": self.bearing_name.get()
                }],
                table = self.ch_pairs,
                name = bearing_name,
                x = self.x,
                y = self.y
            )
    
    #Button command callback method doesn't have event param.
    def ok_event(self):
        self.call_callback()
        self.destroy()
            
    def return_pressed(self, e):
        self.call_callback()
        self.destroy()

    def rotation_pressed(self):
        if self.rotate_var.get():
            self.enable_rotation_elements()
        else:
            self.disable_rotation_elements()
    
    def enable_rotation_elements(self):
        for i in [
            self.angle_rotation_label,
            self.angle_rotation
        ]:
            i['state'] = NORMAL

    def disable_rotation_elements(self):
        for i in [
            self.angle_rotation_label,
            self.angle_rotation
        ]:
            i['state'] = DISABLED


    def cancel_event(self):
        self.cancel_callback()
        self.destroy()
    
    def x_button(self):
        self.cancel_callback()
        self.destroy()


class AirGapPlaneInterface(Toplevel):
    def __init__(
        self,
        init_value,
        agp_name,
        x,
        y,
        ch_pairs,
        callback = None,
        cancel_callback = None
    ):
        Toplevel.__init__(self)
        self.title("Air gap plane:")
        self.value = init_value
        self.callback = callback
        self.cancel_callback = cancel_callback
        self.ch_pairs = ch_pairs
        self.x = x
        self.y = y
        self.protocol('WM_DELETE_WINDOW', self.x_button)
        self.content_frame = Frame(self, borderwidth = 5)
        self.agp_name_label = Label(
            self.content_frame,
            text = "Air Gap Plane Name:")
        self.agp_name = Entry(self.content_frame)
        self.agp_name.insert(0, agp_name)
        self.sensors_selection_label = Label(
            self.content_frame,
            text = "Sensors in plane:"
        )
        self.selection_frame = Frame(self.content_frame, border = 5)
        selected_sensors = []
        if 'sensors' in self.value:
            if self.value['sensors'] != []:
                for i in self.value['sensors']:
                    selected_sensors.append(i)
        self.selection_list = SelectorList(
            self.selection_frame,
            pairs = ch_pairs,
            selectmode = MULTIPLE,
            init_sensors = selected_sensors
        )
        self.yscrollbar = Scrollbar(
            self.selection_frame,
            command = self.selection_list.yview
        )
        self.selection_list['yscrollcommand'] = self.yscrollbar.set
        
        self.buttons_frame = Frame(self.content_frame)
        self.ok_button = Button(
            self.buttons_frame, text='Ok', command = self.ok_event
        )
        self.cancel_button = Button(
            self.buttons_frame, text='Cancel', command = self.cancel_event
        )

        self.content_frame.pack(fill = BOTH, expand = 1)
        self.geometry(f'280x300+{x}+{y}')
        self.resizable(False, False)
        self.agp_name_label.pack(side = TOP, anchor = 'w')
        self.agp_name.pack(side = TOP, fill = X, expand = 1)
        self.sensors_selection_label.pack(side = TOP, anchor = 'w')
        self.selection_frame.pack(fill = BOTH, expand = 1)
        self.selection_list.pack(expand = True, fill = BOTH, side = LEFT)
        self.yscrollbar.pack(side = LEFT, expand = False, fill = Y)
        
        
        self.buttons_frame.pack(side = TOP, fill = X)
        self.ok_button.pack(side = RIGHT, expand = 1)
        self.cancel_button.pack(side = RIGHT, expand = 1)

    def call_callback(self):
        if self.call_callback != None:
            selected_sensors = self.selection_list.get()
            self.value['sensors'] = []
            for i in selected_sensors:
                self.value['sensors'].append(i)
            signal_updates = []
            self.agp_name_reduced = ''
            self.measuring_unit = ''
            self.name = self.agp_name.get()
            found = False
            if '[' and ']' in self.name:
                found = True
                bracket_start = self.name.find('[')
                bracket_end = self.name.find(']')+1
                self.mu = self.name[bracket_start:bracket_end]
                self.measuring_unit = f' {self.mu}'
            if found:
                self.agp_name_reduced = self.name[:bracket_start]
            if self.agp_name_reduced != '':
                signal_name = self.agp_name_reduced
            else:
                signal_name = self.name
            agp_label = self.value['label']
            signal_updates.append({
                'label': f'{agp_label}.MinExtremaMin',
                'name': f'{signal_name} min air gap{self.measuring_unit}'
            })
            signal_updates.append({
                'label': f'{agp_label}.MinExtremaMinPoleNum',
                'name': f'{signal_name} min pole num'
            })
            signal_updates.append({
                'label': f'{agp_label}.MaxDiff',
                'name': f'{signal_name} max diff{self.measuring_unit}'
            })
            signal_updates.append({
                'label': f'{agp_label}.MaxDiffPoleNum',
                'name': f'{signal_name} max diff pole num'
            })
            air_gap_plane_updates = [{
                'label': agp_label,
                'name': self.agp_name.get()
            }]
            self.callback(
                new_value = self.value,
                signal_updates = signal_updates,
                air_gap_plane_updates = air_gap_plane_updates
            )


    def ok_event(self):
        self.call_callback()
        self.destroy()
            
    def return_pressed(self, e):
        self.call_callback()
        self.destroy()

    def cancel_event(self):
        self.cancel_callback()
        self.destroy()

    def x_button(self):
        self.cancel_callback()
        self.destroy()


class PeakAnalysis(Toplevel):
    def __init__(
        self,
        x,
        y,
        init_value,
        signal_label = '',
        signal_name = '',
        title = '',
        callback = None,
        cancel_callback = None
    ):
        Toplevel.__init__(self)
        if title == 'Smax':
            self.title("Smax:")
        elif title == 'SP2Pmax':
            self.title('SP2Pmax')
        elif title == 'Peak2Peak':
            self.title('Peak2Peak')
        elif title == 'EqPeak':
            self.title('Eq Peak:')
        else:
            self.title("Unknown:")
        self.value = init_value
        self.signal_label = signal_label
        self.callback = callback
        self.cancel_callback = cancel_callback
        self.protocol('WM_DELETE_WINDOW', self.x_button)
        self.content_frame = Frame(self, border = 5)
        self.sig_name_label = Label(self.content_frame, text = "Signal name:")
        self.sig_name = Entry(self.content_frame)
        if signal_name != None:
            self.sig_name.insert(0, signal_name)
        else:
            self.sig_name.insert(0, '')

        self.t2t_var = BooleanVar()
        if 'param' in self.value:
            if 'triggerToTrigger' in self.value['param']:
                self.t2t_var.set(self.value['param']['triggerToTrigger'])
        self.t2t = Checkbutton(
            self.content_frame,
            text = "Trigger to trigger",
            variable= self.t2t_var,
            onvalue= True,
            offvalue= False)
        
        self.av_per_rev_var = BooleanVar()
        if 'param' in self.value:
            if 'averagePerRevolution' in self.value['param']:
                val = self.value['param']['averagePerRevolution']
                self.av_per_rev_var.set(val)
        self.av_per_rev = Checkbutton(
            self.content_frame,
            text = "Average per revolution",
            variable= self.av_per_rev_var,
            onvalue= True,
            offvalue= False)
        
        self.filter_var = BooleanVar()
        if 'param' in self.value:
            if 'filterParam' in self.value['param']:
                if 'filter' in self.value['param']['filterParam']:
                    val = self.value['param']['filterParam']['filter']
                    self.filter_var.set(val)
                else:
                    self.filter_var.set(False)
            else:
                self.filter_var.set(False)
        else:
            self.filter_var.set(False)

        self.filter = Checkbutton(
            self.content_frame,
            text = "Filter",
            variable= self.filter_var,
            onvalue= True,
            offvalue= False,
            command = self.filter_pressed)

        self.filter_frame = Frame(self.content_frame, border = 5)
        self.filter_type_label = Label(
            self.filter_frame,
            text = "Filter type:"
        )
        if 'param' in self.value:
            if 'filterParam' in self.value['param']:
                if 'type' in self.value['param']['filterParam']:
                    f_param = self.value['param']['filterParam']
                    init_filter_type = f_param['type']
                else:
                    init_filter_type = ''
            else:
                init_filter_type = ''
        else:
            init_filter_type = ''
        self.filter_type = SelectorCombo(
            self.filter_frame,
            pairs = FILTER_TYPE_LABEL_NAME_PAIRS,
            init_name = init_filter_type
        )
        self.f1_label = Label(self.filter_frame, text = "f1 [Hz]:")
        self.f1 = FloatEntry(self.filter_frame)
        self.f2_label = Label(self.filter_frame, text = "f2 [Hz]:")
        self.f2 = FloatEntry(self.filter_frame)
        self.order_label = Label(self.filter_frame, text = "Order:")
        self.order = UnsignedIntegerEntry(self.filter_frame)
        if 'param' in self.value:
            if 'filterParam' in self.value['param']:
                if 'f1' in self.value['param']['filterParam']:
                    val = self.value['param']['filterParam']['f1']
                    self.f1.insert(0, val)
                else:
                    self.f1.insert(0, '0')
                if 'f2' in self.value['param']['filterParam']:
                    val = self.value['param']['filterParam']['f2']
                    self.f2.insert(0, val)
                else:
                    self.f2.insert(0, '0')
                if 'order' in self.value['param']['filterParam']:
                    val = self.value['param']['filterParam']['order']
                    self.order.insert(0, val)
                else:
                    self.order.insert(0, '4')
        self.glide_var = BooleanVar()
        if 'param' in self.value:
            if 'glide' in self.value['param']:
                val = self.value['param']['glide']
                self.glide_var.set(val)
        self.glide = Checkbutton(
            self.content_frame,
            text = 'Glide',
            variable= self.glide_var,
            onvalue= True,
            offvalue= False,
            command = self.gliding_pressed)
        if 'param' in self.value:
            if 'glide' in self.value['param']:
                    val = self.value['param']['glide']
                    self.glide_var.set(val)

        self.gliding_frame = Frame(self.content_frame, border = 5)
        self.number_of_points_label = Label(
            self.gliding_frame,
            text = "Number of points for averaging:"
        )
        self.number_of_points = UnsignedIntegerEntry(self.gliding_frame)
        if 'numOfPoints' in self.value['param']:
            val = self.value['param']['numOfPoints']
            self.number_of_points.insert(0,val)
        else:
            self.number_of_points.insert(0,'10')
        self.p_server_var = BooleanVar()
        if 'performOnServer' in self.value:
            self.p_server_var.set(self.value['performOnServer'])
        self.p_server = Checkbutton(
            self.content_frame,
            text = 'Perform on server',
            variable= self.p_server_var,
            onvalue= True,
            offvalue= False)
                    
        self.buttons_frame = Frame(self.content_frame)
        self.ok_button = Button(
            self.buttons_frame, text='Ok', command = self.ok_event
        )
        self.cancel_button = Button(
            self.buttons_frame, text='Cancel', command = self.cancel_event
        )
        self.content_frame.pack(fill = BOTH, expand = 1)
        self.geometry(f'240x460+{x}+{y}')
        self.resizable(False, False)
        self.sig_name_label.pack(side = TOP, anchor = 'w')
        self.sig_name.pack(side = TOP, fill = X, expand = 1)
        self.t2t.pack(side = TOP, expand = 1, anchor = 'w')
        self.av_per_rev.pack(side = TOP, expand = 1, anchor = 'w')
        self.filter.pack(side = TOP, expand = 1, anchor = 'w')

        self.filter_frame.pack(fill = BOTH, expand = 1)
        self.filter_type_label.pack(side = TOP, anchor = 'w')
        self.filter_type.pack(side = TOP, fill = X, expand = 1)
        self.f1_label.pack(side = TOP, anchor = 'w')
        self.f1.pack(side = TOP, fill = X, expand = 1)
        self.f2_label.pack(side = TOP, anchor = 'w')
        self.f2.pack(side = TOP, fill = X, expand = 1)
        self.order_label.pack(side = TOP, anchor = 'w')
        self.order.pack(side = TOP, fill = X, expand = 1)

        self.glide.pack(side = TOP, expand = 1, anchor = 'w')
        self.gliding_frame.pack(fill = BOTH, expand = 1)
        self.number_of_points_label.pack(side = TOP, anchor = 'w')
        self.number_of_points.pack(side = TOP, fill = X, expand = 1)

        self.p_server.pack(side = TOP, expand = 1, anchor = 'w')
        self.buttons_frame.pack(side = TOP, fill = X)
        self.ok_button.pack(side = RIGHT, expand = 1)
        self.cancel_button.pack(side = RIGHT, expand = 1)

        self.gliding_pressed()
        self.filter_pressed()

    #Button command callback method doesn't have event param.
    def ok_event(self):
        if self.callback != None:
            if not 'param' in self.value:
                self.value['param'] = {}
            self.value['param']['triggerToTrigger'] = self.t2t_var.get()
            val = self.av_per_rev_var.get()
            self.value['param']['averagePerRevolution'] = val
            self.value['param']['glide'] = self.glide_var.get()
            self.value['param']['numOfPoints'] = self.number_of_points.get()
            if not 'filterParam' in self.value['param']:
                self.value['param']['filterParam'] = {}
            self.value['param']['filterParam']['filter'] = self.filter_var.get()
            type = self.filter_type.get()
            self.value['param']['filterParam']['type'] = type
            self.value['param']['filterParam']['f1'] = self.f1.get()
            self.value['param']['filterParam']['f2'] = self.f2.get()
            self.value['param']['filterParam']['order'] = self.order.get()
            self.value['performOnServer'] = self.p_server_var.get()
            self.callback(
                new_value = self.value,
                signal_updates = [{
                    "label": self.signal_label,
                    "name": self.sig_name.get()
                }]
            )
            self.destroy()

    def filter_pressed(self):
        if self.filter_var.get():
            self.enable_filter_elements()
        else:
            self.disable_filter_elements()

    def gliding_pressed(self):
        if self.glide_var.get():
            self.enable_gliding_elements()
        else:
            self.disable_gliding_elements()

    def disable_filter_elements(self):
        for i in [
                self.filter_type_label,
                self.filter_type,
                self.f1_label,
                self.f1,
                self.f2_label,
                self.f2,
                self.order_label,
                self.order
            ]:
                i['state'] = DISABLED

    def enable_filter_elements(self):
        for i in [
                self.filter_type_label,
                self.filter_type,
                self.f1_label,
                self.f1,
                self.f2_label,
                self.f2,
                self.order_label,
                self.order
            ]:
                i['state'] = NORMAL

    def disable_gliding_elements(self):
        for i in [
                self.number_of_points_label,
                self.number_of_points
            ]:
                i['state'] = DISABLED

    def enable_gliding_elements(self):
        for i in [
                self.number_of_points_label,
                self.number_of_points
            ]:
                i['state'] = NORMAL

    def cancel_event(self):
        self.cancel_callback()
        self.destroy()
    
    def x_button(self):
        self.cancel_callback()
        self.destroy()


class RegimeInterface(Toplevel):
    def __init__(
        self,
        x,
        y,
        init_value,
        regime_name = '',
        sig_pairs = [],
        callback = None,
        cancel_callback = None
    ):
        Toplevel.__init__(self)
        self.title('Regime:')
        self.value = init_value
        self.sig_pairs = sig_pairs
        self.callback = callback
        self.cancel_callback = cancel_callback
        self.protocol('WM_DELETE_WINDOW', self.x_button)
        self.content_frame = Frame(self, border = 5)
        self.regime_name_label = Label(self.content_frame, text = 'Regime Name:')
        self.regime_name = Entry(self.content_frame)
        if regime_name != None:
            self.regime_name.insert(0, regime_name)
        else:
            self.regime_name.insert(0, '')
        self.regime_definitions_label = Label(
            self.content_frame,
            text = 'Regime logical definition statement:')
        self.regime_definitions = Entry(self.content_frame)
        self.regime_definitions.insert(0, self.value['regimeLogicalDefinitionStatement'])
        self.statement_description_label = Label(
            self.content_frame,
            text = """Write signal names with quotation marks "signal name" or 'signal name'! For example:"""
        )
        self.statement_example_label = Label(
            self.content_frame,
            text = """"Unit rotational speed [rpm]" or 'Unit rotational speed [rpm]'"""
        )
        self.buttons_frame = Frame(self.content_frame)
        self.ok_button = Button(
            self.buttons_frame, text='Ok', command = self.ok_event
        )
        self.cancel_button = Button(
            self.buttons_frame, text='Cancel', command = self.cancel_event
        )

        self.geometry(f'600x300+{x}+{y}')
        self.resizable(False, False)
        self.content_frame.pack(fill = BOTH, expand = 1)
        self.regime_name_label.pack(side = TOP, anchor = 'w')
        self.regime_name.pack(side = TOP, fill = X, expand = 1)
        self.regime_definitions_label.pack(side = TOP, anchor = 'w')
        self.regime_definitions.pack(side = TOP, fill = X, expand = 1)
        self.statement_description_label.pack(side = TOP, anchor = 'w')
        self.statement_example_label.pack(side = TOP, anchor = 'w')
        self.buttons_frame.pack(side = TOP, fill = BOTH)
        self.ok_button.pack(side = RIGHT, expand = 1)
        self.cancel_button.pack(side = RIGHT, expand = 1)


    def call_callback(self):
        self.value['regimeLogicalDefinitionStatement'] = self.definitions
        self.callback(
            new_value = self.value,
            regime_updates = [{
                "label": self.value['label'],
                "name": self.regime_name.get()
            }]
        )

    def ok_event(self):
        reg_def = self.regime_definitions.get()
        self.definitions = self.replace_names_with_labels(self.sig_pairs, reg_def)
        if self.definitions != None:
            self.call_callback()
            self.destroy()
        else:
            pass
            
    def return_pressed(self, e):
        self.call_callback()
        return 'break'

    def cancel_event(self):
        self.cancel_callback()
        self.destroy()
    
    def x_button(self):
        self.cancel_callback()
        self.destroy()

    def replace_names_with_labels(self, sig_pairs, definitions):
        for i in sig_pairs:
            old_str = "'"+f"{i['name']}"+"'"
            definitions = definitions.replace(old_str, i['label'])
            old_str = '"'+f'{i["name"]}'+'"'
            definitions = definitions.replace(old_str, i['label'])

        if "'" in definitions or '"' in definitions:
            messagebox.showinfo("Error:", "The signal name could not be found in database.")
            return None
        else:
            return definitions

        
class AlarmInterface(Toplevel):
    def __init__(
        self,
        x,
        y,
        init_value,
        sig_pairs = [],
        callback = None,
        cancel_callback = None
    ):
        Toplevel.__init__(self)
        self.title('Alarm:')
        self.value = init_value
        self.sig_pairs = sig_pairs
        self.callback = callback
        self.cancel_callback = cancel_callback
        self.protocol('WM_DELETE_WINDOW', self.x_button)
        self.content_frame = Frame(self, border = 5)
        self.alarm_logic_label = Label(
            self.content_frame,
            text = 'Alarm logic:'
        )
        self.alarm_logic = Entry(self.content_frame)
        self.alarm_logic.insert(0, self.value['logicalSentence'])
        self.delay_entry_label = Label(
            self.content_frame,
            text = "Alarm delay:"
        )
        self.delay_entry = IntegerEntry(self.content_frame)
        if 'delay' in self.value:
            self.delay_entry.insert(0, init_value['delay'])
        self.alarm_priority_label = Label(
            self.content_frame,
            text = "Alarm priority:"
        )
        self.alarm_priority = IntegerEntry(self.content_frame)
        if 'alarmPriority' in self.value:
            self.alarm_priority.insert(0, init_value['alarmPriority'])
        self.buttons_frame = Frame(self.content_frame)
        self.ok_button = Button(
            self.buttons_frame, text='Ok', command = self.ok_event
        )
        self.cancel_button = Button(
            self.buttons_frame, text='Cancel', command = self.cancel_event
        )
        self.geometry(f'600x300+{x}+{y}')
        self.resizable(False, False)
        self.content_frame.pack(fill = BOTH, expand = 1)
        self.alarm_logic_label.pack(side = TOP, anchor = 'w')
        self.alarm_logic.pack(side = TOP, fill = X, expand = 1)
        self.delay_entry_label.pack(side = TOP, anchor = 'w')
        self.delay_entry.pack(side = TOP, fill = X, expand = 1)
        self.alarm_priority_label.pack(side = TOP, anchor = 'w')
        self.alarm_priority.pack(side = TOP, fill = X, expand = 1)
        self.buttons_frame.pack(side = TOP, fill = BOTH)
        self.ok_button.pack(side = RIGHT, expand = 1)
        self.cancel_button.pack(side = RIGHT, expand = 1)

    def call_callback(self):
        self.value['logicalSentence'] = self.definitions
        self.value['delay'] = int(self.delay_entry.get())
        self.value['alarmPriority'] = int(self.alarm_priority.get())
        self.callback(
            new_value = self.value
        )

    def ok_event(self):
        self.definitions = self.replace_names_with_labels(
            sig_pairs = self.sig_pairs,
            definitions = self.alarm_logic.get()
        )
        if self.definitions != None:
            self.call_callback()
            self.destroy()
        else:
            pass

    def cancel_event(self):
        self.cancel_callback()
        self.destroy()
    
    def x_button(self):
        self.cancel_callback()
        self.destroy()

    def replace_names_with_labels(self, sig_pairs, definitions):
        for i in sig_pairs:
            old_str = "'"+f"{i['name']}"+"'"
            definitions = definitions.replace(old_str, i['label'])
            old_str = '"'+f'{i["name"]}'+'"'
            definitions = definitions.replace(old_str, i['label'])

        if "'" in definitions or '"' in definitions:
            messagebox.showinfo("Error:", "The signal name could not be found in database.")
            return None
        else:
            return definitions


class ChannelInterface(Toplevel):

    def __init__(
        self,
        init_value,
        ch_name,
        x,
        y,
        callback = None,
        cancel_callback = None
    ):
        Toplevel.__init__(self)
        self.title("Channel:")
        self.value = init_value
        self.callback = callback
        self.cancel_callback = cancel_callback
        self.protocol('WM_DELETE_WINDOW', self.x_button)
        #This line removes title bar. It is OS dependent.
        #self.wm_overrideredirect(True)
        """self.border_frame = Frame(
            self,
            borderwidth = 2,
            relief = FLAT,
            bg = 'gray'
        )"""
        self.content_frame = Frame(self, borderwidth = 5)
        self.ch_name_label = Label(self.content_frame, text = "Channel name:")
        self.ch_name = Entry(self.content_frame)
        self.ch_name.insert(0, ch_name)
        self.ph_ch_label = Label(self.content_frame, text = "Physical channel:")
        self.ph_ch = IntegerEntry(self.content_frame)

        if 'physicalChannel' in self.value:
            self.ph_ch.insert(0, init_value['physicalChannel'])
        else:
            self.ph_ch.insert(0, '0')
        self.slope_label = Label(self.content_frame, text = "Slope:")
        self.slope = FloatEntry(self.content_frame)
        if 'slope' in self.value:
            self.slope.insert(0, init_value['slope'])
        else:
            self.slope.insert(0, '1')
        self.intercept_label = Label(self.content_frame, text = "Intercept:")
        self.intercept = FloatEntry(self.content_frame)
        if 'intercept' in self.value:
            self.intercept.insert(0, init_value['intercept'])
        else:
            self.intercept.insert(0, '0')

        self.filter_var = BooleanVar()
        if 'filter' in self.value:
            val = self.value['filter']
            self.filter_var.set(val)
        else:
            self.filter_var.set(False)

        self.filter = Checkbutton(
            self.content_frame,
            text = "Filter",
            variable= self.filter_var,
            onvalue= True,
            offvalue= False,
            command = self.filter_pressed)

        self.filter_frame = Frame(self.content_frame, border = 5)
        self.filter_type_label = Label(
            self.filter_frame,
            text = "Filter type:"
        )
        if 'filterType' in self.value:
            init_filter_type = self.value['filterType']
        else:
            init_filter_type = 'Lowpass'
        self.filter_type = SelectorCombo(
            self.filter_frame,
            pairs = FILTER_TYPE_LABEL_NAME_PAIRS,
            init_name = init_filter_type
        )
        self.f1_label = Label(self.filter_frame, text = "f1 [Hz]:")
        self.f1 = FloatEntry(self.filter_frame)
        self.f2_label = Label(self.filter_frame, text = "f2 [Hz]:")
        self.f2 = FloatEntry(self.filter_frame)
        self.order_label = Label(self.filter_frame, text = "Order:")
        self.order = UnsignedIntegerEntry(self.filter_frame)
        if 'f1' in self.value:
            val = self.value['f1']
            self.f1.insert(0, val)
        else:
            self.f1.insert(0, '0')

        if 'f2' in self.value:
            val = self.value['f2']
            self.f2.insert(0, val)
        else:
            self.f2.insert(0, '0')
        if 'order' in self.value:
            val = self.value['order']
            self.order.insert(0, val)
        else:
            self.order.insert(0, '4')

        self.integration_label = Label(
            self.content_frame,
            text = "Integration:"
        )
        if 'integration' in self.value:
            init_integration_type = self.value['integration']
        else:
            init_integration_type = 'Do not integrate'
        self.integration = SelectorCombo(
            self.content_frame,
            pairs = INTEGRATE_TYPE_LABEL_NAME_PAIRS,
            init_name = init_integration_type
        )

        self.save_to_db_var = BooleanVar()
        if 'saveTodBase' in self.value:
            self.save_to_db_var.set(self.value['saveTodBase'])
        else:
            self.save_to_db_var.set('True')
        self.save_to_db = Checkbutton(
            self.content_frame,
            text = 'Save to data base',
            variable= self.save_to_db_var,
            onvalue= True,
            offvalue= False)

        self.buttons_frame = Frame(self.content_frame)
        self.ok_button = Button(
            self.buttons_frame, text='Ok', command = self.ok_event
        )
        self.cancel_button = Button(
            self.buttons_frame, text='Cancel', command = self.cancel_event
        )
        #self.border_frame.pack(fill = BOTH, expand = 1)
        self.content_frame.pack(fill = BOTH, expand = 1)
        self.geometry(f'280x520+{x}+{y}')
        self.resizable(False, False)
        self.ch_name_label.pack(side = TOP, anchor = 'w')
        self.ch_name.pack(side = TOP, fill = X, expand = 1)
        self.ph_ch_label.pack(side = TOP, anchor = 'w')
        self.ph_ch.pack(side = TOP, fill = X, expand = 1)
        self.slope_label.pack(side = TOP, anchor = 'w')
        self.slope.pack(side = TOP, fill = X, expand = 1)
        self.intercept_label.pack(side = TOP, anchor = 'w')
        self.intercept.pack(side = TOP, fill = X, expand = 1)
        self.filter.pack(side = TOP, expand = 1, anchor = 'w')
        self.filter_frame.pack(fill = BOTH, expand = 1)
        self.filter_type_label.pack(side = TOP, anchor = 'w')
        self.filter_type.pack(side = TOP, fill = X, expand = 1)
        self.f1_label.pack(side = TOP, anchor = 'w')
        self.f1.pack(side = TOP, fill = X, expand = 1)
        self.f2_label.pack(side = TOP, anchor = 'w')
        self.f2.pack(side = TOP, fill = X, expand = 1)
        self.order_label.pack(side = TOP, anchor = 'w')
        self.order.pack(side = TOP, fill = X, expand = 1)
        self.integration_label.pack(side = TOP, anchor = 'w')
        self.integration.pack(side = TOP, fill = X, expand = 1)
        self.save_to_db.pack(side = TOP, expand = 1, anchor = 'w')
        self.buttons_frame.pack(side = TOP, fill = X)
        self.ok_button.pack(side = RIGHT, expand = 1)
        self.cancel_button.pack(side = RIGHT, expand = 1)
        self.filter_pressed()

    def call_callback(self):
        if self.callback != None:
            self.value['physicalChannel'] = int(self.ph_ch.get())
            self.value['slope'] = float(self.slope.get())
            self.value['intercept'] = float(self.intercept.get())
            self.value['filter'] = self.filter_var.get()
            type = self.filter_type.get()
            self.value['filterType'] = type
            self.value['f1'] = self.f1.get()
            self.value['f2'] = self.f2.get()
            self.value['order'] = self.order.get()
            self.value['integration'] = self.integration.get()
            self.value['saveTodBase'] = self.save_to_db_var.get()
            if 'samplingRate' not in self.value:
                self.value['samplingRate'] = 2048
            if 'analyses' not in self.value:
                self.value['analyses'] = []
            self.callback(
                new_value = self.value,
                sensor_updates = [{
                    "label": self.value['label'],
                    "name": self.ch_name.get()
                }]
            )

    #Button command callback method doesn't have event param.
    def ok_event(self):
        self.call_callback()
        self.destroy()

    def filter_pressed(self):
        if self.filter_var.get():
            self.enable_filter_elements()
        else:
            self.disable_filter_elements()


    def disable_filter_elements(self):
        for i in [
                self.filter_type_label,
                self.filter_type,
                self.f1_label,
                self.f1,
                self.f2_label,
                self.f2,
                self.order_label,
                self.order
            ]:
                i['state'] = DISABLED


    def enable_filter_elements(self):
        for i in [
                self.filter_type_label,
                self.filter_type,
                self.f1_label,
                self.f1,
                self.f2_label,
                self.f2,
                self.order_label,
                self.order
            ]:
                i['state'] = NORMAL
            
    def return_pressed(self, e):
        self.call_callback()
        self.destroy()

    def cancel_event(self):
        self.cancel_callback()
        self.destroy()
    
    def x_button(self):
        self.cancel_callback()
        self.destroy()


class TempJsonEditor(Toplevel):

    
    def __init__(
        self,
        init_value,
        x,
        y,
        callback = None,
        cancel_callback = None
    ):
        Toplevel.__init__(self)
        self.title("Json:")
        self.value = init_value
        self.callback = callback
        self.cancel_callback = cancel_callback
        self.protocol('WM_DELETE_WINDOW', self.x_button)
        self.content_frame = Frame(self, borderwidth = 5)
        self.text = Text(self.content_frame, height = 10)
        self.text.insert(END, dumps(init_value))
        self.text.bind('<Key-Return>', self.return_pressed)
        self.buttons_frame = Frame(self.content_frame)
        self.ok_button = Button(
            self.buttons_frame, text='Ok', command = self.ok_event
        )
        self.cancel_button = Button(
            self.buttons_frame, text='Cancel', command = self.cancel_event
        )
        self.geometry(f'600x600+{x}+{y}')
        self.resizable(False, False)
        self.content_frame.pack(fill = BOTH, expand = 1)
        self.text.pack(side = TOP, fill = BOTH, expand = 1)
        self.buttons_frame.pack(side = TOP, fill = BOTH)
        self.ok_button.pack(side = RIGHT, expand = 1)
        self.cancel_button.pack(side = RIGHT, expand = 1)
    
    def call_callback(self):
        try:
            new_value = loads(self.text.get('0.0', END))
        except JSONDecodeError:
            showerror(
                parent = self, 
                title = "Greska!", 
                message = "JSON razmrdan!"
            )
            return
        self.callback(new_value = new_value)
        self.destroy()

    def ok_event(self):
        self.call_callback()
            
    def return_pressed(self, e):
        self.call_callback()
        return 'break'

    def cancel_event(self):
        self.cancel_callback()
        self.destroy()
    
    def x_button(self):
        self.cancel_callback()
        self.destroy()


class UnitInterface(Toplevel):

    def __init__(
        self,
        init_value,
        x,
        y,
        callback = None,
        cancel_callback = None
    ):
        #-----------------------------------------------------------
        #init_value: string
        #ch_pairs: object of Label_name_pairs class
        #-----------------------------------------------------------
        Toplevel.__init__(self)
        self.title("Unit:")
        self.value = init_value
        self.callback = callback
        self.cancel_callback = cancel_callback
        self.protocol('WM_DELETE_WINDOW', self.x_button)
        self.content_frame = Frame(self, borderwidth = 5)
        self.t_freq_label = Label(
            self.content_frame,
            text = "Electric frequency:"
        )
        f_pairs =[
            {'name': '50', 'label': '50'},
            {'name': '60', 'label': '60'}
        ]
        if 'electricFrequency' in self.value:
            if self.value['electricFrequency'] == 50: init_f = '50'
            if self.value['electricFrequency'] == 60: init_f = '60'
        else:
            init_f = '50'
        self.frequency = SelectorCombo(
            self.content_frame,
            pairs = Label_name_pairs(f_pairs),
            init_name = init_f
        )
        self.num_poles_label = Label(self.content_frame, text = "Number of poles:")
        self.num_poles = UnsignedIntegerEntry(self.content_frame)
        if 'numberOfPoles' in self.value:
            self.num_poles.insert(0, self.value['numberOfPoles'])
        else:
            self.num_poles.insert(0, '0')
        self.buttons_frame = Frame(self.content_frame)
        self.ok_button = Button(
            self.buttons_frame, text='Ok', command = self.ok_event
        )
        self.cancel_button = Button(
            self.buttons_frame, text='Cancel', command = self.cancel_event
        )
        self.content_frame.pack(fill = BOTH, expand = 1)
        self.geometry(f'200x150+{x}+{y}')
        self.resizable(False, False)
        self.t_freq_label.pack(side = TOP, anchor = 'w')
        self.frequency.pack(side = TOP, fill = X, expand = 1)
        self.num_poles_label.pack(side = TOP, anchor = 'w')
        self.num_poles.pack(side = TOP, fill = X, expand = 1)
        self.buttons_frame.pack(side = TOP, fill = X)
        self.ok_button.pack(side = RIGHT, expand = 1)
        self.cancel_button.pack(side = RIGHT, expand = 1)

    def call_callback(self):
        if self.callback != None:
            self.value['electricFrequency'] = int(self.frequency.get())
            self.value['numberOfPoles'] = int(self.num_poles.get())
            self.callback(new_value = self.value)

    #Button command callback method doesn't have event param.
    def ok_event(self):
        self.call_callback()
        self.destroy()
            
    def return_pressed(self, e):
        self.call_callback()
        self.destroy()

    def cancel_event(self):
        self.cancel_callback()
        self.destroy()
    
    def x_button(self):
        self.cancel_callback()
        self.destroy()


class ChannelAnalysisDC(Toplevel):

    def __init__(
        self,
        x,
        y,
        init_value,
        signal_label = '',
        signal_name = '',
        callback = None,
        cancel_callback = None
    ):
        Toplevel.__init__(self)
        self.title("Dc:")
        self.value = init_value
        self.signal_label = signal_label
        self.callback = callback
        self.cancel_callback = cancel_callback
        self.protocol('WM_DELETE_WINDOW', self.x_button)
        self.content_frame = Frame(self, border = 5)
        self.sig_name_label = Label(self.content_frame, text = "Signal name:")
        self.sig_name = Entry(self.content_frame)
        self.sig_name.insert(0, signal_name)
        self.t2t_var = BooleanVar()
        if 'param' in self.value:
            if 'triggerToTrigger' in self.value['param']:
                self.t2t_var.set(self.value['param']['triggerToTrigger'])
        self.t2t = Checkbutton(
            self.content_frame,
            text = "Trigger to trigger",
            variable= self.t2t_var,
            onvalue= True,
            offvalue= False)


        self.p_server_var = BooleanVar()
        if 'performOnServer' in self.value:
            self.p_server_var.set(self.value['performOnServer'])
        self.p_server = Checkbutton(
            self.content_frame,
            text = 'Perform on server',
            variable= self.p_server_var,
            onvalue= True,
            offvalue= False)

        self.buttons_frame = Frame(self.content_frame)
        self.ok_button = Button(
            self.buttons_frame, text='Ok', command = self.ok_event
        )
        self.cancel_button = Button(
            self.buttons_frame, text='Cancel', command = self.cancel_event
        )
        self.content_frame.pack(fill = BOTH, expand = 1)
        self.geometry(f'200x160+{x}+{y}')
        self.resizable(False, False)
        self.sig_name_label.pack(side = TOP, anchor = 'w')
        self.sig_name.pack(side = TOP, fill = X, expand = 1)
        self.t2t.pack(side = TOP, expand = 1, anchor = 'w')
        self.p_server.pack(side = TOP, expand = 1, anchor = 'w')
        self.buttons_frame.pack(side = TOP, fill = X)
        self.ok_button.pack(side = RIGHT, expand = 1)
        self.cancel_button.pack(side = RIGHT, expand = 1)

    #Button command callback method doesn't have event param.
    def ok_event(self):
        if self.callback != None:
            if 'param' in self.value:
                self.value['param']['triggerToTrigger'] = self.t2t_var.get()
            else:
                self.value['param'] = {}
                self.value['param']['triggerToTrigger'] = self.t2t_var.get()
            self.value['performOnServer'] = self.p_server_var.get()
            self.callback(
                new_value = self.value,
                signal_updates = [{
                    "label": self.signal_label,
                    "name": self.sig_name.get()
                }]
            )
            self.destroy()

    def cancel_event(self):
        self.cancel_callback()
        self.destroy()
    
    def x_button(self):
        self.cancel_callback()
        self.destroy()


class ChannelAnalysisRms(Toplevel):

    def __init__(
        self,
        x,
        y,
        init_value,
        signal_label = '',
        signal_name = '',
        callback = None,
        cancel_callback = None
    ):
        Toplevel.__init__(self)
        self.title("Rms:")
        self.value = init_value
        self.signal_label = signal_label
        self.callback = callback
        self.cancel_callback = cancel_callback
        self.protocol('WM_DELETE_WINDOW', self.x_button)
        self.content_frame = Frame(self, border = 5)
        self.sig_name_label = Label(self.content_frame, text = "Signal name:")
        self.sig_name = Entry(self.content_frame)
        self.sig_name.insert(0, signal_name)

        self.t2t_var = BooleanVar()
        if 'param' in self.value:
            if 'triggerToTrigger' in self.value['param']:
                self.t2t_var.set(self.value['param']['triggerToTrigger'])
        self.t2t = Checkbutton(
            self.content_frame,
            text = "Trigger to trigger",
            variable= self.t2t_var,
            onvalue= True,
            offvalue= False)

        self.av_per_rev_var = BooleanVar()
        if 'param' in self.value:
            if 'averagePerRevolution' in self.value['param']:
                val = self.value['param']['averagePerRevolution']
                self.av_per_rev_var.set(val)
        self.av_per_rev = Checkbutton(
            self.content_frame,
            text = "Average per revolution",
            variable= self.av_per_rev_var,
            onvalue= True,
            offvalue= False)

        self.substract_dc_var = BooleanVar()
        if 'param' in self.value:
            if 'substractDc' in self.value['param']:
                val = self.value['param']['substractDc']
                self.substract_dc_var.set(val)
        self.substract_dc = Checkbutton(
            self.content_frame,
            text = "Substract Dc",
            variable= self.substract_dc_var,
            onvalue= True,
            offvalue= False)

        self.filter_var = BooleanVar()
        if 'param' in self.value:
            if 'filterParam' in self.value['param']:
                if 'filter' in self.value['param']['filterParam']:
                    val = self.value['param']['filterParam']['filter']
                    self.filter_var.set(val)
                else:
                    self.filter_var.set(False)
            else:
                self.filter_var.set(False)
        else:
            self.filter_var.set(False)

        self.filter = Checkbutton(
            self.content_frame,
            text = "Filter",
            variable= self.filter_var,
            onvalue= True,
            offvalue= False,
            command = self.filter_pressed)

        self.filter_frame = Frame(self.content_frame, border = 5)
        self.filter_type_label = Label(
            self.filter_frame,
            text = "Filter type:"
        )
        if 'param' in self.value:
            if 'filterParam' in self.value['param']:
                if 'type' in self.value['param']['filterParam']:
                    f_param = self.value['param']['filterParam']
                    init_filter_type = f_param['type']
                else:
                    init_filter_type = ''
            else:
                init_filter_type = ''
        else:
            init_filter_type = ''
        self.filter_type = SelectorCombo(
            self.filter_frame,
            pairs = FILTER_TYPE_LABEL_NAME_PAIRS,
            init_name = init_filter_type
        )
        self.f1_label = Label(self.filter_frame, text = "f1 [Hz]:")
        self.f1 = FloatEntry(self.filter_frame)
        self.f2_label = Label(self.filter_frame, text = "f2 [Hz]:")
        self.f2 = FloatEntry(self.filter_frame)
        self.order_label = Label(self.filter_frame, text = "Order:")
        self.order = UnsignedIntegerEntry(self.filter_frame)
        if 'param' in self.value:
            if 'filterParam' in self.value['param']:
                if 'f1' in self.value['param']['filterParam']:
                    val = self.value['param']['filterParam']['f1']
                    self.f1.insert(0, val)
                else:
                    self.f1.insert(0, '0')
                if 'f2' in self.value['param']['filterParam']:
                    val = self.value['param']['filterParam']['f2']
                    self.f2.insert(0, val)
                else:
                    self.f2.insert(0, '0')
                if 'order' in self.value['param']['filterParam']:
                    val = self.value['param']['filterParam']['order']
                    self.order.insert(0, val)
                else:
                    self.order.insert(0, '4')
        self.glide_var = BooleanVar()
        if 'param' in self.value:
            if 'glide' in self.value['param']:
                val = self.value['param']['glide']
                self.glide_var.set(val)
        self.glide = Checkbutton(
            self.content_frame,
            text = 'Glide',
            variable= self.glide_var,
            onvalue= True,
            offvalue= False,
            command = self.gliding_pressed)
        if 'param' in self.value:
            if 'glide' in self.value['param']:
                    val = self.value['param']['glide']
                    self.glide_var.set(val)

        self.gliding_frame = Frame(self.content_frame, border = 5)
        self.number_of_points_label = Label(
            self.gliding_frame,
            text = "Number of points for averaging:"
        )
        self.number_of_points = UnsignedIntegerEntry(self.gliding_frame)
        if 'numOfPoints' in self.value['param']:
            val = self.value['param']['numOfPoints']
            self.number_of_points.insert(0,val)
        else:
            self.number_of_points.insert(0,'10')
        self.p_server_var = BooleanVar()
        if 'performOnServer' in self.value:
            self.p_server_var.set(self.value['performOnServer'])
        self.p_server = Checkbutton(
            self.content_frame,
            text = 'Perform on server',
            variable= self.p_server_var,
            onvalue= True,
            offvalue= False)
                    
        self.buttons_frame = Frame(self.content_frame)
        self.ok_button = Button(
            self.buttons_frame, text='Ok', command = self.ok_event
        )
        self.cancel_button = Button(
            self.buttons_frame, text='Cancel', command = self.cancel_event
        )
        self.content_frame.pack(fill = BOTH, expand = 1)
        self.geometry(f'240x460+{x}+{y}')
        self.resizable(False, False)
        self.sig_name_label.pack(side = TOP, anchor = 'w')
        self.sig_name.pack(side = TOP, fill = X, expand = 1)
        self.t2t.pack(side = TOP, expand = 1, anchor = 'w')
        self.av_per_rev.pack(side = TOP, expand = 1, anchor = 'w')
        self.substract_dc.pack(side = TOP, expand = 1, anchor = 'w')
        self.filter.pack(side = TOP, expand = 1, anchor = 'w')

        self.filter_frame.pack(fill = BOTH, expand = 1)
        self.filter_type_label.pack(side = TOP, anchor = 'w')
        self.filter_type.pack(side = TOP, fill = X, expand = 1)
        self.f1_label.pack(side = TOP, anchor = 'w')
        self.f1.pack(side = TOP, fill = X, expand = 1)
        self.f2_label.pack(side = TOP, anchor = 'w')
        self.f2.pack(side = TOP, fill = X, expand = 1)
        self.order_label.pack(side = TOP, anchor = 'w')
        self.order.pack(side = TOP, fill = X, expand = 1)

        self.glide.pack(side = TOP, expand = 1, anchor = 'w')
        self.gliding_frame.pack(fill = BOTH, expand = 1)
        self.number_of_points_label.pack(side = TOP, anchor = 'w')
        self.number_of_points.pack(side = TOP, fill = X, expand = 1)

        self.p_server.pack(side = TOP, expand = 1, anchor = 'w')
        self.buttons_frame.pack(side = TOP, fill = X)
        self.ok_button.pack(side = RIGHT, expand = 1)
        self.cancel_button.pack(side = RIGHT, expand = 1)

        self.gliding_pressed()
        self.filter_pressed()

    #Button command callback method doesn't have event param.
    def ok_event(self):
        if self.callback != None:
            if not 'param' in self.value:
                self.value['param'] = {}
            self.value['param']['triggerToTrigger'] = self.t2t_var.get()
            val = self.av_per_rev_var.get()
            self.value['param']['averagePerRevolution'] = val
            self.value['param']['substractDc'] = self.substract_dc_var.get()
            self.value['param']['glide'] = self.glide_var.get()
            self.value['param']['numOfPoints'] = self.number_of_points.get()
            if not 'filterParam' in self.value['param']:
                self.value['param']['filterParam'] = {}
            self.value['param']['filterParam']['filter'] = self.filter_var.get()
            type = self.filter_type.get()
            self.value['param']['filterParam']['type'] = type
            self.value['param']['filterParam']['f1'] = self.f1.get()
            self.value['param']['filterParam']['f2'] = self.f2.get()
            self.value['param']['filterParam']['order'] = self.order.get()
            self.value['performOnServer'] = self.p_server_var.get()
            self.callback(
                new_value = self.value,
                signal_updates = [{
                    "label": self.signal_label,
                    "name": self.sig_name.get()
                }]
            )
            self.destroy()

    def filter_pressed(self):
        if self.filter_var.get():
            self.enable_filter_elements()
        else:
            self.disable_filter_elements()

    def gliding_pressed(self):
        if self.glide_var.get():
            self.enable_gliding_elements()
        else:
            self.disable_gliding_elements()

    def disable_filter_elements(self):
        for i in [
                self.filter_type_label,
                self.filter_type,
                self.f1_label,
                self.f1,
                self.f2_label,
                self.f2,
                self.order_label,
                self.order
            ]:
                i['state'] = DISABLED

    def enable_filter_elements(self):
        for i in [
                self.filter_type_label,
                self.filter_type,
                self.f1_label,
                self.f1,
                self.f2_label,
                self.f2,
                self.order_label,
                self.order
            ]:
                i['state'] = NORMAL

    def disable_gliding_elements(self):
        for i in [
                self.number_of_points_label,
                self.number_of_points
            ]:
                i['state'] = DISABLED

    def enable_gliding_elements(self):
        for i in [
                self.number_of_points_label,
                self.number_of_points
            ]:
                i['state'] = NORMAL

    def cancel_event(self):
        self.cancel_callback()
        self.destroy()
    
    def x_button(self):
        self.cancel_callback()
        self.destroy()


class NoParameterAnalysis(Toplevel):

    def __init__(
        self,
        x,
        y,
        init_value,
        signal_label = '',
        signal_name = '',
        title = '',
        callback = None,
        cancel_callback = None
    ):
        Toplevel.__init__(self)
        if title == 'sigfreq':
            self.title("Signal Frequency:")
        elif title == 'thd':
            self.title("Thd:")
        elif title == 'actpwr':
            self.title("Active power:")
        elif title == 'reactpwr':
            self.title("Reactive power:")
        else:
            self.title("Unknown:")

        self.value = init_value
        self.signal_label = signal_label
        self.callback = callback
        self.cancel_callback = cancel_callback
        self.protocol('WM_DELETE_WINDOW', self.x_button)
        self.content_frame = Frame(self, border = 5)
        self.sig_name_label = Label(self.content_frame, text = "Signal name:")
        self.sig_name = Entry(self.content_frame)
        self.sig_name.insert(0, signal_name)

        self.p_server_var = BooleanVar()
        if 'performOnServer' in self.value:
            self.p_server_var.set(self.value['performOnServer'])
        self.p_server = Checkbutton(
            self.content_frame,
            text = 'Perform on server',
            variable= self.p_server_var,
            onvalue= True,
            offvalue= False)

        self.buttons_frame = Frame(self.content_frame)
        self.ok_button = Button(
            self.buttons_frame, text='Ok', command = self.ok_event
        )
        self.cancel_button = Button(
            self.buttons_frame, text='Cancel', command = self.cancel_event
        )
        self.content_frame.pack(fill = BOTH, expand = 1)
        self.geometry(f'200x160+{x}+{y}')
        self.resizable(False, False)
        self.sig_name_label.pack(side = TOP, anchor = 'w')
        self.sig_name.pack(side = TOP, fill = X, expand = 1)
        self.p_server.pack(side = TOP, expand = 1, anchor = 'w')
        self.buttons_frame.pack(side = TOP, fill = X)
        self.ok_button.pack(side = RIGHT, expand = 1)
        self.cancel_button.pack(side = RIGHT, expand = 1)

    #Button command callback method doesn't have event param.
    def ok_event(self):
        if self.callback != None:
            self.value['performOnServer'] = self.p_server_var.get()
            self.callback(
                new_value = self.value,
                signal_updates = [{
                    "label": self.signal_label,
                    "name": self.sig_name.get()
                }]
            )
            self.destroy()

    def cancel_event(self):
        self.cancel_callback()
        self.destroy()
    
    def x_button(self):
        self.cancel_callback()
        self.destroy()


class ChannelAnalysisHarmonic(Toplevel):

    def __init__(
        self,
        x,
        y,
        init_value,
        channel_label = '',
        signal_name_A = '',
        signal_name_Ph = '',
        signal_label_A_old = '',
        signal_label_Ph_old = '',
        callback = None,
        cancel_callback = None
    ):
        Toplevel.__init__(self)
        self.title("Harmonic:")
        self.value = init_value
        self.channel_label = channel_label
        self.callback = callback
        self.cancel_callback = cancel_callback
        self.signal_label_A_old = signal_label_A_old
        self.signal_label_Ph_old = signal_label_Ph_old
        self.protocol('WM_DELETE_WINDOW', self.x_button)
        self.content_frame = Frame(self, border = 5)
        self.sig_name_A_label = Label(self.content_frame, text = "Signal amplitude name:")
        self.sig_name_A = Entry(self.content_frame)
        self.sig_name_A.insert(0, signal_name_A)
        self.sig_name_Ph_label = Label(self.content_frame, text = "Signal phase name:")
        self.sig_name_Ph = Entry(self.content_frame)
        self.sig_name_Ph.insert(0, signal_name_Ph)

        self.ampl_var = BooleanVar()
        if 'param' in self.value:
            if 'amplitude' in self.value['param']:
                self.ampl_var.set(self.value['param']['amplitude'])
        self.ampl = Checkbutton(
            self.content_frame,
            text = "Amplitude",
            variable= self.ampl_var,
            onvalue= True,
            offvalue= False)
        
        self.harmonic_number_label = Label(self.content_frame, text = "Harmonic number:")
        self.harmonic_number = UnsignedIntegerEntry(self.content_frame)
        if 'harmonic' in self.value['param']:
            val = self.value['param']['harmonic']
            self.harmonic_number.insert(0,val)
        else:
            self.harmonic_number.insert(0,'1')

        self.p_server_var = BooleanVar()
        if 'performOnServer' in self.value:
            self.p_server_var.set(self.value['performOnServer'])
        self.p_server = Checkbutton(
            self.content_frame,
            text = 'Perform on server',
            variable= self.p_server_var,
            onvalue= True,
            offvalue= False)

        self.buttons_frame = Frame(self.content_frame)
        self.ok_button = Button(
            self.buttons_frame, text='Ok', command = self.ok_event
        )
        self.cancel_button = Button(
            self.buttons_frame, text='Cancel', command = self.cancel_event
        )

        self.content_frame.pack(fill = BOTH, expand = 1)
        self.geometry(f'230x260+{x}+{y}')
        self.resizable(False, False)
        self.sig_name_A_label.pack(side = TOP, anchor = 'w')
        self.sig_name_A.pack(side = TOP, fill = X, expand = 1)
        self.sig_name_Ph_label.pack(side = TOP, anchor = 'w')
        self.sig_name_Ph.pack(side = TOP, fill = X, expand = 1)
        self.ampl.pack(side = TOP, expand = 1, anchor = 'w')
        self.harmonic_number_label.pack(side = TOP, anchor = 'w')
        self.harmonic_number.pack(side = TOP, fill = X, expand = 1)
        self.p_server.pack(side = TOP, expand = 1, anchor = 'w')
        self.buttons_frame.pack(side = TOP, fill = X)
        self.ok_button.pack(side = RIGHT, expand = 1)
        self.cancel_button.pack(side = RIGHT, expand = 1)

    #Button command callback method doesn't have event param.
    def ok_event(self):
        if self.callback != None:
            if not 'param' in self.value:
                self.value['param'] = {}
            self.value['param']['amplitude'] = self.ampl_var.get()
            self.value['param']['harmonic'] = self.harmonic_number.get()
            self.value['performOnServer'] = self.p_server_var.get()
            self.signal_label_A = f'{self.channel_label}.s{self.harmonic_number.get()}.00A'
            self.signal_label_Ph = f'{self.channel_label}.s{self.harmonic_number.get()}.00Ph'
            if self.signal_label_A_old == '':
                self.callback(
                    new_value = self.value,
                    signal_updates = [{
                        "label": self.signal_label_A,
                        "name": self.sig_name_A.get()
                    }, {
                        "label": self.signal_label_Ph,
                        "name": self.sig_name_Ph.get()
                    }]
                )
                self.destroy()
            elif self.signal_label_A == self.signal_label_A_old:
                self.callback(
                    new_value = self.value,
                    signal_updates = [{
                        "label": self.signal_label_A,
                        "name": self.sig_name_A.get()
                    }, {
                        "label": self.signal_label_Ph,
                        "name": self.sig_name_Ph.get()
                    }]
                )
                self.destroy()
            else:
                self.callback(
                    new_value = self.value,
                    signal_updates = [{
                        "label": self.signal_label_A,
                        "name": self.sig_name_A.get()
                    }, {
                        "label": self.signal_label_Ph,
                        "name": self.sig_name_Ph.get()
                    }],
                    condition_vector_add = [{
                        "label": self.signal_label_A,
                        "name": self.sig_name_A.get()
                    }, {
                        "label": self.signal_label_Ph,
                        "name": self.sig_name_Ph.get()
                    }],
                    signal_remove = [{
                        "label": self.signal_label_A_old,
                        "name": self.sig_name_A.get()
                    }, {
                        "label": self.signal_label_Ph_old,
                        "name": self.sig_name_Ph.get()
                    }]
                )
                self.destroy()


    def cancel_event(self):
        self.cancel_callback()
        self.destroy()
    
    def x_button(self):
        self.cancel_callback()
        self.destroy()


class ChannelAnalysisRest(Toplevel):
    
    def __init__(
        self,
        x,
        y,
        init_value,
        signal_label = '',
        signal_name = '',
        callback = None,
        cancel_callback = None
    ):
        Toplevel.__init__(self)
        self.title("Rest:")
        self.value = init_value
        self.signal_label = signal_label
        self.callback = callback
        self.cancel_callback = cancel_callback
        self.protocol('WM_DELETE_WINDOW', self.x_button)
        self.content_frame = Frame(self, border = 5)
        self.sig_name_label = Label(self.content_frame, text = "Signal name:")
        self.sig_name = Entry(self.content_frame)
        self.sig_name.insert(0, signal_name)

        self.ampl_var = BooleanVar()
        if 'param' in self.value:
            if 'amplitude' in self.value['param']:
                self.ampl_var.set(self.value['param']['amplitude'])
            else:
                self.ampl_var.set(True)
        else:
            self.ampl_var.set(True)
        self.ampl = Checkbutton(
            self.content_frame,
            text = "Amplitude",
            variable= self.ampl_var,
            onvalue= True,
            offvalue= False)

        self.p_server_var = BooleanVar()
        if 'performOnServer' in self.value:
            self.p_server_var.set(self.value['performOnServer'])
        self.p_server = Checkbutton(
            self.content_frame,
            text = 'Perform on server',
            variable= self.p_server_var,
            onvalue= True,
            offvalue= False)

        self.buttons_frame = Frame(self.content_frame)
        self.ok_button = Button(
            self.buttons_frame, text='Ok', command = self.ok_event
        )
        self.cancel_button = Button(
            self.buttons_frame, text='Cancel', command = self.cancel_event
        )
        self.content_frame.pack(fill = BOTH, expand = 1)
        self.geometry(f'200x180+{x}+{y}')
        self.resizable(False, False)
        self.sig_name_label.pack(side = TOP, anchor = 'w')
        self.sig_name.pack(side = TOP, fill = X, expand = 1)
        self.ampl.pack(side = TOP, expand = 1, anchor = 'w')
        self.p_server.pack(side = TOP, expand = 1, anchor = 'w')
        self.buttons_frame.pack(side = TOP, fill = X)
        self.ok_button.pack(side = RIGHT, expand = 1)
        self.cancel_button.pack(side = RIGHT, expand = 1)

    #Button command callback method doesn't have event param.
    def ok_event(self):
        if self.callback != None:
            self.value['param']['amplitude'] = self.ampl_var.get()
            self.value['performOnServer'] = self.p_server_var.get()
            self.callback(
                new_value = self.value,
                signal_updates = [{
                    "label": self.signal_label,
                    "name": self.sig_name.get()
                }]
            )
            self.destroy()

    def cancel_event(self):
        self.cancel_callback()
        self.destroy()
    
    def x_button(self):
        self.cancel_callback()
        self.destroy()


class ChannelAnalysisAirGap(Toplevel):
    
    def __init__(
        self,
        x,
        y,
        init_value,
        channel_label = '',
        sensor_name = '',
        reg_pairs = [],
        number_of_poles = 0,
        callback = None,
        cancel_callback = None
    ):
        Toplevel.__init__(self)
        self.title("Air gap:")
        self.value = init_value
        self.channel_label = channel_label
        self.sensor_name = sensor_name
        self.reg_pairs = reg_pairs
        self.number_of_poles = number_of_poles
        self.callback = callback
        self.cancel_callback = cancel_callback
        self.protocol('WM_DELETE_WINDOW', self.x_button)
        self.content_frame = Frame(self, border = 5)
        self.threshold_label = Label(self.content_frame, text = "Threshold:")
        self.threshold = FloatEntry(self.content_frame)
        if 'threshold' in self.value['param']:
            val = self.value['param']['threshold']
            self.threshold.insert(0, val)
        else:
            self.threshold.insert(0, '10')

        self.pole_num_asc_var = BooleanVar()
        self.pole_num_asc = Checkbutton(
            self.content_frame,
            text = "Pole number ascending",
            variable= self.pole_num_asc_var,
            onvalue= True,
            offvalue= False)

        if 'param' in self.value:
            if 'regimeParam' in self.value['param']:
                rp = self.value['param']['regimeParam']
                if len(rp) != 0:
                    if 'poleNumbersAscending' in rp[0]:
                        self.pole_num_asc_var.set(rp[0]['poleNumbersAscending'])
                    else:
                        self.pole_num_asc_var.set(True)
                else:
                    self.pole_num_asc_var.set(True)
            else:
                self.pole_num_asc_var.set(True)    
        else:
            self.pole_num_asc_var.set(True)

        self.first_pole_label = Label(self.content_frame,
            text = "First pole after trigger:")
        self.first_pole = UnsignedIntegerEntry(self.content_frame)

        if 'param' in self.value:
            if 'regimeParam' in self.value['param']:
                rp = self.value['param']['regimeParam']
                if len(rp) != 0:
                    if 'firstPoleAfterTrigger' in rp[0]:
                        self.first_pole.insert(
                            0,
                            rp[0]['firstPoleAfterTrigger']
                        )
                    else:
                        self.first_pole.insert(0, '0')
                else:
                    self.first_pole.insert(0, '0')
            else:
                self.first_pole.insert(0, '0')
        else:
            self.first_pole.insert(0, '0')

        self.regime_picked_label = Label(self.content_frame, text = 'Regime:')
        
        if 'param' in self.value:
            if 'regimeParam' in self.value['param']:
                rp = self.value['param']['regimeParam']
                if len(rp) != 0:
                    if 'regime' in rp[0]:
                        init_name = self.reg_pairs.get_name(rp[0]['regime'])
                    else:
                        init_name = reg_pairs.labels_names[0]['name']
                else:
                    init_name = reg_pairs.labels_names[0]['name']
            else:
                init_name = reg_pairs.labels_names[0]['name']
        else:
            init_name = reg_pairs.labels_names[0]['name']


        self.regime_picked = SelectorCombo(
            self.content_frame,
            pairs = self.reg_pairs,
            init_name = init_name
        )
        self.current_regime_picked = self.regime_picked.get()
        self.regime_picked.bind('<<ComboboxSelected>>', self.regime_picked_event)
        if 'param' in self.value:
            if 'regimeParam' in self.value['param']:
                self.regime_value = self.value['param']['regimeParam']
        if self.regime_value == []:
            for i in self.reg_pairs.labels_names:
                self.regime_value.append({
                    'regime': i['label'],
                    'firstPoleAfterTrigger': 0,
                    'poleNumbersAscending': True
                })
        self.p_server_var = BooleanVar()
        if 'performOnServer' in self.value:
            self.p_server_var.set(self.value['performOnServer'])
        self.p_server = Checkbutton(
            self.content_frame,
            text = 'Perform on server',
            variable= self.p_server_var,
            onvalue= True,
            offvalue= False)

        self.buttons_frame = Frame(self.content_frame)
        self.ok_button = Button(
            self.buttons_frame, text='Ok', command = self.ok_event
        )
        self.cancel_button = Button(
            self.buttons_frame, text='Cancel', command = self.cancel_event
        )

        self.content_frame.pack(fill = BOTH, expand = 1)
        self.geometry(f'260x300+{x}+{y}')
        self.resizable(False, False)
        self.threshold_label.pack(side = TOP, anchor = 'w')
        self.threshold.pack(side = TOP, fill = X, expand = 1)
        self.regime_picked_label.pack(side = TOP, anchor = 'w')
        self.regime_picked.pack(side = TOP, fill = X, expand = 1)
        self.first_pole_label.pack(side = TOP, anchor = 'w')
        self.first_pole.pack(side = TOP, fill = X, expand = 1)
        self.pole_num_asc.pack(side = TOP, expand = 1, anchor = 'w')
        self.p_server.pack(side = TOP, expand = 1, anchor = 'w')
        self.buttons_frame.pack(side = TOP, fill = X)
        self.ok_button.pack(side = RIGHT, expand = 1)
        self.cancel_button.pack(side = RIGHT, expand = 1)

    #Button command callback method doesn't have event param.

    def regime_picked_event(self, event):
        if self.current_regime_picked == self.regime_picked.get():
            pass
        else:
            for i in self.regime_value:
                if i['regime'] == self.current_regime_picked:
                    i['poleNumbersAscending'] = self.pole_num_asc_var.get()
                    i['firstPoleAfterTrigger'] = self.first_pole.get()
            for i in self.value['param']['regimeParam']:
                if i['regime'] == self.regime_picked.get():
                    if 'poleNumbersAscending' in i:
                        self.pole_num_asc_var.set(i['poleNumbersAscending'])
                    if 'firstPoleAfterTrigger' in i:
                        val = i['firstPoleAfterTrigger']
                        self.first_pole.delete(0, 'end')
                        self.first_pole.insert(0, val)
            self.current_regime_picked = self.regime_picked.get()

    def ok_event(self):
        if self.callback != None:
            for i in self.regime_value:
                if i['regime'] == self.current_regime_picked:
                    i['poleNumbersAscending'] = self.pole_num_asc_var.get()
                    i['firstPoleAfterTrigger'] = self.first_pole.get()    
            self.value['param']['regimeParam'] = self.regime_value
            self.value['param']['threshold'] = self.threshold.get()
            self.value['performOnServer'] = self.p_server_var.get()

            signal_updates = []
            self.sensor_name_reduced = ''
            self.measuring_unit = ''
            self.name = self.sensor_name
            for i in range(1, self.number_of_poles+1):
                if i < 10:
                    num = '0'+str(i)
                else:
                    num = str(i)
                label = f'{self.channel_label}.MinPole{num}'
                found = False
                if '[' and ']' in self.name:
                    found = True
                    bracket_start = self.name.find('[')
                    bracket_end = self.name.find(']')+1
                    self.mu = self.name[bracket_start:bracket_end]
                    self.measuring_unit = f' {self.mu}'
                if found:
                    self.sensor_name_reduced = self.name[:bracket_start]
                    name = f'{self.sensor_name_reduced} min pole{num}{self.measuring_unit}'
                else:
                    name = f'{self.name} min pole{num}'
                signal_updates.append({
                    'label': label,
                    'name': name
                })
            if self.sensor_name_reduced != '':
                signal_name = self.sensor_name_reduced
            else:
                signal_name = self.name
            signal_updates.append({
            'label': f'{self.channel_label}.s1.00A',
            'name': f'{signal_name} 1x Ampl{self.measuring_unit}'
            })
            signal_updates.append({
            'label': f'{self.channel_label}.s2.00A',
            'name': f'{signal_name} 2x Ampl{self.measuring_unit}'
            })
            signal_updates.append({
            'label': f'{self.channel_label}.s1.00Ph',
            'name': f'{signal_name} 1x Phase [deg]'
            })
            signal_updates.append({
            'label': f'{self.channel_label}.s2.00Ph',
            'name': f'{signal_name} 2x Phase [deg]'
            })
            signal_updates.append({
            'label': f'{self.channel_label}.DCExtremaMin',
            'name': f'{signal_name} average air gap{self.measuring_unit}'
            })
            signal_updates.append({
            'label': f'{self.channel_label}.MaxExtremaMin',
            'name': f'{signal_name} max air gap{self.measuring_unit}'
            })
            signal_updates.append({
            'label': f'{self.channel_label}.MinExtremaMin',
            'name': f'{signal_name} min air gap{self.measuring_unit}'
            })
            signal_updates.append({
            'label': f'{self.channel_label}.MaxDiffPoleNum',
            'name': f'{signal_name} max diff pole num'
            })
            signal_updates.append({
            'label': f'{self.channel_label}.MaxPoleDiff',
            'name': f'{signal_name} max pole diff{self.measuring_unit}'
            })

            self.callback(
                new_value = self.value,
                signal_updates = signal_updates
            )
            self.destroy()

    def cancel_event(self):
        self.cancel_callback()
        self.destroy()
    
    def x_button(self):
        self.cancel_callback()
        self.destroy()


class ChannelAnalysisRpm(Toplevel):

    def __init__(
        self,
        x,
        y,
        init_value,
        signal_label = '',
        signal_name = '',
        callback = None,
        cancel_callback = None
    ):
        Toplevel.__init__(self)
        self.title('Rotational speed:')
        self.value = init_value
        self.signal_label = signal_label
        self.callback = callback
        self.cancel_callback = cancel_callback
        self.protocol('WM_DELETE_WINDOW', self.x_button)
        self.content_frame = Frame(self, border = 5)
        self.sig_name_label = Label(self.content_frame, text = "Signal name:")
        self.sig_name = Entry(self.content_frame)
        if signal_name != None:
            self.sig_name.insert(0, signal_name)
        else:
            self.sig_name.insert(0, '')
        self.on_rising_var = BooleanVar()
        if 'param' in self.value:
            if 'onRising' in self.value['param']:
                self.on_rising_var.set(self.value['param']['onRising'])
        self.on_rising = Checkbutton(
            self.content_frame,
            text = "On rising pulse",
            variable = self.on_rising_var,
            onvalue = True,
            offvalue = False
        )

        self.pulse_width_label = Label(self.content_frame, text = "Pulse width:")
        self.pulse_width = UnsignedIntegerEntry(self.content_frame)
        self.sig_threshold_label = Label(self.content_frame, text = "Signal threshold:")
        self.sig_threshold = FloatEntry(self.content_frame)
        if 'param' in self.value:
            if 'pulseWidth' in self.value['param']:
                val = self.value['param']['pulseWidth']
                self.pulse_width.insert(0, val)
            else:
                self.pulse_width.insert(0, '0')
            if 'treshold' in self.value['param']:
                val = self.value['param']['treshold']
                self.sig_threshold.insert(0, val)
            else:
                self.sig_threshold.insert(0, '0')

        self.p_server_var = BooleanVar()
        if 'performOnServer' in self.value:
            self.p_server_var.set(self.value['performOnServer'])
        self.p_server = Checkbutton(
            self.content_frame,
            text = 'Perform on server',
            variable= self.p_server_var,
            onvalue= True,
            offvalue= False)

        self.buttons_frame = Frame(self.content_frame)
        self.ok_button = Button(
            self.buttons_frame, text='Ok', command = self.ok_event
        )
        self.cancel_button = Button(
            self.buttons_frame, text='Cancel', command = self.cancel_event
        )
        self.content_frame.pack(fill = BOTH, expand = 1)
        self.geometry(f'270x280+{x}+{y}')
        self.resizable(False, False)
        self.sig_name_label.pack(side = TOP, anchor = 'w')
        self.sig_name.pack(side = TOP, fill = X, expand = 1)
        self.on_rising.pack(side = TOP, expand = 1, anchor = 'w')
        self.pulse_width_label.pack(side = TOP, anchor = 'w')
        self.pulse_width.pack(side = TOP, fill = X, expand = 1)
        self.sig_threshold_label.pack(side = TOP, anchor = 'w')
        self.sig_threshold.pack(side = TOP, fill = X, expand = 1)
        self.p_server.pack(side = TOP, expand = 1, anchor = 'w')
        self.buttons_frame.pack(side = TOP, fill = X)
        self.ok_button.pack(side = RIGHT, expand = 1)
        self.cancel_button.pack(side = RIGHT, expand = 1)

    def ok_event(self):
        if self.callback != None:
            if not 'param' in self.value:
                self.value['param'] = {}  
            self.value['param']['onRising'] = self.on_rising_var.get()
            self.value['param']['pulseWidth'] = self.pulse_width.get()
            self.value['param']['treshold'] = self.sig_threshold.get()
            self.value['performOnServer'] = self.p_server_var.get()
            self.callback(
                new_value = self.value,
                signal_updates = [{
                    "label": self.signal_label,
                    "name": self.sig_name.get()
                }]
            )
            self.destroy()

    def cancel_event(self):
        self.cancel_callback()
        self.destroy()
    
    def x_button(self):
        self.cancel_callback()
        self.destroy()


class UnitAnalysisRpm(Toplevel):

    def __init__(
        self,
        x,
        y,
        init_value,
        ch_pairs,
        signal_label = '',
        signal_name = '',
        callback = None,
        cancel_callback = None
    ):
        Toplevel.__init__(self)
        self.title('Rotational speed:')
        self.value = init_value
        self.signal_label = signal_label
        self.callback = callback
        self.cancel_callback = cancel_callback
        self.protocol('WM_DELETE_WINDOW', self.x_button)
        self.content_frame = Frame(self, border = 5)
        self.sig_name_label = Label(self.content_frame, text = "Signal name:")
        self.sig_name = Entry(self.content_frame)
        if signal_name != None:
            self.sig_name.insert(0, signal_name)
        else:
            self.sig_name.insert(0, '')
        self.m_trigger_label = Label(
            self.content_frame,
            text = "Main trigger sensor:"
        )
        if 'param' in self.value:
            if 'mainTriggerSensor' in self.value['param']:
                m_t = ch_pairs.get_name(self.value['param']['mainTriggerSensor'])
            else:
                m_t=''
            if m_t == None:
                m_t = ''
        self.m_trigger = SelectorCombo(
            self.content_frame,
            pairs = ch_pairs,
            init_name = m_t
        )
        self.on_rising_var = BooleanVar()
        if 'param' in self.value:
            if 'onRising' in self.value['param']:
                self.on_rising_var.set(self.value['param']['onRising'])
        self.on_rising = Checkbutton(
            self.content_frame,
            text = "On rising pulse",
            variable = self.on_rising_var,
            onvalue = True,
            offvalue = False
        )

        self.pulse_width_label = Label(self.content_frame, text = "Pulse width:")
        self.pulse_width = UnsignedIntegerEntry(self.content_frame)
        self.sig_threshold_label = Label(self.content_frame, text = "Signal threshold:")
        self.sig_threshold = FloatEntry(self.content_frame)
        if 'param' in self.value:
            if 'pulseWidth' in self.value['param']:
                val = self.value['param']['pulseWidth']
                self.pulse_width.insert(0, val)
            else:
                self.pulse_width.insert(0, '0')
            if 'treshold' in self.value['param']:
                val = self.value['param']['treshold']
                self.sig_threshold.insert(0, val)
            else:
                self.sig_threshold.insert(0, '0')

        self.p_server_var = BooleanVar()
        if 'performOnServer' in self.value:
            self.p_server_var.set(self.value['performOnServer'])
        self.p_server = Checkbutton(
            self.content_frame,
            text = 'Perform on server',
            variable= self.p_server_var,
            onvalue= True,
            offvalue= False)

        self.buttons_frame = Frame(self.content_frame)
        self.ok_button = Button(
            self.buttons_frame, text='Ok', command = self.ok_event
        )
        self.cancel_button = Button(
            self.buttons_frame, text='Cancel', command = self.cancel_event
        )
        self.content_frame.pack(fill = BOTH, expand = 1)
        self.geometry(f'270x300+{x}+{y}')
        self.resizable(False, False)
        self.sig_name_label.pack(side = TOP, anchor = 'w')
        self.sig_name.pack(side = TOP, fill = X, expand = 1)
        self.m_trigger_label.pack(side = TOP, anchor = 'w')
        self.m_trigger.pack(side = TOP, fill = X, expand = 1)
        self.on_rising.pack(side = TOP, expand = 1, anchor = 'w')
        self.pulse_width_label.pack(side = TOP, anchor = 'w')
        self.pulse_width.pack(side = TOP, fill = X, expand = 1)
        self.sig_threshold_label.pack(side = TOP, anchor = 'w')
        self.sig_threshold.pack(side = TOP, fill = X, expand = 1)
        self.p_server.pack(side = TOP, expand = 1, anchor = 'w')
        self.buttons_frame.pack(side = TOP, fill = X)
        self.ok_button.pack(side = RIGHT, expand = 1)
        self.cancel_button.pack(side = RIGHT, expand = 1)

    def ok_event(self):
        if self.callback != None:
            if not 'param' in self.value:
                self.value['param'] = {}
            self.value['param']['mainTriggerSensor'] = self.m_trigger.get()    
            self.value['param']['onRising'] = self.on_rising_var.get()
            self.value['param']['pulseWidth'] = self.pulse_width.get()
            self.value['param']['treshold'] = self.sig_threshold.get()
            self.value['performOnServer'] = self.p_server_var.get()
            self.callback(
                new_value = self.value,
                signal_updates = [{
                    "label": self.signal_label,
                    "name": self.sig_name.get()
                }]
            )
            self.destroy()

    def cancel_event(self):
        self.cancel_callback()
        self.destroy()
    
    def x_button(self):
        self.cancel_callback()
        self.destroy()


class UnitAnalysisPowers(Toplevel):

    def __init__(
        self,
        x,
        y,
        init_value,
        ch_pairs,
        signal_label_act = '',
        signal_name_act = '',
        signal_label_react = '',
        signal_name_react = '',
        callback = None,
        cancel_callback = None
    ):
        #-----------------------------------------------------------
        #init_value: string
        #ch_pairs: object of Label_name_pairs class
        #-----------------------------------------------------------
        Toplevel.__init__(self)
        self.title("Act&React Powers:")
        self.value = init_value
        self.signal_label_act = signal_label_act
        self.signal_label_react = signal_label_react
        self.callback = callback
        self.cancel_callback = cancel_callback
        self.protocol('WM_DELETE_WINDOW', self.x_button)
        self.content_frame = Frame(self, borderwidth = 5)
        self.sig_name_act_label = Label(
            self.content_frame,
            text = "Signal name active power:"
        )
        self.sig_name_act = Entry(self.content_frame)
        self.sig_name_act.insert(0, signal_name_act)
        self.sig_name_react_label = Label(
            self.content_frame,
            text = "Signal name reactive power:"
        )
        self.sig_name_react = Entry(self.content_frame)
        self.sig_name_react.insert(0, signal_name_react)

        self.electric_param_frame = Frame(self.content_frame, borderwidth = 5)
        self.voltage_frame = Frame(self.electric_param_frame, borderwidth = 5)
        self.r_voltage_label = Label(
            self.voltage_frame,
            text = "R voltage:"
        )
        if 'param' in self.value:
            if 'voltageSensors' in init_value['param']:
                r_voltage = ch_pairs.get_name(init_value['param']['voltageSensors'][0])
                if r_voltage == None:
                    r_voltage = ''
            else:
                r_voltage = ''
        self.r_voltage = SelectorCombo(
            self.voltage_frame,
            pairs = ch_pairs,
            init_name = r_voltage
        )
        self.s_voltage_label = Label(
            self.voltage_frame,
            text = "S voltage:"
        )
        if 'param' in self.value:
            if 'voltageSensors' in init_value['param']:
                s_voltage = ch_pairs.get_name(init_value['param']['voltageSensors'][1])
                if s_voltage == None:
                    s_voltage = ''
            else:
                s_voltage = ''
        self.s_voltage = SelectorCombo(
            self.voltage_frame,
            pairs = ch_pairs,
            init_name = s_voltage
        )
        self.t_voltage_label = Label(
            self.voltage_frame,
            text = "T voltage:"
        )
        if 'param' in self.value:
            if 'voltageSensors' in init_value['param']:
                t_voltage = ch_pairs.get_name(init_value['param']['voltageSensors'][2])
                if t_voltage == None:
                    t_voltage = ''
            else:
                t_voltage = ''
        self.t_voltage = SelectorCombo(
            self.voltage_frame,
            pairs = ch_pairs,
            init_name = t_voltage
        )
        self.current_frame = Frame(self.electric_param_frame, borderwidth = 5)
        self.r_current_label = Label(
            self.current_frame,
            text = "R current:"
        )
        if 'param' in self.value:
            if 'currentSensors' in init_value['param']:
                r_current = ch_pairs.get_name(init_value['param']['currentSensors'][0])
                if r_current == None:
                    r_current = ''
            else:
                r_current = ''
        self.r_current = SelectorCombo(
            self.current_frame,
            pairs = ch_pairs,
            init_name = r_current
        )
        self.s_current_label = Label(
            self.current_frame,
            text = "S current:"
        )
        if 'param' in self.value:
            if 'currentSensors' in init_value['param']:
                s_current = ch_pairs.get_name(init_value['param']['currentSensors'][1])
                if s_current == None:
                    s_current = ''
            else:
                s_current = ''
        self.s_current = SelectorCombo(
            self.current_frame,
            pairs = ch_pairs,
            init_name = s_current
        )
        self.t_current_label = Label(
            self.current_frame,
            text = "T current:"
        )
        if 'param' in self.value:
            if 'currentSensors' in init_value['param']:
                t_current = ch_pairs.get_name(init_value['param']['currentSensors'][2])
                if t_current == None:
                    t_current = ''
            else:
                t_current = ''
        self.t_current = SelectorCombo(
            self.current_frame,
            pairs = ch_pairs,
            init_name = t_current
        )
        self.line_var = BooleanVar()
        if 'param' in self.value:
            if 'lineVoltage' in self.value['param']:
                self.line_var.set(self.value['param']['lineVoltage'])
            else:
                self.line_var.set(False)
        self.line = Checkbutton(
            self.content_frame,
            text = 'Line voltage:',
            variable= self.line_var,
            onvalue= True,
            offvalue= False)

        self.p_server_var = BooleanVar()
        if 'performOnServer' in self.value:
            self.p_server_var.set(self.value['performOnServer'])
        self.p_server = Checkbutton(
            self.content_frame,
            text = 'Perform on server',
            variable= self.p_server_var,
            onvalue= True,
            offvalue= False)

        self.buttons_frame = Frame(self.content_frame)
        self.ok_button = Button(
            self.buttons_frame, text='Ok', command = self.ok_event
        )
        self.cancel_button = Button(
            self.buttons_frame, text='Cancel', command = self.cancel_event
        )
        self.content_frame.pack(fill = BOTH, expand = 1)
        self.geometry(f'400x340+{x}+{y}')
        self.resizable(False, False)
        self.sig_name_act_label.pack(side = TOP, anchor = 'w')
        self.sig_name_act.pack(side = TOP, fill = X, expand = 1)
        self.sig_name_react_label.pack(side = TOP, anchor = 'w')
        self.sig_name_react.pack(side = TOP, fill = X, expand = 1)
        self.electric_param_frame.pack(side = TOP, fill = X, expand = 1)
        self.voltage_frame.pack(side = LEFT, fill = X, expand = 1)
        self.current_frame.pack(side = LEFT, fill = X, expand = 1)
        self.r_voltage_label.pack(side = TOP, anchor = 'w')
        self.r_voltage.pack(side = TOP, fill = X, expand = 1)
        self.s_voltage_label.pack(side = TOP, anchor = 'w')
        self.s_voltage.pack(side = TOP, fill = X, expand = 1)
        self.t_voltage_label.pack(side = TOP, anchor = 'w')
        self.t_voltage.pack(side = TOP, fill = X, expand = 1)
        self.r_current_label.pack(side = TOP, anchor = 'w')
        self.r_current.pack(side = TOP, fill = X, expand = 1)
        self.s_current_label.pack(side = TOP, anchor = 'w')
        self.s_current.pack(side = TOP, fill = X, expand = 1)
        self.t_current_label.pack(side = TOP, anchor = 'w')
        self.t_current.pack(side = TOP, fill = X, expand = 1)
        self.line.pack(side = TOP, expand = 1, anchor = 'w')
        self.p_server.pack(side = TOP, expand = 1, anchor = 'w')   
        self.buttons_frame.pack(side = TOP, fill = X)
        self.ok_button.pack(side = RIGHT, expand = 1)
        self.cancel_button.pack(side = RIGHT, expand = 1)

    def call_callback(self):
        if self.callback != None:
            self.value['param']['voltageSensors'][0] = self.r_voltage.get()
            self.value['param']['voltageSensors'][1] = self.s_voltage.get()
            self.value['param']['voltageSensors'][2] = self.t_voltage.get()
            self.value['param']['currentSensors'][0] = self.r_current.get()
            self.value['param']['currentSensors'][1] = self.s_current.get()
            self.value['param']['currentSensors'][2] = self.t_current.get()
            self.value['param']['lineVoltage'] = self.line_var.get()
            self.value['performOnServer'] = self.p_server_var.get()
            self.callback(
                new_value = self.value,
                signal_updates = [
                    {
                        "label": self.signal_label_act,
                        "name": self.sig_name_act.get()
                    },
                    {
                        "label": self.signal_label_react,
                        "name": self.sig_name_react.get()
                    }
                ]
            )

    #Button command callback method doesn't have event param.
    def ok_event(self):
        self.call_callback()
        self.destroy()
            
    def return_pressed(self, e):
        self.call_callback()
        self.destroy()

    def cancel_event(self):
        self.cancel_callback()
        self.destroy()
    
    def x_button(self):
        self.cancel_callback()
        self.destroy()


class ModbusSentInterface(Toplevel):
    def __init__(
        self,
        x,
        y,
        init_value,
        sig_pairs = [],
        callback = None,
        cancel_callback = None,
        labels = []
    ):
        Toplevel.__init__(self)
        self.title('Sent to modbus:')
        self.value = init_value
        self.sig_pairs = sig_pairs
        self.callback = callback
        self.cancel_callback = cancel_callback
        self.labels = labels
        self.protocol('WM_DELETE_WINDOW', self.x_button)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.content_frame = Frame(self, border = 5)
        self.content_frame.grid(sticky = NSEW)
        #create a frame for the canvas with non-zero row&column weights
        self.signals_table_frame = Frame(self.content_frame)
        self.signals_table_frame.grid(row = 0, column = 0, pady = (5, 15), sticky = NW)
        self.signals_table_frame.grid_rowconfigure(0, weight=1)
        self.signals_table_frame.grid_columnconfigure(0, weight=1)
        # Set grid_propagate to False to allow resizing later
        self.signals_table_frame.grid_propagate(False)
        
        if 'labels' in self.value:
            if len(self.value['labels']) == 0:
                self.signals = [['', 'floatLoHi', 1]]
            else:
                self.signals = []
                for i in range(len(self.value['labels'])):
                    self.signals.append([
                        self.value['labels'][i],
                        self.value['dataTypes'][i],
                        self.value['scaleFactors'][i]
                    ])
        else:
            self.signals = [['', 'floatLoHi', 1]]
        self.fill_signals_table()

        self.register_type_label = Label(
            self.content_frame,
            text = 'Register type:'
        )
        if 'registerType' in self.value:
            init_register_type = self.value['registerType']
        else:
            init_register_type = 'holdingRegisters'
        self.register_type = SelectorCombo(
            self.content_frame,
            pairs = REGISTER_TYPE_LABEL_NAME_PAIRS,
            init_name = init_register_type
        )

        self.address_label = Label(
            self.content_frame,
            text = 'Adress:'
        )
        self.address = Unsigned16bitIntegerEntry(self.content_frame)
        if 'address' in self.value:
            val = self.value['address']
            self.address.insert(0, val)
        else:
            self.address.insert(0, 16000)

        self.buttons_frame = Frame(self.content_frame)
        self.ok_button = Button(
            self.buttons_frame, text='Ok', command = self.ok_event
        )
        self.cancel_button = Button(
            self.buttons_frame, text='Cancel', command = self.cancel_event
        )

        self.geometry(f'500x500+{x}+{y}')
        self.resizable(False, False)
        self.register_type_label.grid(row = 2, column = 0, pady = (0,0), sticky = W)
        self.register_type.grid(row = 3, column = 0, pady = (0,0), sticky = W)
        self.address_label.grid(row = 4, column = 0, pady = (0,0), sticky = W)
        self.address.grid(row = 5, column = 0, pady = (0,0), sticky = W)
        self.buttons_frame.grid(row = 6, column = 0, pady = (15,15), sticky = EW)
        self.ok_button.pack(side = RIGHT, expand = 1)
        self.cancel_button.pack(side = RIGHT, expand = 1)


    def call_callback(self):
        self.value['registerType'] = self.register_type.get()
        self.value['address'] = self.address.get()
        self.callback(
            new_value = self.value,
            regime_updates = [{
                "label": self.value['label'],
                "name": self.regime_name.get()
            }]
        )

    def ok_event(self):
        self.value['labels'] = []
        self.value['dataTypes'] = []
        self.value['scaleFactors'] = []
        wrong_signals = []
        i = 0
        for row in self.signals_entry:
            j = 0
            for col in row:
                if j == 0:
                    self.value['labels'].append(self.replace_name_with_label(col.get()))
                    if self.value['labels'][i] == None:
                        wrong_signals.append(col.get())
                elif j == 1:
                    self.value['dataTypes'].append(col.get())
                else:
                    self.value['scaleFactors'].append(col.get())
                j += 1
            i += 1
        if None in self.value['labels']:
            messagebox.showinfo("Error:", f"Signals {wrong_signals} could not be found in database.")
        else:
            self.call_callback()
            self.destroy()
            
    def return_pressed(self, e):
        self.call_callback()
        return 'break'

    def cancel_event(self):
        self.cancel_callback()
        self.destroy()
    
    def x_button(self):
        self.cancel_callback()
        self.destroy()

    def replace_name_with_label(self, name):
        for i in self.sig_pairs:
            if i['name'] == name:
                return i['label']

    def add_new(self):
        self.signals.append(['', 'floatLoHi', 1])
        if len(self.signals) == 1:
            for widget in self.signals_table_frame.winfo_children():
                widget.destroy()

            self.fill_signals_table()
        else:
            cols = []
            for j in range(4):
                if j < 2:
                    e = Entry(self.frame_signals, relief = GROOVE)
                elif j == 2:
                    e = Unsigned16bitIntegerEntry(self.frame_signals, relief = GROOVE)
                else:
                    e = Button(
                        self.frame_signals, text = 'Delete', command = self.remove_signal
                    )
                    e.grid(row = len(self.signals), column = j, sticky = NSEW)
                if j < 3:
                    e.grid(row = len(self.signals), column = j, sticky = NSEW)
                    e.insert(0, self.signals[-1][j])
                    cols.append(e)
            self.signals_entry.append(cols)
            self.add_button.grid(row = len(self.signals)+1, column = 0, sticky = NSEW)
            self.frame_signals.update_idletasks()
            self.signals_table_canvas.config(scrollregion = self.signals_table_canvas.bbox("all"))

    def remove_signal(self):
        c, r = self.signals_table_frame.grid_location(
            x = self.winfo_pointerx() - self.signals_table_frame.winfo_rootx(),
            y = self.winfo_pointery() - self.signals_table_frame.winfo_rooty()
        )
        self.signals.pop(r-1)
        self.signals_entry.pop(r-1)
        i = 0
        for row in self.signals_entry:
            j = 0
            for col in row:
                self.signals[i][j] = col.get()
                j += 1
            i += 1
        for widget in self.signals_table_frame.winfo_children():
            widget.destroy()

        self.fill_signals_table()

    def fill_signals_table(self):
        # Add a canvas in the signal table frame
        self.signals_table_canvas = Canvas(self.signals_table_frame)
        self.signals_table_canvas.grid(row = 0, column = 0, sticky = NSEW)

        self.yscrollbar = Scrollbar(self.signals_table_frame,orient = VERTICAL, command = self.signals_table_canvas.yview)
        self.yscrollbar.grid(row = 0, column = 1, sticky = NS)
        self.signals_table_canvas.configure(yscrollcommand = self.yscrollbar.set)

        self.frame_signals = Frame(self.signals_table_canvas)
        self.signals_table_canvas.create_window((0,0), window = self.frame_signals, anchor = NW)
        
        self.signal_name_label = Label(self.frame_signals, text = 'Signal name:')
        self.signal_type_label = Label(self.frame_signals, text = 'Data type:')
        self.signal_scale_factor_label = Label(self.frame_signals, text = 'Scale factor:')
        self.signal_name_label.grid(row = 0, column = 0, sticky = NSEW)
        self.signal_type_label.grid(row = 0, column = 1, sticky = NSEW)
        self.signal_scale_factor_label.grid(row = 0, column = 2, sticky = NSEW)
        self.signals_entry = []
        for i in range(1, len(self.signals)+1):
            cols = []
            for j in range(4):
                if j == 0:
                    e = AutocompleteEntry(self.labels, self.frame_signals, relief = GROOVE)
                elif j == 1:
                    init_label = self.signals[i-1][j]
                    for k in MODBUS_DATA_TYPE_LABEL_NAME_PAIRS:
                        if k['label'] == init_label:
                            init_name = k['name']
                    e = SelectorCombo(
                        self.frame_signals,
                        pairs = MODBUS_DATA_TYPE_LABEL_NAME_PAIRS,
                        init_name = init_name
                    )
                    e.grid(row = i, column = j, sticky = NSEW)
                    cols.append(e)
                elif j == 2:
                    e = Unsigned16bitIntegerEntry(self.frame_signals, relief = GROOVE)
                else:
                    e = Button(
                        self.frame_signals, text = 'Delete', command = self.remove_signal
                    )
                    e.grid(row = i, column = j, sticky = NSEW)
                    self.delete_button_width = e.winfo_width()
                if j == 0 or j == 2:
                    e.grid(row = i, column = j, sticky = NSEW)
                    e.insert(0, self.signals[i-1][j])
                    cols.append(e)
            self.signals_entry.append(cols)
        self.add_button = Button(
            self.frame_signals, text='Add new', command = self.add_new
        )
        self.add_button.grid(row = len(self.signals_entry)+2, column = 0, sticky = NSEW)
        self.frame_signals.update_idletasks()
        self.column_width = self.signal_name_label.winfo_width()*3 + 84
        self.column_height = self.signal_name_label.winfo_height()*15
        self.signals_table_frame.config(width = self.column_width, height = self.column_height)
        self.signals_table_canvas.config(scrollregion = self.signals_table_canvas.bbox("all"))


class Progress(Toplevel):


    def __init__(
        self,
        cancel_callback,
        title = '',
    ):
        Toplevel.__init__(self)
        self.cancel_callback = cancel_callback
        self.title(title)
        self.protocol('WM_DELETE_WINDOW', self.x_button)
        self.content_frame = Frame(self, borderwidth = 0)
        
        self.pb = Progressbar(
            self.content_frame,
            orient = 'horizontal',
            mode = 'determinate',
            length = 280
        )

        self.value_label = Label(
            self.content_frame,
            text = self.update_progress_label()
        )

        self.text_label = Label(
            self.content_frame,
            text = self.update_text_progress_label()
        )

        self.cancel_button = Button(
            self.content_frame,
            text = 'Cancel',
            command = self.cancel
        )

        self.geometry('300x110')
        self.center(self.master, self)
        self.resizable(False, False)
        self.content_frame.pack(fill = BOTH, expand = 1)
        self.pb.grid(column=0, row=1, columnspan=2, padx=10, pady=2)
        self.value_label.grid(column=0, row=0, columnspan=2, pady=2)
        self.text_label.grid(column=0, row=2, columnspan=2, pady=2)
        self.cancel_button.grid(column=0, row=3, columnspan=2, pady=2)
        #self.update()
    
    def set_num_iteration(self, num_iteration):
        self.iteration = 100/num_iteration
        
    def update_progress_label(self):
        return f"Current Progress: {round(self.pb['value'])}%"

    def update_text_progress_label(self, text_progress = ''):
        if self.pb['value'] == 0:
            return 'Getting system settings...'
        return f'{text_progress}'

    def progress(self, text_progress = ''):
        if round(self.pb['value']) < 100:
            self.pb['value'] += self.iteration
            self.value_label['text'] = self.update_progress_label()
            self.text_label['text'] = self.update_text_progress_label(text_progress)
        else:
            self.destroy()
    
    def cancel(self):
        self.cancel_callback()
        self.destroy()

    def x_button(self):
        self.cancel_callback()
        self.destroy()

    def center(self, win, top):
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
        top.update_idletasks()
        width = top.winfo_width()
        frm_width = top.winfo_rootx() - top.winfo_x()
        top_width = width + 2 * frm_width
        height = top.winfo_height()
        titlebar_height = top.winfo_rooty() - top.winfo_y()
        top_height = height + titlebar_height + frm_width
        x = win_width // 2 - top_width // 2
        y = win_height // 2 - top_height // 2
        x += win.winfo_x()
        y += win.winfo_y()
        top.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        win.deiconify()
        top.deiconify()


class ProgressUpload(Toplevel):


    def __init__(
        self,
        num_iteration = 0,
        title = ''
    ):
        Toplevel.__init__(self)
        self.title(title)
        self.protocol('WM_DELETE_WINDOW', self.x_button)
        self.content_frame = Frame(self, borderwidth = 0)
        self.num_iteration = num_iteration
        self.iteration = 100/self.num_iteration
        
        self.pb = Progressbar(
            self.content_frame,
            orient = 'horizontal',
            mode = 'determinate',
            length = 280
        )

        self.value_label = Label(
            self.content_frame,
            text = self.update_progress_label()
        )

        self.text_label = Label(
            self.content_frame,
            text = self.update_text_progress_label()
        )

        self.geometry('300x90')
        self.center(self.master, self)
        self.resizable(False, False)
        self.content_frame.pack(fill = BOTH, expand = 1)
        self.pb.grid(column=0, row=1, columnspan=2, padx=10, pady=2)
        self.value_label.grid(column=0, row=0, columnspan=2, pady=2)
        self.text_label.grid(column=0, row=2, columnspan=2, pady=2)
        self.update()
        
    def update_progress_label(self):
        return f"Current Progress: {round(self.pb['value'])}%"

    def update_text_progress_label(self, text_progress = ''):
        if self.pb['value'] == 0:
            return 'Getting system settings...'
        return f'{text_progress}'

    def progress(self, text_progress = ''):
        if round(self.pb['value']) < 100:
            self.pb['value'] += self.iteration
            self.value_label['text'] = self.update_progress_label()
            self.text_label['text'] = self.update_text_progress_label(text_progress)
            self.update()
        else:
            self.destroy()

    def x_button(self):
        self.destroy()

    def center(self, win, top):
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
        top.update_idletasks()
        width = top.winfo_width()
        frm_width = top.winfo_rootx() - top.winfo_x()
        top_width = width + 2 * frm_width
        height = top.winfo_height()
        titlebar_height = top.winfo_rooty() - top.winfo_y()
        top_height = height + titlebar_height + frm_width
        x = win_width // 2 - top_width // 2
        y = win_height // 2 - top_height // 2
        x += win.winfo_x()
        y += win.winfo_y()
        top.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        win.deiconify()
        top.deiconify()


class IpFrame(Frame):


    def __init__(
        self,
        master_frame
    ):
        Frame.__init__(self, master_frame, bg = 'white', highlightthickness=1)
        self.config(highlightbackground = "grey", highlightcolor= "grey")
        self.ip1 = IpIntegerEntry(self, width = 3, borderwidth = 0, justify = CENTER)
        self.ip2 = IpIntegerEntry(self, width = 3, borderwidth = 0, justify = CENTER)
        self.ip3 = IpIntegerEntry(self, width = 3, borderwidth = 0, justify = CENTER)
        self.ip4 = IpIntegerEntry(self, width = 3, borderwidth = 0, justify = CENTER)
        self.ip_dot1 = Label(self, text = '.', borderwidth = 0, bg = 'white')
        self.ip_dot2 = Label(self, text = '.', borderwidth = 0, bg = 'white')
        self.ip_dot3 = Label(self, text = '.', borderwidth = 0, bg = 'white')
        self.ip1.pack(side = LEFT)
        self.ip_dot1.pack(side = LEFT)
        self.ip2.pack(side = LEFT)
        self.ip_dot2.pack(side = LEFT)
        self.ip3.pack(side = LEFT)
        self.ip_dot3.pack(side = LEFT)
        self.ip4.pack(side = LEFT)
    
    def get(self):
        return f'{self.ip1.get()}.{self.ip2.get()}.{self.ip3.get()}.{self.ip4.get()}'

             


if __name__ == '__main__':
    # window=Tk()
    # #i = TempJsonEditor(init_value = {"Poruka":"Dobar dan"})
    # i1 = {
    #         "param": {
    #             "averagePerRevolution": False,
    #             "filterParam":{
    #                 "f1":0,
    #                 "f2":0,
    #                 "filter": False,
    #                 "order":0,
    #                 "type":"Lowpass"
    #             },
    #             "glide": False,
    #             "labelAddition":"",
    #             "numOfPoints":0,
    #             "substractDc": False,
    #             "triggerToTrigger": False
    #         },
    #         "performOnServer": False,
    #         "analysis": "rms"
    #     }
    # i2 = {
    #         "performOnServer": False,
    #         "analysis": "rms"
    #     }
    # i = ChannelAnalysisRms(
    #     x = 100,
    #     y = 100,
    #     init_value = i2,
    #     signal_name = "AV UGB X [mm/s]"    
    # )
    # #i = UnsignedIntegerInterface(title = 'Physical channel:')
    # window.title('Hello Python')
    # window.geometry("300x200+10+20")
    # window.mainloop()

    window=Tk()
    init_value = {
            'dataSource': 'value',
            'labels': ['label1', 'label2', 'label3'],
            'dataTypes': ['floatLoHi','floatLoHi','floatLoHi'],
            'scaleFactors': [int(1),int(2),int(3)],
            'registerType': 'holdingRegisters',
            'adress': 16000
        }
    ModbusSentInterface(
            init_value = init_value,
            sig_pairs = None,
            callback = None,
            cancel_callback = None,
            x = None,
            y = None
        )



    window.title('Hello Python')
    window.geometry("300x200+10+20")
    window.mainloop()