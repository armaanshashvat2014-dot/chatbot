import streamlit as st
import sympy as sp
import wikipedia
import matplotlib.pyplot as plt
import numpy as np
from PyPDF2 import PdfReader
from duckduckgo_search import DDGS
import random
import re
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(page_title="SmartBot AI", layout="wide")

st.title("🧠 SmartBot AI")
st.caption("SmartBot AI • Math • PDF • Knowledge")

# -------------------------
# STATE
# -------------------------

for key, default in {
    "pdf_text": "",
    "points": 0,
    "history": [],
    "weak_topics": []
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# -------------------------
# PERSONALITY
# -------------------------

def personality(text):
    t = text.lower()

    if t in ["hi", "hello", "hey"]:
        return "Hey 👋 I’m SmartBot AI. What do you want to learn today?"

    if "how are you" in t:
        return "I’m doing great 🚀 Let’s learn something interesting!"

    if "what can you do" in t:
        return """I can:
🧮 Solve math  
📄 Understand PDFs  
📊 Plot graphs  
🧪 Generate quizzes  
📚 Explain concepts"""

    return None

# -------------------------
# MATH (SAFE)
# -------------------------

def solve_math(expr):
    try:
        x = sp.symbols('x')

        if "=" in expr:
            left, right = expr.split("=")
            eq = sp.Eq(sp.sympify(left), sp.sympify(right))
            return f"🧮 Solution: {sp.solve(eq)}"

        if any(c.isdigit() for c in expr):
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

    result = "📄 From your PDF:\n\n"
    for i in top:
        result += chunks[i][:300] + "\n\n"

    return result

def summarize_pdf():
    chunks = chunk_text(st.session_state.pdf_text)
    return "📄 Summary:\n\n" + "\n\n".join(c[:200] for c in chunks[:3])

# -------------------------
# KNOWLEDGE ENGINE (FIXED)
# -------------------------

def wiki_answer(prompt):
    try:
        results = wikipedia.search(prompt)

        if not results:
            return None

        return wikipedia.summary(results[0], sentences=3)

    except:
        return None

def web_answer(prompt):
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(prompt, max_results=2))

            if results:
                return results[0]["body"]

    except:
        pass

    return None

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
# MAIN AI
# -------------------------

def smartbot(prompt):
    st.session_state.history.append(prompt)
    text = prompt.lower()

    # personality
    p = personality(prompt)
    if p:
        return p

    # math
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

    # KNOWLEDGE (FIXED)
    wiki = wiki_answer(prompt)
    if wiki:
        return "📘 " + wiki

    # WEB
    web = web_answer(prompt)
    if web:
        return "🌐 " + web

    return """🤔 I couldn’t find a strong answer.

Try:
• Asking more clearly  
• Or upload a PDF 📄  
"""

# -------------------------
# UI
# -------------------------

uploaded = st.sidebar.file_uploader("📄 Upload PDF")

if uploaded:
    st.session_state.pdf_text = read_pdf(uploaded)
    st.sidebar.success("PDF Loaded!")

st.sidebar.write("🏆 Points:", st.session_state.points)

prompt = st.chat_input("Ask anything...")

if prompt:
    st.chat_message("user").write(prompt)

    response = smartbot(prompt)

    st.chat_message("assistant").write(response)

    st.session_state.points += 5
