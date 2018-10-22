import pyrebase
from getpass import getpass
from datetime import datetime
import os

def db_connect():
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, 'auth_keys/blackincapp-firebase-adminsdk-8914t-13046da8cf.json')
    config = {
    "apiKey": "AIzaSyDfkaO2XYX6w_vHFCwRuAxiKTwsWQ_mZRs",
    "authDomain": "blackincapp.firebaseapp.com",
    "databaseURL": "https://blackincapp.firebaseio.com",
    "storageBucket": "blackincapp.appspot.com",
    ##Edit this line to point to whereever the auth key is stored
    "serviceAccount": filename
    }
    firebase = pyrebase.initialize_app(config)
    auth = firebase.auth()
    db =firebase.database()
    connection={"Auth": auth, "Database":db}
    return connection



def login_manual(connection):
    email = input('Enter Your Email: ')
    if email == "quit":
        sys.exit()
    password= getpass()
    #authenticate user
    try:
        return connection['Auth'].sign_in_with_email_and_password(email, password)
    except:
        print("Email or password invalid")
        login()

def login(connection, email, password):
    try:
        return connection['Auth'].sign_in_with_email_and_password(email, password)
    except:
        raise ValueError('Email or password invalid')






def post_notification_manual(user, connection):
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

def post_notification(user, connection, symbol, price, message):
    if symbol=='':
        raise ValueError('Symbol Cannot Be Empty')
        return
    if price == '': price = '0.00'
    if message == '':
        raise ValueError('Message Cannot be Empty')
        return
    else:
        #email = user['email']
        #userID = email.split('@')[0]
        userID = cut_email(user)
        notif = {"timestamp":{".sv": "timestamp"}, "symbol": symbol, "price": price, "message": message, "author": userID}
        try:
            connection['Database'].child("notifications").push(notif, user['idToken'])
        except:
            raise ValueError('permission denied')


def pull_notifications(user, connection):
    if user=='':
        raise ValueError('User Invalid')
        return
    if connection=='':
        raise ValueError('Connection Invalid')
        return
    else:
        time = datetime
        notifList = []
        try:
            notifList = connection['Database'].child("notifications").get(user['idToken']).val()
        except:
            notifList = []
        return notifList

def user_dir(user, connection): #localId is persistent for firebase
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
        print('director created')

def pull_users(user, connection):
    if user=='':
        raise ValueError('User Invalid')
        return
    if connection=='':
        raise ValueError('Connection Invalid')
        return
    else:
        user_list=[]
        try:
            user_list = connection['Database'].child("users").get(user['idToken']).val()
            for i in user_list:
                print (user_list[i])
            if user_list==[]:
                raise Exception('No Users')
        except:
            user_list=[]
    return user_list



def cut_email(user):
    return user['email'].split('@')[0]



if __name__== "__main__":
    quit= False
    connection = db_connect()
    user = login_manual(connection)
    pull_users(user, connection)

    #while quit==False:
        #post_notification_manual(user, connection)
