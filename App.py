import streamlit as st
from io import StringIO
import tempfile
from model import load_data
import os
import stat
import shutil
import time
query_engine = None

def response_generator(response):

    for word in response.split():
        yield word + " "
        time.sleep(0.05)

def process_file(file):
    global query_engine
    if file is not None:
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(file.getvalue())
            temp_file_path = temp_file.name
    return temp_file_path


st.set_page_config(page_title="Chatbot", page_icon="🤖", layout="wide" )

st.title("Rag Bot")

openai_api_key = st.sidebar.text_input('OpenAI API Key', type='password')




if st.sidebar.button("Delete data"):
    try:
        new_permissions = stat.S_IMODE(os.lstat("./storage").st_mode) | stat.S_IRWXU
        shutil.rmtree('./storage')
        st.sidebar.success("Data deleted")
    except:
        st.sidebar.warning("Data not found")
else:
    st.sidebar.warning("This will delete the data")






# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What is up?"):
    st.chat_message("user",avatar="👨").markdown(prompt)
    try:
        query_engine = load_data(path='Data/',openai_api_key=openai_api_key)
        responses=query_engine.query(f'{prompt}answer in detail with page number and refrence pdf name')
        st.session_state.messages.append({"role": "user", "content": prompt})

        response = f"{(responses)}"
        # Display assistant response in chat message container
        with st.chat_message("assistant",avatar="👾"):
            response = st.write_stream(response_generator(response))
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
    except Exception as e:
        st.error("Error: "+str(e))