import streamlit as st
import sys
import os
import html
import re

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from chatbot.state_manager import initialize_state, get_next_step
from utils.translator import normalize_language, translate_to_language


st.set_page_config(
    page_title="TalentScout AI",
    page_icon="TS",
    layout="wide",
)

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;600;700;800&family=Space+Grotesk:wght@500;700&display=swap');

:root {
    --bg-1: #f5f2e9;
    --bg-2: #dff3eb;
    --ink: #102a43;
    --muted: #486581;
    --brand: #0f766e;
    --accent: #f97316;
    --panel: rgba(255, 255, 255, 0.82);
    --panel-strong: rgba(255, 255, 255, 0.94);
    --line: rgba(15, 118, 110, 0.20);
    --shadow: 0 20px 50px rgba(16, 42, 67, 0.12);
}

html, body, [class*="css"] {
    font-family: 'Manrope', sans-serif;
}

.stApp {
    color: var(--ink);
    background:
        radial-gradient(circle at 10% 10%, rgba(249, 115, 22, 0.16), transparent 30%),
        radial-gradient(circle at 90% 20%, rgba(15, 118, 110, 0.2), transparent 35%),
        linear-gradient(130deg, var(--bg-1), var(--bg-2));
}

.stApp::before {
    content: "";
    position: fixed;
    inset: 0;
    pointer-events: none;
    background-image:
        linear-gradient(rgba(15, 118, 110, 0.05) 1px, transparent 1px),
        linear-gradient(90deg, rgba(15, 118, 110, 0.05) 1px, transparent 1px);
    background-size: 32px 32px;
    mask-image: radial-gradient(circle at center, black 10%, transparent 85%);
}

.main .block-container {
    max-width: 1024px;
    padding-top: 2rem;
    padding-bottom: 2rem;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(16, 42, 67, 0.92), rgba(12, 74, 110, 0.94));
    border-right: 1px solid rgba(255, 255, 255, 0.16);
}

[data-testid="stSidebar"] * {
    color: #f8fafc !important;
}

.shell {
    border: 1px solid var(--line);
    background: linear-gradient(165deg, var(--panel-strong), var(--panel));
    border-radius: 24px;
    box-shadow: var(--shadow);
    overflow: hidden;
    animation: riseIn 480ms ease-out;
}

.hero {
    padding: 1.4rem 1.4rem 1.2rem 1.4rem;
    border-bottom: 1px solid var(--line);
    background: linear-gradient(90deg, rgba(15, 118, 110, 0.08), rgba(249, 115, 22, 0.1));
}

.hero-badge {
    display: inline-block;
    padding: 0.3rem 0.65rem;
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: #0f766e;
    border: 1px solid rgba(15, 118, 110, 0.28);
    border-radius: 999px;
    background: rgba(240, 253, 250, 0.8);
}

.hero-title {
    margin: 0.65rem 0 0.2rem 0;
    font-family: 'Space Grotesk', sans-serif;
    font-size: clamp(1.7rem, 2.7vw, 2.35rem);
    font-weight: 800;
    line-height: 1.15;
    color: #0b253f;
    background: linear-gradient(100deg, #0b253f 0%, #0f766e 55%, #f97316 100%);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    text-shadow: 0 6px 24px rgba(15, 118, 110, 0.15);
}

.hero-subtitle {
    margin: 0;
    color: var(--muted);
    font-size: 1.02rem;
    max-width: 760px;
}

.metrics {
    display: grid;
    grid-template-columns: repeat(3, minmax(120px, 1fr));
    gap: 0.75rem;
    padding: 1rem 1.2rem 0.8rem 1.2rem;
}

.metric-card {
    border: 1px solid var(--line);
    border-radius: 14px;
    background: rgba(255, 255, 255, 0.82);
    padding: 0.75rem;
}

.metric-label {
    color: var(--muted);
    font-size: 0.78rem;
    margin-bottom: 0.25rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.metric-value {
    color: #0b253f;
    font-size: 1.05rem;
    font-weight: 800;
}

.chat-wrap {
    padding: 0 1.2rem 5.6rem 1.2rem;
}

.msg {
    border: 1px solid var(--line);
    border-radius: 16px;
    padding: 0.82rem 0.95rem 0.9rem 0.95rem;
    margin-top: 0.7rem;
    line-height: 1.5;
    white-space: pre-wrap;
    box-shadow: 0 8px 20px rgba(15, 118, 110, 0.06);
    animation: fadeSlide 260ms ease-out;
    position: relative;
    overflow: hidden;
}

.msg.bot {
    background: rgba(240, 253, 250, 0.86);
}

.msg.user {
    background: rgba(255, 247, 237, 0.94);
    border-color: rgba(249, 115, 22, 0.28);
}

.msg::after {
    content: "";
    position: absolute;
    inset: auto auto -50px -30px;
    width: 120px;
    height: 120px;
    border-radius: 999px;
    background: radial-gradient(circle, rgba(15, 118, 110, 0.16), transparent 65%);
    pointer-events: none;
}

.msg.user::after {
    background: radial-gradient(circle, rgba(249, 115, 22, 0.18), transparent 65%);
}

.msg-head {
    display: flex;
    align-items: center;
    gap: 0.55rem;
    margin-bottom: 0.32rem;
}

.assistant-logo {
    position: relative;
    width: 28px;
    height: 28px;
    border-radius: 10px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: 0.65rem;
    font-weight: 800;
    letter-spacing: 0.04em;
    color: #ecfeff;
    background: linear-gradient(135deg, #0f766e, #0ea5a4);
    border: 1px solid rgba(255, 255, 255, 0.45);
    box-shadow: 0 8px 16px rgba(15, 118, 110, 0.26);
}

.assistant-logo::after {
    content: "";
    position: absolute;
    top: -2px;
    right: -2px;
    width: 8px;
    height: 8px;
    border-radius: 999px;
    background: #f97316;
    box-shadow: 0 0 0 2px rgba(255, 255, 255, 0.95);
}

.user-dot {
    width: 10px;
    height: 10px;
    border-radius: 999px;
    background: linear-gradient(135deg, #fb923c, #f97316);
    box-shadow: 0 0 0 2px rgba(255, 247, 237, 0.9);
}

.msg-label {
    font-size: 0.72rem;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 0;
    font-weight: 700;
}

.msg-content {
    color: #0b253f;
    position: relative;
    z-index: 1;
}

[data-testid="stProgress"] {
    padding: 0.15rem 1.1rem 0.6rem 1.1rem;
}

[data-testid="stProgress"] > div > div {
    background: linear-gradient(90deg, #0f766e, #f97316);
}

[data-testid="stChatInput"] {
    border: 1px solid var(--line);
    border-radius: 14px;
    background: rgba(255, 255, 255, 0.94);
    box-shadow: var(--shadow);
    overflow: hidden;
}

[data-testid="stChatInput"] textarea {
    font-family: 'Manrope', sans-serif !important;
    color: #102a43 !important;
    opacity: 1 !important;
    caret-color: #0f766e !important;
}

[data-testid="stChatInput"] textarea::placeholder {
    color: #486581 !important;
    opacity: 0.92 !important;
}

[data-testid="stBottomBlockContainer"] {
    background: transparent !important;
}

[data-testid="stBottomBlockContainer"] > div {
    max-width: 1024px;
    margin: 0 auto;
    padding-left: 1.1rem;
    padding-right: 1.1rem;
    padding-bottom: 0.85rem;
}

.stButton button {
    border: 1px solid rgba(255, 255, 255, 0.38) !important;
    border-radius: 12px !important;
    font-weight: 700 !important;
    background: linear-gradient(90deg, rgba(249, 115, 22, 0.92), rgba(15, 118, 110, 0.9)) !important;
    color: #f8fafc !important;
}

@keyframes riseIn {
    from {
        opacity: 0;
        transform: translateY(10px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes fadeSlide {
    from {
        opacity: 0;
        transform: translateX(8px);
    }
    to {
        opacity: 1;
        transform: translateX(0);
    }
}

@media (max-width: 900px) {
    .main .block-container {
        padding-top: 1rem;
        padding-left: 0.7rem;
        padding-right: 0.7rem;
    }

    .shell {
        border-radius: 16px;
    }

    .metrics {
        grid-template-columns: 1fr;
        padding-top: 0.75rem;
    }

    .hero {
        padding: 1rem;
    }

    .chat-wrap {
        padding-left: 0.85rem;
        padding-right: 0.85rem;
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

conversation_started = len(st.session_state.messages) > 0
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


if len(st.session_state.messages) == 0:
    intro = get_next_step(st.session_state.chat_state, "")
    st.session_state.messages.append({"role": "assistant", "content": intro})

progress_count = st.session_state.chat_state.get("current_question_index", 0)
progress_ratio = min(progress_count / 4, 1.0)

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

    st.markdown("---")
    st.metric(ui_text("questions_completed"), progress_count)

    st.markdown(f"### {ui_text('controls')}")
    if st.button(ui_text("restart"), use_container_width=True):
        st.session_state.clear()
        st.rerun()

    st.markdown("---")
    st.markdown(f"### {ui_text('about')}")
    st.write(ui_text("about_text"))

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

status_value = ui_text("status_value_active") if conversation_started else ui_text("status_value_ready")

st.markdown(
    f'''
    <div class="metrics">
        <div class="metric-card">
            <div class="metric-label">{ui_text("progress")}</div>
            <div class="metric-value">{int(progress_ratio * 100)}%</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">{ui_text("status")}</div>
            <div class="metric-value">{status_value}</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">{ui_text("language_card")}</div>
            <div class="metric-value">{selected_language_label}</div>
        </div>
    </div>
    ''',
    unsafe_allow_html=True,
)

st.progress(progress_ratio)

st.markdown('<div class="chat-wrap">', unsafe_allow_html=True)
for msg in st.session_state.messages:
    role_class = "user" if msg["role"] == "user" else "bot"
    role_label = "Candidate" if msg["role"] == "user" else "Assistant"
    normalized_text = str(msg["content"] or "").replace("\r\n", "\n").strip("\n ")
    safe_content = html.escape(normalized_text).replace("\n", "<br>")
    safe_content = re.sub(r"^(<br>)+", "", safe_content)
    safe_content = re.sub(r"(<br>){3,}", "<br><br>", safe_content)
    if not safe_content.strip():
        safe_content = "..."
    role_icon = '<div class="user-dot"></div>' if msg["role"] == "user" else '<div class="assistant-logo">TS</div>'

    st.markdown(
        f'''
        <div class="msg {role_class}">
            <div class="msg-head">
                {role_icon}
                <div class="msg-label">{role_label}</div>
            </div>
            <div class="msg-content">{safe_content}</div>
        </div>
        ''',
        unsafe_allow_html=True,
    )
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

user_input = st.chat_input(ui_text("chat_placeholder"))
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    response = get_next_step(st.session_state.chat_state, user_input)
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()
