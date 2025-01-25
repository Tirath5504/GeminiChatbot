# Chatbot using Gemini on Streamlit

import os
from dotenv import load_dotenv
import streamlit as st
import google.generativeai as palm

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    st.error("API key not found. Please set the GOOGLE_API_KEY environment variable.")
    st.stop()

palm.configure(api_key=GOOGLE_API_KEY)

model = palm.GenerativeModel(model_name="gemini-pro")

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []
    st.session_state["chat"] = model.start_chat()

def get_gemini_response(prompt):
    try:
        response = st.session_state["chat"].send_message(prompt)
        return response
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

st.set_page_config(page_title="Gemini Chatbot")
st.header("Gemini Chatbot")

user_input = st.text_input("You:", key="input")

if st.button("Send"):
    if user_input:
        with st.spinner("Thinking..."):
            response = get_gemini_response(user_input)
            if response:
                st.session_state["chat_history"].append({"role": "user", "parts": [user_input]})
                st.session_state["chat_history"].append({"role": "model", "parts": [response.last]})

    for message in st.session_state["chat_history"]:
        with st.chat_message(message["role"]):
            st.markdown(message["parts"][0])
