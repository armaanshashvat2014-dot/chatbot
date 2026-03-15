import streamlit as st
import sympy as sp
import wikipedia
import matplotlib.pyplot as plt
import re

st.set_page_config(page_title="SmartBot AI", layout="wide")

st.title("🧠 SmartBot AI")
st.caption("A friendly AI assistant that helps answer questions and solve problems.")

# Chat memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# -------------------------
# Check if input is math
# -------------------------

def looks_like_math(text):
    return bool(re.match(r'^[0-9\+\-\*\/\^\(\)\.\s]+$', text))

# -------------------------
# Math Solver
# -------------------------

def solve_math(expr):
    try:
        result = sp.sympify(expr)
        return f"The answer is **{result}**."
    except:
        return None

# -------------------------
# Knowledge Search
# -------------------------

def search_knowledge(question):
    try:
        return wikipedia.summary(question, sentences=3)
    except:
        return None

# -------------------------
# Diagram Generator
# -------------------------

def draw_graph():

    fig, ax = plt.subplots()

    x = list(range(-10,10))
    y = [i*i for i in x]

    ax.plot(x,y)
    ax.set_title("Example Graph: y = x²")

    st.pyplot(fig)

# -------------------------
# SmartBot Brain
# -------------------------

def ask_ai(prompt):

    text = prompt.lower()

    if "who are you" in text:
        return "I am **SmartBot AI**, a friendly assistant designed to help answer questions and explain topics."

    if text in ["hi","hello","hey"]:
        return "Hello! I'm SmartBot AI. How can I help you today?"

    # solve command
    if text.startswith("solve:"):
        return solve_math(text.replace("solve:",""))

    # detect math only if it really looks like math
    if looks_like_math(text):
        return solve_math(text)

    # diagrams
    if "graph" in text or "diagram" in text:
        draw_graph()
        return "I created a simple graph diagram."

    # knowledge search
    knowledge = search_knowledge(prompt)
    if knowledge:
        return knowledge

    return "That's an interesting question! I'm still learning, but try asking about science, history, or math."

# -------------------------
# Chat Display
# -------------------------

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# -------------------------
# Input Box
# -------------------------

st.markdown("### 💬 Ask SmartBot a Question")

user_prompt = st.text_input(
    "Type your question here:",
    placeholder="Example: What is photosynthesis?"
)

if st.button("Ask SmartBot") and user_prompt:

    st.session_state.messages.append({"role":"user","content":user_prompt})

    with st.chat_message("user"):
        st.write(user_prompt)

    response = ask_ai(user_prompt)

    with st.chat_message("assistant"):
        st.write(response)

    st.session_state.messages.append({"role":"assistant","content":response})

# -------------------------
# Sidebar
# -------------------------

st.sidebar.title("🧰 SmartBot Tools")

st.sidebar.markdown("""
Examples you can try:

2+2*10  
solve: 45*12  
What is photosynthesis  
Who invented computers  
Draw graph
""")
