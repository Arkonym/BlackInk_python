import pyforms
from pyforms.basewidget import BaseWidget
from pyforms.controls import ControlList, ControlButton
from Notifications import Notifications
from Notification import Notification
from Notification_View import NotificationWidget


class NotificationsWidget(Notifications, BaseWidget):
    def __init__(self, connection = None):
        Notifications.__init__(self)
        BaseWidget.__init__(self)
        self._notifList = ControlList('Notifications',
            plusFunction = self.__addNotifBtnAction,
            minusFunction = self.__rmNotifBtnAction)

        self._notifList.horizontal_headers = [ 'Timestamp', 'Symbol', 'Index', 'Message']
        self._plusBtn = ControlButton('New Notification')
        self._plusBtn.value= self.__addNotifBtnAction

    def add_notification(self, notif):
        super().add_notification(notif)
        self._notifList+=[notif._timestamp, notif._symbol, notif._index, notif._message]
        notif.close()

    def __addNotifBtnAction(self):
        win = NotificationWidget()
        win.parent = self
        win.show()

    def __rmNotifBtnAction(self):
        self.remove_notification(self._notifList.selected_row_index)


if __name__== "__main__": pyforms.start_app(NotificationsWidget, geometry=(400, 400, 600, 600))
