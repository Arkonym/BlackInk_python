import pyforms
from pyforms.basewidget import BaseWidget
from pyforms.controls import ControlText, ControlTextArea, ControlButton
from DB_Actions import post_notification
from Notification import Notification
from Error_Windows import ErrorWin, close_win
from datetime import datetime


class NotificationWidget(Notification, BaseWidget):
    def __init__(self, user=None, connection=None, timestamp='', symbol= '', price='', message=''):
        Notification.__init__(self, timestamp, symbol, price, message)
        BaseWidget.__init__(self, 'Notification')
        self._user = user
        self._connection = connection
        self._symbol_field = ControlText('Company Symbol')
        self._price_field = ControlText('Current Price (Optional)')
        self._message_field = ControlTextArea('Advisory')
        if symbol != '':
            self._symbol_field.value = symbol
        if price != '':
            self._price_field.value=price
        if message != '':
            self._message_field.value = message
        if timestamp == '':
            self._sendButton = ControlButton('Send')
            self._sendButton.value = self.__sendNotification
        else:
            self._sendButton = ControlButton('Close')
            self._sendButton.value = self._close


        self._formset =[' ', ('||', '_symbol_field', '||', ' '), '=',
                        ('||','_price_field', '||', ' '),
                        ('||', '_message_field', '||'),
                        ('||', '_sendButton', '||')]

    def __sendNotification(self):
        self.timestamp = datetime.now().timestamp()
        self.symbol = self._symbol_field.value
        self.price = self._price_field.value
        self.message = self._message_field.value
        try:
            post_notification(self._user, self._connection, self._symbol,
                        self._price, self._message)
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
