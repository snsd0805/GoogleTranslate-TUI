import npyscreen

class EditBox(npyscreen.BoxTitle):
    _contained_widget = npyscreen.MultiLineEdit

class SelectBox(npyscreen.BoxTitle):
    _contained_widget = npyscreen.SelectOne