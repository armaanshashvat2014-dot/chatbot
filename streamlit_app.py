import streamlit as st
import sympy as sp
import wikipedia
import matplotlib.pyplot as plt
import fitz
import re

from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

st.set_page_config(page_title="SmartBot AI", layout="wide")

st.title("🧠 SmartBot AI")
st.caption("Ask questions, solve math, and analyze PDFs.")

# --------------------
# MEMORY
# --------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "pdf_text" not in st.session_state:
    st.session_state.pdf_text = None


# --------------------
# MATH
# --------------------

def looks_like_math(text):
    return bool(re.match(r'^[0-9\+\-\*\/\^\(\)\.\s]+$', text))


def solve_math(expr):

    try:
        result = sp.sympify(expr)
        return f"The answer is **{result}**."
    except:
        return None


# --------------------
# KNOWLEDGE
# --------------------

def search_knowledge(question):

    try:
        return wikipedia.summary(question, sentences=4)
    except:
        return None


# --------------------
# DIAGRAM
# --------------------

def draw_graph():

    fig, ax = plt.subplots()

    x = list(range(-10,10))
    y = [i*i for i in x]

    ax.plot(x,y)
    ax.set_title("Example Graph: y = x²")

    st.pyplot(fig)


# --------------------
# PDF READER
# --------------------

def read_pdf(file):

    doc = fitz.open(stream=file.read(), filetype="pdf")

    text = ""

    for page in doc:
        text += page.get_text()

    return text


# --------------------
# PDF SUMMARIZER
# --------------------

def summarize_text(text):

    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LsaSummarizer()

    summary = summarizer(parser.document, 6)

    result = ""

    for sentence in summary:
        result += str(sentence) + " "

    return result


# --------------------
# SMARTBOT BRAIN
# --------------------

def ask_ai(prompt):

    text = prompt.lower()

    if "who are you" in text:
        return "I am **SmartBot AI**, your assistant for learning, answering questions, solving math, and analyzing PDFs."

    if text in ["hi","hello","hey"]:
        return "Hello! How can I help you today?"

    if text.startswith("solve:"):
        return solve_math(text.replace("solve:",""))

    if looks_like_math(text):
        return solve_math(text)

    if "graph" in text or "diagram" in text:
        draw_graph()
        return "Here is a graph diagram."

    # PDF QUESTIONS
    if st.session_state.pdf_text:

        if "summary" in text or "summarize" in text:
            return summarize_text(st.session_state.pdf_text)

        if "pdf" in text or "document" in text:
            return summarize_text(st.session_state.pdf_text)

    knowledge = search_knowledge(prompt)

    if knowledge:
        return knowledge

    return "I'm not sure about that yet, but I can help with science, math, history, or PDF summaries."


# --------------------
# CHAT DISPLAY
# --------------------

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])


# --------------------
# INPUT AREA
# --------------------

st.markdown("### 💬 Ask SmartBot")

col1, col2 = st.columns([6,1])

with col1:
    user_prompt = st.text_input(
        "Type your question:",
        placeholder="Example: What is photosynthesis?"
    )

with col2:
    pdf_file = st.file_uploader("➕", type="pdf")


# --------------------
# HANDLE PDF
# --------------------

if pdf_file:

    st.session_state.pdf_text = read_pdf(pdf_file)

    st.success("PDF uploaded! You can now ask me to summarize it.")


# --------------------
# ASK BUTTON
# --------------------

if st.button("Ask") and user_prompt:

    st.session_state.messages.append({"role":"user","content":user_prompt})

    with st.chat_message("user"):
        st.write(user_prompt)

    response = ask_ai(user_prompt)

    with st.chat_message("assistant"):
        st.write(response)

    st.session_state.messages.append({"role":"assistant","content":response})


# --------------------
# SIDEBAR HELP
# --------------------

st.sidebar.title("Examples")

st.sidebar.markdown("""
Questions:

What is photosynthesis  
Explain gravity  

Math:

2+2*10  
solve: 25*12  

PDF:

Upload a PDF ➕  
Then ask:

summarize the pdf  
what is the document about
""")
