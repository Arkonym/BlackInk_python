import unittest
import DB_Actions

class TestDBactions(unittest.TestCase):
    def TestConnect(self):
        self.assertTrue(db_connect()!=None)

    def TestLogin(self):
        self.account = 'btna3jCd7IUsr0gflHAJl4FYg3D2'
        self.connection = db_connect()
        self.user = login(self.connection, 'blackinkadm1n@gmail.com', 'BlackInk')
        self.assertEqual(self.user['localId'], self.account);

    def TestCutEmail(self):
        self.connection = db_connect()
        self.user = login(self.connection, 'blackinkadm1n@gmail.com', 'BlackInk')
        self.assertEqual(cut_email(self.user), 'blackinkadm1n')

    def TestPullUsers(self):
        self.connection = db_connect()
        self.user = login(self.connection, 'blackinkadm1n@gmail.com', 'BlackInk')
        userList = user_pull(self.user, self.connection)
        self.assertNotEqual(userList, None)
        self.assertEqual(userList[0], 'btna3jCd7IUsr0gflHAJl4FYg3D2')
        for i in userList:
            if i=='btna3jCd7IUsr0gflHAJl4FYg3D2':
                self.assertEqual(userList[i]['name'], 'Test Account')
                self.assertEqual(userList[i]['email'], 'blackinkadm1n@gmail.com')


#class TestNotifsWidget(unittest.TestCase):
#    def


if __name__== '__main__':
    unittest.main()
