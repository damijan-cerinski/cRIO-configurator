from tkinter import messagebox
from requests import get, post, codes
from .label_name_pairs import Label_name_pairs, TableType
from .codis_enums import Unit
from .loading import LoadingProcess
from .interfaces import ProgressUpload

class UploadingProcess:

    def __init__(
        self,
        ip,
        get_main_cluster,
        get_system_settings,
        get_table):
        
        self.ip = ip
        self.get_main_cluster = get_main_cluster
        self.get_system_settings = get_system_settings
        self.get_table = get_table

    def execute(self):
        self.upload_settings()

    #This method is a copy of the method from the LoadingProcess
    #class with the same name.
    def load_tsensor_table(self, dBaseName):
        #Function returns True for successful completion
        # of loading tsensor table from a dBase.
        labels_names = []
        try:
            r = get(f'http://{self.ip}:8002/CoDiS_Live_Data/Get_tsensor',
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

    #This method is a copy of the method from the LoadingProcess
    #class with the same name.
    def load_tsignal_table(self, dBaseName):
        #Function returns True for successful completion
        # of loading tsensor table from a dBase.
        labels_names = []
        try:
            r = get(f'http://{self.ip}:8002/CoDiS_Live_Data/Get_tsignal',
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

    #This method is a copy of the method from the LoadingProcess
    #class with the same name.
    def load_tbearing_table(self, dBaseName):
        #Function returns True for successful completion
        # of loading tbearing table from a dBase.
        labels_names = []
        try:
            r = get(f'http://{self.ip}:8002/CoDiS_Live_Data/Get_tbearing',
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

    #This method is a copy of the method from the LoadingProcess
    #class with the same name.  
    def load_tregime_table(self, dBaseName):
        #Function returns True for successful completion
        # of loading tregime table from a dBase.
        labels_names = []
        try:
            rt = f'http://{self.ip}:8002/CoDiS_Live_Data/Get_operating_regime'
            r = get(
                rt,
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

    def load_air_gap_plane_table(self, dBaseName):
        #Function returns True for successful completion
        # of loading air gap plane table from a dBase.
        labels_names = []
        try:
            r = get(f'http://{self.ip}:8002/CoDiS_Live_Data/Get_air_gap_plane',
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

    def upload_main_cluster(self, main_cluster):
        try:
            r = post(
                f'http://{self.ip}:8002/CoDiS_Live_Data/saveMainCluster',
                json = main_cluster
            )
        except:
            return False
        else:
            if r.status_code==codes.ok:
                return True
        return False

    def update_tsensor_table(self, dbase_name, current_table):
        success, dbase_table_pairs = self.load_tsensor_table(dbase_name)
        if not success:
            print("Updating of tsenor table failed!")
            return False
        dbase_table = Label_name_pairs(labels_names = dbase_table_pairs)
        to_update = []
        to_add = []
        for i in current_table:
            if dbase_table.get_name(i['label']) == None:
                to_add.append(i)
            elif i['name'] != dbase_table.get_name(i['label']):
                to_update.append(i)
        try:
            r = post(
                f'http://{self.ip}:8002/CoDiS_Live_Data/Rename_tsensor',
                json = {
                    'pairs': to_update,
                    'dBaseName': dbase_name
                }
            )
        except:
            print("Updating of tsenor table failed!")
            return False
        else:
            if r.status_code==codes.ok:
                pass
        try:
            r = post(
                f'http://{self.ip}:8002/CoDiS_Live_Data/insert_sensors',
                json = {
                    'pairs': to_add,
                    'dBaseName': dbase_name
                }
            )
        except:
            print("Updating of tsenor table failed!")
            return False
        else:
            if r.status_code==codes.ok:
                return True
        print("Updating of tsenor table failed!")
        return False

    def update_tsignal_table(self, dbase_name, current_table):
        success, dbase_table_pairs = self.load_tsignal_table(dbase_name)
        if not success:
            print("Updating of tsignal table failed!")
            return False
        dbase_table = Label_name_pairs(
            labels_names = dbase_table_pairs,
            table_type = TableType.SIGNALS
            )
        to_update = []
        to_add = []
        for i in current_table:
            if dbase_table.get_name(i['label']) == None:
                to_add.append(i)
            elif i['name'] != dbase_table.get_name(i['label']):
                to_update.append(i)
        try:
            r = post(
                f'http://{self.ip}:8002/CoDiS_Live_Data/Rename_tsignal',
                json = {
                    'pairs': to_update,
                    'dBaseName': dbase_name
                }
            )
        except:
            print("Updating of tsignal table failed!")
            return False
        else:
            if r.status_code==codes.ok:
                pass
        try:
            r = post(
                f'http://{self.ip}:8002/CoDiS_Live_Data/insert_signals',
                json = {
                    'pairs': to_add,
                    'dBaseName': dbase_name
                }
            )
        except:
            print("Updating of tsignal table failed!")
            return False
        else:
            if r.status_code==codes.ok:
                return True
        print("Updating of tsignal table failed!")
        return False

    def update_tbearing_table(self, dbase_name, current_table):
        success, dbase_table_pairs = self.load_tbearing_table(dbase_name)
        if not success:
            print("Updating of tbearing table failed!")
            return False
        dbase_table = Label_name_pairs(labels_names = dbase_table_pairs)
        to_update = []
        to_add = []
        for i in current_table:
            if dbase_table.get_name(i['label']) == None:
                to_add.append(i)
            elif i['name'] != dbase_table.get_name(i['label']):
                to_update.append(i)
        try:
            r = post(
                f'http://{self.ip}:8002/CoDiS_Live_Data/Rename_tbearing',
                json = {
                    'pairs': to_update,
                    'dBaseName': dbase_name
                }
            )
        except:
            print("Updating of tbearing table failed!")
            return False
        else:
            if r.status_code==codes.ok:
                pass
        try:
            r = post(
                f'http://{self.ip}:8002/CoDiS_Live_Data/insert_bearings',
                json = {
                    'pairs': to_add,
                    'dBaseName': dbase_name
                }
            )
        except:
            print("Updating of tbearing table failed!")
            return False
        else:
            if r.status_code==codes.ok:
                return True
        print("Updating of tbearing table failed!")
        return False

    def update_tregime_table(self, dbase_name, current_table):
        success, dbase_table_pairs = self.load_tregime_table(dbase_name)
        if not success:
            print("Updating of tsenor table failed!")
            return False
        dbase_table = Label_name_pairs(labels_names = dbase_table_pairs)
        to_update = []
        to_add = []
        for i in current_table:
            if dbase_table.get_name(i['label']) == None:
                to_add.append(i)
            elif i['name'] != dbase_table.get_name(i['label']):
                to_update.append(i)
        try:
            u = f'http://{self.ip}:8002/CoDiS_Live_Data/Rename_operating_regime'
            r = post(
                u,
                json = {
                    'pairs': to_update,
                    'dBaseName': dbase_name
                }
            )
        except:
            print("Updating of tregime table failed!")
            return False
        else:
            if r.status_code==codes.ok:
                pass
        try:
            r = post(
                f'http://{self.ip}:8002/CoDiS_Live_Data/insert_regimes',
                json = {
                    'pairs': to_add,
                    'dBaseName': dbase_name
                }
            )
        except:
            print("Updating of tregime table failed!")
            return False
        else:
            if r.status_code==codes.ok:
                return True
        print("Updating of tregime table failed!")
        return False

    def update_air_gap_plane_table(self, dbase_name, current_table):
        success, dbase_table_pairs = self.load_air_gap_plane_table(dbase_name)
        if not success:
            print("Updating of air gap plane table failed!")
            return False
        dbase_table = Label_name_pairs(labels_names = dbase_table_pairs)
        to_update = []
        to_add = []
        for i in current_table:
            if dbase_table.get_name(i['label']) == None:
                to_add.append(i)
            elif i['name'] != dbase_table.get_name(i['label']):
                to_update.append(i)
        try:
            u = f'http://{self.ip}:8002/CoDiS_Live_Data/Rename_air_gap_plane'
            r = post(
                u,
                json = {
                    'pairs': to_update,
                    'dBaseName': dbase_name
                }
            )
        except:
            print("Updating of air gap plane table failed!")
            return False
        else:
            if r.status_code==codes.ok:
                pass
        try:
            r = post(
                f'http://{self.ip}:8002/CoDiS_Live_Data/Insert_air_gap_planes',
                json = {
                    'pairs': to_add,
                    'dBaseName': dbase_name
                }
            )
        except:
            print("Updating of air gap plane table failed!")
            return False
        else:
            if r.status_code==codes.ok:
                return True
        print("Updating of air gap plane table failed!")
        return False

    def upload_settings(self):
        main_cluster = self.get_main_cluster()
        system_settings = self.get_system_settings()
        if system_settings != {}:
            num_iteration = 1 + len(system_settings['dBaseSettingsList'])*5
            pb = ProgressUpload(
                num_iteration = num_iteration,
                title = 'Uploading progress'
            )
            pb.progress('Uploading main cluster...')
            self.upload_main_cluster(main_cluster)
            for i in system_settings['dBaseSettingsList']:
                unit = Unit.get_unit(i['unitName'])
                tsensor_table = self.get_table(unit, TableType.SENSORS)
                tsignal_table = self.get_table(unit, TableType.SIGNALS)
                tbearing_table = self.get_table(unit, TableType.BEARINGS)
                tregime_table = self.get_table(unit, TableType.REGIMES)
                air_gap_plane_table = self.get_table(unit, TableType.AIR_GAP_PLANES)
                unit_name = i['unitName']
                pb.progress(f'Uploading tsensor table for {unit_name}...')
                self.update_tsensor_table(
                    dbase_name = i['dBaseName'],
                    current_table = tsensor_table
                )
                pb.progress(f'Uploading tsignal table for {unit_name}...')
                self.update_tsignal_table(
                    dbase_name = i['dBaseName'],
                    current_table = tsignal_table
                )
                pb.progress(f'Uploading tbearing table for {unit_name}...')
                self.update_tbearing_table(
                    dbase_name = i['dBaseName'],
                    current_table = tbearing_table
                )
                pb.progress(f'Uploading tregime table for {unit_name}...')
                self.update_tregime_table(
                    dbase_name = i['dBaseName'],
                    current_table = tregime_table
                )
                pb.progress(f'Uploading air gap plane table for {unit_name}...')
                self.update_air_gap_plane_table(
                    dbase_name = i['dBaseName'],
                    current_table = air_gap_plane_table
                )
            pb.progress()
        else:
            messagebox.showinfo("Upload Failed!", "The configuration system is empty.")
