import os
import json
import traceback
import pandas as pd
import streamlit as st
import re

from src.mcqgenerator.utils import read_file
from src.mcqgenerator.MCQGenerator import generate_evaluate_chain
from src.mcqgenerator.logger import logging

# ---------------- CONFIG ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
st.set_page_config(page_title="MCQ Generator", layout="wide", page_icon="🧠")

# ---------------- FABULOUS DARK ENHANCEMENTS ----------------
st.markdown("""
<style>
/* App Background and Font */
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');

html, body, [class*="css"]  {
    font-family: 'Outfit', sans-serif;
    color: #f1f5f9;
}

/* App Background Gradient */
.stApp {
    background: linear-gradient(135deg, #000000 0%, #0a0a0a 100%, #111111 100%);
    background-size: 200% 200%;
    animation: gradientBG 20s ease infinite;
}

@keyframes gradientBG {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* Fabulous gradient title */
.gradient-text {
    background: linear-gradient(to right, #eaff00, #ffcc00, #eaff00);
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 4rem;
    font-weight: 800;
    margin-bottom: 2rem;
    padding-bottom: 0px;
    text-shadow: 0 0 20px rgba(234, 255, 0, 0.3);
    animation: shine 3s linear infinite;
}

@keyframes shine {
    to { background-position: 200% center; }
}

/* Beautiful translucent containers (Glassmorphism effect) */
div[data-testid="stForm"], div.stMarkdown, div[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(15, 15, 15, 0.6) !important;
    border-radius: 20px;
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
}

div[data-testid="stForm"], div[data-testid="stVerticalBlockBorderWrapper"] {
    padding: 2rem !important;
    border: 1px solid rgba(234, 255, 0, 0.4) !important;
    box-shadow: 0 0 20px rgba(234, 255, 0, 0.15) !important;
    transition: transform 0.3s ease, border-color 0.3s ease, box-shadow 0.3s ease;
}

div[data-testid="stForm"]:hover, div[data-testid="stVerticalBlockBorderWrapper"]:hover {
    transform: translateY(-5px);
    border-color: rgba(234, 255, 0, 1) !important;
    box-shadow: 0 0 35px rgba(234, 255, 0, 0.5) !important;
}

div[data-testid="stFileUploader"] {
    background: transparent !important;
}

/* Smooth input elements */
div[data-baseweb="base-input"], div[data-baseweb="select"] > div {
    border-radius: 12px !important;
    background-color: rgba(20, 20, 20, 0.8) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    color: #f8fafc !important;
    transition: all 0.3s ease;
}

div[data-baseweb="base-input"]:focus-within, div[data-baseweb="select"] > div:focus-within {
    border-color: #eaff00 !important;
    box-shadow: 0 0 15px rgba(234, 255, 0, 0.4) !important;
}

/* Fabulous Primary Buttons and Form Submit Button */
div[data-testid="stFormSubmitButton"] > button,
button[kind="primary"],
.stButton > button[kind="primary"] {
    background: linear-gradient(45deg, #eaff00, #ff7b00) !important;
    color: #000000 !important;
    border: none !important;
    border-radius: 50px !important;
    font-weight: 800 !important;
    letter-spacing: 1px !important;
    padding: 0.6rem 2rem !important;
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
    box-shadow: 0 0 20px rgba(12, 5, 5, 0.7) !important;
}

div[data-testid="stFormSubmitButton"] > button *,
button[kind="primary"] *,
.stButton > button[kind="primary"] * {
    color: #000000 !important;
    font-weight: 800 !important;
}

div[data-testid="stFormSubmitButton"] > button:hover,
button[kind="primary"]:hover,
.stButton > button[kind="primary"]:hover {
    transform: scale(1.05) translateY(-3px) !important;
    box-shadow: 0 0 35px rgba(12, 5, 5, 0.7), inset 0 0 15px linear-gradient(45deg, #eaff00, #ff7b00) !important;
}

div[data-testid="stFormSubmitButton"] > button:hover *,
button[kind="primary"]:hover *,
.stButton > button[kind="primary"]:hover * {
    color: #000000 !important;
}

/* Secondary Button Styling */
button[kind="secondary"] {
    border-radius: 50px !important;
    border: 1px solid rgba(234, 255, 0, 0.4) !important;
    color: #e2e8f0 !important;
    background: rgba(20, 20, 20, 0.5) !important;
    font-weight: 600 !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 0 10px rgba(234, 255, 0, 0.1) !important;
}
button[kind="secondary"]:hover {
    background: rgba(234, 255, 0, 0.15) !important;
    color: #fff !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 0 25px rgba(234, 255, 0, 0.6) !important;
    border-color: #eaff00 !important;
}

/* Question Cards & Highlights */
div.stMarkdown h4 {
    color: #eaff00;
    font-weight: 700;
}

h2, h3 {
    color: #f8fafc !important;
    text-shadow: 0 2px 4px rgba(0,0,0,0.5);
}

hr {
    border-color: rgba(255, 255, 255, 0.1) !important;
}

</style>
""", unsafe_allow_html=True)

# ---------------- TEXT CLEANER ----------------
def clean_text(s):
    if not s:
        return ""
    return re.sub(r"\\s+", " ", str(s)).strip()

# ---------------- UNIQUE KEYS FOR EACH QUESTION ----------------
def get_radio_key(qno):
    return f"radio_{qno}"

st.markdown('<div class="gradient-text">🧠 MCQ Generator</div>', unsafe_allow_html=True)

# ---------------- JSON PARSER ----------------
def parse_json(text):
    if not text:
        return None
    text = text.replace("```json", "").replace("```", "").strip()
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1:
        return None
    try:
        return json.loads(text[start:end + 1])
    except:
        return None

# ---------------- MAIN PAGE CONTROLS ----------------
with st.container(border=True):
    st.subheader("⚙️ Quiz Configuration")
    
    with st.form("mcq_form"):
        col1, col2 = st.columns([1, 1], gap="large")
        
        with col1:
            uploaded_file = st.file_uploader(
                "📂 Upload document (PDF, TXT, DOCX)",
                type=["txt", "pdf", "docx"]
            )
            
        with col2:
            user_prompt = st.text_area(
                "📝 OR enter a topic", 
                placeholder="e.g., Database Management Systems, Normalization...",
                height=135
            )
            
        st.divider()
        st.markdown("#### 🔧 Output Settings")
        scol1, scol2, scol3, scol4 = st.columns(4)
        
        with scol1:
            mcq_count = st.number_input("🔢 Count", min_value=1, max_value=50, value=10)
        with scol2:
            subject = st.text_input("📚 Subject", "DBMS")
        with scol3:
            tone = st.selectbox("🎯 Difficulty", ["easy", "medium", "hard", "general"])
        with scol4:
            language = st.selectbox("🌐 Language", ["English", "Hindi", "Telugu", "Tamil", "Kannada"])

        st.write("") # Spacer
        submit = st.form_submit_button("🚀 Generate MCQs", use_container_width=True, type="primary")

# ---------------- SESSION STATE ----------------
if "quiz_data" not in st.session_state:
    st.session_state.quiz_data = None
if "user_answers" not in st.session_state:
    st.session_state.user_answers = {}
if "q_index" not in st.session_state:
    st.session_state.q_index = 0
if "show_results" not in st.session_state:
    st.session_state.show_results = False

# ---------------- GENERATE MCQS ----------------
if submit:
    try:
        if uploaded_file:
            full_text = read_file(uploaded_file)
        elif user_prompt.strip():
            full_text = user_prompt
        else:
            st.error("Please upload a file OR enter a topic to proceed.")
            st.stop()

        merged = {}
        seen = set()

        with st.spinner("⏳ Analyzing content and generating your MCQs... This may take a moment."):
            response = generate_evaluate_chain({
                "text": full_text,
                "number": mcq_count,
                "subject": subject,
                "tone": tone,
                "language": language
            })

        parsed = parse_json(response.get("quiz",""))

        if parsed:
            for _, q in parsed.items():
                if isinstance(q, list):
                    q = q[0]

                ques = clean_text(str(q.get("question", "")))
                raw_opts = q.get("options", {})
                if not isinstance(raw_opts, dict):
                    raw_opts = {}
                opts = {str(k).lower(): clean_text(v) for k, v in raw_opts.items()}
                corr = clean_text(str(q.get("correct", ""))).lower()

                if (not ques or ques in seen or
                    len(opts) < 4 or
                    corr not in ["a", "b", "c", "d"]):
                    continue

                q["question"] = ques
                q["options"] = opts
                q["correct"] = corr

                seen.add(ques)
                merged[str(len(merged)+1)] = q

        if not merged:
            st.error("No MCQs were generated. Please try a different topic.")
            st.stop()

        st.session_state.quiz_data = merged
        st.session_state.user_answers = {}
        st.session_state.q_index = 0
        st.session_state.show_results = False

    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        logging.error(str(e))
        st.error(f"An error occurred: {str(e)}")

# ---------------- EXAM MODE QUIZ ----------------
if st.session_state.quiz_data:
    st.divider()
    
    col1, col2 = st.columns([0.85, 0.15])
    with col1:
        st.markdown('<h2 style="color: #0ea5e9;">📘 Exam Mode</h2>', unsafe_allow_html=True)
    with col2:
        if st.button("🔄 Reset Quiz", use_container_width=True):
            st.session_state.quiz_data = None
            st.session_state.user_answers = {}
            st.session_state.q_index = 0
            st.session_state.show_results = False
            st.rerun()

    quiz_items = list(st.session_state.quiz_data.items())
    total_q = len(quiz_items)
    idx = st.session_state.q_index

    answered = len(st.session_state.user_answers)
    st.progress(answered / total_q)
    st.caption(f"**Progress**: Answered {answered} of {total_q}")

    qno, qdata = quiz_items[idx]

    st.write("") # Spacer
    
    # Custom Question Card
    with st.container(border=True):
        st.markdown(f"#### 📝 Question {idx+1} of {total_q}")
        st.markdown(f"**{qdata['question']}**")
        st.write("") # some spacing

        options = qdata["options"]

        # Get previous answer
        previous_answer = st.session_state.user_answers.get(qno, None)
        choice_index = ["a", "b", "c", "d"].index(previous_answer) if previous_answer else None

        choice = st.radio(
            "Select your answer:",
            options=["a", "b", "c", "d"],
            format_func=lambda x: f"{x.upper()}) {options.get(x, '')}",
            index=choice_index,
            key=get_radio_key(qno)
        )

        if choice:
            st.session_state.user_answers[qno] = choice

    # ---------- NAVIGATION ----------
    st.write("") # spacing
    nav_col1, nav_col2, nav_col3 = st.columns(3)

    with nav_col1:
        if st.button("⬅ Previous", disabled=(idx == 0), use_container_width=True):
            st.session_state.q_index -= 1
            st.rerun()

    with nav_col2:
        if st.button("Next ➡", disabled=(idx == total_q - 1), use_container_width=True):
            st.session_state.q_index += 1
            st.rerun()

    with nav_col3:
        if st.button("✅ Submit Quiz", type="primary", use_container_width=True):
            if len(st.session_state.user_answers) < total_q:
                st.warning("⚠️ Please answer all questions before submitting.")
            else:
                st.session_state.show_results = True

    # ---------- RESULTS VIEW ----------
    if st.session_state.get("show_results", False):
        st.divider()
        score = 0
        st.markdown('<h2 style="color: #10b981;">📊 Your Results</h2>', unsafe_allow_html=True)
        
        results_container = st.container(border=True)

        for _qno, _qdata in quiz_items:
            correct = _qdata["correct"]
            user = st.session_state.user_answers.get(_qno, None)

            with results_container:
                if user == correct:
                    score += 1
                    st.success(f"**Q{_qno}**: ✅ Correct! ({correct.upper()})")
                elif user:
                    st.error(
                        f"**Q{_qno}**: ❌ Incorrect. You chose {user.upper()}. "
                        f"**Correct Answer**: {correct.upper()} — {_qdata['options'].get(correct, 'N/A')}"
                    )
                else:
                    st.warning(f"**Q{_qno}**: ⚠️ Unanswered. **Correct Answer**: {correct.upper()} — {_qdata['options'].get(correct, 'N/A')}")

        st.write("")
        st.markdown(f"### 🎉 Final Score: \n# {score} / {total_q}")
        
        if score == total_q and score > 0:
            st.balloons()
        else:
            st.snow()