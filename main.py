import streamlit as st


st.set_page_config(page_title="Chat Bot",
                   page_icon=":bar_chart:",
                   layout="wide")


from template.template import st_style, footer
from loader import cookie_controller
from data.config import BASE_API
from functions.functions import send_request


st.markdown(st_style, 
            unsafe_allow_html=True)


cookie = cookie_controller.get('access_token')

access_token = cookie_controller.get('access_token')
st.markdown(footer, unsafe_allow_html=True)


if access_token:
    url = f"{BASE_API}/auth/login_with_token?access_token={access_token}"
    res, status = send_request(url)
    if 'id' in res and status == 200:
        from routes.home import app
        app(access_token)
    else:
        from routes.registry import app
        app()
else:
    from routes.registry import app
    app()










