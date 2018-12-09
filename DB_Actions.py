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
    except:
        raise ValueError('Email or password invalid')
    if connection['Database'].child('admins').child(user['localId']).get(user['idToken']).val() == True:
        return user
    else:
        raise ValueError('Account not registered as admin')






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

def post_notification(user, connection, notif):
    if notif.symbol=='':
        raise ValueError('Symbol Cannot Be Empty')
        return
    if notif.price == '': notif.price = '0.00'
    if notif.message == '':
        raise ValueError('Message Cannot be Empty')
        return
    else:
        #email = user['email']
        #userID = email.split('@')[0]
        userID = cut_email(user)
        notif = {"timestamp":{".sv": "timestamp"}, "symbol": notif.symbol, "price": notif.price, "message": notif.message, "author": userID}
        try:
            tmp =connection['Database'].child("notifications").push(notif, user['idToken'])
        except:
            raise ValueError('permission denied')
            return
        return tmp

def del_notification(user, connection, key):
    if user=='':
        raise ValueError('User Invalid')
        return
    if connection=='':
        raise ValueError('Connection Invalid')
        return
    else:
        try:
            connection['Database'].child("notifications").child(key).remove()
        except:
            raise ValueError("Key not found")

def update_notification(user, connection, notif):
    if user=='':
        raise ValueError('User Invalid')
        return
    if connection=='':
        raise ValueError('Connection Invalid')
        return
    else:
        try:
            connection['Database'].child("notifications").child(notif.key).update({"symbol": notif.symbol, "message": notif.message, "price": notif.price})
        except:
            raise ValueError("Woops. That didn't work")

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



def user_dir(user, connection): #localId is persisten record key in firebase
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
        user_list=None
        try:
            user_list = connection['Database'].child("users").get().val()
            print(user_list)
            if user_list==None:
                raise Exception('No Users')
        except:
            user_list=None
        #for user in user_list:
            #print (user_list[user])

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
