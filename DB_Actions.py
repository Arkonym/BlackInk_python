import pyrebase
from getpass import getpass
import datetime

def db_connect():
    config = {
    "apiKey": "AIzaSyDfkaO2XYX6w_vHFCwRuAxiKTwsWQ_mZRs",
    "authDomain": "blackincapp.firebaseapp.com",
    "databaseURL": "https://blackincapp.firebaseio.com",
    "storageBucket": "blackincapp.appspot.com",
    "serviceAccount": "G:/BlackInk_python/auth_keys/blackincapp-firebase-adminsdk-8914t-13046da8cf.json."
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
        print("Email or password invalid")
        login()






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

    notif = {"timestamp":{".sv": "timestamp"}, "symbol": comp, "index": price, "message": message}
    try:
        connection['Database'].child("notifications").push(notif, user['idToken'])
        notif['timestamp'] = datetime.datetime.now().timestamp()
        return notif
    except:
        print_tb()
        raw_input()

def post_notification(user, connection, symbol, index, message):
    if symbol==None: raise ValueError('Symbol Cannot Be Empty')
    if index == None: index = '0.00'
    if message == None: raise ValueError('Message Cannot be Empty')
    else:
        notif = {"timestamp":{".sv": "timestamp"}, "symbol": symbol, "index": index, "message": message, "author": user['email']}
        connection['Database'].child("notifications").push(notif, user['idToken'])



#def pull_notifications(user, connection):

if __name__== "__main__":
    quit= False
    connection = db_connect()
    user = login_manual(connection)
    while quit==False:
        post_notification_manual(user, connection)
