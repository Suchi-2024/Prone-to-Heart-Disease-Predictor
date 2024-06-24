import streamlit as st
import firebase_admin
import pyrebase
from firebase_admin import credentials, firestore
import time
from fire import base


firebaseConfig=base()
#Firebase Authentication
firebase=pyrebase.initialize_app(firebaseConfig)
auth=firebase.auth()

verification_times = {}

# Function to send verification email and record timestamp
def send_verification_email(email):
    verification_times[email] = time.time()
    auth.send_email_verification(email=email)

# Function to check if verification link is expired
def is_verification_expired(user,count):
    current_time = time.time()
    verification_time = count
    if current_time - verification_time > 5:  # 600 seconds = 10 minutes
        auth.delete_user_account(user)
        st.warning("User Deleted")