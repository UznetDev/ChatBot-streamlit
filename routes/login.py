import streamlit as st
from functions.functions import send_request, save_access_token
from data.config import BASE_API



def logIn():
    cols = st.columns(3)
    cols[0].header(':blue[Log] In')
    with cols[1].form(key='login_form'):
        username = st.text_input("Username:", placeholder="Foydalanuvchi nomingizni kiriting")
        password = st.text_input("Password:", type="password", placeholder="Parolni kiriting")
            
        submit_button = st.form_submit_button(label="Log Up")




    if submit_button:
        if not username or not password:
            st.warning("Iltimos, barcha maydonlarni to‘ldiring!")
        else:
            data = {
                "username": username,
                "password": password
            }
            res, status = send_request(data=data, method='POST', url=f"{BASE_API}/auth/login")
            if status == 200 and 'access_token' in res:
                # save_access_token(res['access_token'])
                st.write(res)
            else:
                cols[1].warning(res['message'])
