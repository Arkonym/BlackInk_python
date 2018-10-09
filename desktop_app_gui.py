import pyforms
from pyforms.basewidget import BaseWidget
from pyforms.controls import ControlDockWidget, ControlText, ControlButton
from DB_Actions import db_connect, login, post_notification
from ControlPasswordText import ControlPasswordText


class BlackInkBE(BaseWidget):
    def __init__(self):
        super(BlackInkBE, self).__init__('BlackInk Backend')
        self._panel = ControlDockWidget
        self._connection = db_connect()
        self._email = ControlText('Email')
        self._password = ControlPasswordText('Password')
        self._loginButton = ControlButton('Login')
        self._loginButton.value= self.__loginAction
        self.formset =[' ', (' ', '||', '_email', '||',' '),
            (' ', '||', '_password', '||',' '),
            (' ', '||', '_loginButton', '||',' '), ' ']


    def __loginAction(self):
        self._user= login(self._connection, self._email.value, self._password.value)
        #self._user.value = self._email.value + " " +self._password.value





if __name__=="__main__":
    pyforms.start_app(BlackInkBE, geometry=(200, 200, 400, 400))
