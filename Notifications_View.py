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
            plusFunction = self._newNotifBtnAction)

        self._notifList.horizontal_headers = ['Symbol', 'Timestamp']

    def add_notification(self, notif):
        super().add_notification(notif)
        self._notifList+=[notif._timestamp, notif._symbol, notif._index, notif._message]
        notif.close()

    def _newNotifBtnAction(self):
        win = NotificationWidget()
        win.parent = self
        win.show()


if __name__== "__main__": pyforms.start_app(NotificationsWidget, geometry=(400, 400, 600, 600))
