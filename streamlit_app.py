import streamlit as st
import sympy as sp
import wikipedia
import matplotlib.pyplot as plt
import numpy as np
import requests
import re
from PyPDF2 import PdfReader
from duckduckgo_search import DDGS

st.set_page_config(page_title="SmartBot v7", layout="wide")

st.title("🧠 SmartBot-your mentor, upgraded")
st.caption("Math • Diagrams • Knowledge • Web Search • Simplified Learning")

# -------------------------
# SESSION MEMORY
# -------------------------

if "chats" not in st.session_state:
    st.session_state.chats = {}

if "current_chat" not in st.session_state:
    st.session_state.current_chat = None


def new_chat():

    cid = f"chat{len(st.session_state.chats)+1}"

    st.session_state.chats[cid] = {
        "title":"New Chat",
        "messages":[]
    }

    st.session_state.current_chat = cid


def add_message(role,text):

    chat = st.session_state.current_chat

    st.session_state.chats[chat]["messages"].append({
        "role":role,
        "content":text
    })

    if st.session_state.chats[chat]["title"]=="New Chat":
        st.session_state.chats[chat]["title"]=text[:30]


# -------------------------
# MATH ENGINE
# -------------------------

def looks_like_math(text):

    math_chars = "0123456789+-*/^=().x "

    return all(c.lower() in math_chars for c in text)


def solve_math(expr):

    try:

        x=sp.symbols('x')

        if "=" in expr:

            left,right=expr.split("=")

            eq=sp.Eq(sp.sympify(left),sp.sympify(right))

            sol=sp.solve(eq)

            return f"🧮 Solution: **{sol}**"

        result=sp.simplify(expr)

        return f"🧮 Result: **{result}**"

    except:

        return None


# -------------------------
# GRAPH ENGINE
# -------------------------

def plot_function(expr):

    try:

        x=sp.symbols('x')

        f=sp.sympify(expr)

        func=sp.lambdify(x,f,"numpy")

        xs=np.linspace(-10,10,400)

        ys=func(xs)

        fig,ax=plt.subplots()

        ax.plot(xs,ys)

        ax.set_title(f"Graph of {expr}")

        st.pyplot(fig)

        return True

    except:

        return False


# -------------------------
# WIKIPEDIA SEARCH
# -------------------------

def search_wikipedia(q):

    try:

        results = wikipedia.search(q)

        if results:

            return wikipedia.summary(results[0], sentences=3)

    except:
        pass

    return None


# -------------------------
# WEB SEARCH
# -------------------------

def web_search(q):

    try:

        with DDGS() as ddgs:

            results = list(ddgs.text(q, max_results=3))

            if results:

                answer = ""

                for r in results:
                    answer += f"**{r['title']}**\n{r['body']}\n\n"

                return answer

    except:
        pass

    return None


# -------------------------
# SIMPLIFY ENGINE
# -------------------------

def simplify_text(text):

    sentences=text.split(".")

    simple=sentences[:2]

    result=". ".join(simple)

    replacements={
        "approximately":"about",
        "utilize":"use",
        "numerous":"many",
        "individuals":"people"
    }

    for k,v in replacements.items():
        result=result.replace(k,v)

    return "🧠 Simple explanation:\n\n"+result+"."


# -------------------------
# IMAGE / DIAGRAM SEARCH
# -------------------------

def get_diagram(topic):

    try:

        url="https://en.wikipedia.org/api/rest_v1/page/summary/"+topic.replace(" ","_")

        res=requests.get(url)

        data=res.json()

        if "thumbnail" in data:
            return data["thumbnail"]["source"]

    except:
        pass

    return None


def show_diagram(topic):

    img=get_diagram(topic)

    if img:

        st.image(img, caption=topic)

        return True

    return False


# -------------------------
# PDF READER
# -------------------------

def read_pdf(file):

    reader=PdfReader(file)

    text=""

    for page in reader.pages:

        text+=page.extract_text()

    return text[:2000]


# -------------------------
# SMARTBOT BRAIN
# -------------------------

def smartbot(prompt):

    text=prompt.lower()

    # greeting
    if text in ["hi","hello","hey"]:
        return "Hello! Ask me about math, science, diagrams, or explanations."

    # math
    if looks_like_math(text):

        math=solve_math(text)

        if math:
            return math

    # graph
    if "plot" in text or "graph" in text:

        expr=text.replace("plot","").replace("graph","").replace("y=","").strip()

        if plot_function(expr):
            return f"Graph generated for **{expr}**."

    # diagram / image detection
    if any(word in text for word in [
        "draw","diagram","show","image","picture","pic","photo"
    ]):

        topic=text

        for w in [
            "draw","diagram","show","image","picture","pic","photo","of"
        ]:
            topic=topic.replace(w,"")

        topic=topic.strip()

        if show_diagram(topic):
            return f"Here is a diagram of **{topic}**."

    # wikipedia
    knowledge=search_wikipedia(prompt)

    if knowledge:

        if "simple" in text or "simplify" in text:
            return simplify_text(knowledge)

        return knowledge

    # web fallback
    web=web_search(prompt)

    if web:
        return web

    return "I couldn't find a clear answer."


# -------------------------
# SIDEBAR
# -------------------------

st.sidebar.title("💬 Chats")

if st.sidebar.button("➕ New Chat"):
    new_chat()

for cid in st.session_state.chats:

    if st.sidebar.button(st.session_state.chats[cid]["title"]):
        st.session_state.current_chat=cid

if st.session_state.current_chat is None:
    new_chat()


# -------------------------
# PDF TOOL
# -------------------------

st.sidebar.title("📄 PDF Reader")

pdf_file=st.sidebar.file_uploader("Upload PDF")

if pdf_file:

    text=read_pdf(pdf_file)

    st.sidebar.write("Preview:")

    st.sidebar.write(text[:500])


# -------------------------
# DISPLAY CHAT
# -------------------------

chat=st.session_state.current_chat

messages=st.session_state.chats[chat]["messages"]

for msg in messages:

    with st.chat_message(msg["role"]):
        st.write(msg["content"])


# -------------------------
# USER INPUT
# -------------------------

prompt=st.chat_input("Ask SmartBot...")

if prompt:

    add_message("user",prompt)

    with st.chat_message("user"):
        st.write(prompt)

    response=smartbot(prompt)

    with st.chat_message("assistant"):
        st.write(response)

    add_message("assistant",response)

    st.rerun()


# -------------------------
# HELP
# -------------------------

st.sidebar.markdown("### Example Prompts")

st.sidebar.markdown("""

Math  
2*x + 4 = 10  

Graphs  
plot y=x^2  

Knowledge  
Who was Napoleon  

Simplify  
Explain gravity simply
""")
