import pyrebase
from urllib.error import HTTPError
from getpass import getpass
from datetime import datetime
import os

def db_connect():
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, 'pathtoyourauthkey.json')
    config = {
    "apiKey": "AIzaSyDfkaO2XYX6w_vHFCwRuAxiKTwsWQ_mZRs",
    "authDomain": "yourapp.firebaseapp.com",
    "databaseURL": "https://yourapp.firebaseio.com",
    "storageBucket": "yourapp.appspot.com",
    ##Edit this line to point to whereever the auth key is stored
    "serviceAccount": filename
    }
    firebase = pyrebase.initialize_app(config)
    auth = firebase.auth()
    db =firebase.database()
    connection={"Auth": auth, "Database":db}
    return connection



def login_manual(connection):# pragma no cover
    email = input('Enter Your Email: ')
    if email == "quit":
        sys.exit()
    email.replace('\t', "")
    email.replace(" ", "")
    password= getpass()
    password.replace(" ", "")
    password.replace("\t", "")
    #authenticate user
    try:
        return connection['Auth'].sign_in_with_email_and_password(email, password)
    except:
        print("Email or password invalid")
        login_manual()

def login(connection, email, password):
    email.replace(" ", "")
    email.replace("\t", "")
    password.replace("\t", "")
    try:
        user = connection['Auth'].sign_in_with_email_and_password(email, password)
    except HTTPError:
        raise ValueError("Email does not match a registered account")
    except:
        raise ValueError('Email or password invalid')
    if connection['Database'].child('admins').child(user['localId']).get(user['idToken']).val() == True:
        return user
    else:
        raise ValueError('Account not registered as admin')






def post_notification_manual(user, connection):# pragma no cover
    try:
        comp=input('Enter ticker symbol: ')
    except:
        comp = " "
    if comp=="quit":
        sys.exit()
    try:
        message =input('Enter advisory ')
    except:
        message = " "
    try:
        price =input('Enter price ')
    except:
        price = "0.00"

    notif = {"timestamp":{".sv": "timestamp"}, "symbol": comp, "price": price, "message": message}
    try:
        connection['Database'].child("notifications").push(notif, user['idToken'])
        notif['timestamp'] = datetime.datetime.now().timestamp()
        return notif
    except:
        print_tb()
        raw_input()

def post_notification(user, connection, notif):
    if notif.symbol=='':
        raise ValueError('Symbol Cannot Be Empty')
    if notif.price == '': notif.price = '0.00'
    if notif.message == '':
        raise ValueError('Message Cannot be Empty')
    else:
        userID = cut_email(user)
        notif = {"timestamp":{".sv": "timestamp"}, "symbol": notif.symbol, "price": notif.price, "message": notif.message, "author": userID}
        try:
            tmp =connection['Database'].child("notifications").push(notif, user['idToken'])
        except:
            raise ValueError('permission denied')
        #print (tmp)
        return tmp

def del_notification(user, connection, key):
    if user=='' or user == None:
        raise ValueError('User Invalid')
    if connection=='' or user == None:
        raise ValueError('Connection Invalid')
    if key=='' or key == None:
        raise ValueError('Missing key')
    else:
        try:
            removed = connection['Database'].child("notifications").child(key).remove()
        except:
            raise ValueError("Key not found")
        if removed == None or removed =='':
            raise ValueError("No match found")

def update_notification(user, connection, notif): #pragma no cover
    if user=='':
        raise ValueError('User Invalid')
    if connection=='':
        raise ValueError('Connection Invalid')
    else:
        try:
            connection['Database'].child("notifications").child(notif.key).update({"symbol": notif.symbol, "message": notif.message, "price": notif.price})
        except:
            raise ValueError("Woops. That didn't work")


def pull_notifications(user, connection):
    if user=='' or user == None:
        raise ValueError('User Invalid')
    if connection=='' or connection == None:
        raise ValueError('Connection Invalid')
    else:
        time = datetime
        notifList = []
        try:
            notifList = connection['Database'].child("notifications").get(user['idToken']).val()
        except:
            notifList = []
        return notifList


#not used
def user_dir(user, connection): #pragma no cover
    userDir=[]
    try:
        userDir = connection['Database'].child("users").child(user['localId']).get(user['idToken']).val()
        for i in userDir:
            print (userDir[i])
        if userDir==[]:
            raise Exception('no directory found')
        else:
            return userDir
    except:
        u = {"name":'', 'email':user['email']}
        connection['Database'].child("users").child(user['localId']).set(u, user['idToken'])
        print('directory created')

def pull_users(user, connection):
    if user=='' or user ==None:
        raise ValueError('User Invalid')
    if connection=='' or connection ==None:
        raise ValueError('Connection Invalid')
    else:
        user_list=None
        try:
            user_list = connection['Database'].child("users").get().val()
            if user_list==None:
                raise Exception('No Users')
        except:
            user_list=None
    return user_list

def add_user(user, connection, new_user): #pragma no cover
    if user=='':
        raise ValueError('User Invalid')
    if connection=='':
        raise ValueError('Connection Invalid')
    else:
        try:
            connection['Database'].child('users').push(new_user, user['idToken'])
        except:
            raise HTTPError('Auth refused')

def toggle_admin(user, connection, user_id):
    if user=='' or user == None:
        raise ValueError('User Invalid')
    if connection=='' or user == None:
        raise ValueError('Connection Invalid')
    if user_id == '' or user_id == None:
        raise ValueError('Missing account key')
    else:
        users = connection['Database'].child("users").shallow().get()
        admins = connection['Database'].child('admins').shallow().get(user['idToken'])
        if user['localId']==user_id:
            raise ValueError("Cannot remove self as admin")
        elif user_id in users.val() and user_id not in admins.val():
            try:
                connection['Database'].child('admins').update({user_id: True}, user['idToken'])
            except:
                raise HTTPError('Auth refused')
        elif user_id in admins.val():
            try:
                connection['Database'].child('admins').child(user_id).remove()
            except:
                raise HTTPError('Auth refused')
        else: raise ValueError('User not found')


def cut_email(user):
    return user['email'].split('@')[0]


from Notification import Notification
if __name__== "__main__":#pragma no cover

    quit= False
    connection = db_connect()
    user = login(connection, 'rsaitta@mail.csuchico.edu', 'Topgun01')
    #toggle_admin(user, connection, 'btna3jCd7IUsr0gflHAJl4FYg3D2')
    notif = Notification('', 'GOOGL', 0.00, 'Hello World')

    post_notification(user, connection, notif)
    #while quit==False:
        #post_notification_manual(user, connection)
