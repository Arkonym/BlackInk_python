


class Notification:
    def __init__(self, timestamp, symbols, index, message):
        self._timestamp = timestamp
        self._symbol   = symbols
        self._price     = index
        self._message   =  message
    @property
    def timestamp(self):
        return self._timestamp
    @timestamp.setter
    def timestamp(self, time):
        self._timestamp= time
    @property
    def symbol(self):
        return self._symbol
    @symbol.setter
    def symbol(self, sym):
        self._symbol=sym
    @property
    def price(self):
        return self.price
    @price.setter
    def price(self, price):
        self._price=price
    @property
    def message(self):
        return self._message
    @message.setter
    def message(self, mess):
        self._message=mess

    @property
    def readOut(self):
        return "{0} {1} {2} {3}".format(self._timestamp, self._symbols, self._price, self._message)
