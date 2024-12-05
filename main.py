import streamlit as st
from template.template import st_style, footer
from streamlit_cookies_controller import CookieController
from loader import cookie_controller
from data.config import BASE_API
from functions.functions import send_request



# st.set_page_config(page_title="Chat Bot",
#                    page_icon=":bar_chart:",
#                    layout="wide")


st.markdown(st_style, 
            unsafe_allow_html=True)

token = "WHETJx7Y26kgfm4GYl6CywxT4CH4P7E9TNHWUhxh6gmUV7lXhj"

cookie_controller.set('access_token', token)

cookie = cookie_controller.get('access_token')

access_token = cookie_controller.get('access_token')
st.write(access_token)
st.markdown(footer, unsafe_allow_html=True)


if access_token:
    url = f"{BASE_API}/auth/login_with_token?access_token={access_token}"
    res, status = send_request(url)
    if 'id' in res and status == 200:
        # st.write(res, status)
        from routes.home import app
        app(access_token)
    else:
        from routes.registry import app
        app()
else:
    st.write("No access token found")
    from routes.registry import app
    app()










