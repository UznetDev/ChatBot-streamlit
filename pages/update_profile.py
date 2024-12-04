import streamlit as st
from loader import cookie_controller
from data.config import BASE_API
from functions.functions import send_request, get_cookie



access_token = cookie_controller.get('access_token')
url = f"{BASE_API}/auth/login_with_token?access_token={access_token}"
user_data, status = send_request(url)

if access_token and status == 200:
    st.write("You are logged in")
    st.write(user_data)
else:
    st.write("You are not logged in")
    st.stop()

if st.button("Logout"):
    cookie_controller.remove('access_token')
    # st.experimental_rerun()