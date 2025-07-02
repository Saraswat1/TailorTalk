import streamlit as st
import sys
import os
import google.generativeai as genai
st.write("💡 Model: ", genai.GenerativeModel("gemini-1.5-pro"))


# Fix: Add parent directory to sys.path so we can import from `agent/`
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agent.agent import chat_with_agent

# Set page title
st.set_page_config(page_title="TailorTalk Assistant", page_icon="🧵", layout="centered")

st.title("🤖 TailorTalk Assistant")
st.markdown("Book your appointments via chat — powered by Google Calendar!")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Input box for user's message
user_input = st.text_input("🧑 You:", key="user_input", placeholder="e.g. Book appointment on July 3 at 11:00 AM")

# Handle submit
if user_input:
    try:
        response = chat_with_agent(user_input)
    except Exception as e:
        response = f"⚠️ Error: {e}"
    st.session_state.chat_history.append(("You", user_input))
    st.session_state.chat_history.append(("Bot", response))

# Clear chat button
if st.button("🧹 Clear Chat"):
    st.session_state.chat_history = []
    st.rerun()


# Display chat history
for speaker, message in st.session_state.chat_history:
    if speaker == "You":
        st.markdown(f"**🧑 You:** {message}")
    else:
        st.markdown(f"**🤖 Bot:** {message}")
