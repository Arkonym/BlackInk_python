import pyforms
from pyforms.basewidget import BaseWidget
from pyforms.controls import ControlText, ControlTextArea, ControlButton
from Notification import Notification

class NotificationWindow(Notification, BaseWidget):
    def __init__(self, timestamp=None, symbol= None, index=None, message=None):
        Notification.__init__(self, '', '', '', '')
        BaseWidget.__init__(self, 'Notification')

        self._symbolField = ControlText('Company Symbol', 'GOOGL, AAPL, etc.')
        self._indexField = ControlText('Current Index')
        self._messageField = ControlTextArea('Advisory')
        if symbol != None:
            self._symbolField.value = symbol
        if index != None:
            self._indexField.value=index
        if message != None:
            self._messageField.value = message
        if timestamp == None:
            self._sendButton = ControlButton('Send')
            self._sendButton.value = self.__sendNotification


        self._formset =[' ', ('||', '_symbolField', '||', ' '), '=',
                        ('||','_indexField', '||', ' '),
                        ('||', '_messageField', '||'),
                        ('||', '_sendButton', '||')]

    def __sendNotification(self):
        self._symbol = self._symbolField.value
        self._index = self._indexField.value
        self._message = self._indexField.value
        if self.parent!=None: self.parent.add_notification

if __name__== "__main__": pyforms.start_app(NotificationWindow, geometry=(400, 400, 600, 600))
