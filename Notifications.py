import pickle
import Notification

class Notifications(object):

    def __init__(self):
        self._notifications=[]

    def add_notification(self, notif):
        self._notifications.append(notif)

    def remove_notification(self, symbol):
        return self._notifications.pop(symbol)
    def save(self, filename):
        output= open(filename, 'wb')
        pickle.dump(self._notifications, output)
