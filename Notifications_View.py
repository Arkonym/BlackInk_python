import pyforms
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from pyforms.basewidget import BaseWidget
from pyforms.controls import ControlList, ControlButton, ControlToolButton
from Notifications import Notifications
from Notification import Notification
from Notification_View import NotificationWidget
from DB_Actions import db_connect, login_manual, pull_notifications, del_notification
from datetime import datetime
from Error_Windows import ErrorWin



class NotificationsWidget(Notifications, BaseWidget):
    def __init__(self, user = None, connection = None):
        Notifications.__init__(self)
        BaseWidget.__init__(self)
        self._user = user
        self._connection = connection
        self._refresh_button = ControlToolButton('Refresh', maxheight= 50, maxwidth= 100)

        self._notifCache=None
        self._notifList = ControlList('Notifications',
            select_entire_row = True)
        self._notifList.readonly = True
        self._notifList.cell_double_clicked_event = self.__onDouble
        #self._notifList.item_selection_changed_event = self.__softSelect
        self._notifList.horizontal_headers = [ 'Timestamp', 'Symbol', 'Price', 'Message']
        self._notifList.add_popup_menu_option('Edit', function_action= self.__popEdit)
        self._notifList.add_popup_menu_option('Delete', function_action= self.__deleteNotif)

        self._plusBtn = ControlButton('New Notification')
        self._plusBtn.value= self.__addNotifBtnAction
        if self._user!=None and self._connection!=None:
            self._refresh_button.value= self._refresh
            self._retreive_existing()



    def _refresh(self):
        self._notifList.clear()
        self._retreive_existing()
        if self.parent!=None: self.parent.persist_login()

    def _retreive_existing(self):
        try:
            pull_list = pull_notifications(self._user, self._connection)
            self._notifCache=pull_list
        except ValueError as err:
            err= ErrorWin(err)
            err.parent = self
            err.show()
            return
        if pull_list:
            for i in pull_list:
                ts = pull_list[i]['timestamp']
                datestring=datetime.fromtimestamp(ts/1e3).strftime('%Y-%m-%d %H:%M:%S')
                self._notifList.__add__([datestring, pull_list[i]['symbol'], pull_list[i]['price'], pull_list[i]['message']])


    def __addNotifBtnAction(self):
        if self.parent!=None: self.parent.persist_login()
        win = NotificationWidget(self._user, self._connection, '', '', '', '', 'new')
        win.parent = self
        win.show()



    def __rmNotifBtnAction(self):
        self.__deleteNotif(self)

    def __onDouble(self, row, column):
        if self.parent!=None: self.parent.persist_login()
        timestamp = self._notifList.get_value(0, row)
        symbol = self._notifList.get_value(1, row)
        index = self._notifList.get_value(2, row)
        message = self._notifList.get_value(3, row)
        win = NotificationWidget(self._user, self._connection, timestamp, symbol, index, message, 'view')
        win.parent = self
        win.show()

    def __popEdit(self):
        row = self._notifList.selected_row_index
        timestamp = self._notifList.get_value(0, row)
        symbol = self._notifList.get_value(1, row)
        index = self._notifList.get_value(2, row)
        message = self._notifList.get_value(3, row)
        for i in self._notifCache:
            if self._notifCache[i]['message']== message:
                key = i
                #print("popedit key found: " + key)
        win = NotificationWidget(self._user, self._connection, timestamp, symbol, index, message, "edit", key)
        win.parent = self
        win.show()


    def __softSelect(self, row, column):
        self._notifList.form.get_value(row, column)

    def __deleteNotif(self):
        row = self._notifList.selected_row_index
        message = self._notifList.get_value(3, row)
        for i in self._notifCache:
            if self._notifCache[i]['message']== message:
                key= i
        try:
            del_notification(self._user, self._connection, key)
            self._notifList.__sub__(row)
        except ValueError as error:
            err= ErrorWin(error)
            err.parent = self
            err.show()
            return



if __name__== "__main__":
    pyforms.start_app(NotificationsWidget, geometry=(400, 400, 600, 600))
