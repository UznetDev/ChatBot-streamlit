import streamlit as st
from functions.functions import send_request_with_files
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
    # access_token = st.text_input("Access Token", type="password")

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
        st.write(data)
        files = {"file": (file.name, file, "application/pdf")}
        response, status_code = send_request_with_files(f"{BASE_API}/promts/upload/", method="POST", data=data, file=files)

        st.write(response)
        if status_code == 200 and response['status_code'] == 200:
            st.write(response)
            st.success(f"File uploaded successfully! Document ID: {response.get('doc_id')}")
        elif response['status_code'] == 401:
            st.error("Invalid access token. Please check your token and try again.")
        elif response['status_code'] == 400:
            st.error("Bad request. Please check your input data and try again.")
        elif response['status_code'] == 500:
            st.error("Internal server error. Please try again later.")
        else:
            st.write(response)