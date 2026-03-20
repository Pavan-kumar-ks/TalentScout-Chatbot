# import streamlit as st
# from chatbot.state_manager import initialize_state, get_next_step
# import sys
# import os

# sys.path.append(os.path.abspath(os.path.dirname(__file__)))
# # Page config
# st.set_page_config(page_title="TalentScout Hiring Assistant")
# st.title("🤖 TalentScout Hiring Assistant")

# # Initialize session state
# if "chat_state" not in st.session_state:
#     st.session_state.chat_state = initialize_state()

# if "messages" not in st.session_state:
#     st.session_state.messages = []

# # User input
# user_input = st.chat_input("Type your response...")

# if user_input:
#     # Store user message
#     st.session_state.messages.append({
#         "role": "user",
#         "content": user_input
#     })

#     # Get chatbot response
#     response = get_next_step(st.session_state.chat_state, user_input)

#     # Store bot response
#     st.session_state.messages.append({
#         "role": "assistant",
#         "content": response
#     })

# # Display chat history (AFTER updating messages)
# for msg in st.session_state.messages:
#     with st.chat_message(msg["role"]):
#         st.write(msg["content"])





import streamlit as st
import sys, os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from chatbot.state_manager import initialize_state, get_next_step

# Page config
st.set_page_config(page_title="TalentScout AI", page_icon="🤖", layout="wide")

# Custom CSS
st.markdown("""
<style>
.chat-container {
    max-width: 800px;
    margin: auto;
}
.big-title {
    font-size: 36px;
    font-weight: bold;
    text-align: center;
}
.subtitle {
    text-align: center;
    color: gray;
}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="big-title">🤖 TalentScout AI Interviewer</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Smart Hiring Assistant powered by LLM</div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("⚙️ About")
    st.write("""
    This AI assistant:
    - Collects candidate details
    - Conducts technical interview
    - Evaluates answers in real-time
    """)
    st.divider()
    st.write("💡 Type 'exit' anytime to quit")

# Init state
if "chat_state" not in st.session_state:
    st.session_state.chat_state = initialize_state()

if "messages" not in st.session_state:
    st.session_state.messages = []

# Intro message
if len(st.session_state.messages) == 0:
    intro = get_next_step(st.session_state.chat_state, "")
    st.session_state.messages.append({"role": "assistant", "content": intro})

# Chat container
with st.container():
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# Input box
user_input = st.chat_input("💬 Type your response here...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    response = get_next_step(st.session_state.chat_state, user_input)

    st.session_state.messages.append({"role": "assistant", "content": response})

    st.rerun()