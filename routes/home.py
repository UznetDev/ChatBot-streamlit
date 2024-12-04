import streamlit as st
import streamlit.components.v1 as components
from data.config import BASE_API
from functions.functions import send_request
from loader import cookie_controller


def app(access_token):
    models, status = send_request(f"{BASE_API}/promts/get_models?access_token={access_token}")
    if status != 200:
        st.error(f"Error: {models['detail']}")
        return

    if "start" not in st.session_state:
        st.session_state.start = True
        # st.stop()

    model_names = [item["name"] for item in models['models']]
    selected_model = st.sidebar.selectbox('Choose a model', model_names, key='selected_model')
    
    model_info, status = send_request(f"{BASE_API}/promts/get_model_info?access_token={access_token}&model_name={selected_model}")
    if status != 200:
        st.write(model_info)

    st.write(model_info)
    description = model_info['model_data']['description']
    st.markdown(f':blue[{selected_model}] {description}')
    st.session_state.start = False
    

    if "messages" not in st.session_state.keys():
        st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

        

    for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])

    def clear_chat_history():
        st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]
    st.sidebar.button('New Chat', on_click=clear_chat_history)


    if prompt := st.chat_input(disabled=0):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)


    if st.session_state.messages[-1]["role"] != "assistant":
        if st.session_state.start == False:
            res, _ = send_request(f"{BASE_API}/user/create_chat?access_token={access_token}&model_id={model_info['model_data']['id']}")
            if _ == 200:
                st.session_state.chat_id = res['chat_id']
            else:
                st.write(res)
                

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                url = f"{BASE_API}/promts/answer?question={prompt}&chat_id={st.session_state.chat_id}&access_token={access_token}&model_name={selected_model}"
                response, status = send_request(url)
                if status != 200:
                    st.write(response)
                st.write(response)
                placeholder = st.empty()
                full_response = ''
                st.write(1)
                if status == 200:
                    for item in response['answer']:
                        full_response += item
                        placeholder.markdown(full_response)
                    placeholder.markdown(full_response)
                else:
                    placeholder.markdown(f"Error: {response} {st.session_state.chat_id}")
        message = {"role": "assistant", "content": full_response}
        st.session_state.messages.append(message)


    chats, status = send_request(f"{BASE_API}/user/get_chats?access_token={access_token}")
    if status != 200:
        st.write(chats)
        st.stop()

    st.sidebar.markdown("### Chats")
    for chat in chats["chats"]:
        if st.sidebar.button(f"{chat['name']} ({chat['timestamp']})", key=f"btn_{chat['id']}"):
            clear_chat_history()
            chat_data, status = send_request(f"{BASE_API}/user/get_chat_data?access_token={access_token}&chat_id={chat['id']}")
            for i in chat_data['chat_data']:
                if i['role'] == 'user':
                    with st.chat_message("user"):
                        st.write(i['content'])
                else:
                    with st.chat_message("assistant"):
                        st.write(i['content'])
            st.session_state.chat_id = chat['id']
            st.session_state.messages = chat_data['chat_data']
                