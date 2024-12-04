import streamlit as st
from loader import cookie_controller
from data.config import BASE_API
from functions.functions import send_request



access_token = cookie_controller.get('access_token')
url = f"{BASE_API}/auth/login_with_token?access_token={access_token}"
user_data, status = send_request(url)

if access_token and status == 200:
    st.write("You are logged in")

    surname = st.text_input("Familiyangiz:", user_data['surname'])
    name = st.text_input("Ismingiz:", user_data['name'])
    api_key = st.text_input("API Key:", user_data['api_key'])
    phone = st.text_input("Telefon raqamingiz:", user_data['phone_number'])
    email = st.text_input("Emailingiz:", user_data['email'])

    if st.button("Save"):
        url = f"{BASE_API}/auth/update_user"
        data = {
            "id": user_data["id"],
            "access_token": access_token,
            "surname": surname,
            "name": name,
            "api_key": api_key,
            "phone": phone,
            "email": email
        }
        response, status = send_request(url, data=data, method="PUT")
        if status == 200:
            st.success("User updated successfully")
        else:
            st.error("Error updating user")
            st.write(response)
else:
    st.write("You are not logged in")
    st.stop()

if st.button("Logout"):
    cookie_controller.remove('access_token')
    # st.experimental_rerun()