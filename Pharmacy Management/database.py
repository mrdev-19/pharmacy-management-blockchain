import os
from deta import Deta
from dotenv import load_dotenv

#load env var

load_dotenv(".env")

DETA_KEY=os.getenv("DETA_KEY")
deta=Deta(DETA_KEY)

cred=deta.Base("Creds")

def emailexists(email):
    dev=fetch_all_users()
    emails=[user["email"] for user in dev]
    for user in dev:
        if(user["email"]==email):
            return True
    else:
        return "False"

def getaddr(username):
    dev=fetch_all_users()
    for user in dev:
        if user["key"]==username:
            return user["account"] 

def insert_user(username,password,email,number,account):
    cred.put({"key":username,"password":password,"email":email,"number":number,"curkey":"","account":account})

def authenticate(username,password):
    var=1
    dev=fetch_all_users()
    usernames=[user["key"] for user in dev]
    emails=[user["email"] for user in dev]
    for user in dev:
        if(username==user["key"] and user["password"]==password):
            return True
            var=0
    if(var):
        return False
    
def fetch_all_instances():
    dev=entries.fetch()
    res=dev.items
    return res

def fetch_all_users():
    res=cred.fetch()
    return res.items

def forgot_pass(email,otp):
    dev=fetch_all_users()
    usernames=[user["key"] for user in dev]
    emails=[user["email"] for user in dev]
    for user in dev:
        if(user["email"]==email):
            mkey=user["key"]
            change={"curkey":otp}
            cred.update(change,mkey)