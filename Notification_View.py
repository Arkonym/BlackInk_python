import pyforms
from pyforms.basewidget import BaseWidget
from pyforms.controls import ControlText, ControlTextArea, ControlButton
from DB_Actions import post_notification
from Notification import Notification
from Error_Windows import ErrorWin, close_win
from datetime import datetime


class NotificationWidget(Notification, BaseWidget):
    def __init__(self, user=None, connection=None, timestamp='', symbol= '', index='', message=''):
        Notification.__init__(self, timestamp, symbol, index, message)
        BaseWidget.__init__(self, 'Notification')
        self._user = user
        self._connection = connection
        self._symbolField = ControlText('Company Symbol')
        self._indexField = ControlText('Current Index')
        self._messageField = ControlTextArea('Advisory')
        if symbol != '':
            self._symbolField.value = symbol
        if index != '':
            self._indexField.value=index
        if message != '':
            self._messageField.value = message
        if timestamp == '':
            self._sendButton = ControlButton('Send')
            self._sendButton.value = self.__sendNotification
        else:
            self._sendButton = ControlButton('Close')
            self._sendButton.value = self._close


        self._formset =[' ', ('||', '_symbolField', '||', ' '), '=',
                        ('||','_indexField', '||', ' '),
                        ('||', '_messageField', '||'),
                        ('||', '_sendButton', '||')]

    def __sendNotification(self):
        self._timestamp = datetime.now().timestamp()
        self._symbol = self._symbolField.value
        self._index = self._indexField.value
        self._message = self._messageField.value
        try:
            post_notification(self._user, self._connection, self._symbol,
                        self._index, self._message)
        except ValueError as error:
            err= ErrorWin(error)
            err.parent = self
            err.show()
            return

        except TypeError as type_err:
            err= ErrorWin('Connection or User Token Invalid')
            err.parent = self
            err.show()
            return


        if self.parent!=None: self.parent.add_notification(self)

    def _close(self):
        close_win(self)


if __name__== "__main__": pyforms.start_app(NotificationWidget, geometry=(400, 400, 600, 600))
