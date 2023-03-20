from requests import get, codes
from modules.codis_enums import Unit, Source, UnitAnalyses
from modules.tree_items import Item, ItemType
from modules.label_name_pairs import TableType
from tkinter import TclError
from json import load
from threading import Thread
from modules.label_name_pairs import Label_name_pairs, TableType

class LoadingProcess(Thread):


    def __init__(
        self,
        ip,
        load_settings_process_ok,
        load_settings_process_failed,
        set_num_iteration,
        update_interface,
        canceled
    ):
        Thread.__init__(
            self,
            target = self.load_settings,
            kwargs = {
                'ip': ip,
                'load_settings_process_ok': load_settings_process_ok,
                'load_settings_process_failed': load_settings_process_failed,
                'set_num_iteration': set_num_iteration,
                'update_interface': update_interface,
                'canceled': canceled
            }
        )
        self.tables = []
        self.start()

    def load_system_settings(self, ip):
        #Function returns True for successful completion
        # of loading system settings.
        system_settings = {}
        try:
            r = get(f'http://{ip}:8002/CoDiS_Live_Data/System_Settings')
        except:
            return False, system_settings
        else:
            if r.status_code==codes.ok:
                system_settings = r.json()
                return True, system_settings
            else:
                return False, system_settings


    def load_main_cluster(self, ip):
        #Function returns True for successful completion
        # of loading system settings.
        main_cluster = []
        try:
            r = get(f'http://{ip}:8002/CoDiS_Live_Data/Main_Cluster_Settings')
        except:
            return False, main_cluster
        else:
            if r.status_code==codes.ok:
                main_cluster = r.json()
                return True, main_cluster
            else:
                return False, main_cluster

    def load_tsensor_table(self, ip, dBaseName):
        #Function returns True for successful completion
        # of loading tsensor table from a dBase.
        labels_names = []
        try:
            r = get(f'http://{ip}:8002/CoDiS_Live_Data/Get_tsensor',
                params = {'dBaseName': dBaseName}
            )
        except:
            return False, labels_names
        else:
            if r.status_code==codes.ok:
                labels_names = r.json()
                return True, labels_names
            else:
                return False, labels_names

    def load_tsignal_table(self, ip, dBaseName):
        #Function returns True for successful completion
        # of loading tsensor table from a dBase.
        labels_names = []
        try:
            r = get(f'http://{ip}:8002/CoDiS_Live_Data/Get_tsignal',
                params = {'dBaseName': dBaseName}
            )
        except:
            return False, labels_names
        else:
            if r.status_code==codes.ok:
                labels_names = r.json()
                return True, labels_names
            else:
                return False, labels_names

    def load_tbearing_table(self, ip, dBaseName):
        #Function returns True for successful completion
        # of loading tbearing table from a dBase.
        labels_names = []
        try:
            r = get(f'http://{ip}:8002/CoDiS_Live_Data/Get_tbearing',
                params = {'dBaseName': dBaseName}
            )
        except:
            return False, labels_names
        else:
            if r.status_code==codes.ok:
                labels_names = r.json()
                return True, labels_names
            else:
                return False, labels_names

    def load_tregime_table(self, ip, dBaseName):
        #Function returns True for successful completion
        # of loading tregime table from a dBase.
        labels_names = []
        try:
            r = get(f'http://{ip}:8002/CoDiS_Live_Data/Get_operating_regime',
                params = {'dBaseName': dBaseName}
            )
        except:
            return False, labels_names
        else:
            if r.status_code==codes.ok:
                labels_names = r.json()
                return True, labels_names
            else:
                return False, labels_names

    def load_air_gap_plane_table(self, ip, dBaseName):
        #Function returns True for successful completion
        # of loading air gap plane table from a dBase.
        labels_names = []
        try:
            r = get(f'http://{ip}:8002/CoDiS_Live_Data/Get_air_gap_plane',
                params = {'dBaseName': dBaseName}
            )
        except:
            return False, labels_names
        else:
            if r.status_code==codes.ok:
                labels_names = r.json()
                return True, labels_names
            else:
                return False, labels_names

    def load_settings(
            self,
            ip,
            load_settings_process_ok,
            load_settings_process_failed,
            set_num_iteration,
            update_interface,
            canceled
    ):
        ss_loading_ok, system_settings = self.load_system_settings(ip)
        if not ss_loading_ok:
            print("Get system settings request failed.")
            load_settings_process_failed(self.name)
            return
        if canceled(self.name): return
        num_iteration = 1 + len(system_settings['dBaseSettingsList'])*5
        try:
            set_num_iteration(num_iteration)
        except TclError:
            print("Progress interface was destroyed before!")
        try:
            #In case Progress window was destroyed exception is thrown.
            update_interface('Loading main cluster...')
        except TclError:
            print("Progress interface was destroyed before!")
        mc_loading_ok, main_cluster = self.load_main_cluster(ip)
        if not mc_loading_ok:
            print("Get main cluster request failed.")
            load_settings_process_failed(self.name)
            return
        for i in system_settings['dBaseSettingsList']:
            unit = i['unitName']
            if canceled(self.name): return
            try:
                update_interface(f'Loading tsensor table for {unit}...')
            except TclError:
                print("Progress interface was destroyed before!")
            req_ok, labels_names = self.load_tsensor_table(
                ip,
                i['dBaseName']
            )
            if not req_ok:
                print("dBase sensor labels-names request failed.")
                load_settings_process_failed(self.name)
                return
            self.append_table(
                    unit = Unit.get_unit(i['unitName']),
                    labels_names = labels_names,
                    table_type = TableType.SENSORS
            )
            if canceled(self.name): return
            try:
                update_interface(f'Loading tsignal table for {unit}...')
            except TclError:
                print("Progress interface was destroyed before!")
            req_ok, labels_names = self.load_tsignal_table(
                ip,
                i['dBaseName']
            )
            if not req_ok:
                print("dBase signal labels-names request failed.")
                load_settings_process_failed(self.name)
                return
            self.append_table(
                    unit = Unit.get_unit(i['unitName']),
                    labels_names = labels_names,
                    table_type = TableType.SIGNALS
            )
            if canceled(self.name): return
            try:
                update_interface(f'Loading tbearing table for {unit}...')
            except TclError:
                print("Progress interface was destroyed before!")
            req_ok, labels_names = self.load_tbearing_table(
                ip,
                i['dBaseName']
            )
            if not req_ok:
                print("dBase bearings labels-names request failed.")
                load_settings_process_failed(self.name)
                return
            self.append_table(
                    unit = Unit.get_unit(i['unitName']),
                    labels_names = labels_names,
                    table_type = TableType.BEARINGS
            )
            if canceled(self.name): return
            try:
                update_interface(f'Loading tregime table for {unit}...')
            except TclError:
                print("Progress interface was destroyed before!")
            req_ok, labels_names = self.load_tregime_table(
                ip,
                i['dBaseName']
            )
            if not req_ok:
                print("dBase regimes labels-names request failed.")
                load_settings_process_failed(self.name)
                return
            self.append_table(
                    unit = Unit.get_unit(i['unitName']),
                    labels_names = labels_names,
                    table_type = TableType.REGIMES
            )
            if canceled(self.name): return
            try:
                update_interface(f'Loading air gap plane table for {unit}...')
            except TclError:
                print("Progress interface was destroyed before!")
            req_ok, labels_names = self.load_air_gap_plane_table(
                ip,
                i['dBaseName']
            )
            if not req_ok:
                print("dBase air gap planes labels-names request failed.")
                load_settings_process_failed(self.name)
                return
            self.append_table(
                    unit = Unit.get_unit(i['unitName']),
                    labels_names = labels_names,
                    table_type = TableType.AIR_GAP_PLANES
            )
        if canceled(self.name): return
        try:
            update_interface()
        except TclError:
            print("Progress interface was destroyed before!")
        load_settings_process_ok(
            system_settings = system_settings,
            main_cluster = main_cluster,
            tables = self.tables
        )
        return

    def append_table(self, unit, labels_names, table_type):
        self.tables.append(Label_name_pairs(labels_names, unit, table_type))


class OpenProcess(Thread):


    def __init__(
        self,
        load_settings_process_ok,
        load_settings_process_failed,
        set_num_iteration,
        update_interface,
        canceled,
        folder_name
    ):
        Thread.__init__(
            self,
            target = self.open_settings,
            kwargs = {
                'folder_name': folder_name,
                'load_settings_process_ok': load_settings_process_ok,
                'load_settings_process_failed': load_settings_process_failed,
                'set_num_iteration': set_num_iteration,
                'update_interface': update_interface,
                'canceled': canceled
            }
        )
        self.tables = []
        self.start()

    def open_system_settings(self, folder_name):
        # Function returns True for succesful completion 
        # of open system settings from json file
        system_settings = {}
        system_settings_filename = f'{folder_name}/system_settings.json'
        try:
            f = open(system_settings_filename)
            system_settings = load(f)
        except:
            return False, system_settings
        else:
            return True, system_settings

    def open_main_cluster(self, folder_name):
        # Function returns True for succesful completion 
        # of open main cluster from json file
        main_cluster = []
        main_cluster_filename = f'{folder_name}/main_settings.json'
        try:
            f = open(main_cluster_filename)
            main_cluster = load(f)
        except:
            return False, main_cluster
        else:
            return True, main_cluster

    def open_tsensor_table(self, folder_name, unit_name):
        #Function returns True for successful completion
        # of opening tsensor table from json file.
        labels_names = []
        filename = f'{folder_name}/tsensor_{unit_name}.json'
        try:
            f = open(filename)
            labels_names = load(f)
        except:
            return False, labels_names
        else:
            return True, labels_names

    def open_tsignal_table(self, folder_name, unit_name):
        #Function returns True for successful completion
        # of opening tsignal table from json file.
        labels_names = []
        filename = f'{folder_name}/tsignal_{unit_name}.json'
        try:
            f = open(filename)
            labels_names = load(f)
        except:
            return False, labels_names
        else:
            return True, labels_names

    def open_tregime_table(self, folder_name, unit_name):
        #Function returns True for successful completion
        # of opening tregime table from json file.
        labels_names = []
        filename = f'{folder_name}/tregime_{unit_name}.json'
        try:
            f = open(filename)
            labels_names = load(f)
        except:
            return False, labels_names
        else:
            return True, labels_names

    def open_tbearing_table(self, folder_name, unit_name):
        #Function returns True for successful completion
        # of opening tbearing table from json file.
        labels_names = []
        filename = f'{folder_name}/tbearing_{unit_name}.json'
        try:
            f = open(filename)
            labels_names = load(f)
        except:
            return False, labels_names
        else:
            return True, labels_names

    def open_air_gap_plane_table(self, folder_name, unit_name):
        #Function returns True for successful completion
        # of opening air gap planes table from json file.
        labels_names = []
        filename = f'{folder_name}/air_gap_plane_{unit_name}.json'
        try:
            f = open(filename)
            labels_names = load(f)
        except:
            return False, labels_names
        else:
            return True, labels_names

    def open_settings(
        self,
        load_settings_process_ok,
        load_settings_process_failed,
        set_num_iteration,
        update_interface,
        canceled,
        folder_name
    ):
        ss_open_ok, system_settings = self.open_system_settings(folder_name)
        if not ss_open_ok:
            print('Opening of system settings failed.')
            load_settings_process_failed(self.name)
            return
        if canceled(self.name): return
        num_iteration = 1 + len(system_settings['dBaseSettingsList'])*5
        try:
            set_num_iteration(num_iteration)
        except TclError:
            print("Progress interface was destroyed before!")
        try:
            #In case Progress window was destroyed exception is thrown.
            update_interface('Opening main cluster...')
        except TclError:
            print("Progress interface was destroyed before!")
        mc_open_ok, main_cluster = self.open_main_cluster(folder_name)
        if not mc_open_ok:
            print('Opening of main cluster failed.')
            load_settings_process_failed(self.name)
            return
        for i in system_settings['dBaseSettingsList']:
            unit = i['unitName']
            if canceled(self.name): return
            try:
                update_interface(f'Opening tsensor table for {unit}...')
            except TclError:
                print("Progress interface was destroyed before!")
            req_ok, labels_names = self.open_tsensor_table(
                folder_name,
                i['unitName']
            )
            if not req_ok:
                print("Open sensor labels-names request failed.")
                load_settings_process_failed(self.name)
                return
            self.append_table(
                unit = Unit.get_unit(i['unitName']),
                labels_names = labels_names,
                table_type = TableType.SENSORS
            )
            if canceled(self.name): return
            try:
                update_interface(f'Opening tsignal table for {unit}...')
            except TclError:
                print("Progress interface was destroyed before!")
            req_ok, labels_names = self.open_tsignal_table(
                folder_name, 
                i['unitName']
            )
            if not req_ok:
                print("Open signal labels-names request failed.")
                load_settings_process_failed(self.name)
                return
            self.append_table(
                unit = Unit.get_unit(i['unitName']),
                labels_names = labels_names,
                table_type = TableType.SIGNALS
            )
            if canceled(self.name): return
            try:
                update_interface(f'Opening tregime table for {unit}...')
            except TclError:
                print("Progress interface was destroyed before!")
            req_ok, labels_names = self.open_tregime_table(
                folder_name, 
                i['unitName']
            )
            if not req_ok:
                print("Open regime labels-names request failed.")
                load_settings_process_failed(self.name)
                return
            self.append_table(
                unit = Unit.get_unit(i['unitName']),
                labels_names = labels_names,
                table_type = TableType.REGIMES
            )
            if canceled(self.name): return
            try:
                update_interface(f'Opening tbearing table for {unit}...')
            except TclError:
                print("Progress interface was destroyed before!")
            req_ok, labels_names = self.open_tbearing_table(
                folder_name,
                i['unitName']
            )
            if not req_ok:
                print("Open bearing labels-names request failed.")
                load_settings_process_failed(self.name)
                return
            self.append_table(
                unit = Unit.get_unit(i['unitName']),
                labels_names = labels_names,
                table_type = TableType.BEARINGS
            )

            if canceled(self.name): return
            try:
                update_interface(f'Opening air gap plane table for {unit}...')
            except TclError:
                print("Progress interface was destroyed before!")
            req_ok, labels_names = self.open_air_gap_plane_table(
                folder_name,
                i['unitName']
            )
            if not req_ok:
                print("Open air gap planes labels-names request failed.")
                load_settings_process_failed(self.name)
                return
            self.append_table(
                unit = Unit.get_unit(i['unitName']),
                labels_names = labels_names,
                table_type = TableType.AIR_GAP_PLANES
            )
        if canceled(self.name): return
        try:
            update_interface()
        except TclError:
            print("Progress interface was destroyed before!")
        load_settings_process_ok(
            system_settings = system_settings,
            main_cluster = main_cluster,
            tables = self.tables
        )
        return

    def append_table(self, unit, labels_names, table_type):
        self.tables.append(Label_name_pairs(labels_names, unit, table_type))
