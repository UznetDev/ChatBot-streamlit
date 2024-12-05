import streamlit as st
import streamlit.components.v1 as components
from data.config import BASE_API
from functions.functions import send_request
from loader import cookie_controller


def app():
    # Sign-Up
    col = st.columns(1)
    cols = st.columns(2)
    with cols[1].form(key='signup_form'):
        st.header(':blue[Sign] In')
        name = st.text_input("Your Name:", placeholder="Enter your name")
        surname = st.text_input("Your Surname:", placeholder="Enter your surname")
        api_key = st.text_input("API Key:", placeholder="Enter your API key")
        username = st.text_input("Username:", placeholder="Enter your username")
        email = st.text_input("Email:", placeholder="Enter your email")
        password = st.text_input("Password:", type="password", placeholder="Enter your password")
        confirm_password = st.text_input("Confirm Password:", type="password", placeholder="Re-enter your password")
        
        s_submit_button = st.form_submit_button(label="Continue")

    if s_submit_button:
        if password != confirm_password:
            st.error("Passwords do not match. Please try again!")
        elif not username or not email or not password or not name or not surname or not api_key:
            st.warning("Please fill out all the fields!")
        else:
            data = {
                "username": username,
                "email": email,
                "password": password,
                "name": name,
                "surname": surname,
                "api_key": api_key
            }
            res, status = send_request(data=data, url=f"{BASE_API}/auth/register")
            if status == 200 and 'access_token' in res:
                cookie_controller.set('access_token', res['access_token'])
                st.write('Login successful, please refresh the page')
                st.rerun()
            else:
                cols[1].warning(res['detail'])

    with cols[0].form(key='log_in'):
        st.header(':blue[Log] In')
        l_username = st.text_input("Username:", placeholder="Enter your username")
        l_password = st.text_input("Password:", type="password", placeholder="Enter your password")
        
        l_submit_button = st.form_submit_button(label="Continue")

    if l_submit_button:
        if not l_username or not l_password:
            st.warning("Please fill out all the fields!")
        else:
            data = {
                "username": l_username,
                "password": l_password
            }
            res, status = send_request(data=data, method='POST', url=f"{BASE_API}/auth/login")
            if status == 200 and 'access_token' in res:
                cookie_controller.set('access_token', res['access_token'])
                col[0].write('Login successful, please refresh the page')
            else:
                cols[0].warning(res['detail'])
