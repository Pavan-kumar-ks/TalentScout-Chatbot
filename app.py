import streamlit as st
import sys, os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from chatbot.state_manager import initialize_state, get_next_step
from utils.translator import normalize_language, translate_to_language

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
if "chat_state" not in st.session_state:
    st.session_state.chat_state = initialize_state()

if "messages" not in st.session_state:
    st.session_state.messages = []

if "ui_copy_cache" not in st.session_state:
    st.session_state.ui_copy_cache = {}

language_options = {
    "English": "en",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Portuguese": "pt",
    "Russian": "ru",
    "Arabic": "ar",
    "Chinese (Simplified)": "zh-cn",
    "Japanese": "ja",
    "Hindi": "hi"
}

conversation_started = len(st.session_state.messages) > 0
current_lang_code = normalize_language(st.session_state.chat_state.get("language", "en"))
default_language_label = next(
    (label for label, code in language_options.items() if code == current_lang_code),
    "English"
)

ui_copy_en = {
    "title": "TalentScout AI",
    "subtitle": "Next-Gen Intelligent Hiring Assistant",
    "dashboard": "Dashboard",
    "language": "Interview Language",
    "language_help": "Choose language before interview starts.",
    "questions_completed": "Questions Completed",
    "controls": "Controls",
    "restart": "Restart Interview",
    "about": "About",
    "about_text": """
AI-powered hiring assistant that:
- Conducts technical interviews
- Evaluates answers
- Generates follow-ups
""",
    "chat_placeholder": "Type your answer here...",
    "language_locked": "Language is locked for this session. Restart to change."
}


def get_ui_copy(language_code):
    if language_code in st.session_state.ui_copy_cache:
        return st.session_state.ui_copy_cache[language_code]

    if language_code == "en":
        translated = dict(ui_copy_en)
    else:
        translated = {
            key: translate_to_language(value, language=language_code, src_lang="en")
            for key, value in ui_copy_en.items()
        }

    st.session_state.ui_copy_cache[language_code] = translated
    return translated


def ui_text(key):
    return get_ui_copy(current_lang_code)[key]

with st.sidebar:
    st.header(ui_text("dashboard"))

    selected_language_label = st.selectbox(
        ui_text("language"),
        options=list(language_options.keys()),
        index=list(language_options.keys()).index(default_language_label),
        disabled=conversation_started,
        help=ui_text("language_help")
    )

    selected_language_code = language_options[selected_language_label]
    st.session_state.chat_state["language"] = selected_language_code
    current_lang_code = selected_language_code

    if conversation_started:
        st.caption(ui_text("language_locked"))

    if "chat_state" in st.session_state:
        progress = st.session_state.chat_state.get("current_question_index", 0)
        st.metric(ui_text("questions_completed"), progress)

    st.divider()

    st.markdown(f"### {ui_text('controls')}")

    if st.button(ui_text("restart")):
        st.session_state.clear()
        st.rerun()

    st.divider()

    st.markdown(f"### {ui_text('about')}")
    st.write(ui_text("about_text"))

st.markdown(f'<div class="title">{ui_text("title")}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="subtitle">{ui_text("subtitle")}</div>', unsafe_allow_html=True)

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
user_input = st.chat_input(ui_text("chat_placeholder"))

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    response = get_next_step(st.session_state.chat_state, user_input)

    st.session_state.messages.append({"role": "assistant", "content": response})

    st.rerun()