import streamlit as st
import pandas as pd
import joblib

model = joblib.load('trainedModel.pkl')

# User registration form
st.title('User Registration and Spending Limit Prediction')
st.subheader('Registration')

name = st.text_input('Name', key='name_input')
phone = st.text_input('Phone', key='phone_input')
username = st.text_input('Username', key='username_input')
gender = st.selectbox('Gender', ['Male', 'Female', 'Other'], key='gender_input')
salary = st.number_input('Salary', key='salary_input')
password = st.text_input('Password', type='password', key='password_input')

if st.button('Sign Up'):
    try:
        # Add registration logic here (e.g., store data in a database)
        st.write("User registered successfully!")

    except Exception as e:
        st.write("Error:", str(e))

# User login form
st.subheader('Login')

username = st.text_input('Username', key='login_username_input')
password = st.text_input('Password', type='password', key='login_password_input')

if st.button('Log In'):
    # Add login logic here (e.g., validate user credentials)
    st.write("Login successful!")

# Spending limit prediction form
st.subheader('Spending Limit Prediction')

uploaded_file = st.file_uploader('Upload a CSV file with earnings and earning potential', key='file_upload')
if uploaded_file is not None:
    try:
        data = pd.read_csv(uploaded_file)
        predictions = model.predict(data[['earnings','earning_potential']]) 
        data['preferred_spending_limit'] = predictions *30
        data['savings'] = data['earnings'] - data['preferred_spending_limit']
        data['ROI'] = (data['earning_potential'] / data['earnings']) * 100

        st.write('Predicted Spending Limits:')
        st.write(data)

    except Exception as e:
        st.write("Error:", str(e))
