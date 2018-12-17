

class User: #pragma no cover
    def __init__(self, uid='', email='', name= '',  services=[]):
        self._uid = uid
        self._email = email
        self._name = name
        self._services= services

    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, name):
        self._name = name

    @property
    def email(self):
        return self._email
    @email.setter
    def email(self, email):
        self._email = email

    @property
    def uid(self):
        return self._uid
    @uid.setter
    def uid(self, key):
        self._uid = key

    @property
    def services(self):
        return self._email
    @services.setter
    def services(self, servs):
        self._services = servs
