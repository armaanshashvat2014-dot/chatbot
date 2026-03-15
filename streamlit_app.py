import streamlit as st
import sympy as sp
import wikipedia
import matplotlib.pyplot as plt
import fitz
import re
import nltk

from nltk.tokenize import sent_tokenize, word_tokenize
from collections import Counter

nltk.download("punkt")

st.set_page_config(page_title="SmartBot AI", layout="wide")

st.title("🧠 SmartBot AI")
st.caption("Ask questions, solve math, and summarize PDFs.")

# -------------------------
# MEMORY
# -------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "pdf_text" not in st.session_state:
    st.session_state.pdf_text = None

# -------------------------
# MATH
# -------------------------

def looks_like_math(text):
    return bool(re.match(r'^[0-9\+\-\*\/\^\(\)\.\s]+$', text))

def solve_math(expr):
    try:
        result = sp.sympify(expr)
        return f"The answer is **{result}**."
    except:
        return None

# -------------------------
# KNOWLEDGE
# -------------------------

def search_knowledge(question):

    try:
        return wikipedia.summary(question, sentences=4)
    except:
        return None

# -------------------------
# GRAPH
# -------------------------

def draw_graph():

    fig, ax = plt.subplots()

    x = list(range(-10,10))
    y = [i*i for i in x]

    ax.plot(x,y)
    ax.set_title("Example Graph: y = x²")

    st.pyplot(fig)

# -------------------------
# READ PDF
# -------------------------

def read_pdf(file):

    doc = fitz.open(stream=file.read(), filetype="pdf")

    text = ""

    for page in doc:
        text += page.get_text()

    return text

# -------------------------
# SMART PDF SUMMARIZER
# -------------------------

def summarize_pdf(text, n=6):

    sentences = sent_tokenize(text)

    words = word_tokenize(text.lower())

    word_freq = Counter(words)

    sentence_scores = {}

    for sentence in sentences:

        for word in word_tokenize(sentence.lower()):

            if word in word_freq:

                if sentence not in sentence_scores:
                    sentence_scores[sentence] = word_freq[word]
                else:
                    sentence_scores[sentence] += word_freq[word]

    best_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:n]

    return " ".join(best_sentences)

# -------------------------
# SMARTBOT
# -------------------------

def ask_ai(prompt):

    text = prompt.lower()

    # PDF priority
    if st.session_state.pdf_text:

        if "summary" in text or "summarize" in text:
            return summarize_pdf(st.session_state.pdf_text)

        if "pdf" in text or "document" in text:
            return summarize_pdf(st.session_state.pdf_text)

    if "who are you" in text:
        return "I am **SmartBot AI**, a helpful assistant for learning and summarizing documents."

    if text in ["hi","hello","hey"]:
        return "Hello! How can I help you today?"

    if text.startswith("solve:"):
        return solve_math(text.replace("solve:",""))

    if looks_like_math(text):
        return solve_math(text)

    if "graph" in text:
        draw_graph()
        return "Here is a graph diagram."

    knowledge = search_knowledge(prompt)

    if knowledge:
        return knowledge

    return "I'm not sure about that yet, but I can help with math, science questions, or PDF summaries."

# -------------------------
# DISPLAY CHAT
# -------------------------

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# -------------------------
# INPUT AREA
# -------------------------

st.markdown("### 💬 Ask SmartBot")

col1, col2 = st.columns([6,1])

with col1:
    user_prompt = st.text_input(
        "Type your question:",
        placeholder="Example: What is photosynthesis?"
    )

with col2:
    pdf_file = st.file_uploader("➕", type="pdf")

# -------------------------
# LOAD PDF
# -------------------------

if pdf_file:

    st.session_state.pdf_text = read_pdf(pdf_file)

    st.success("PDF loaded successfully. Ask me to summarize it!")

# -------------------------
# ASK BUTTON
# -------------------------

if st.button("Ask") and user_prompt:

    st.session_state.messages.append({"role":"user","content":user_prompt})

    with st.chat_message("user"):
        st.write(user_prompt)

    response = ask_ai(user_prompt)

    with st.chat_message("assistant"):
        st.write(response)

    st.session_state.messages.append({"role":"assistant","content":response})

# -------------------------
# SIDEBAR
# -------------------------

st.sidebar.title("Examples")

st.sidebar.markdown("""
Questions:

What is photosynthesis  
Explain gravity  

Math:

2+2*10  
solve: 25*12  

PDF:

Upload PDF ➕  
Then ask:

summarize the pdf
""")
