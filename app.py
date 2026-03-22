import os
import sys
import html

import streamlit as st

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from chatbot.state_manager import get_next_step, initialize_state
from utils.translator import normalize_language, translate_to_language


st.set_page_config(
    page_title="TalentScout",
    page_icon="TS",
    layout="wide",
)

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;600;700;800&display=swap');

:root {
    --bg-a: #f6f4ee;
    --bg-b: #ddf1ea;
    --ink: #14314b;
    --muted: #4d6b83;
    --brand: #0f766e;
    --accent: #f97316;
    --line: rgba(15, 118, 110, 0.18);
    --card: rgba(255, 255, 255, 0.88);
    --shadow: 0 16px 36px rgba(20, 49, 75, 0.12);
}

html, body, [class*="css"] {
    font-family: 'Manrope', sans-serif;
}

.stApp {
    color: var(--ink);
    background:
        radial-gradient(circle at 15% 8%, rgba(249, 115, 22, 0.14), transparent 32%),
        radial-gradient(circle at 90% 15%, rgba(15, 118, 110, 0.2), transparent 38%),
        linear-gradient(135deg, var(--bg-a), var(--bg-b));
}

.stApp::before {
    content: "";
    position: fixed;
    inset: 0;
    pointer-events: none;
    background-image:
        linear-gradient(rgba(20, 49, 75, 0.04) 1px, transparent 1px),
        linear-gradient(90deg, rgba(20, 49, 75, 0.04) 1px, transparent 1px);
    background-size: 32px 32px;
}

.main .block-container {
    max-width: 980px;
    padding-top: 1.1rem;
    padding-bottom: 6.1rem;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(20, 49, 75, 0.95), rgba(12, 74, 110, 0.92));
    border-right: 1px solid rgba(255, 255, 255, 0.16);
}

[data-testid="stSidebar"] * {
    color: #f8fafc !important;
}

.shell {
    border: 1px solid var(--line);
    border-radius: 22px;
    background: linear-gradient(165deg, rgba(255, 255, 255, 0.95), var(--card));
    box-shadow: var(--shadow);
    padding: 1rem 1rem 0.35rem 1rem;
}

.hero {
    border: 1px solid var(--line);
    border-radius: 16px;
    background: linear-gradient(100deg, rgba(15, 118, 110, 0.1), rgba(249, 115, 22, 0.1));
    padding: 1rem 1rem 0.85rem 1rem;
}

.hero-badge {
    display: inline-block;
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: #0f766e;
    border: 1px solid rgba(15, 118, 110, 0.34);
    border-radius: 999px;
    background: rgba(255, 255, 255, 0.7);
    padding: 0.27rem 0.62rem;
}

.hero-title {
    margin: 0.56rem 0 0.22rem 0;
    font-size: clamp(1.56rem, 2.5vw, 2.1rem);
    font-weight: 800;
    color: #0d2f4e;
}

.hero-subtitle {
    margin: 0;
    color: var(--muted);
}

.metric-card {
    border: 1px solid var(--line);
    border-radius: 14px;
    background: rgba(255, 255, 255, 0.88);
    padding: 0.7rem 0.8rem;
}

.metric-label {
    font-size: 0.74rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--muted);
    margin-bottom: 0.15rem;
}

.metric-value {
    font-size: 1rem;
    font-weight: 800;
    color: #0d2f4e;
}

.chat-area {
    margin-top: 0.65rem;
}

[data-testid="stChatMessage"] {
    margin-bottom: 0.28rem;
}

.bubble {
    display: inline-block;
    max-width: min(78%, 700px);
    border-radius: 16px;
    padding: 0.62rem 0.82rem;
    line-height: 1.45;
    color: #102a43;
    border: 1px solid var(--line);
    box-shadow: 0 6px 16px rgba(20, 49, 75, 0.08);
    word-break: break-word;
    white-space: pre-wrap;
}

.bubble-assistant {
    background: rgba(240, 253, 250, 0.95);
    border-radius: 16px 16px 16px 9px;
}

.bubble-user {
    background: rgba(255, 247, 237, 0.98);
    border-color: rgba(249, 115, 22, 0.28);
    border-radius: 16px 16px 9px 16px;
}

[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] p {
    margin: 0;
}

[data-testid="stProgress"] {
    margin-top: 0.45rem;
    margin-bottom: 0.45rem;
}

[data-testid="stProgress"] > div > div {
    background: linear-gradient(90deg, #0f766e, #f97316);
}

[data-testid="stBottomBlockContainer"],
[data-testid="stBottom"],
.stChatFloatingInputContainer {
    background: #f6f4ee !important;
    border-top: 1px solid rgba(15, 118, 110, 0.16);
}

[data-testid="stBottomBlockContainer"] > div {
    max-width: 980px;
    margin: 0 auto;
    padding-left: 1rem;
    padding-right: 1rem;
    padding-bottom: 0.8rem;
}

[data-testid="stChatInput"] {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
}

[data-testid="stChatInput"] textarea,
[data-testid="stChatInput"] input,
[data-testid="stChatInput"] [contenteditable="true"],
[data-testid="stChatInput"] [data-baseweb="textarea"],
[data-testid="stChatInput"] [data-baseweb="base-input"] {
    color: #102a43 !important;
    -webkit-text-fill-color: #102a43 !important;
    caret-color: #0f766e !important;
    opacity: 1 !important;
    filter: none !important;
    mix-blend-mode: normal !important;
    font-size: 1rem !important;
}

[data-testid="stChatInput"] textarea::placeholder,
[data-testid="stChatInput"] input::placeholder {
    color: #56738a !important;
    opacity: 1 !important;
}

[data-testid="stChatInput"] input:-webkit-autofill,
[data-testid="stChatInput"] textarea:-webkit-autofill,
[data-testid="stChatInput"] input:-internal-autofill-selected {
    -webkit-text-fill-color: #102a43 !important;
    box-shadow: 0 0 0 1000px #ffffff inset !important;
}

[data-testid="stChatInput"] button {
    color: #0f766e !important;
}

[data-testid="stChatInput"] button:hover {
    color: #0d2f4e !important;
}

.stButton button {
    border-radius: 12px !important;
    border: 1px solid rgba(255, 255, 255, 0.35) !important;
    background: linear-gradient(90deg, rgba(249, 115, 22, 0.95), rgba(15, 118, 110, 0.9)) !important;
    color: #f8fafc !important;
    font-weight: 700 !important;
}

@media (max-width: 900px) {
    .main .block-container {
        padding-top: 0.7rem;
        padding-left: 0.5rem;
        padding-right: 0.5rem;
    }

    .shell {
        border-radius: 14px;
        padding-left: 0.65rem;
        padding-right: 0.65rem;
    }
}

@media (max-width: 640px) {
    .bubble {
        max-width: 94%;
    }
}
</style>
""",
    unsafe_allow_html=True,
)

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
    "Hindi": "hi",
}

current_lang_code = normalize_language(st.session_state.chat_state.get("language", "en"))
default_language_label = next(
    (label for label, code in language_options.items() if code == current_lang_code),
    "English",
)

ui_copy_en = {
    "title": "TalentScout Pulse",
    "subtitle": "Smart interviews. Sharp signals.",
    "dashboard": "Interview Controls",
    "language": "Interview Language",
    "language_help": "Choose language before interview starts.",
    "questions_completed": "Questions Completed",
    "controls": "Session",
    "restart": "Start New Interview",
    "about": "About This Assistant",
    "about_text": (
        "Collects candidate information, runs a structured technical interview, "
        "evaluates responses, and stores results for review."
    ),
    "chat_placeholder": "Type your response...",
    "language_locked": "Language is locked for this session. Start a new interview to switch.",
    "badge": "Hire Better, Faster",
    "progress": "Progress",
    "status": "Status",
    "status_value_active": "In Progress",
    "status_value_ready": "Ready",
    "language_card": "Current Language",
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


conversation_started = len(st.session_state.messages) > 0

with st.sidebar:
    st.header(ui_text("dashboard"))

    selected_language_label = st.selectbox(
        ui_text("language"),
        options=list(language_options.keys()),
        index=list(language_options.keys()).index(default_language_label),
        disabled=conversation_started,
        help=ui_text("language_help"),
    )

    selected_language_code = language_options[selected_language_label]
    st.session_state.chat_state["language"] = selected_language_code
    current_lang_code = selected_language_code

    if conversation_started:
        st.caption(ui_text("language_locked"))

    progress_count = st.session_state.chat_state.get("current_question_index", 0)
    st.metric(ui_text("questions_completed"), progress_count)

    st.markdown("---")
    st.markdown(f"### {ui_text('controls')}")
    if st.button(ui_text("restart"), use_container_width=True):
        st.session_state.clear()
        st.rerun()

    st.markdown("---")
    st.markdown(f"### {ui_text('about')}")
    st.write(ui_text("about_text"))

if len(st.session_state.messages) == 0:
    intro = get_next_step(st.session_state.chat_state, "")
    st.session_state.messages.append({"role": "assistant", "content": intro})

progress_count = st.session_state.chat_state.get("current_question_index", 0)
progress_ratio = min(progress_count / 4, 1.0)
status_value = ui_text("status_value_active") if len(st.session_state.messages) > 0 else ui_text("status_value_ready")

st.markdown('<div class="shell">', unsafe_allow_html=True)

st.markdown(
    f'''
    <div class="hero">
        <span class="hero-badge">{ui_text("badge")}</span>
        <h1 class="hero-title">{ui_text("title")}</h1>
        <p class="hero-subtitle">{ui_text("subtitle")}</p>
    </div>
    ''',
    unsafe_allow_html=True,
)

metric_col_1, metric_col_2, metric_col_3 = st.columns(3)
with metric_col_1:
    st.markdown(
        f'''
        <div class="metric-card">
            <div class="metric-label">{ui_text("progress")}</div>
            <div class="metric-value">{int(progress_ratio * 100)}%</div>
        </div>
        ''',
        unsafe_allow_html=True,
    )
with metric_col_2:
    st.markdown(
        f'''
        <div class="metric-card">
            <div class="metric-label">{ui_text("status")}</div>
            <div class="metric-value">{status_value}</div>
        </div>
        ''',
        unsafe_allow_html=True,
    )
with metric_col_3:
    st.markdown(
        f'''
        <div class="metric-card">
            <div class="metric-label">{ui_text("language_card")}</div>
            <div class="metric-value">{selected_language_label}</div>
        </div>
        ''',
        unsafe_allow_html=True,
    )

st.progress(progress_ratio)

with st.container():
    st.markdown('<div class="chat-area">', unsafe_allow_html=True)
    for msg in st.session_state.messages:
        role = "user" if msg["role"] == "user" else "assistant"
        avatar = "🧑" if role == "user" else "🤖"
        content = str(msg.get("content", "")).strip() or "..."
        safe_content = html.escape(content).replace("\n", "<br>")
        bubble_class = "bubble-user" if role == "user" else "bubble-assistant"
        with st.chat_message(role, avatar=avatar):
            st.markdown(f'<div class="bubble {bubble_class}">{safe_content}</div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

user_input = st.chat_input(ui_text("chat_placeholder"))
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    response = get_next_step(st.session_state.chat_state, user_input)
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()
