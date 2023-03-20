from tkinter import *
from tkinter.ttk import Combobox
from tkinter import Variable
import re


class UnsignedIntegerEntry(Entry):


    def __init__(self, *args, **kwargs):
        self.old = ''
        Entry.__init__(self, *args, **kwargs)
        self.bind('<FocusIn>', self.focus_in)
        self.bind('<FocusOut>', self.focus_out)

    def validate(self):
        try:
            val = int(Entry.get(self))
            if val < 0:
                self.delete(0, 'end')
                self.insert(0, self.old)
        except ValueError:
            self.delete(0, 'end')
            self.insert(0, self.old)

    def focus_in(self, e):
        self.old = Entry.get(self)

    def focus_out(self, e):
        self.validate()

    #Method overrides get method of the Entry class.
    #Validation is done every time value is read.
    #Ex. form is completed before UnsignedIntegerEntry
    #object was focused out.
    def get(self):
        self.validate()
        try:
            val = int(Entry.get(self))
        except ValueError:
            val = None
        return val


class Unsigned16bitIntegerEntry(Entry):


    def __init__(self, *args, **kwargs):
        self.old = ''
        Entry.__init__(self, *args, **kwargs)
        self.bind('<FocusIn>', self.focus_in)
        self.bind('<FocusOut>', self.focus_out)

    def validate(self):
        try:
            val = int(Entry.get(self))
            if val < 0 or val > 65535:
                self.delete(0, 'end')
                self.insert(0, self.old)
        except ValueError:
            self.delete(0, 'end')
            self.insert(0, self.old)

    def focus_in(self, e):
        self.old = Entry.get(self)

    def focus_out(self, e):
        self.validate()

    #Method overrides get method of the Entry class.
    #Validation is done every time value is read.
    #Ex. form is completed before FloatEntry
    #object was focused out.
    def get(self):
        self.validate()
        try:
            val = int(Entry.get(self))
        except ValueError:
            val = None
        return val


class IntegerEntry(Entry):


    def __init__(self, *args, **kwargs):
        self.old = ''
        Entry.__init__(self, *args, **kwargs)
        self.bind('<FocusIn>', self.focus_in)
        self.bind('<FocusOut>', self.focus_out)

    def validate(self):
        try:
            int(Entry.get(self))
        except ValueError:
            self.delete(0, 'end')
            self.insert(0, self.old)

    def focus_in(self, e):
        self.old = Entry.get(self)

    def focus_out(self, e):
        self.validate()

    #Method overrides get method of the Entry class.
    #Validation is done every time value is read.
    #Ex. form is completed before IntegerEntry
    #object was focused out.
    def get(self):
        self.validate()
        try:
            val = int(Entry.get(self))
        except ValueError:
            val = None
        return val


class FloatEntry(Entry):


    def __init__(self, *args, **kwargs):
        self.old = ''
        Entry.__init__(self, *args, **kwargs)
        self.bind('<FocusIn>', self.focus_in)
        self.bind('<FocusOut>', self.focus_out)

    def validate(self):
        try:
            float(Entry.get(self))
        except ValueError:
            self.delete(0, 'end')
            self.insert(0, self.old)

    def focus_in(self, e):
        self.old = Entry.get(self)

    def focus_out(self, e):
        self.validate()

    #Method overrides get method of the Entry class.
    #Validation is done every time value is read.
    #Ex. form is completed before FloatEntry
    #object was focused out.
    def get(self):
        self.validate()
        try:
            val = float(Entry.get(self))
        except ValueError:
            val = None
        return val


class IpIntegerEntry(Entry):


    def __init__(self, *args, **kwargs):
        self.old = ''
        Entry.__init__(self, *args, **kwargs)
        self.bind('<FocusIn>', self.focus_in)
        self.bind('<FocusOut>', self.focus_out)
        self.bind('<KeyRelease>', self.focus_next_widget)
        self.bind('<Any-Key>', self.focus_arrow)

    def validate(self):
        if Entry.get(self) == '':
            pass
        else:
            try:
                val = int(Entry.get(self))
                if val < 0 or val not in range(0,256):
                    self.delete(0, 'end')
                    self.insert(0, self.old)
                    self.focus_set()
            except ValueError:
                self.delete(0, 'end')
                self.insert(0, self.old)
                self.focus_set()
            
    def focus_in(self, e):
        self.old = Entry.get(self)
        self.select_range(0, 'end')

    def focus_out(self, e):
        self.validate()

    def focus_next_widget(self, e):
        if e.keysym in ['period', 'comma']:
            self.delete(len(Entry.get(self))-1, 'end')
            self.tk_focusNext().focus()
        elif e.keysym in ['Left', 'Right', 'Tab']:
            pass
        else:
            val = Entry.get(self)
            if len(val) >= 3:
                self.tk_focusNext().focus()

    def focus_arrow(self, e):
        if e.keysym == 'Left' or e.keysym == 'BackSpace':
            if Entry.index(self, INSERT) == 0:
                self.tk_focusPrev().focus()
        elif e.keysym == 'Right':
            val = Entry.get(self)
            cur_pos = Entry.index(self, INSERT)
            if cur_pos == len(val):
                self.tk_focusNext().focus()
        else:
            pass

    #Method overrides get method of the Entry class.
    #Validation is done every time value is read.
    #Ex. form is completed before UnsignedIntegerEntry
    #object was focused out.
    def get(self):
        self.validate()
        try:
            val = int(Entry.get(self))
        except ValueError:
            val = None
        return val


class SelectorCombo(Combobox):


    def __init__(self, *args, **kwargs):
        self.pairs = kwargs.pop('pairs')
        init_name_given = False
        if 'init_name' in kwargs: 
            init_name = kwargs.pop('init_name')
            init_name_given = True
        if 'values' in kwargs: kwargs.pop('values')
        values = []
        for i in self.pairs:
            values.append(i['name'])
        Combobox.__init__(self, *args, values = values, **kwargs)
        self.bind('<Key>', self.check_key)
        if init_name_given: self.insert(0, init_name)

    def check_key(self, e):
        if (
            e.keysym == 'Left'
            or e.keysym == 'Right'
            or e.keysym == 'Up'
            or e.keysym == 'Down'
            or e.keysym == 'Return'
        ):
            return
        else:
            return 'break'
    
    def get(self):
        name = Combobox.get(self)
        for i in self.pairs:
            if i['name'] == name: return i['label']
        return ''


class SelectorList(Listbox):


    def __init__(self, *args, **kwargs):
        self.pairs = kwargs.pop('pairs')
        init_sensors_given = False
        if 'init_sensors' in kwargs:
            init_sensors = kwargs.pop('init_sensors')
            init_sensors_given = True
        if 'listvariable' in kwargs: kwargs.pop('listvariable')
        values = []
        for i in self.pairs:
            values.append(i['name'])
        selected_indexes = []
        for i in init_sensors:
            index = 0
            for j in self.pairs:
                if i == j['label']:
                    selected_indexes.append(index)
                index += 1
        values = tuple(values)
        var = Variable(value = values)
        Listbox.__init__(self, *args, listvariable = var, **kwargs)
        for i in selected_indexes:
            self.selection_set(i)
    #     self.bind('<Key>', self.check_key)

    # def check_key(self, e):
    #     if (
    #         e.keysym == 'Left'
    #         or e.keysym == 'Right'
    #         or e.keysym == 'Up'
    #         or e.keysym == 'Down'
    #         or e.keysym == 'Return'
    #     ):
    #         return
    #     else:
    #         return 'break'
    
    def get(self):
        selected_list = []
        selected_index = Listbox.curselection(self)
        for i in selected_index:
            select = Listbox.get(self, i)
            selected_list.append(select)
        labels = []
        for i in self.pairs:
            if i['name'] in selected_list:
                labels.append(i['label'])
        return labels


class AutocompleteEntry(Entry):
    def __init__(self, autocompleteList, *args, **kwargs):

        self.listboxLength = 0
        self.parent = args[0]

        # Custom matches function
        if 'matchesFunction' in kwargs:
            self.matchesFunction = kwargs['matchesFunction']
            del kwargs['matchesFunction']
        else:
            def matches(fieldValue, acListEntry):
                pattern = re.compile(
                    '.*' + re.escape(fieldValue) + '.*', re.IGNORECASE)
                return re.match(pattern, acListEntry)

            self.matchesFunction = matches

        # Custom return function
        if 'returnFunction' in kwargs:
            self.returnFunction = kwargs['returnFunction']
            del kwargs['returnFunction']
        else:
            def selectedValue(value):
                print(value)
            self.returnFunction = selectedValue

        Entry.__init__(self, *args, **kwargs)
        #super().__init__(*args, **kwargs)
        self.focus()

        self.autocompleteList = autocompleteList

        self.var = self["textvariable"]
        if self.var == '':
            self.var = self["textvariable"] = StringVar()

        self.var.trace('w', self.changed)
        self.bind("<Right>", self.selection)
        self.bind("<Up>", self.moveUp)
        self.bind("<Down>", self.moveDown)
        self.bind("<Return>", self.selection)
        self.bind("<Escape>", self.deleteListbox)

        self.listboxUp = False

    def deleteListbox(self, event=None):
        if self.listboxUp:
            self.listbox.destroy()
            self.listboxUp = False

    def select(self, event=None):
        if self.listboxUp:
            index = self.listbox.curselection()[0]
            value = self.listbox.get(ACTIVE)
            self.listbox.destroy()
            self.listboxUp = False
            self.delete(0, END)
            self.insert(END, value)
            self.returnFunction(value)

    def changed(self, name, index, mode):
        if self.var.get() == '':
            self.deleteListbox()
        else:
            words = self.comparison()
            if words:
                if not self.listboxUp:
                    self.listboxLength = len(words)
                    self.listbox = Listbox(self.parent,
                        width=self["width"], height=self.listboxLength)
                    self.listbox.bind("<Button-1>", self.selection)
                    self.listbox.bind("<Right>", self.selection)
                    self.listbox.place(
                        x=self.winfo_x(), y=self.winfo_y() + self.winfo_height())
                    self.listboxUp = True
                else:
                    self.listboxLength = len(words)
                    self.listbox.config(height=self.listboxLength)

                self.listbox.delete(0, END)
                for w in words:
                    self.listbox.insert(END, w)
            else:
                self.deleteListbox()

    def selection(self, event):
        if self.listboxUp:
            self.var.set(self.listbox.get(ACTIVE))
            self.listbox.destroy()
            self.listboxUp = False
            self.icursor(END)

    def moveUp(self, event):
        if self.listboxUp:
            if self.listbox.curselection() == ():
                index = '0'
            else:
                index = self.listbox.curselection()[0]

            self.listbox.selection_clear(first=index)
            index = str(int(index) - 1)
            if int(index) == -1:
                index = str(self.listboxLength-1)

            self.listbox.see(index)  # Scroll!
            self.listbox.selection_set(first=index)
            self.listbox.activate(index)

    def moveDown(self, event):
        if self.listboxUp:
            if self.listbox.curselection() == ():
                index = '-1'
            else:
                index = self.listbox.curselection()[0]

            if index != END:
                self.listbox.selection_clear(first=index)
                if int(index) == self.listboxLength-1:
                    index = "0"
                else:
                    index = str(int(index)+1)

                self.listbox.see(index)  # Scroll!
                self.listbox.selection_set(first=index)
                self.listbox.activate(index)

    def comparison(self):
        return [w for w in self.autocompleteList if self.matchesFunction(self.var.get(), w)]
    

if __name__ == '__main__':
    window=Tk()
    vals = ["Jedan", "Dva", "Tri"]
    def com():
        print(widget.get())
    button = Button(window, text = "Tipka", command = com)
    widget = SelectorCombo(
        init_name = 'fdfd',
        pairs = [
            {'name': 'Brzina', 'label': 'TRG000.RotSpeed'},
            {'name': 'Rel', 'label': 'RV000'},
            {'name': 'Abs', 'label': 'AV000'}
        ],
        master = window,
        width = 10)
    widget.pack()
    button.pack()
    window.title('Hello Python')
    window.geometry("300x200+10+20")
    window.mainloop()
