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
st.caption("A helpful AI that answers questions, solves math, explains topics, and summarizes PDFs.")

# -----------------------------
# CHAT MEMORY
# -----------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------------
# MATH DETECTION
# -----------------------------

def looks_like_math(text):
    return bool(re.match(r'^[0-9\+\-\*\/\^\(\)\.\s]+$', text))

def solve_math(expr):
    try:
        result = sp.sympify(expr)
        return f"The answer is **{result}**."
    except:
        return None

# -----------------------------
# KNOWLEDGE SEARCH
# -----------------------------

def search_knowledge(question):

    try:
        return wikipedia.summary(question, sentences=4)
    except:
        return None

# -----------------------------
# DIAGRAM GENERATOR
# -----------------------------

def draw_graph():

    fig, ax = plt.subplots()

    x = list(range(-10,10))
    y = [i*i for i in x]

    ax.plot(x,y)
    ax.set_title("Example Graph: y = x²")

    st.pyplot(fig)

# -----------------------------
# PDF READER
# -----------------------------

def read_pdf(file):

    doc = fitz.open(stream=file.read(), filetype="pdf")

    text = ""

    for page in doc:
        text += page.get_text()

    return text

# -----------------------------
# PDF SUMMARIZER
# -----------------------------

def summarize_text(text):

    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LsaSummarizer()

    summary = summarizer(parser.document, 5)

    result = ""

    for sentence in summary:
        result += str(sentence) + " "

    return result

# -----------------------------
# SMARTBOT BRAIN
# -----------------------------

def ask_ai(prompt):

    text = prompt.lower()

    if "who are you" in text:
        return "I am **SmartBot AI**, a friendly assistant that helps explain topics, solve math problems, and summarize documents."

    if text in ["hi","hello","hey"]:
        return "Hello! I'm SmartBot AI. What would you like to learn today?"

    if text.startswith("solve:"):
        return solve_math(text.replace("solve:",""))

    if looks_like_math(text):
        return solve_math(text)

    if "graph" in text or "diagram" in text:
        draw_graph()
        return "I created a graph diagram for you."

    knowledge = search_knowledge(prompt)

    if knowledge:
        return knowledge

    return "I'm not completely sure about that yet, but try asking about science, history, math, or upload a PDF for me to summarize."

# -----------------------------
# DISPLAY CHAT
# -----------------------------

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# -----------------------------
# QUESTION INPUT
# -----------------------------

st.markdown("### 💬 Ask SmartBot")

user_prompt = st.text_input(
    "Type your question:",
    placeholder="Example: What is photosynthesis?"
)

if st.button("Ask") and user_prompt:

    st.session_state.messages.append({"role":"user","content":user_prompt})

    with st.chat_message("user"):
        st.write(user_prompt)

    response = ask_ai(user_prompt)

    with st.chat_message("assistant"):
        st.write(response)

    st.session_state.messages.append({"role":"assistant","content":response})

# -----------------------------
# PDF TOOL
# -----------------------------

st.sidebar.title("📄 PDF Analyzer")

pdf_file = st.sidebar.file_uploader("Upload a PDF", type="pdf")

if pdf_file:

    text = read_pdf(pdf_file)

    st.sidebar.write("### PDF Summary")

    summary = summarize_text(text)

    st.sidebar.write(summary)

# -----------------------------
# SIDEBAR HELP
# -----------------------------

st.sidebar.title("🧰 Examples")

st.sidebar.markdown("""
Try asking:

What is photosynthesis  
Who invented computers  
What is gravity  

Math:

2+2*10  
solve: 25*12  

Tools:

draw graph  
Upload a PDF to summarize it
""")
