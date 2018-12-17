import pyforms
from pyforms.basewidget import BaseWidget
from pyforms.controls import ControlList, ControlButton
from Account_View import UserWidget
from Confirm_Window import ConfirmWin
from Error_Windows import ErrorWin
from DB_Actions import pull_users, toggle_admin


class AdminWidget(BaseWidget):
    def __init__(self, user=None, connection=None):
        BaseWidget.__init__(self)
        self._admin = user
        self._connection = connection
        self._add_user_button = ControlButton('New User')
        self._refresh_button = ControlButton('Refresh List')
        self._add_user_button.value= self.__add_User_btnAction
        self._refresh_button.value= self.__refresh
        self._userList = ControlList('Users',select_entire_row=True)
        self._userList.readonly=True
        self._userList.cell_double_clicked_event = self.__onSelect
        self._userList.horizontal_headers=['Admin', 'Name', 'Email']
        self._userList.add_popup_menu_option('Toggle Admin Status', function_action=self.__admin_power)
        self._userList.add_popup_menu_option('Edit', function_action=self.__popEdit)
        if self._admin!=None and self._connection!=None:
            self.__retreive_users()


    def __refresh(self):
        self._userList.clear()
        self.__retreive_users()
        if self.parent!=None: self.parent.persist_login()

    def __retreive_users(self):
        try:
            self._user_pull= pull_users(self._admin, self._connection)
        except ValueError as err:
            err=ErrorWin(err)
            err.parent=self
            err.show()
            return
        if self._user_pull!=None:
            admins = self._connection['Database'].child('admins').shallow().get(self._admin['idToken'])
            for user in self._user_pull:
                check = False
                if user in admins.val():
                    check = True
                self._userList.__add__([check, self._user_pull[user]['name'], self._user_pull[user]['email']])

    def __onSelect(self, row, column):
        if self.parent!=None: self.parent.persist_login()
        name = self._userList.get_value(1, row)
        email  = self._userList.get_value(2, row)
        for i in self._user_pull:
            if self._user_pull[i]['email'] == email:
                uid = i
                try:
                    services = self._user_pull[i]['services']
                except:
                    services = {"notifications" : False, "analysis": False, "newsletter" : False}
        win = UserWidget(self._admin, self._connection, 'edit', uid, email, name, services)
        win.parent = self
        win.show()

    def _refresh(self):
        self._userList.clear()
        self._user_pull= pull_users(self._admin, self._connection)
        if self._user_pull!=None:
            for user in self._user_pull:
                self._userList.__add__([self._user_pull[user]['name'], self._user_pull[user]['email']])

    def __popEdit(self):
        row = self._userList.selected_row_index
        name = self._userList.get_value(1, row)
        email  = self._userList.get_value(2, row)
        print(email)
        for i in self._user_pull:
            if self._user_pull[i]['email'] == email:
                uid = i
                try:
                    services = self._user_pull[i]['services']
                except:
                    services = {"notifications" : False, "analysis": False, "newsletter" : False}
        win = UserWidget(self._admin, self._connection,'edit', uid, email, name, services)
        win.parent = self
        win.show()

    def __add_User_btnAction(self):
        if self.parent!=None: self.parent.persist_login()
        win = UserWidget(self._admin, self._connection, 'new')
        win.parent = self
        win.show()
    def _add_User(self, user):
        pass

    def _update_user(self, account):
        self._connection['Database'].child("users").child(account._uid).update({"name": account.name, "email": account.email, "services": account.services})

    def __admin_power(self):
        if self.parent!=None: self.parent.persist_login()
        row = self._userList.selected_row_index
        email  = self._userList.get_value(2, row)
        for i in self._user_pull:
            if self._user_pull[i]['email'] == email:
                self._selected_uid = i
        if self._selected_uid == self._admin['localId']:
            err = ErrorWin('Action not allowed - Cannot remove self as admin.')
            err.parent= self
            err.show()
            return
        if self._userList.get_value(0, row)== 'true':#already admin
            conf= ConfirmWin('Are you sure you want to remove this admin?', self._userList.get_value(1, row))
            conf.parent = self
            conf.show()
            return
        else:
            conf= ConfirmWin('Are you sure you want to make this account admin?', self._userList.get_value(1, row))
            conf.parent = self
            conf.show()
            return

    def _admin_toggle(self):
        toggle_admin(self._admin, self._connection, self._selected_uid)
        self._selected_uid=''
        self.__refresh()



if __name__== "__main__":
    pyforms.start_app(AdminWidget, geometry=(400, 400, 600, 600))
