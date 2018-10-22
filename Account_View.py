import pyforms
from pyforms.basewidget import BaseWidget
from pyforms.controls import ControlText, ControlButton, ControlList
from User import User
from Error_Windows import ErrorWin, close_win
from DB_Actions import pull_users

class UserWidget(User, BaseWidget):
    def __init__(self, admin=None, connection=None, email='', name='', services=[]):
        User.__init__(self, email, name, '', services)
        BaseWidget.__init__(self, 'User')
        self._admin = admin
        self._connection = connection

        self._editBtn = ControlButton('Edit')
        self._editBtn.value = self._edit

        self._email_field = ControlText('Email')
        self._email_field.readonly = True
        if email!='':
            self._email_field = email

        self._name_field =ControlText('Name')
        self._name_field.readonly = True
        if name!='':
            self._name_field = name

        self._services_field = ControlList('Services')
        self._services_field.readonly= True
        self._services_field.horizontal_headers = ['Service', 'Value']
        self._services_field.cell_double_clicked_event = None
        if services!=[]:
            for i in services:
                self._services_field.__add__([services[i]['service'], services[i]['value']])


    def _edit(self):
        pass
    def _save(self):
        pass

    def _toggle(self, row, column):
        pass

if __name__== "__main__": pyforms.start_app(UserWidget, geometry=(400, 400, 600, 600))
