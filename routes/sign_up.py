import streamlit as st
import streamlit.components.v1 as components
from data.config import BASE_API
from functions.functions import send_request
from loader import cookie


def sign_up_app():
    cols = st.columns(3)
    with cols[1].form(key='signup_form'):
        username = st.text_input("Username:", placeholder="Foydalanuvchi nomingizni kiriting")
        email = st.text_input("Email:", placeholder="Elektron pochtangizni kiriting")
        password = st.text_input("Password:", type="password", placeholder="Parolni kiriting")
        confirm_password = st.text_input("Confirm Password:", type="password", placeholder="Parolni qayta kiriting")
        
        submit_button = st.form_submit_button(label="Sign Up")

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
            st.write(res, status)
            if status == 200 and 'access_token' in res:
                cookie["access_token"] = res['access_token']
                cookie["access_token"]["path"] = "/" 
                cookie["access_token"]["max-age"] = 172800 # 2 DAY
            else:
                cols[1].warning(res['message'])
                components.html(
                    """
                    <script>
                        location.reload();
                    </script>
                    """,
                    height=0,
                )