import streamlit as st
import firebase_admin
import pyrebase
from firebase_admin import credentials, firestore
import time

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