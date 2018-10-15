import pyforms
from pyforms.basewidget import BaseWidget
from pyforms.controls import ControlEmptyWidget, ControlText, ControlButton, ControlLabel
from DB_Actions import db_connect
from LoginWindow import loginWidget
from Notifications_View import NotificationsWidget
from datetime import datetime
from time import sleep

delta_hour =0

class BlackInkBE(BaseWidget):
    def __init__(self):
        super(BlackInkBE, self).__init__('BlackInk Backend')
        self._display_name = ControlLabel('')
        self._user = None
        self._connection = db_connect()
        self._panel = ControlEmptyWidget()
        #self._formset= { ('||','_display_name', '||'), ('_panel')
        #}
        self._login()
        #self._persist_login()


    def _login(self):
        logwin = loginWidget()
        logwin.parent = self
        self._panel.value = logwin
        self._login_time = datetime.now().hour

    def _logout(self):
        self._user = None
        self._connection = None
        self._login()

    def _Notifications(self):
        notwin = NotificationsWidget(self._user, self._connection)
        notwin.parent=self
        self._panel.value =notwin

    def loadUser(self, user):
        self._user = user
        self._display_name.value = self._user['email'].split('@')[0]
        #self._persist_login()
        self._Notifications()

    def persist_login(self):
        cur_time = datetime.now().hour
        if cur_time - self._login_time > 0.9:
            try:
                self._user = self._connection['Auth'].refresh(user['refreshToken'])
            except:
                self._login()















if __name__=="__main__":
    pyforms.start_app(BlackInkBE, geometry=(200, 200, 400, 400))
