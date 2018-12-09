


class Notification:
    def __init__(self, timestamp, symbols, index, message, key=''):
        self._key = key
        self._timestamp = timestamp
        self._symbol   = symbols
        self._price     = index
        self._message   =  message

    @property
    def key(self):
        return self._key
    @key.setter
    def key(self, ky):
        self._key=ky

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
        return self._price
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
        return "{0} {1} {2} {3} {4}".format(self._key, self._timestamp, self._symbol, self._price, self._message)


if __name__ == '__main__':
    tmp = Notification('', 'AAPL', 0.00, 'hello world', '+=+')
    print(tmp.key)
    print(tmp.readOut)
