import logging
import sys
import streamlit as st
from template.template import st_style, footer
from loader import cookie



st.set_page_config(page_title="Chat Bot",
                   page_icon=":bar_chart:",
                   layout="wide")



st.markdown(st_style, 
            unsafe_allow_html=True)




st.markdown(footer, unsafe_allow_html=True)


if 'access_token' in cookie:
    access_token = cookie['access_token']
    st.write(access_token)
else:
    from routes.sign_up import sign_up_app
    sign_up_app()










