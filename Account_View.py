import pyforms
from pyforms.basewidget import BaseWidget
from pyforms.controls import ControlText, ControlButton, ControlList, ControlLabel
from User import User
from Error_Windows import ErrorWin, close_win
from DB_Actions import pull_users

class UserWidget(User, BaseWidget):
    def __init__(self, admin=None, connection=None, flag='', uid='', email='', name='', services={}):
        super(UserWidget, self).__init__(uid, email, name, services)
        BaseWidget.__init__(self, 'User')
        self._admin = admin
        self._connection = connection
        self.changes = [] #0 is name change, 1 is services change
        if flag=='edit':
            self._editBtn = ControlButton('Edit')
            self._editBtn.value = self._edit
        elif flag=='new':
            self._editBtn = ControlButton('Save')
            self._editBtn.value() = self._save
        else:
            self._closeBtn= ControlButton('Close')
            self._closeBtn.value = self._close

        if uid!='':
            self._uid_field = ControlText('User_Key')
            self._uid_field.value= uid
        self._email_field = ControlText('Email')
        self._email_field.readonly = True
        if email!='':
            self._email_field.value = email

        self._name_field =ControlText('Name')
        self._name_field.readonly = True
        if name!='':
            self._name_field.value = name

        self._services = services
        self._services_field = ControlList('Services')
        self._services_field.readonly= True
        self._services_field.horizontal_headers = ['Service', 'Value']
        #self._services_field.cell_double_clicked_event = None
        if services!={}:
            for i in services:
                self._services_field.__add__([i, services[i]])


    def _edit(self):
        self._editBtn.label = 'Save'
        self._editBtn.value = self._save
        self._email_field.readonly = False
        self._name_field.readonly = False
        self._services_field.readonly = False
        self._services_field.cell_double_clicked_event = self._toggle

    def _save(self):
        if self.parent!=None:
            self.name = self._name_field.value
            self.email = self._email_field.value
            self.services = self._services
            self.uid = self._uid_field.value
            if flag=='edit':
                self.parent._update_user(self)
            elif flag =='new':
                self.parent._add_User(self)
        self._close()

    def _toggle(self, row, column):
        val = self._services_field.get_value(column, row)
        if val == True:
            self._services_field.set_value(column, row, False)
            self._services[self._services_field.get_value(0, row)] = False
        else:
            self._services_field.set_value(column, row,True)
            self._services[self._services_field.get_value(0, row)] = True
        self.changes[1] =True

    def _close(self):
        close_win(self)


if __name__== "__main__": pyforms.start_app(UserWidget, geometry=(400, 400, 600, 600))
