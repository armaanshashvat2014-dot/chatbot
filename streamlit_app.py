import streamlit as st
import sympy as sp
import wikipedia
import random
import matplotlib.pyplot as plt
from transformers import pipeline
from PIL import Image
import fitz

st.set_page_config(page_title="UltraAI", layout="wide")

st.title("🧠 UltraAI Lab")
st.caption("GitHub Open-Source AI Assistant")

# load open source AI model
generator = pipeline("text-generation", model="distilgpt2")

# chat memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# math solver
def solve_math(expr):
    try:
        result = sp.sympify(expr)
        return f"Answer: {result}"
    except:
        return None

# wikipedia
def wiki(topic):
    try:
        return wikipedia.summary(topic, sentences=3)
    except:
        return "Topic not found."

# diagram generator
def draw_graph():
    fig, ax = plt.subplots()
    x = list(range(-10,10))
    y = [i*i for i in x]
    ax.plot(x,y)
    ax.set_title("y = x²")
    st.pyplot(fig)

# pdf reader
def read_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text[:800]

# AI brain
def ask_ai(prompt):

    if prompt.startswith("solve:"):
        return solve_math(prompt.replace("solve:",""))

    if prompt.startswith("wiki:"):
        return wiki(prompt.replace("wiki:",""))

    if prompt.startswith("diagram"):
        draw_graph()
        return "Graph generated."

    math = solve_math(prompt)
    if math:
        return math

    result = generator(prompt, max_length=60)
    return result[0]["generated_text"]

# display messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# input
if prompt := st.chat_input("Ask anything..."):

    st.session_state.messages.append({"role":"user","content":prompt})

    with st.chat_message("user"):
        st.write(prompt)

    response = ask_ai(prompt)

    with st.chat_message("assistant"):
        st.write(response)

    st.session_state.messages.append({"role":"assistant","content":response})

# sidebar tools
st.sidebar.title("AI Tools")

img = st.sidebar.file_uploader("Upload Image", type=["png","jpg"])

if img:
    image = Image.open(img)
    st.sidebar.image(image)
    st.sidebar.write(f"Image size: {image.size}")

pdf = st.sidebar.file_uploader("Upload PDF", type="pdf")

if pdf:
    st.sidebar.write(read_pdf(pdf))
