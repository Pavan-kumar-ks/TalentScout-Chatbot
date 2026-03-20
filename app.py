import streamlit as st
import sys, os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from chatbot.state_manager import initialize_state, get_next_step

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="TalentScout AI",
    page_icon="🤖",
    layout="wide"
)

# =========================
# CUSTOM CSS (🔥 MODERN UI)
# =========================
st.markdown("""
<style>

/* Background Gradient */
.stApp {
    background: linear-gradient(135deg, #1f4037, #99f2c8);
    color: white;
}

/* Title */
.title {
    text-align: center;
    font-size: 42px;
    font-weight: bold;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    color: #e0e0e0;
    margin-bottom: 30px;
}

/* Chat bubbles */
.user-bubble {
    background: #4CAF50;
    padding: 12px 16px;
    border-radius: 15px;
    margin: 5px 0;
    color: white;
}

.bot-bubble {
    background: rgba(255,255,255,0.1);
    padding: 12px 16px;
    border-radius: 15px;
    margin: 5px 0;
    backdrop-filter: blur(10px);
}

/* Sidebar */
.css-1d391kg {
    background: rgba(0,0,0,0.2);
}

/* Buttons */
.stButton button {
    border-radius: 10px;
    background: #00c6ff;
    color: white;
}

/* Progress bar */
.stProgress > div > div {
    background-color: #00ffcc;
}

</style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================
st.markdown('<div class="title">🤖 TalentScout AI</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Next-Gen Intelligent Hiring Assistant</div>', unsafe_allow_html=True)

# =========================
# SIDEBAR (COOL DASHBOARD)
# =========================
with st.sidebar:
    st.header("📊 Dashboard")

    if "chat_state" in st.session_state:
        progress = st.session_state.chat_state.get("current_question_index", 0)
        st.metric("Questions Completed", progress)

    st.divider()

    st.markdown("### ⚙️ Controls")

    if st.button("🔄 Restart Interview"):
        st.session_state.clear()
        st.rerun()

    st.divider()

    st.markdown("### ℹ️ About")
    st.write("""
    AI-powered hiring assistant that:
    - Conducts technical interviews  
    - Evaluates answers  
    - Generates follow-ups  
    """)

# =========================
# INIT STATE
# =========================
if "chat_state" not in st.session_state:
    st.session_state.chat_state = initialize_state()

if "messages" not in st.session_state:
    st.session_state.messages = []

# =========================
# INTRO MESSAGE (NO BLANK SCREEN)
# =========================
if len(st.session_state.messages) == 0:
    intro = get_next_step(st.session_state.chat_state, "")
    st.session_state.messages.append({"role": "assistant", "content": intro})

# =========================
# PROGRESS BAR
# =========================
progress = st.session_state.chat_state.get("current_question_index", 0)
st.progress(min(progress / 4, 1.0))

# =========================
# CHAT DISPLAY (STYLED)
# =========================
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="user-bubble">🧑 {msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="bot-bubble">🤖 {msg["content"]}</div>', unsafe_allow_html=True)

# =========================
# INPUT
# =========================
user_input = st.chat_input("💬 Type your answer here...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    response = get_next_step(st.session_state.chat_state, user_input)

    st.session_state.messages.append({"role": "assistant", "content": response})

    st.rerun()