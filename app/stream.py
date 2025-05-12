import streamlit as st
import requests
import pandas as pd


def get_api_response(question, session_id, model):
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }
    data = {
        "question": question,
        "model": model
    }
    if session_id:
        data["session_id"] = session_id

    try:
        response = requests.post("http://localhost:8000/chat", headers=headers, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API request failed with status code {response.status_code}: {response.text}")
            return None
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return None

def list_hist():
    try:
        response = requests.get("http://localhost:8000/hist")
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API request failed with status code {response.status_code}: {response.text}")
            return None
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return None
    
if "messages" not in st.session_state:
    st.session_state.messages = []

if "session_id" not in st.session_state:
    st.session_state.session_id = None

if "documents" not in st.session_state:
    st.session_state.documents = [] 


with st.sidebar:
    st.header("History")

    # Spinner placeholder for refreshing history
    spinner_placeholder = st.empty()

    # Button to refresh history
    if st.button("Refresh History List"):
        with spinner_placeholder:
            with st.spinner("Refreshing..."):
                st.session_state.documents = list_hist()  # ✅ Store history in session state

    # Display stored history
    if st.session_state.documents:
        df = pd.DataFrame(st.session_state.documents)
        st.table(df)  # ✅ Sidebar content persists






st.title('Danucore ChatBot')

def display_chat():
    # Chat interface
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Query:"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.spinner("Generating response..."):
            response = get_api_response(prompt, st.session_state.session_id, 'llama3-8b-8192')
            
            if response:
                st.session_state.session_id = response.get('session_id')
                st.session_state.messages.append({"role": "assistant", "content": response['answer']})
                
                with st.chat_message("assistant"):
                    st.markdown(response['answer'])
                    
                    with st.expander("Details"):
                        st.subheader("Generated Answer")
                        st.code(response['answer'])
                        st.subheader("Model Used")
                        st.code(response['model'])
                        st.subheader("Session ID")
                        st.code(response['session_id'])
            else:
                st.error("Failed to get a response from the API. Please try again.")



display_chat()


