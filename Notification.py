


class Notification:
    def __init__(self, timestamp, symbols, index, message):
        self._timestamp = timestamp
        self._symbol   = symbols
        self._price     = index
        self._message   =  message

    @property
    def readOut(self):
        return "{0} {1} {2} {3}".format(self._timestamp, self._symbols, self._price, self._message)
