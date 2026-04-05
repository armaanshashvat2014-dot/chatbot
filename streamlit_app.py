import streamlit as st
import sympy as sp
import wikipedia
import matplotlib.pyplot as plt
import numpy as np
import requests
from PyPDF2 import PdfReader
from duckduckgo_search import DDGS
import random
import re
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(page_title="MentorLoop AI Ultimate", layout="wide")

st.title("🚀 MentorLoop AI - Ultimate Offline")
st.caption("PDF AI • Semantic Search • Quiz • Gamified Learning")

# -------------------------
# STATE
# -------------------------

for key, default in {
    "pdf_text": "",
    "points": 0,
    "history": [],
    "weak_topics": [],
    "leaderboard": {"You": 0}
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# -------------------------
# MODES
# -------------------------

mode = st.sidebar.radio("🧠 Mode", [
    "📘 Study",
    "🧪 Quiz",
    "⚡ Quick",
    "🧠 Deep Explain"
])

eli10 = st.sidebar.checkbox("Explain like I'm 10")

# -------------------------
# PERSONALITY
# -------------------------

def personality_response(text):
    t = text.lower()

    if t in ["hi", "hello", "hey"]:
        return "Hey 👋 I’m MentorLoop AI. Ready to learn something cool today?"

    if "how are you" in t:
        return "I’m doing great 🚀 What do you want to learn today?"

    if "what can you do" in t:
        return """I can:
🧮 Solve math  
📄 Understand PDFs  
📊 Plot graphs  
🧪 Generate quizzes  
📚 Explain concepts  
Try me 😎"""

    if len(t.split()) <= 2:
        return "Give me a bit more detail so I can help better 😊"

    return None

# -------------------------
# MATH (FIXED)
# -------------------------

def looks_like_math(text):
    allowed = "0123456789+-*/^=().x "
    return all(c.lower() in allowed for c in text.strip())

def solve_math(expr):
    try:
        x = sp.symbols('x')

        if "=" in expr:
            left, right = expr.split("=")
            eq = sp.Eq(sp.sympify(left), sp.sympify(right))
            sol = sp.solve(eq)
            return f"🧮 Solution: {sol}"

        result = sp.simplify(expr)

        if result is True or result is False:
            return None

        return f"🧮 Result: {result}"

    except:
        return None

# -------------------------
# GRAPH
# -------------------------

def plot(expr):
    try:
        x = sp.symbols('x')
        f = sp.sympify(expr)
        func = sp.lambdify(x, f, "numpy")

        xs = np.linspace(-10, 10, 400)
        ys = func(xs)

        fig, ax = plt.subplots()
        ax.plot(xs, ys)
        st.pyplot(fig)
        return True
    except:
        return False

# -------------------------
# PDF ENGINE
# -------------------------

def read_pdf(file):
    reader = PdfReader(file)
    text = ""
    for p in reader.pages:
        t = p.extract_text()
        if t:
            text += t
    return text

def chunk_text(text, size=400):
    words = text.split()
    return [" ".join(words[i:i+size]) for i in range(0, len(words), size)]

def semantic_search(question):
    chunks = chunk_text(st.session_state.pdf_text)
    vectorizer = TfidfVectorizer(stop_words="english")
    vectors = vectorizer.fit_transform(chunks)

    q_vec = vectorizer.transform([question])
    scores = cosine_similarity(q_vec, vectors).flatten()

    top = scores.argsort()[-3:][::-1]

    result = "📄 **From your PDF:**\n\n"
    for i in top:
        result += chunks[i][:300] + "\n\n"

    return result

def summarize_pdf():
    chunks = chunk_text(st.session_state.pdf_text)
    return "📄 Summary:\n\n" + "\n\n".join(c[:250] for c in chunks[:3])

def extract_topics(text):
    words = re.findall(r'\b[a-zA-Z]{4,}\b', text.lower())
    return [w for w, _ in Counter(words).most_common(10)]

# -------------------------
# QUIZ
# -------------------------

def generate_quiz(text):
    sentences = text.split(".")
    random.shuffle(sentences)

    quiz = "🧪 Quiz:\n\n"
    for i in range(5):
        quiz += f"Q{i+1}: What does this refer to?\n{sentences[i][:80]}...\n\n"
    return quiz

# -------------------------
# SIMPLIFY
# -------------------------

def simplify(text):
    s = text.split(".")
    return "🧠 Simple:\n\n" + ". ".join(s[:2])

# -------------------------
# MAIN AI
# -------------------------

def smartbot(prompt):
    st.session_state.history.append(prompt)
    text = prompt.lower()

    # personality
    p = personality_response(prompt)
    if p:
        return p

    # math (ONLY if it looks like math)
    if looks_like_math(prompt):
        m = solve_math(prompt)
        if m:
            return m

    # graph
    if "plot" in text:
        expr = text.replace("plot", "").strip()
        if plot(expr):
            return "📊 Graph generated."

    # PDF
    if st.session_state.pdf_text:
        if "summary" in text:
            return summarize_pdf()
        if "quiz" in text:
            return generate_quiz(st.session_state.pdf_text)
        if "pdf" in text:
            return semantic_search(prompt)

    # Wikipedia (concept questions)
    try:
        if "what is" in text or "who is" in text:
            topic = text.replace("what is", "").replace("who is", "")
            res = wikipedia.summary(topic, sentences=2)
            if eli10:
                return simplify(res)
            return "📘 " + res
    except:
        pass

    # fallback wiki
    try:
        res = wikipedia.summary(prompt, sentences=2)
        return "📚 " + res
    except:
        pass

    # web fallback
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(prompt, max_results=1))
            if results:
                return "🌐 " + results[0]["body"]
    except:
        pass

    return "Hmm… I couldn’t find a strong answer. Try rephrasing or upload a PDF 📄"

# -------------------------
# UI
# -------------------------

uploaded = st.sidebar.file_uploader("📄 Upload PDF")

if uploaded:
    st.session_state.pdf_text = read_pdf(uploaded)
    st.sidebar.success("PDF Loaded!")

st.sidebar.write("🏆 Points:", st.session_state.points)
st.sidebar.progress(min(st.session_state.points / 100, 1.0))

if st.session_state.pdf_text:
    st.sidebar.subheader("📚 Topics")
    st.sidebar.write(", ".join(extract_topics(st.session_state.pdf_text)))

st.sidebar.subheader("⚠️ Weak Areas")
st.sidebar.write(st.session_state.weak_topics[-5:])

st.sidebar.subheader("📊 Stats")
st.sidebar.write("Questions:", len(st.session_state.history))

st.session_state.leaderboard["You"] = st.session_state.points
st.sidebar.subheader("🏆 Leaderboard")
for u, p in st.session_state.leaderboard.items():
    st.sidebar.write(f"{u}: {p}")

prompt = st.chat_input("Ask anything...")

if prompt:
    st.chat_message("user").write(prompt)

    response = smartbot(prompt)

    st.chat_message("assistant").write(response)

    st.session_state.points += 5

    if "couldn’t" in response.lower():
        st.session_state.weak_topics.append(prompt)
