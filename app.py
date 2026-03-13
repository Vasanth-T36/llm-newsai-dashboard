import streamlit as st
from news_fetcher import fetch_news
from article_extractor import extract_article
from summarizer import summarize
from vector_store import search
from ai_chatbot import ask_ai, get_follow_up_suggestions, analyze_sentiment
import time
from datetime import datetime

# ─────────────────────────────────────────────
#  Page Config
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="NewsAI — Real-Time Intelligence",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@400;500;600;700&display=swap');

/* ── Reset & Base ── */
*, *::before, *::after { box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"] {
    background: #090e1a !important;
    color: #e2e8f0 !important;
    font-family: 'Inter', sans-serif !important;
}

[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #090e1a 0%, #0d1627 50%, #0a1220 100%) !important;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stToolbar"] { display: none !important; }
.block-container { padding-top: 0 !important; max-width: 100% !important; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d1627 0%, #111827 100%) !important;
    border-right: 1px solid rgba(99,102,241,0.2) !important;
}
[data-testid="stSidebar"] .block-container {
    padding: 1rem 1rem !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #111827; }
::-webkit-scrollbar-thumb { background: #4338ca; border-radius: 3px; }

/* ── Hero Banner ── */
.hero-banner {
    background: linear-gradient(135deg, #1e1b4b 0%, #312e81 30%, #1e3a5f 70%, #0c4a6e 100%);
    border-radius: 20px;
    padding: 2.5rem 3rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
    border: 1px solid rgba(99,102,241,0.3);
    box-shadow: 0 20px 60px rgba(99,102,241,0.15), inset 0 1px 0 rgba(255,255,255,0.1);
}
.hero-banner::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -20%;
    width: 500px;
    height: 500px;
    background: radial-gradient(circle, rgba(99,102,241,0.2) 0%, transparent 70%);
    animation: pulse-hero 4s ease-in-out infinite;
}
.hero-banner::after {
    content: '';
    position: absolute;
    bottom: -30%;
    left: -10%;
    width: 300px;
    height: 300px;
    background: radial-gradient(circle, rgba(6,182,212,0.15) 0%, transparent 70%);
}
@keyframes pulse-hero {
    0%, 100% { transform: scale(1); opacity: 0.5; }
    50% { transform: scale(1.1); opacity: 1; }
}
.hero-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2.8rem;
    font-weight: 800;
    background: linear-gradient(135deg, #fff 0%, #a5b4fc 50%, #67e8f9 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0 0 0.5rem 0;
    line-height: 1.1;
}
.hero-subtitle {
    color: rgba(255,255,255,0.65);
    font-size: 1.05rem;
    font-weight: 400;
    margin: 0;
}
.hero-time {
    background: rgba(99,102,241,0.2);
    border: 1px solid rgba(99,102,241,0.4);
    border-radius: 999px;
    padding: 0.35rem 1rem;
    font-size: 0.8rem;
    color: #a5b4fc;
    display: inline-block;
    margin-top: 1rem;
    backdrop-filter: blur(10px);
}

/* ── Stats Bar ── */
.stats-bar {
    display: flex;
    gap: 1rem;
    margin-bottom: 2rem;
}
.stat-card {
    flex: 1;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 14px;
    padding: 1rem 1.25rem;
    text-align: center;
    transition: all 0.3s;
    backdrop-filter: blur(10px);
}
.stat-card:hover {
    background: rgba(99,102,241,0.1);
    border-color: rgba(99,102,241,0.4);
    transform: translateY(-2px);
}
.stat-value {
    font-size: 1.8rem;
    font-weight: 700;
    background: linear-gradient(135deg, #818cf8, #67e8f9);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.stat-label {
    font-size: 0.75rem;
    color: rgba(255,255,255,0.5);
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-top: 0.25rem;
}

/* ── Section Header ── */
.section-header {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 1.5rem;
    padding-bottom: 0.75rem;
    border-bottom: 1px solid rgba(255,255,255,0.08);
}
.section-icon {
    width: 38px;
    height: 38px;
    background: linear-gradient(135deg, #4338ca, #0891b2);
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.1rem;
}
.section-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.3rem;
    font-weight: 700;
    color: #f1f5f9;
    margin: 0;
}

/* ── News Cards ── */
.news-card {
    background: linear-gradient(135deg, rgba(255,255,255,0.04) 0%, rgba(255,255,255,0.02) 100%);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1.25rem;
    position: relative;
    overflow: hidden;
    transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
    cursor: pointer;
}
.news-card:hover {
    background: linear-gradient(135deg, rgba(99,102,241,0.12) 0%, rgba(6,182,212,0.08) 100%);
    border-color: rgba(99,102,241,0.4);
    transform: translateY(-3px);
    box-shadow: 0 12px 40px rgba(99,102,241,0.2);
}
.news-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 4px;
    height: 100%;
    background: linear-gradient(180deg, #818cf8, #67e8f9);
    border-radius: 4px 0 0 4px;
    opacity: 0;
    transition: opacity 0.3s;
}
.news-card:hover::before { opacity: 1; }

.news-card-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 1rem;
    margin-bottom: 0.75rem;
}
.news-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.05rem;
    font-weight: 600;
    color: #f1f5f9;
    line-height: 1.4;
    flex: 1;
}
.news-badge {
    background: rgba(99,102,241,0.15);
    border: 1px solid rgba(99,102,241,0.3);
    border-radius: 6px;
    padding: 0.2rem 0.6rem;
    font-size: 0.72rem;
    color: #a5b4fc;
    white-space: nowrap;
    flex-shrink: 0;
}
.news-summary {
    color: rgba(255,255,255,0.65);
    font-size: 0.92rem;
    line-height: 1.7;
    margin-bottom: 1rem;
}
.news-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.news-meta {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    color: rgba(255,255,255,0.4);
    font-size: 0.78rem;
}
.news-sentiment {
    font-size: 0.8rem;
    padding: 0.2rem 0.6rem;
    border-radius: 6px;
}
.sentiment-positive { background: rgba(34,197,94,0.15); color: #4ade80; border: 1px solid rgba(34,197,94,0.3); }
.sentiment-negative { background: rgba(239,68,68,0.15); color: #f87171; border: 1px solid rgba(239,68,68,0.3); }
.sentiment-neutral  { background: rgba(99,102,241,0.15); color: #a5b4fc; border: 1px solid rgba(99,102,241,0.3); }
.news-link {
    color: #67e8f9;
    font-size: 0.8rem;
    text-decoration: none;
    display: flex;
    align-items: center;
    gap: 0.3rem;
    transition: color 0.2s;
}
.news-link:hover { color: #a5b4fc; }

/* ── Chat UI ── */
.chat-container {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 0;
    overflow: hidden;
}
.chat-header {
    background: linear-gradient(135deg, rgba(67,56,202,0.3), rgba(8,145,178,0.2));
    padding: 1rem 1.25rem;
    border-bottom: 1px solid rgba(255,255,255,0.08);
    display: flex;
    align-items: center;
    gap: 0.75rem;
}
.chat-avatar {
    width: 36px;
    height: 36px;
    background: linear-gradient(135deg, #4338ca, #0891b2);
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.1rem;
    flex-shrink: 0;
}
.chat-title { font-weight: 600; font-size: 0.95rem; color: #f1f5f9; }
.chat-status { font-size: 0.75rem; color: #4ade80; display: flex; align-items: center; gap: 0.3rem; }
.status-dot { width: 7px; height: 7px; background: #4ade80; border-radius: 50%; animation: blink 1.5s infinite; }
@keyframes blink { 0%,100% { opacity: 1; } 50% { opacity: 0.3; } }

.chat-messages {
    padding: 1.25rem;
    max-height: 450px;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    gap: 1rem;
}
.chat-bubble {
    display: flex;
    gap: 0.75rem;
    align-items: flex-start;
    animation: slideIn 0.3s ease-out;
}
@keyframes slideIn {
    from { opacity: 0; transform: translateY(10px); }
    to   { opacity: 1; transform: translateY(0); }
}
.chat-bubble.user { flex-direction: row-reverse; }
.bubble-avatar {
    width: 32px;
    height: 32px;
    border-radius: 9px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.9rem;
    flex-shrink: 0;
}
.bubble-avatar.ai   { background: linear-gradient(135deg, #4338ca, #0891b2); }
.bubble-avatar.user { background: linear-gradient(135deg, #7c3aed, #db2777); }
.bubble-text {
    max-width: 80%;
    padding: 0.85rem 1.1rem;
    border-radius: 14px;
    font-size: 0.9rem;
    line-height: 1.65;
}
.bubble-text.ai {
    background: rgba(99,102,241,0.12);
    border: 1px solid rgba(99,102,241,0.2);
    color: #e2e8f0;
    border-top-left-radius: 4px;
}
.bubble-text.user {
    background: linear-gradient(135deg, rgba(124,58,237,0.25), rgba(219,39,119,0.15));
    border: 1px solid rgba(124,58,237,0.3);
    color: #f1f5f9;
    border-top-right-radius: 4px;
    text-align: right;
}
.bubble-meta {
    font-size: 0.7rem;
    color: rgba(255,255,255,0.35);
    margin-top: 0.3rem;
}

/* ── Follow-up chips ── */
.followup-chip {
    display: inline-block;
    background: rgba(99,102,241,0.1);
    border: 1px solid rgba(99,102,241,0.25);
    border-radius: 999px;
    padding: 0.35rem 0.85rem;
    font-size: 0.8rem;
    color: #a5b4fc;
    cursor: pointer;
    transition: all 0.2s;
    margin: 0.2rem;
}
.followup-chip:hover {
    background: rgba(99,102,241,0.25);
    border-color: rgba(99,102,241,0.5);
    color: #c7d2fe;
}

/* ── Web badge ── */
.web-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.3rem;
    background: rgba(6,182,212,0.1);
    border: 1px solid rgba(6,182,212,0.25);
    border-radius: 999px;
    padding: 0.2rem 0.7rem;
    font-size: 0.72rem;
    color: #67e8f9;
    margin-bottom: 0.5rem;
}

/* ── Streamlit widget overrides ── */
.stTextInput > div > div > input {
    background: #111827 !important;
    border: 1px solid rgba(99,102,241,0.4) !important;
    border-radius: 12px !important;
    color: #ffffff !important;
    padding: 0.75rem 1rem !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.95rem !important;
    transition: all 0.2s !important;
}
.stTextInput > div > div > input:focus {
    border-color: #6366f1 !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.2) !important;
}
.stTextInput > div > div > input::placeholder { color: rgba(255,255,255,0.4) !important; }

/* Better Chat Message Visibility */
[data-testid="stChatMessage"] {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 12px !important;
    margin-bottom: 1rem !important;
    color: #f1f5f9 !important;
}
[data-testid="stChatMessage"] p, 
[data-testid="stChatMessage"] li, 
[data-testid="stChatMessage"] span,
[data-testid="stChatMessage"] div {
    color: #f1f5f9 !important;
    font-size: 0.95rem !important;
}
[data-testid="stChatMessage"] h1, 
[data-testid="stChatMessage"] h2, 
[data-testid="stChatMessage"] h3 {
    color: #ffffff !important;
    margin-top: 1rem !important;
    margin-bottom: 0.5rem !important;
}
[data-testid="stChatMessage"] strong {
    color: #a5b4fc !important;
    font-weight: 600 !important;
}
[data-testid="stChatMessage"] code {
    background: rgba(0,0,0,0.4) !important;
    color: #67e8f9 !important;
    padding: 0.1rem 0.3rem !important;
    border-radius: 4px !important;
}

.stSelectbox > div > div {
    background: #111827 !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 12px !important;
    color: #ffffff !important;
}
.stButton > button {
    background: linear-gradient(135deg, #4338ca 0%, #0891b2 100%) !important;
    border: none !important;
    border-radius: 12px !important;
    color: white !important;
    font-weight: 600 !important;
    font-family: 'Inter', sans-serif !important;
    padding: 0.6rem 1.5rem !important;
    transition: all 0.2s !important;
    letter-spacing: 0.02em;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 25px rgba(67,56,202,0.4) !important;
    background: linear-gradient(135deg, #5b50d6 0%, #0ea5e9 100%) !important;
}
.stCheckbox, .stCheckbox label { color: rgba(255,255,255,0.7) !important; }
.stCheckbox > label > div[data-testid="stCheckbox"] > div {
    border-color: rgba(99,102,241,0.5) !important;
}

[data-testid="stSpinner"] > div { color: #818cf8 !important; }

/* Dividers */
hr { border-color: rgba(255,255,255,0.08) !important; }

/* Sidebar specifics */
.sidebar-logo {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.5rem 0 1.5rem 0;
    border-bottom: 1px solid rgba(255,255,255,0.08);
    margin-bottom: 1.5rem;
}
.sidebar-logo-icon {
    width: 42px;
    height: 42px;
    background: linear-gradient(135deg, #4338ca, #0891b2);
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.3rem;
}
.sidebar-logo-text { font-family: 'Space Grotesk', sans-serif; font-size: 1.25rem; font-weight: 700; color: #f1f5f9; }
.sidebar-logo-sub { font-size: 0.7rem; color: rgba(255,255,255,0.4); }

.sidebar-section-label {
    font-size: 0.68rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: rgba(255,255,255,0.4);
    margin: 1.25rem 0 0.5rem 0;
}

/* Category tabs */
.cat-tab-row {
    display: flex;
    flex-wrap: wrap;
    gap: 0.4rem;
    margin-bottom: 1.5rem;
}
.cat-tab {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 999px;
    padding: 0.35rem 0.9rem;
    font-size: 0.8rem;
    color: rgba(255,255,255,0.6);
    cursor: pointer;
    transition: all 0.2s;
}
.cat-tab.active, .cat-tab:hover {
    background: rgba(99,102,241,0.2);
    border-color: rgba(99,102,241,0.5);
    color: #a5b4fc;
}

/* Loading skeleton */
.skeleton-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1.25rem;
    animation: shimmer 1.5s infinite;
}
@keyframes shimmer {
    0%   { opacity: 0.5; }
    50%  { opacity: 1; }
    100% { opacity: 0.5; }
}
.skeleton-line {
    height: 14px;
    background: rgba(255,255,255,0.08);
    border-radius: 4px;
    margin-bottom: 0.75rem;
}

/* Refresh indicator */
.refresh-bar {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    background: rgba(34,197,94,0.08);
    border: 1px solid rgba(34,197,94,0.2);
    border-radius: 10px;
    padding: 0.6rem 1rem;
    font-size: 0.8rem;
    color: #4ade80;
    margin-bottom: 1.5rem;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  Session state init
# ─────────────────────────────────────────────
defaults = {
    "latest_news": [],
    "last_refresh": 0,
    "chat_history": [],
    "location": "Global",
    "category": "All",
    "pending_question": "",
    "last_answer": None,
    "follow_ups": [],
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ─────────────────────────────────────────────
#  Sidebar
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <div class="sidebar-logo-icon">🌐</div>
        <div>
            <div class="sidebar-logo-text">NewsAI</div>
            <div class="sidebar-logo-sub">Real-Time Intelligence</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section-label">⚙️ Settings</div>', unsafe_allow_html=True)
    location = st.selectbox("🌍 Region", ["Global", "India", "US", "UK", "Europe", "Asia"], index=0)
    hours_range = st.slider("⏱ News from last N hours", 1, 48, 12)

    st.markdown('<div class="sidebar-section-label">🔄 Feed Controls</div>', unsafe_allow_html=True)
    col_r1, col_r2 = st.columns(2)
    with col_r1:
        refresh_btn = st.button("🔄 Refresh", use_container_width=True)
    with col_r2:
        clear_cache = st.button("🗑 Clear", use_container_width=True)

    if clear_cache:
        st.session_state.latest_news = []
        st.session_state.last_refresh = 0

    st.markdown("---")
    st.markdown('<div class="sidebar-section-label">💬 AI Chat Assistant</div>', unsafe_allow_html=True)

    # Chat input area in sidebar
    user_question = st.text_input(
        "Ask about the news…",
        placeholder="e.g. What happened in AI today?",
        key="chat_input_sidebar",
        label_visibility="collapsed"
    )
    use_web = st.checkbox("🌐 Search the web too", value=False)

    col_a1, col_a2 = st.columns(2)
    with col_a1:
        ask_btn = st.button("✨ Ask AI", use_container_width=True)
    with col_a2:
        clear_chat_btn = st.button("🗑 Clear Chat", use_container_width=True)

    if clear_chat_btn:
        st.session_state.chat_history = []
        st.session_state.follow_ups = []
        st.session_state.last_answer = None

    # Follow-up suggestions
    if st.session_state.follow_ups:
        st.markdown('<div class="sidebar-section-label">💡 Suggested Questions</div>', unsafe_allow_html=True)
        for q in st.session_state.follow_ups:
            if st.button(f"→ {q}", key=f"followup_{q[:30]}", use_container_width=True):
                st.session_state.pending_question = q

# ─────────────────────────────────────────────
#  Fetch / refresh news
# ─────────────────────────────────────────────
needs_refresh = (
    refresh_btn
    or not st.session_state.latest_news
    or (time.time() - st.session_state.last_refresh) > 300
    or location != st.session_state.location
)

if needs_refresh:
    st.session_state.location = location
    with st.spinner("⚡ Fetching latest news..."):
        st.session_state.latest_news = fetch_news(
            location=location,
            hours=hours_range,
            max_articles=200
        )
        st.session_state.last_refresh = time.time()

news_items = st.session_state.latest_news

# ─────────────────────────────────────────────
#  Handle AI question (sidebar or follow-up)
# ─────────────────────────────────────────────
pending_q = st.session_state.pop("pending_question", "") if st.session_state.get("pending_question") else ""
question_to_ask = user_question if ask_btn and user_question else pending_q

if question_to_ask:
    # Build context from news (Limit to 30 for speed)
    context = ""
    for a in news_items[:30]:
        context += f"Title: {a['title']}\nSummary: {a.get('summary','')}\nLink: {a['link']}\n\n"

    # Vector search (Limit to top 3)
    try:
        docs = search(question_to_ask)
        for d in docs[:3]:
            context += d + "\n\n"
    except Exception:
        pass

    with st.sidebar:
        # Use a placeholder for the streaming response
        st.markdown("---")
        st.markdown(f"**Question:** {question_to_ask}")
        answer_placeholder = st.empty()
        full_answer = ""
        
        # Show a minimal spinner only for the start
        with st.spinner("⚡ Connecting..."):
            stream_gen, web_searched = ask_ai(
                question=question_to_ask,
                context=context,
                chat_history=st.session_state.chat_history,
                use_web_search=use_web,
                stream=True
            )
            
            # Streaming loop
            for chunk in stream_gen:
                full_answer += chunk
                answer_placeholder.markdown(full_answer + "▌")
            
            answer_placeholder.markdown(full_answer)

        # After streaming, get follow-ups (Fast call)
        follow_ups = get_follow_up_suggestions(question_to_ask, full_answer)

    # Save to history
    st.session_state.chat_history.append({
        "question": question_to_ask,
        "answer": full_answer,
        "web_searched": web_searched,
        "time": datetime.now().strftime("%H:%M"),
    })
    st.session_state.follow_ups = follow_ups
    st.session_state.last_answer = {"answer": full_answer, "web_searched": web_searched}
    
    # Rerun to clear input and update UI
    st.rerun()

# ─────────────────────────────────────────────
#  MAIN LAYOUT
# ─────────────────────────────────────────────
now_str = datetime.now().strftime("%A, %B %d %Y · %I:%M %p")

st.markdown(f"""
<div class="hero-banner">
    <h1 class="hero-title">📰 NewsAI Intelligence</h1>
    <p class="hero-subtitle">Real-time news powered by AI — summarized, analyzed &amp; searchable</p>
    <div class="hero-time">🕐 {now_str}</div>
</div>
""", unsafe_allow_html=True)

# Stats bar
total_articles = len(news_items)
chat_count = len(st.session_state.chat_history)
last_refresh_mins = int((time.time() - st.session_state.last_refresh) / 60) if st.session_state.last_refresh else 0

st.markdown(f"""
<div class="stats-bar">
    <div class="stat-card">
        <div class="stat-value">{total_articles}</div>
        <div class="stat-label">Articles Loaded</div>
    </div>
    <div class="stat-card">
        <div class="stat-value">{chat_count}</div>
        <div class="stat-label">AI Interactions</div>
    </div>
    <div class="stat-card">
        <div class="stat-value">{last_refresh_mins}m</div>
        <div class="stat-label">Last Refreshed</div>
    </div>
    <div class="stat-card">
        <div class="stat-value">{location}</div>
        <div class="stat-label">Region Focus</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Two-column layout: news feed + chat
col_news, col_chat = st.columns([1.55, 1], gap="large")

# ─────────────────────────────────────────────
#  LEFT: News Feed
# ─────────────────────────────────────────────
with col_news:
    # Search bar
    search_query = st.text_input(
        "🔍 Search news…",
        placeholder="Filter by keyword, topic, or entity…",
        label_visibility="collapsed"
    )

    st.markdown("""
    <div class="section-header">
        <div class="section-icon">📡</div>
        <h2 class="section-title">Live News Feed</h2>
    </div>
    """, unsafe_allow_html=True)

    if time.time() - st.session_state.last_refresh < 5:
        st.markdown(f"""
        <div class="refresh-bar">
            ✅ Feed refreshed — {total_articles} articles loaded from the last {hours_range} hours
        </div>
        """, unsafe_allow_html=True)

    # Filter news by search
    display_news = news_items
    if search_query:
        q_lower = search_query.lower()
        display_news = [
            a for a in news_items
            if q_lower in a["title"].lower() or q_lower in a.get("summary", "").lower()
        ]

    if not display_news:
        st.markdown("""
        <div style="text-align:center; padding:3rem; color:rgba(255,255,255,0.4);">
            <div style="font-size:3rem;">🔍</div>
            <div style="font-size:1rem; margin-top:1rem;">No articles found. Try refreshing or changing the filter.</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        shown = min(20, len(display_news))
        for i, article in enumerate(display_news[:shown]):
            title = article["title"]
            link  = article["link"]
            pub   = article.get("published", "")
            raw_summary = article.get("summary", "")

            # Use existing summary from feed (fast); avoid heavy article extraction per card
            summary_text = raw_summary[:350] if raw_summary else "Click to read the full article."

            # Simple heuristic sentiment badge (no API call per card for performance)
            positive_words = ["growth", "success", "win", "record", "boom", "rise", "breakthrough", "gain", "positive", "profit"]
            negative_words = ["crash", "war", "death", "crisis", "collapse", "fail", "attack", "loss", "disaster", "danger"]
            title_lower = title.lower()
            if any(w in title_lower for w in positive_words):
                sentiment_class = "sentiment-positive"
                sentiment_label = "😊 Positive"
            elif any(w in title_lower for w in negative_words):
                sentiment_class = "sentiment-negative"
                sentiment_label = "😟 Negative"
            else:
                sentiment_class = "sentiment-neutral"
                sentiment_label = "😐 Neutral"

            # Numbered badge
            badge_num = i + 1

            st.markdown(f"""
            <div class="news-card">
                <div class="news-card-header">
                    <div class="news-title">{title}</div>
                    <div class="news-badge">#{badge_num}</div>
                </div>
                <div class="news-summary">{summary_text}</div>
                <div class="news-footer">
                    <div class="news-meta">
                        📅 {pub}
                    </div>
                    <div style="display:flex;align-items:center;gap:0.75rem;">
                        <span class="news-sentiment {sentiment_class}">{sentiment_label}</span>
                        <a class="news-link" href="{link}" target="_blank">Read full ↗</a>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  RIGHT: AI Chat Panel
# ─────────────────────────────────────────────
with col_chat:
    st.markdown("""
    <div class="section-header">
        <div class="section-icon">🤖</div>
        <h2 class="section-title">AI Chat Assistant</h2>
    </div>
    """, unsafe_allow_html=True)

    # Chat Container
    chat_container = st.container(height=500, border=True)
    
    with chat_container:
        if not st.session_state.chat_history:
            st.markdown("""
                <div style="text-align:center;padding:3rem 1rem;color:rgba(255,255,255,0.3);">
                    <div style="font-size:3rem;margin-bottom:1rem;">💬</div>
                    <div style="font-size:1.1rem;font-weight:600;color:rgba(255,255,255,0.5);">How can I help you today?</div>
                    <div style="font-size:0.85rem;margin-top:0.5rem;">Ask about breaking news, market trends, or world events.</div>
                </div>
            """, unsafe_allow_html=True)
        else:
            for chat in st.session_state.chat_history:
                with st.chat_message("user", avatar="👤"):
                    st.markdown(f'<div style="color:#f1f5f9;">{chat["question"]}</div>', unsafe_allow_html=True)
                
                with st.chat_message("assistant", avatar="🤖"):
                    if chat.get("web_searched"):
                        st.markdown('<span class="web-badge">🌐 Web searched</span>', unsafe_allow_html=True)
                    st.markdown(chat["answer"])

    # Tip below chat
    if st.session_state.chat_history:
        st.markdown(f"""
        <div style="background:rgba(99,102,241,0.08);border:1px solid rgba(99,102,241,0.2);border-radius:12px;
                    padding:0.85rem 1rem;margin-top:1rem;font-size:0.82rem;color:rgba(255,255,255,0.6);">
            💡 <strong style="color:#a5b4fc;">Tip:</strong> Use the sidebar to ask follow-up questions or enable web search for broader context.
        </div>
        """, unsafe_allow_html=True)

    # Quick-ask shortcuts
    st.markdown("""
    <div style="margin-top:1.25rem;">
        <div style="font-size:0.72rem;font-weight:600;text-transform:uppercase;letter-spacing:0.08em;
                    color:rgba(255,255,255,0.35);margin-bottom:0.6rem;">⚡ QUICK PROMPTS</div>
    </div>
    """, unsafe_allow_html=True)

    quick_prompts = [
        "📊 Top stories right now",
        "💹 Market & economy news",
        "🤖 Latest AI & Tech news",
        "🌍 Geopolitical updates",
    ]
    q_cols = st.columns(2)
    for idx, qp in enumerate(quick_prompts):
        with q_cols[idx % 2]:
            if st.button(qp, key=f"qp_{idx}", use_container_width=True):
                st.session_state.pending_question = qp
                st.rerun()

# ─────────────────────────────────────────────
#  Footer
# ─────────────────────────────────────────────
st.markdown("""
<div style="margin-top:3rem;padding:1.5rem;border-top:1px solid rgba(255,255,255,0.08);
            text-align:center;color:rgba(255,255,255,0.3);font-size:0.8rem;">
    🌐 <strong style="color:rgba(255,255,255,0.5);">NewsAI</strong> — Powered by GPT-4o-mini · 
    FAISS Vector Search · Google News RSS &nbsp;|&nbsp; 
    Built with ❤️ using Streamlit
</div>
""", unsafe_allow_html=True)