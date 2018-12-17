from DB_Actions import db_connect, login, cut_email, pull_users, toggle_admin
from DB_Actions import pull_notifications, post_notification, del_notification
from Notification import Notification
from User import User
from datetime import datetime

import unittest


class TestDBactions(unittest.TestCase):
    def testConnect(self):
        self.connection= db_connect()
        self.assertNotEqual(self.connection, None)

    def testLogin(self):
        self.account = 'btna3jCd7IUsr0gflHAJl4FYg3D2'
        self.connection = db_connect()
        self.user = login(self.connection, 'blackinkadm1n@gmail.com', 'BlackInk')
        self.assertEqual(self.user['localId'], self.account);

    def testLoginNonAccount(self):
        self.connection = db_connect()
        self.failstate=False
        try:
            self.user = login(self.connection, 'doesntexist@gmail.com', 'password')
        except ValueError as e:
            self.failstate=True
        self.assertTrue(self.failstate)

    def testToggleAdmin(self):
        self.other_user_key = 'ygSLcuk1vFXo8VSuu0pFIgGGqg72'
        self.connection = db_connect()
        self.user1 = login(self.connection, 'blackinkadm1n@gmail.com', 'BlackInk')
        self.failstate = False
        try:
            toggle_admin(self.user1, self.connection, self.other_user_key)
        except ValueError as e:
            self.failstate = True
        self.assertFalse(self.failstate)
        try:
            self.user2 = login(self.connection, 'rsaitta@mail.csuchico.edu', 'Topgun01')
        except ValueError as e:
            self.failstate = True
        toggle_admin(self.user1, self.connection, self.other_user_key) #undo toggle
        self.assertTrue(self.failstate)


    def testToggleAdmin_self(self):
        self.other_user_key = 'btna3jCd7IUsr0gflHAJl4FYg3D2'
        self.connection = db_connect()
        self.user1 = login(self.connection, 'blackinkadm1n@gmail.com', 'BlackInk')
        self.failstate = False
        try:
            toggle_admin(self.user1, self.connection, self.other_user_key)
        except ValueError as e:
            self.failstate = True
        self.assertTrue(self.failstate)

    def testToggleAdmin_non_account(self):
        self.other_user_key = 'not_a_key'
        self.connection = db_connect()
        self.user1 = login(self.connection, 'rsaitta@mail.csuchico.edu', 'Topgun01')
        self.failstate = False
        try:
            toggle_admin(self.user1, self.connection, self.other_user_key)
        except ValueError as e:
            self.failstate = True
        self.assertTrue(self.failstate)

    def testToggleAdmin_no_user(self):
        self.other_user_key = ''
        self.connection = db_connect()
        self.user1 = login(self.connection, 'blackinkadm1n@gmail.com', 'BlackInk')
        self.failstate = False
        try:
            toggle_admin(None, self.connection, self.other_user_key)
        except ValueError:
            self.failstate = True
        self.assertTrue(self.failstate)

    def testToggleAdmin_no_connection(self):
        self.other_user_key = ''
        self.connection = db_connect()
        self.user1 = login(self.connection, 'blackinkadm1n@gmail.com', 'BlackInk')
        self.failstate = False
        try:
            toggle_admin(self.user1, None, self.other_user_key)
        except ValueError:
            self.failstate = True
        self.assertTrue(self.failstate)

    def testToggleAdmin_no_account_key(self):
        self.other_user_key = ''
        self.connection = db_connect()
        self.user1 = login(self.connection, 'blackinkadm1n@gmail.com', 'BlackInk')
        self.failstate = False
        try:
            toggle_admin(self.user1, self.connection, self.other_user_key)
        except ValueError:
            self.failstate = True
        self.assertTrue(self.failstate)


    def testCutEmail(self):
        self.connection = db_connect()
        self.user = login(self.connection, 'blackinkadm1n@gmail.com', 'BlackInk')
        self.assertEqual(cut_email(self.user), 'blackinkadm1n')

    def testPullUsers(self):
        self.connection = db_connect()
        self.user = login(self.connection, 'blackinkadm1n@gmail.com', 'BlackInk')
        userList = pull_users(self.user, self.connection)
        self.assertNotEqual(userList, None)
        self.assertEqual(list(userList.keys())[0], 'btna3jCd7IUsr0gflHAJl4FYg3D2')
        for i in userList:
            if i=='btna3jCd7IUsr0gflHAJl4FYg3D2':
                self.assertEqual(userList[i]['name'], 'Test Account')
                self.assertEqual(userList[i]['email'], 'blackinkadm1n@gmail.com')

    def testPullUsers_no_user(self):
        self.connection = db_connect()
        self.failstate = False
        try:
            userList= pull_users(None, self.connection)
        except ValueError:
            self.failstate = True
        self.assertTrue(self.failstate)

    def testPullUsers_no_connection(self):
        self.connection = db_connect()
        self.user = login(self.connection, 'blackinkadm1n@gmail.com', 'BlackInk')
        self.failstate = False
        try:
            userList= pull_users(self.user, None)
        except ValueError:
            self.failstate = True
        self.assertTrue(self.failstate)

    def testPullNotifications(self):
        self.connection = db_connect()
        self.user = login(self.connection, 'blackinkadm1n@gmail.com', 'BlackInk')
        notifList = pull_notifications(self.user, self.connection)
        self.assertNotEqual(notifList, None)

    def testPullNotif_no_user(self):
        self.connection= db_connect()
        self.user=''
        self.failstate = False
        try:
            pull_notifications(self.user, self.connection)
        except ValueError:
            self.failstate=True
        self.assertTrue(self.failstate)

    def testPullNotif_no_connection(self):
        self.connection = db_connect()
        self.user = login(self.connection, 'blackinkadm1n@gmail.com', 'BlackInk')
        self.failstate = False
        try:
            pull_notifications(self.user, None)
        except ValueError:
            self.failstate=True
        self.assertTrue(self.failstate)

    def testPostNotification(self):
        self.connection = db_connect()
        self.user = login(self.connection, 'blackinkadm1n@gmail.com', 'BlackInk')
        self.failstate = False
        notif = Notification('', 'GOOGL', 0.00, 'Hello World')
        try:
            key = post_notification(self.user, self.connection, notif)
        except ValueError:
            self.failstate = True
        self.assertFalse(self.failstate)
        del_notification(self.user, self.connection, key['name'])

    def testPostNotification_empty_sym(self):
        self.connection = db_connect()
        self.user = login(self.connection, 'blackinkadm1n@gmail.com', 'BlackInk')
        notif = Notification()
        try:
            post_notification(self.user, self.connection, notif)
        except ValueError:
            self.failstate = True
        self.assertTrue(self.failstate)

    def testPostNotification_empty_message(self):
        self.connection = db_connect()
        self.user = login(self.connection, 'blackinkadm1n@gmail.com', 'BlackInk')
        notif = Notification()
        try:
            post_notification(self.user, self.connection, notif)
        except ValueError:
            self.failstate = True
        self.assertTrue(self.failstate)

    def testDeleteNotification(self):
        self.connection =db_connect()
        self.user = login(self.connection, 'blackinkadm1n@gmail.com', 'BlackInk')
        self.failstate = False
        notif = Notification('', 'GOOGL', 0.00, 'Hello World')
        key= post_notification(self.user, self.connection, notif)
        notifList = pull_notifications(self.user, self.connection)
        self.assertNotEqual(notifList, None)
        for i in notifList:
            if i == key['name']:
                try:
                    del_notification(self.user, self.connection, i)
                except:
                    self.failstate = True
                self.assertFalse(self.failstate)
                break

    def testDeleteNotification_no_match(self):
        self.connection =db_connect()
        self.user = login(self.connection, 'blackinkadm1n@gmail.com', 'BlackInk')
        self.failstate = False
        try:
            del_notification(self.user, self.connection, 'not_a_key')
        except:
            self.failstate= True
        self.assertTrue(self.failstate)

    def testDeleteNotification_no_user(self):
        self.connection= db_connect()
        self.failstate = False
        try:
            del_notification(None, self.connection, None)
        except:
            self.failstate = True
        self.assertTrue(self.failstate)

    def testDeleteNotification_no_connection(self):
        self.connection= db_connect()
        self.user = login(self.connection, 'blackinkadm1n@gmail.com', 'BlackInk')
        self.failstate = False
        try:
            del_notification(self.user, None, None)
        except:
            self.failstate = True
        self.assertTrue(self.failstate)

    def testDeleteNotification_no_key(self):
        self.connection= db_connect()
        self.user = login(self.connection, 'blackinkadm1n@gmail.com', 'BlackInk')
        self.failstate = False
        try:
            del_notification(self.user, self.connection, None)
        except:
            self.failstate = True
        self.assertTrue(self.failstate)





if __name__== '__main__': #pragma no cover
    unittest.main()
