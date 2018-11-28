import pyforms
from pyforms.basewidget import BaseWidget
from pyforms.controls import ControlEmptyWidget, ControlText, ControlToolButton, ControlLabel
from DB_Actions import db_connect
from LoginWindow import loginWidget
from Account_Admin_View import AdminWidget
from Notifications_View import NotificationsWidget
from datetime import datetime



class BlackInkBE(BaseWidget):
    def __init__(self):
        super(BlackInkBE, self).__init__('BlackInk Backend')
        self._display_name = ControlLabel('')
        self._accounts_admin= ControlToolButton('Accounts Panel', maxheight = 100, maxwidth=100)
        self._accounts_admin.hide()
        self._accounts_admin.value = self._Accounts

        self._user = None
        self._connection = db_connect()

        self._panel = ControlEmptyWidget()
        self._login()



    def _login(self):
        logwin = loginWidget()
        logwin.parent = self
        self._panel.value = logwin
        self._login_time = datetime.now().hour

    def _logout(self):
        self._user = None
        self._connection = None
        self._login()


    def loadUser(self, user):
        self._user = user
        self._display_name.value = self._user['email'].split('@')[0]
        self._accounts_admin.show()
        self._Notifications()

    def _Notifications(self):
        notwin = NotificationsWidget(self._user, self._connection)
        notwin.parent=self
        self._panel.value =notwin

    def _Accounts(self):
        win = AdminWidget(self._user, self._connection)
        win.parent = self
        win.show()


    def persist_login(self):
        cur_time = datetime.now().hour
        if cur_time - self._login_time > 50:
            try:
                self._user = self._connection['Auth'].refresh(user['refreshToken'])
            except:
                self._login()






if __name__=="__main__":
    pyforms.start_app(BlackInkBE, geometry=(200, 200, 400, 400))
