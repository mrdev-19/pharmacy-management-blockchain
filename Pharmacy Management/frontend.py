import streamlit as st
from streamlit_option_menu import option_menu
import database as db
import validations as val
import time
import send_mail as sm
import hasher as hs
import main as send
#---------------------------------------------------
# page config settings:

page_title="Pharmacy Management"
page_icon=":hospital:"
layout="centered"

st.set_page_config(page_title=page_title,page_icon=page_icon,layout=layout)
st.title(page_title+" "+page_icon)

#--------------------------------------------------
#hide the header and footer     

hide_ele="""
        <style>
        #Mainmenu {visibility:hidden;}
        footer {visibility:hidden;}
        header {visibility:hidden;}
        </style>
        """
st.markdown(hide_ele,unsafe_allow_html=True)
#---------------------------------------------------
curlogin=""
otp=""

def log_sign():
    selected=option_menu(
        menu_title=None,
        options=["Login","Signup"],
        icons=["bi bi-fingerprint","bi bi-pencil-square"],
        orientation="horizontal"
    )
    global submit
    if(selected=="Login"):
        tab1,tab2=st.tabs(["Login","Forgot Password"])
        with tab1:
            with st.form("Login",clear_on_submit=True):
                st.header("Login")
                username=st.text_input("Username")
                password=st.text_input("Password",type="password")
                submit=st.form_submit_button()
                if(submit):
                    if(username=="" or password==""):
                        st.warning("Enter your login credentials")
                    else:
                        password=hs.hasher(password)
                        if(db.authenticate(username,password)):
                            curlogin=username
                            st.session_state["curlogin"]=username
                            st.session_state["key"]="main"
                            st.experimental_rerun()
                        else:
                            st.error("Please check your username / password ")
        with tab2:
            with st.form("Forgot Password",clear_on_submit=True):
                st.header("Forgot Password")
                email=st.text_input("Email")
                submit=st.form_submit_button()
                if(submit):
                    if(email==""):
                        st.warning("Enter your email")
                    elif(not db.emailexists(email)):
                        st.warning("User with associated email is not found,kindly recheck the email!")
                    else:
                        otp=sm.forgot_password(email)
                        db.forgot_pass(email,otp)
                        st.success("Check your email for password reset instructions!.")
                
    elif(selected=="Signup"):
         with st.form("Sign Up",clear_on_submit=False):
            st.header("Sign Up")
            email=st.text_input("Enter your email")
            number=st.text_input("Enter your Mobile Number")
            username=st.text_input("Enter your username")
            password=st.text_input("Enter your password",type="password")
            submit=st.form_submit_button()
            if(submit):
                dev=db.fetch_all_users()
                usernames=[]
                emails=[]
                numbers=[]
                accounts=[]
                for user in dev:
                    usernames.append(user["key"])
                    emails.append(user["email"])
                    numbers.append(user["number"])
                    accounts.append(user["account"])
                var=True
                if(val.validate_email(email)==False):
                    st.error("Enter email in a valid format like 'yourname@org.com'")
                elif(email in emails):
                    st.error("email already exists!\nTry with another email !")
                elif(val.validate_mobile(number)==False):
                    st.error("Please Check your mobile Number")
                elif(number in numbers):
                    st.error("Phone number already exists\nTry with another number")
                elif(val.validate_username(username)==False):
                    st.error("Invalid Username!\nUsername must be between 4-20 characters and can contain only _ and . , and username cannot begin with special characters")
                elif(username in usernames):
                    st.error("Username already exists!\nTry another username !")
                elif(val.validate_password(password)==False):
                    st.error("Password must be between 6-20 characters in length and must have at least one Uppercase Letter , Lowercase letter , numeric character and A Special Symbol(#,@,$,%,^,&,+,=)")
                elif(var):
                    password=hs.hasher(password)
                    db.insert_user(username,password,email,number,account_address)
                    st.success("Signed Up Successfully....Redirecting!!")
                    time.sleep(2)
                    st.session_state["curlogin"]=username
                    st.session_state["key"]="main"
                    st.experimental_rerun()

def main():
    btn=st.button("Logout")
    if(btn):
        st.session_state["key"] = "log_sign"
        st.experimental_rerun()
    selected=option_menu(
            menu_title=None,
            options=["Transfer Crypto","Check Balance"],
            icons=["bi bi-search","bi bi-box"],
            orientation="horizontal"
        )
    if(selected=="Transfer Crypto"):
        with st.form("Transfer Crypto",clear_on_submit=False):
            st.header("Transfer Crypto")
            sender=st.text_input("Enter your Address")
            private_key=st.text_input("Enter Your Private Key")
            recipient=st.text_input("Enter the recipient Address")
            amount=st.number_input("Enter the amount to send")
            submit=st.form_submit_button()
            if(submit):
                # print(curlogin)
                # print(db.getaddr(curlogin))
                send.transfer_eth(sender,recipient,private_key,amount)
    elif(selected=="Check Balance"):
        with st.form("Check Balance",clear_on_submit=False):
            st.header("Check Balance")
            acc=st.text_input("Enter your address")
            submit=st.form_submit_button()
            if(submit):
                st.write(send.get_balance(acc))
    
    

if "key" not in st.session_state:
    st.session_state["key"] = "log_sign"

if st.session_state["key"] == "log_sign":
    log_sign()

elif st.session_state["key"] == "main":
    main()
