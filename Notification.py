


class Notification:
    def __init__(self, timestamp, symbols, index, message):
        self._timestamp = timestamp
        self._symbol   = symbols
        self._index     = index
        self._message   =  message

    @property
    def readOut(self):
        return "{0} {1} {2} {3}".format(self._timestamp, self._symbols, self._index, self._message)
