from enum import Enum

class Label_name_pairs:
    def __init__(self, labels_names, unit = None, table_type = None):
        #-----------------------------------------------------------
        #labels_names: list of dicts [{"name":name,"label":label}]
        #where name and label correspond to label-name pairs that
        #are stored in tsensor and tsignal tables.
        #unit: enum Unit from codis_enums
        #-----------------------------------------------------------
        self.unit = unit
        self.table_type = table_type
        self.labels_names = labels_names

    def __iter__(self):
        self.i = 0
        return self

    def __next__(self):
        if self.i < len(self.labels_names):
            x = self.labels_names[self.i]
            self.i += 1
            return x
        else:
            raise StopIteration

    def get_name(self, label):
        for i in self.labels_names:
            if i['label'] == label:
                return i['name']
        return None

    def get_label(self, name):
        for i in self.labels_names:
            if i['name'] == name:
                return i['label']
        return None

    def get_unit(self):
        return self.unit

    def get_table_type(self):
        return self.table_type

    def get_pairs(self):
        return self.labels_names

    def update_name(self, label, name):
        index = 0
        found = False
        for i in self.labels_names:
            if i['label'] == label:
                found = True
                break
            index +=1
        if found: 
            self.labels_names[index]['name'] = name
        else:
            self.labels_names.append(
                {
                    'label': label,
                    'name': name
                }
            )

    def remove(self, label):
        i = 0
        while i < len(self.labels_names):
            element = self.labels_names[i]
            if element['label'] == label:
                self.labels_names.pop(i)
                i -= 1
            i += 1

class TableType(Enum):
    SENSORS = 0
    SIGNALS = 1
    BEARINGS = 2
    REGIMES = 3
    AIR_GAP_PLANES = 4

