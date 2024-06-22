import firebase_admin
import pyrebase
from firebase_admin import credentials, firestore
import streamlit as st
from passlib.hash import pbkdf2_sha256
from google.cloud import storage
import re
import requests
import warnings
from dashboard import main
from about import about
import time


warnings.filterwarnings("ignore")
logged_in = False

firebaseConfig = {
 'apiKey': "AIzaSyBnythJMbS6lnHqOAerJ6F0EBTrJylNeTY",
  'authDomain': "heart-disease-predictor-730c3.firebaseapp.com",
  'databaseURL': "https://heart-disease-predictor-730c3-default-rtdb.europe-west1.firebasedatabase.app",
  'projectId': "heart-disease-predictor-730c3",
  'storageBucket': "heart-disease-predictor-730c3.appspot.com",
  'messagingSenderId': "740324649038",
  'appId': "1:740324649038:web:2c0767947e27f92a3afb1f",
  'measurementId': "G-M1RN5PLLXW"
};

#Firebase Authentication
firebase=pyrebase.initialize_app(firebaseConfig)
auth=firebase.auth()

#Database
db=firebase.database()
storage=firebase.storage()


st.sidebar.title(":orange[Choose Menu]")

#Authentication
# Function to validate password

def clear_query_params():
    #st.experimental_set_query_params()
    st.query_params.clear()
def submit_action(valid_email, valid_pwd, valid_name):
    st.session_state['parameters'] = {'email': valid_email, 'password': valid_pwd, 'username': valid_name}
    st.session_state['submitted'] = True
    try:
                
        user=auth.create_user_with_email_and_password(valid_email,valid_pwd)
        st.success("Account Created Successfully!")
        st.balloons()

        #Sign in
        user=auth.sign_in_with_email_and_password(valid_email,valid_pwd)
        db.child(user['localId']).child("UserName").set(valid_name)
        db.child(user['localId']).child("ID").set(user['localId'])

        st.title("Welcome "+valid_name)
        st.info("👈 Log in to your account to get features.")
        #st.experimental_rerun()
    except requests.exceptions.HTTPError as e:
        st.error("User already exist.")
        #st.experimental_rerun()
        time.sleep(2) 

def validate_email(email):
    patt=r"[a-zA-Z0-9]+@+[a-zA-Z]+.[a-zA-Z]{2,}$"
    if re.match(patt,email):
        return email
    else:
        return "Type a valid email address!"

def validate_password(password):
    if len(password) < 8:
        return "Password must be at least 8 characters long"
    if len(password) > 64:
        return "Password cannot exceed 64 characters"
    if not re.search(r"[A-Z]", password):
        return "Password must contain at least one uppercase letter"
    if not re.search(r"[a-z]", password):
        return "Password must contain at least one lowercase letter"
    if not re.search(r"[0-9]", password):
        return "Password must contain at least one digit"
    if not re.search(r"[@$!%*?&#]", password):  # Adjust special characters as needed
        return "Password must contain at least one special character (@$!%*?&#)"
    return password

def validate_name(name):
    if len(name)<5:
        return("Username can't be less than 5 characters")
    if len(name)>200:
        return("Username can't exceed 200 characters")
    if len(re.findall(r"[A-Za-z]", name)) < 3:
        return "Username must contain at least three alphabetic characters"
    if re.search(r" +",name):
        return "Username can't contain space"
    match=re.search(r"[^a-zA-Z0-9\s]",name)
    if match:
        return "Username can't contain any special character"
    else:
        return name

def forgot_password():
    email = st.text_input("Enter your email address to reset your password")
    reset_button = st.button("Send Password Reset Email")

    if reset_button:
        try:
            auth.send_password_reset_email(email)
            st.success("Password reset email sent! Please check your inbox.")
        except requests.exceptions.HTTPError as e:
            error_msg = e.response.json().get('error', {}).get('message', 'An error occurred.')
            st.error(error_msg)
            st.warning("Invalid email")

def signup():
    st.title("Sign Up")

    email=st.text_input("Please enter your email id")
    password=st.text_input("Password", type='password')
    username=st.text_input("Please enter an user name")
    submit=st.button("Submit")
    valid_pwd=validate_password(password)
    valid_email=validate_email(email)
    valid_name=validate_name(username)
    if len(username)==0 and len(password)==0:
        st.warning("Type your username and password to get started")
    elif valid_pwd!=password:
        st.warning(valid_pwd)
    elif (valid_name)!=username:
        st.warning(valid_name)
    elif (valid_email)!=email:
        st.warning(valid_email)
    else:

        #submit=st.button("Submit")
        if submit:
            submit_action(valid_email, valid_pwd, valid_name)
            
           
            #login()


def login():
    st.title("Log In your account")
    email=st.text_input("Enter your registered email id")
    password=st.text_input("Enter your Password", type='password')
    valid_pwd=validate_password(password)
    valid_email=validate_email(email)
    btn1,btn2=st.columns(2)
    submit=st.button("Log In")
    if st.button("Forgot Password? 😟"):
        forgot_password()
    if len(email)==0 and len(password)==0:
        st.warning("Enter your email id and password")
    elif valid_pwd!=password:
        st.warning("Correctly type your password")
    elif (valid_email)!=email:
        st.warning("Correctly type your password")
    else:
       
        if submit:
            try:
                user=auth.sign_in_with_email_and_password(valid_email,valid_pwd)
                name = db.child(user['localId']).child("UserName").get().val()
                    # Redirect to dashboard with query parameter 'name'
                try:
                    st.query_params(name=name)
                except:
                    pass
                logged_in = True
                st.session_state['logged_in'] = True
                st.success("Credentials matched successfully")
                st.info("Click Log In Button again")    
                    
                return name
            except requests.exceptions.HTTPError as e:
                if e.response is not None:
                    error_msg = e.response.json()['error']['message']
                    if 'TOO_MANY_ATTEMPTS_TRY_LATER' in error_msg:
                        st.error("Access to this account has been temporarily disabled due to many failed login attempts. Please reset your password or try again later.")
                    else:
                        st.error("An error occurred: {}".format(error_msg))
                else:
                    st.error("Invalid Credentials")
                    #time.sleep(2)
            #return ("Hello "+name)
       

def logout():
    btn1,btn2,btn3,btn4,btn5,btn6=st.columns(6)
    with btn6:
        if st.button("Logout"):
            st.session_state['logged_in'] = False
            st.session_state['username']=""
            clear_query_params()
            st.experimental_rerun()

def dashboard(name):
    st.title(f"Welcome :violet[{name}] to Your Dashboard")
    logout()
    st.subheader(":blue[Predict if you are prone to any heart disease.]")

    

#Choice

choice=st.sidebar.radio("Choose an option",("Log In","Sign Up","About","Home"))

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
    
if st.session_state['logged_in']:
    clear_query_params()
    #st.write(f"Logged in as {st.session_state['username']}")
    if choice=="Home":
        dashboard(st.session_state['username'])
        main()

    else:
        if choice=="Sign Up":
            #signup()
            logout()
            st.warning("Log Out First to sign up with new account")
            
        if choice=="Log In":
            # st.title("Don't Have an account?")
            # submit=st.button("Create one")
            logout()
            st.success(f"Already Logged In as {st.session_state['username']}")
            
            # if submit:
            #     signup()
            # else:
            #     name=login()
        if choice=="About":
            logout()
            about()

else:
    
    if choice=="Sign Up":
        # Initialize session state for parameters and submission
        # if 'parameters' not in st.session_state:
        #     st.session_state['parameters'] = {}
        # if 'submitted' not in st.session_state:
        #     st.session_state['submitted'] = False
        signup()
        # if st.session_state['submitted']:
        #     st.experimental_rerun()
        st.subheader(":violet[Already have an account?]")
        st.info("👈 Log In your account.")
    if choice=="Log In":
        st.subheader(":violet[Don't Have an account?]")
        st.info("👈 Sign Up to create new account.")
        name=login()
        if name:
                #st.sidebar.title("Choose Home")
                # st.success("Logged in successfully")
                # st.session_state['logged_in'] = True
                # st.session_state['username'] = name
                #st.write("Press Log In Once again")
            st.session_state['username'] = name
    if choice=="Home":
        st.info("Log In First to get all the features!!")
    if choice=="About":
        about()

