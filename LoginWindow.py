import pyforms
from pyforms.basewidget import BaseWidget
from pyforms.controls import ControlText, ControlButton
from DB_Actions import db_connect, login
from ControlPasswordText import ControlPasswordText
from Error_Windows import ErrorWin


class loginWidget(BaseWidget):
    def __init__(self, connection=None):
        super(loginWidget, self).__init__('Login')
        self._user=None
        if connection==None:
            self._connection = db_connect()
        else:
            self._connection = connection
        self._email = ControlText('Email')
        self._password = ControlPasswordText('Password')
        self._loginButton = ControlButton('Login')
        self._loginButton.value= self.__loginAction
        self.formset =[' ',
            (' ', '||', '_email', '||',' '),
            (' ', '||', '_password', '||',' '),
            (' ', '||', '_loginButton', '||',' '), ' ']


    def __loginAction(self):
        try:
            self._user= login(self._connection, self._email.value, self._password.value) #user also public
        except ValueError as error:
            err = ErrorWin(error)
            err.show()
            return

        if self.parent!=None: self.parent.loadUser(self._user)
        if self._user != None:
                self.close()



        #self._user.value = self._email.value + " " +self._password.value

if __name__=="__main__":
    pyforms.start_app(loginWidget, geometry=(200, 200, 400, 400))
