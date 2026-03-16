import streamlit as st
import sympy as sp
import wikipedia
import matplotlib.pyplot as plt
import numpy as np
import re

st.set_page_config(page_title="SmartBot AI", layout="wide")

st.title("🧠 SmartBot AI")
st.caption("Ask about math, science, history, and generate diagrams.")

# -------------------
# MEMORY
# -------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

# -------------------
# MATH
# -------------------

def looks_like_math(text):
    return bool(re.match(r'^[0-9a-zA-Z\+\-\*\/\^\(\)\.\s=]+$', text))

def solve_math(expr):

    try:
        x = sp.symbols('x')

        if "=" in expr:
            left,right = expr.split("=")
            equation = sp.Eq(sp.sympify(left), sp.sympify(right))
            solution = sp.solve(equation)

            return f"The solution is **{solution}**."

        result = sp.simplify(expr)

        return f"The simplified result is **{result}**."

    except:
        return None

# -------------------
# KNOWLEDGE
# -------------------

def search_knowledge(question):

    try:
        return wikipedia.summary(question, sentences=4)
    except:
        return None

# -------------------
# DIAGRAM GENERATOR
# -------------------

def draw_diagram(topic):

    topic = topic.lower()

    fig, ax = plt.subplots()

    if "triangle" in topic:

        ax.plot([0,1],[0,0])
        ax.plot([1,0.5],[0,1])
        ax.plot([0.5,0],[1,0])
        ax.set_title("Triangle")

    elif "circle" in topic:

        circle = plt.Circle((0,0),1,fill=False)
        ax.add_patch(circle)
        ax.set_xlim(-2,2)
        ax.set_ylim(-2,2)
        ax.set_title("Circle Diagram")

    elif "graph" in topic:

        x = np.linspace(-10,10,100)
        y = x**2
        ax.plot(x,y)
        ax.set_title("Graph of y = x²")

    elif "plant cell" in topic:

        ax.add_patch(plt.Rectangle((0.2,0.2),0.6,0.6))
        ax.text(0.5,0.5,"Nucleus",ha="center")
        ax.set_title("Simple Plant Cell")

    else:

        ax.text(0.3,0.5,"Diagram Not Available",size=15)

    st.pyplot(fig)

# -------------------
# SIMPLIFIER
# -------------------

def simplify_text(text):

    sentences = text.split(".")

    short = sentences[:2]

    return " ".join(short) + "."

# -------------------
# SMARTBOT
# -------------------

def ask_ai(prompt):

    text = prompt.lower()

    if text in ["hi","hello","hey"]:
        return "Hello! I'm SmartBot AI. Ask me anything about math, science, or history."

    if "who are you" in text:
        return "I am SmartBot AI, a knowledge assistant that helps explain topics, solve math, and generate diagrams."
if "Are you smart" in text:
        return "I am an AI, a knowledge assisant. It is your wish to decide it."
if "You are smart" in text:
        return "Thanks for the compliment."
    if "You are dumb, You are average, You are bad" in text:
        return "Thanks for letting me know, I shall improve myself.Please note that as an AI, I do not know human experiences or knowledge"


    if text.startswith("solve:"):
        return solve_math(text.replace("solve:",""))

    if looks_like_math(text):
        math = solve_math(text)

        if math:
            return math

    if "diagram" in text or "draw" in text:

        draw_diagram(text)

        return "Here is the diagram."

    knowledge = search_knowledge(prompt)

    if knowledge:

        if "simple" in text or "simplify" in text:
            return simplify_text(knowledge)

        return knowledge

    return "I'm not sure about that yet, but try asking about science, history, or math."

# -------------------
# DISPLAY CHAT
# -------------------

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# -------------------
# INPUT
# -------------------

user_prompt = st.chat_input("Ask SmartBot...")

if user_prompt:

    st.session_state.messages.append({"role":"user","content":user_prompt})

    with st.chat_message("user"):
        st.write(user_prompt)

    response = ask_ai(user_prompt)

    with st.chat_message("assistant"):
        st.write(response)

    st.session_state.messages.append({"role":"assistant","content":response})

# -------------------
# SIDEBAR
# -------------------

st.sidebar.title("Examples")

st.sidebar.markdown("""
History

Who was Napoleon  
What caused World War 1  

Science

What is photosynthesis  
Explain gravity  

Math

2*x + 4 = 10  
simplify x^2 + 2*x + 1  

Diagrams

draw triangle diagram  
draw plant cell diagram  
draw graph
""")

if st.sidebar.button("Clear Chat"):
    st.session_state.messages = []
