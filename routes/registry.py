import streamlit as st
import streamlit.components.v1 as components
from data.config import BASE_API
from functions.functions import send_request
from loader import cookie_controller



def app():
    # Sgn-Up
    col = st.columns(1)
    cols = st.columns(2)
    with cols[1].form(key='signup_form'):
        st.header(':blue[Sign] In')
        name = st.text_input("Ismingiz:", placeholder="Ismingizni kiriting")
        surname = st.text_input("Familiyangiz:", placeholder="Familiyangizni kiriting")
        api_key = st.text_input("API kaliti:", placeholder="API kalitni kiriting")
        username = st.text_input("Username:", placeholder="Foydalanuvchi nomingizni kiriting")
        email = st.text_input("Email:", placeholder="Elektron pochtangizni kiriting")
        password = st.text_input("Password:", type="password", placeholder="Parolni kiriting")
        confirm_password = st.text_input("Confirm Password:", type="password", placeholder="Parolni qayta kiriting")
        
        s_submit_button = st.form_submit_button(label="Continue")

    if s_submit_button:
        if password != confirm_password:
            st.error("Parollar mos emas. Iltimos, qayta urinib ko‘ring!")
        elif not username or not email or not password or not name or not surname or not api_key:
            st.warning("Iltimos, barcha maydonlarni to‘ldiring!")
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
                st.write('Kirish muvaffaqiyatliy buldi iltimos sahifani yangilang')
                st.rerun()
            else:
                cols[1].warning(res['message'])

    # Log In
    with cols[0].form(key='log_in'):
        st.header(':blue[Log] In')
        l_username = st.text_input("Username:", placeholder="Foydalanuvchi nomingizni kiriting")
        l_password = st.text_input("Password:", type="password", placeholder="Parolni kiriting")
        
        l_submit_button = st.form_submit_button(label="Continue")

    if l_submit_button:
        if not l_username or not l_password:
            st.warning("Iltimos, barcha maydonlarni to‘ldiring!")
        else:
            data = {
                "username": l_username,
                "password": l_password
            }
            res, status = send_request(data=data, method='POST', url=f"{BASE_API}/auth/login")
            if status == 200 and 'access_token' in res:
                cookie_controller.set('access_token', res['access_token'])
                col[0].write('Kirish muvaffaqiyatliy buldi iltimos sahifani yangilang')
            else:
                cols[0].warning(res['detail'])
