from pysettings import conf
from pyforms.controls import ControlText

from PyQt5.QtWidgets import QLineEdit

class ControlPasswordText(ControlText):
    def __init__(self, *args, **kwargs):
        super(ControlPasswordText, self).__init__(*args, **kwargs)
        self.form.lineEdit.setEchoMode(QLineEdit.Password)
