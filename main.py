import firebase_admin
import pyrebase
from firebase_admin import credentials, firestore
import streamlit as st
from passlib.hash import pbkdf2_sha256
from google.cloud import storage
import re
import requests
from datetime import datetime, timedelta
import warnings
from dashboard import main
from about import about
from fire import base
from firebase_admin import credentials, auth
import time
import json

warnings.filterwarnings("ignore")
logged_in = False

firebaseConfig=base()

#Firebase Authentication
firebase=pyrebase.initialize_app(firebaseConfig)
auth2=firebase.auth()


# Initialize the Firebase Admin SDK (if not already initialized)
try:
    firebase_admin.get_app()
except ValueError:
    try:
        cred = credentials.Certificate("source.json")
        firebase_admin.initialize_app(cred, {'projectId': 'heart-disease-predictor-730c3'})
    except Exception as e:
        print("Error initializing Firebase Admin SDK:", e)

#Database
db=firebase.database()
storage=firebase.storage()



st.sidebar.title(":orange[Choose Menu]")

#Authentication
# Function to validate password

def clear_query_params():
    #st.experimental_set_query_params()
    st.query_params.clear()
# Initialize session state variables
# if 'email' not in st.session_state:
#     st.session_state['mail'] = ''
# if 'password' not in st.session_state:
#     st.session_state['pwd'] = ''
# if 'username' not in st.session_state:
#     st.session_state['username'] = ''
# if 'parameters' not in st.session_state:
#     st.session_state['parameters'] = {}
# if 'submitted' not in st.session_state:
#     st.session_state['submitted'] = False
if 'clear' not in st.session_state:
    st.session_state['clear'] = False

def submit_action(valid_email, valid_pwd, valid_name):
    st.session_state['parameters'] = {'email': valid_email, 'password': valid_pwd, 'username': valid_name}
    st.session_state['submitted'] = True
    username_exists = False  # Initialize the variable here
    try:
        users = db.child("").get().val()  # Assuming your users are stored under the root node of your database
        if users:
            for user_id, user_data in users.items():
                username = user_data.get("UserName")
                if username == valid_name:
                    username_exists = True
                    break
        if username_exists:
            st.error("Username already taken. Please choose a different username.")
            #clear_inputs()  # Clear the inputs after successful submission
            #st.experimental_rerun()
        else:    
            user=auth2.create_user_with_email_and_password(valid_email,valid_pwd)
            user = auth2.refresh(user['refreshToken'])
            link = auth2.send_email_verification(user['idToken'])            
            st.info('Please verify your email to Log In!')
            st.success("Account Created Successfully!")
            st.balloons()

            #Sign in
            user=auth2.sign_in_with_email_and_password(valid_email,valid_pwd)
            db.child(user['localId']).child("UserName").set(valid_name)
            db.child(user['localId']).child("ID").set(user['localId'])

            st.title("Welcome "+valid_name)
            st.info("👈 Log in to your account to get features.")

            st.session_state['clear'] = True  # Set clear flag  # Clear the inputs after successful submission
            st.experimental_rerun()
    except requests.exceptions.HTTPError as e:
        st.error("User already exist.")
         # Clear the input fields
        st.session_state['clear'] = True  # Set clear flag # Clear the inputs after successful submission
            
            # Refresh the page to clear the inputs
        #st.experimental_rerun()
        time.sleep(2) 

def is_valid_email(email):
    try:
        # Retrieve the list of users from Firebase Authentication
        user_list = auth.list_users()
        #st.write(user_list)
        # Check if the email exists in the list of registered users
        for user in user_list.iterate_all():
            if user.email == email:
                return True

        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

def validate_email(email):
    patt=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]{2,}$"
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

def forgot_password(email):
    if is_valid_email(email):
        try:
            auth2.send_password_reset_email(email)
            st.success("Password reset email sent! Please check your inbox.")
                #st.rerun()
        except requests.exceptions.HTTPError as e:
            if e.response is not None:
                if e.response.status_code == 400:
                    error_msg = e.response.json()['error']['message']
                    st.error(f"User not found: {error_msg}")
                else:
                    error_msg = e.response.json()['error']['message']
                    st.error(f"An error occurred: {error_msg}")
            else:
                st.error("An error occurred during the password reset process.")
    else:
        st.warning("User Not Found")
    # Clear all output
 
        

def signup():
    st.title("Sign Up")
    if st.session_state['clear']:
        st.session_state['mail'] = ''
        st.session_state['pwd'] = ''
        st.session_state['username'] = ''
        st.session_state['clear'] = False  # Reset clear flag

    
    email = st.text_input("Enter your email id", key="mail")
    password = st.text_input("Enter your Password", type='password', key="pwd")
    username = st.text_input("Enter your Username", key="username")
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

                # Create the user in Firebase but disable the account
            #     user = auth.create_user_with_email_and_password(
            #     email=valid_email,
            #     password=valid_pwd
            #     )
            #     st.success('User created successfully. Please verify your email.')
            #     count=time.time()
                # Generate email verification link
            #     # Refresh ID token
               
            #     # is_verification_expired(user['idToken'],count)
            #     count2=time.time()
    
            #     user_response =auth.get_account_info(user['idToken'])
            #     users = user_response.get('users')
            #     for user in users:
            #         email_verify=(user.get("emailVerified"))
            #         if email_verify and abs(count2-count)<5:
            #             st.write("Email is verified.")
            #         elif email_verify==False and abs(count2-count)>5:
            #             auth.delete_user_account()
            #             st.warning("Session expired")

            # except requests.exceptions.HTTPError as e:
            #     st.error("User already exist.")
            #     #st.experimental_rerun()
            #     time.sleep(2) 
            submit_action(valid_email, valid_pwd, valid_name)
            
           
            #login()
def clear_text():
    st.session_state["text"] = ""

# def login():
#     st.title("Log In your account")
#     email = st.text_input("Enter your registered email id")
#     password = st.text_input("Enter your Password", type='password')
#     valid_pwd = validate_password(password)
#     valid_email = validate_email(email)

#     show_reset = st.session_state.get('show_reset', False)

#     if st.button("Log In"):
#         if len(email) == 0 and len(password) == 0:
#             st.warning("Enter your email id and password")
#         elif valid_pwd != password:
#             st.warning("Correctly type your password")
#         elif (valid_email) != email:
#             st.warning("Correctly type your email id")
#     # Define a session state variable to control the visibility of the reset password section
#     if 'show_reset' not in st.session_state:
#         st.session_state.show_reset = False

#     forget = st.button("Forgot Password? 😟")

#     if forget:
#     # Toggle the visibility of the reset password section
#         st.session_state.show_reset = not st.session_state.show_reset

#     if st.session_state.show_reset:
#         email_id = st.text_input("Enter your registered email id to reset password", value=st.session_state.get("text", ""))
#         valid_email = validate_email(email_id)

#         if st.button("Reset Password"):
#             if len(valid_email) == 0:
#                 st.warning("Please enter your email address to reset your password.")
#             else:
#                 forgot_password(valid_email)
#             # Clear the input field after the button is clicked
#                 email_id = ""
#                 st.session_state.text = email_id

#         else:
            

#             try:
#                 user = auth2.sign_in_with_email_and_password(valid_email, valid_pwd)
#                 user_response = auth2.get_account_info(user['idToken'])
#                 users = user_response.get('users')
#                 for user in users:
#                     email_verify = (user.get("emailVerified"))
#                     if email_verify:
#                         name = db.child(user['localId']).child("UserName").get().val()
#                         try:
#                             st.query_params(name=name)
#                         except:
#                             pass
#                             logged_in = True
#                             st.session_state['logged_in'] = True
#                             st.success("Credentials matched successfully")
#                             st.info("Click Log In Button again")

#                             return name
#                     else:
#                         st.warning(
#                         "Verify your email at first.If you don't find an email, try to sign up with a valid email address.")

#             except requests.exceptions.HTTPError as e:
#                 if e.response is not None:
#                     error_msg = e.response.json()['error']['message']
#                     if 'TOO_MANY_ATTEMPTS_TRY_LATER' in error_msg:
#                         st.error(
#                             "Access to this account has been temporarily disabled due to many failed login attempts. Please reset your password or try again later.")
#                     else:
#                         st.error("An error occurred: {}".format(error_msg))
#                 else:
#                     #st.toast("Invalid Credentials")
#                     time.sleep(2)

def login():
    st.title("Log In your account")
    email = st.text_input("Enter your registered email id")
    password = st.text_input("Enter your Password", type='password')
    valid_pwd = validate_password(password)
    valid_email = validate_email(email)

        # Initialize show_reset if not found in st.session_state
    if 'show_reset' not in st.session_state:
        st.session_state.show_reset = False

    if st.button("Log In"):
        if len(email) == 0 and len(password) == 0:
            st.warning("Enter your email id and password")
        elif valid_pwd != password:
            st.warning("Correctly type your password")
        elif (valid_email) != email:
            st.warning("Correctly type your email id")
        else:
            try:
                user = auth2.sign_in_with_email_and_password(valid_email, valid_pwd)
                user_response = auth2.get_account_info(user['idToken'])
                users = user_response.get('users')
                for user in users:
                    email_verify = (user.get("emailVerified"))
                    if email_verify:
                        name = db.child(user['localId']).child("UserName").get().val()
                        try:
                            st.query_params(name=name)
                        except:
                            pass
                        logged_in = True
                        st.session_state['logged_in'] = True
                        st.success("Credentials matched successfully")
                        st.info("Click Log In Button again")
                        return name
                    else:
                        st.warning(
                            "Verify your email at first.If you don't find an email, try to sign up with a valid email address.")

            except requests.exceptions.HTTPError as e:
                if e.response is not None:
                    error_msg = e.response.json()['error']['message']
                    if 'TOO_MANY_ATTEMPTS_TRY_LATER' in error_msg:
                        st.error(
                            "Access to this account has been temporarily disabled due to many failed login attempts. Please reset your password or try again later.")
                    else:
                        st.error("An error occurred: {}".format(error_msg))
                else:
                    st.error("Invalid Credentials")

    forget = st.button("Forgot Password? 😟")

    if forget:
        st.session_state.show_reset = not st.session_state.show_reset

    if st.session_state.show_reset:
        email_id = st.text_input("Enter your registered email id to reset password")
        valid_email = validate_email(email_id)

        if st.button("Reset Password"):
            if len(valid_email) == 0:
                st.warning("Please enter your email address to reset your password.")
            else:
                forgot_password(valid_email)
                st.session_state.text = ""  # Clear the input field after the button is clicked

        
   

              

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
if 'accname' not in st.session_state:
    st.session_state['accname'] = None

if st.session_state['logged_in']:
    clear_query_params()
    #st.write(f"Logged in as {st.session_state['username']}")
    if choice=="Home":
        dashboard(st.session_state['accname'])
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
            st.success(f"Already Logged In as {st.session_state['accname']}")
            
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
            st.session_state['accname'] = name
    if choice=="Home":
        st.info("Log In First to get all the features!!")
    if choice=="About":
        about()

