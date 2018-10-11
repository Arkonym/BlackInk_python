import pyforms
from pyforms.basewidget import BaseWidget
from pyforms.controls import ControlEmptyWidget, ControlText, ControlButton
from DB_Actions import db_connect
from ControlPasswordText import ControlPasswordText
from LoginWindow import loginWidget
from Notifications_View import NotificationsWidget


class BlackInkBE(BaseWidget):
    def __init__(self):
        super(BlackInkBE, self).__init__('BlackInk Backend')
        self._test = ControlText('logged in user')
        #self._test.readonly = True
        self._user = None
        self._connection = db_connect()
        self._panel = ControlEmptyWidget()
        self.login()


    def login(self):
        logwin = loginWidget()
        logwin.parent = self
        self._panel.value = logwin

    def Notifications(self):
        notwin = NotificationsWidget()
        notwin.parent=self
        self._panel.value =notwin

    def loadUser(self, user):
        self._user = user
        self._test.value = self._user['email']
        self.Notifications()












if __name__=="__main__":
    pyforms.start_app(BlackInkBE, geometry=(200, 200, 400, 400))
