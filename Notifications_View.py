import pyforms
from pyforms.basewidget import BaseWidget
from pyforms.controls import ControlList, ControlButton, ControlToolButton
from Notifications import Notifications
from Notification import Notification
from Notification_View import NotificationWidget
from DB_Actions import db_connect, login_manual, pull_notifications
from datetime import datetime
import time



class NotificationsWidget(Notifications, BaseWidget):
    def __init__(self, user = None, connection = None):
        Notifications.__init__(self)
        BaseWidget.__init__(self)
        self._user = user
        self._connection = connection
        self._refresh_button = ControlToolButton('Refresh', maxheight= 50, maxwidth= 100)
        self._notifList = ControlList('Notifications',
            select_entire_row = True,
            plusFunction = self.__addNotifBtnAction,
            minusFunction = self.__rmNotifBtnAction)
        self._notifList.readonly = True
        self._notifList.cell_double_clicked_event = self.__onSelect
        self._notifList.horizontal_headers = [ 'Timestamp', 'Symbol', 'Price', 'Message']

        self._plusBtn = ControlButton('New Notification')
        self._plusBtn.value= self.__addNotifBtnAction
        if self._user!=None and self._connection!=None:
            self._refresh_button.value= self._refresh
            self._retreive_existing()

    def _refresh(self):
        self._notifList.clear()
        self._retreive_existing()
        
    def _retreive_existing(self):
        pull_list = pull_notifications(self._user, self._connection)

        for i in pull_list:
            ts = pull_list[i]['timestamp']
            datestring=datetime.fromtimestamp(ts/1e3).strftime('%Y-%m-%d %H:%M:%S')
            self._notifList.__add__([datestring, pull_list[i]['symbol'], pull_list[i]['index'], pull_list[i]['message']])

    def add_notification(self, notif):
        super().add_notification(notif)
        self._notifList+=[datetime.fromtimestamp(notif._timestamp).strftime('%Y-%m-%d %H:%M:%S'),
                    notif._symbol, notif._price, notif._message]
        notif.close()

    def __addNotifBtnAction(self):
        win = NotificationWidget(self._user, self._connection)
        win.parent = self
        win.show()

    def __rmNotifBtnAction(self):
        self.remove_notification(self._notifList.selected_row_index)

    def __onSelect(self, row, column):
        timestamp = self._notifList.get_value(0, row)
        symbol = self._notifList.get_value(1, row)
        index = self._notifList.get_value(2, row)
        message = self._notifList.get_value(3, row)
        win = NotificationWidget(self._user, self._connection, timestamp, symbol, index, message)
        win.parent = self
        win.show()

if __name__== "__main__":
    pyforms.start_app(NotificationsWidget, geometry=(400, 400, 600, 600))
