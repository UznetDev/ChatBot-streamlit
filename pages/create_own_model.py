import streamlit as st
from functions.functions import send_request
from data.config import BASE_API
from loader import cookie_controller

st.title("Model Registration")

access_token = cookie_controller.get('access_token')
if access_token is None:
    st.error("You are not logged in. Pleas reload page")
    st.stop()


with st.form("upload_form"):
    st.header("Upload a PDF File and Register a Model")
    file = st.file_uploader("Select a PDF file", type=["pdf"])
    model_name = st.text_input("Model Name")
    description = st.text_area("Description")
    system = st.text_input("System")
    visibility = st.checkbox("Visibility (Public)", value=False)
    max_tokens = st.number_input("Max Tokens", min_value=1, step=1)

    submit_button = st.form_submit_button("Submit")
if submit_button:
    if file is None:
        st.error("Please upload a PDF file.")
    elif not file.name.endswith(".pdf"):
        st.error("Only PDF files are allowed.")
    else:
        
        data = {
            "model_name": model_name,
            "description": description,
            "system": system,
            "visibility": visibility,
            "max_tokens": max_tokens,
            "access_token": access_token,
        }
        files = {"file": (file.name, file, "application/pdf")}
        response, status_code = send_request(url=f"{BASE_API}/promts/upload_model/", data=data, file=files)

        if status_code == 200 and response['status_code'] == 200:
            st.success(f"File uploaded successfully! Document ID: {response.get('doc_id')}")
        else:
            st.error(response['detail'])