import pyforms
from pyforms.basewidget import BaseWidget
from pyforms.controls import ControlText, ControlTextArea, ControlButton, ControlLabel
from DB_Actions import post_notification, update_notification
from Notification import Notification
from Error_Windows import ErrorWin, close_win
from datetime import datetime


class NotificationWidget(Notification, BaseWidget):
    def __init__(self, user=None, connection=None, timestamp='', symbol= '', price='', message='', flag= '', key=''):
        super(NotificationWidget, self).__init__(timestamp, symbol, price, message, key)
        BaseWidget.__init__(self, 'Notification')
        self._user = user
        self._connection = connection
        if timestamp!='':
            self._timestamp_field = ControlLabel(timestamp)
        else:
            ts = datetime.now().timestamp()
            self._timestamp_field = ControlLabel(datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'))
        self._symbol_field = ControlText('Company Symbol')
        self._price_field = ControlText('Current Price (Optional)')
        self._message_field = ControlTextArea('Advisory')
        if symbol != '':
            self._symbol_field.value = symbol
        if price != '':
            self._price_field.value=price
        if message != '':
            self._message_field.value = message
        if flag == 'new':
            self._sendButton = ControlButton('Send')
            self._sendButton.value = self.__sendNotification
        elif flag == 'view':
            self._sendButton = ControlButton('Close')
            self._sendButton.value = self._close
        elif flag == 'edit':
            self._sendButton = ControlButton('Save')
            self._sendButton.value = self.__sendUpdate
        else:
            self._sendButton = ControlButton('Close')
            self._sendButton.value = self._close


        self._formset =[' ', ('||', '_timestamp_field', '||', ' '),
                        ('||', '_symbol_field', '||', ' '), '=',
                        ('||','_price_field', '||', ' '),
                        ('||', '_message_field', '||'),
                        ('||', '_sendButton', '||')]

    def __sendNotification(self):
        Notification.timestamp = datetime.now().timestamp()
        Notification.symbol = self._symbol_field.value
        Notification.price = self._price_field.value
        Notification.message = self._message_field.value
        try:
            post_notification(self._user, self._connection, Notification)
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

        if self.parent!=None: self.parent._refresh()
        self._close()

    def __sendUpdate(self):
        #Notification.timestamp = self.timestamp
        Notification.symbol = self.symbol
        Notification.price = self._price_field.value
        Notification.message = self._message_field.value
        Notification.key =self.key
        try:
            update_notification(self._user, self._connection, Notification)
        except ValueError as error:
            err=ErrorWin(error)
            err.parent=self
            err.show()
            return
        if self.parent!=None: self.parent._refresh()
        self._close()

    def _close(self):
        close_win(self)


if __name__== "__main__":
    pyforms.start_app(NotificationWidget('', '', '', 'AAPL', 0.00, 'hello world', 'edit', '+=+'), geometry=(400, 400, 600, 600))
