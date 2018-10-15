

class User:
    def __init__(self, email='', name= '', displayname='', permissions=[], services=[]):
        self._email = email
        self._name = name
        self._display_name = displayname
        self._permissions = permissions
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
    def displayname(self):
        return self._display_name
    @displayname.setter
    def displayname(self, dispname):
        self._display_name = dispname

    @property
    def permissions(self):
        return self._permissions
    @permissions.setter
    def permissions(self, perms):
        self._permissions = perms

    @property
    def services(self):
        return self._email
    @services.setter
    def services(self, servs):
        self._services = servs
