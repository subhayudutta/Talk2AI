import streamlit as st
import os
import google.generativeai as genai
from google.api_core import exceptions as google_exceptions
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('GOOGLE_API_KEY')
os.environ['GOOGLE_API_KEY'] = api_key
genai.configure(api_key=api_key)

default_temperature = 0.9

generation_config = {
    "temperature": default_temperature,
    "top_p": 0.95,
    "top_k": 1,
    "max_output_tokens": 99998,
}

st.set_page_config(page_title="Talk2AI 😐")

with st.sidebar:
    st.title("Configuration")
    api_key_input = st.text_input("Enter your Gemini API Key (if available)", type="password", placeholder="If you have!")
    temperature = st.slider("Temperature", 0.0, 1.0, 0.8, 0.1)
    model_selection = st.selectbox("Select Model", ("gemini-1.5", "gemini-1.5-pro", "gemini-1.0-pro", "gemini-1.5-flash"))

    st.markdown("App built by Subhayu Dutta")

def generate_response(messages, model="gemini-pro"):
    model_instance = genai.GenerativeModel(model)
    response = model_instance.generate_content(messages, generation_config=generation_config)
    return response

if "messages" not in st.session_state:
    st.session_state["messages"] = []
messages = st.session_state["messages"]

st.header("Talk2AI: Your Personal AI Assistant")
st.write(
    "Engage in intelligent conversations and get instant, insightful responses with Talk2AI, your versatile virtual assistant."
)

if messages:
    for item in messages:
        role, content = item.values()
        if role == "user":
            st.chat_message("user", avatar="user.png").markdown(content[0])
        elif role == "model":
            st.chat_message("assistant", avatar="bot.png").markdown(content[0])

user_input = st.chat_input("Say something")

if user_input:
    st.chat_message("user", avatar="user.png").markdown(user_input)
    response_placeholder = st.chat_message("assistant", avatar="bot.png").markdown("Analyzing...")
    messages.append({"role": "user", "parts": [user_input]})
    
    try:
        response = generate_response(messages)
    except google_exceptions.InvalidArgument as e:
        if "API key not valid" in str(e):
            st.error("Invalid API key. Please provide a valid API key.")
        else:
            st.error("An error occurred. Please refresh the page and try again.")
    except Exception as e:
        st.error("An error occurred. Please refresh the page and try again.")
    
    if response:
        response_text = ""
        for chunk in response:
            if chunk.candidates:
                response_text += chunk.text
            if not response_text:
                response_text = "Inappropriate content"
                st.error("Your input violates the rules. Please try again!")
        response_placeholder.markdown(response_text)
        messages.append({"role": "model", "parts": [response_text]})
