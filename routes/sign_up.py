import streamlit as st
import streamlit.components.v1 as components
from data.config import BASE_API
from functions.functions import send_request, save_access_token
from loader import cookie


def sign_up_app():
    cols = st.columns(3)
    cols[0].header(':blue[Sign] In')
    sign_button = cols[0].button('Sign In')
    login_button = cols[0].button('Log In',  type="primary")
    if login_button:
        from routes.login import logIn
        logIn()
    else:
        with cols[1].form(key='signup_form'):
            username = st.text_input("Username:", placeholder="Foydalanuvchi nomingizni kiriting")
            email = st.text_input("Email:", placeholder="Elektron pochtangizni kiriting")
            password = st.text_input("Password:", type="password", placeholder="Parolni kiriting")
            confirm_password = st.text_input("Confirm Password:", type="password", placeholder="Parolni qayta kiriting")
            
            submit_button = st.form_submit_button(label="Continue")
    


        if submit_button:
            if password != confirm_password:
                st.error("Parollar mos emas. Iltimos, qayta urinib ko‘ring!")
            elif not username or not email or not password:
                st.warning("Iltimos, barcha maydonlarni to‘ldiring!")
            else:
                data = {
                    "username": username,
                    "email": email,
                    "password": password
                }
                res, status = send_request(data=data, method='POST', url=f"{BASE_API}/auth/register")
                if status == 200 and 'access_token' in res:
                    save_access_token(res['access_token'])
                    st.write('Kirish muvaffaqiyatliy buldi iltimos sahifani yangilang')
                else:
                    cols[1].warning(res['message'])
