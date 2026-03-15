import streamlit as st
import sympy as sp
import wikipedia
import matplotlib.pyplot as plt
import re

st.set_page_config(page_title="SmartBot AI", layout="wide")

st.title("🧠 SmartBot AI")
st.caption("A friendly AI assistant that remembers your conversation.")

# ------------------------
# MEMORY
# ------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

# ------------------------
# MATH DETECTION
# ------------------------

def looks_like_math(text):
    return bool(re.match(r'^[0-9\+\-\*\/\^\(\)\.\s]+$', text))


def solve_math(expr):
    try:
        result = sp.sympify(expr)
        return f"The answer is **{result}**."
    except:
        return None

# ------------------------
# KNOWLEDGE SEARCH
# ------------------------

def search_knowledge(question):
    try:
        return wikipedia.summary(question, sentences=4)
    except:
        return None

# ------------------------
# GRAPH
# ------------------------

def draw_graph():

    fig, ax = plt.subplots()

    x = list(range(-10,10))
    y = [i*i for i in x]

    ax.plot(x,y)
    ax.set_title("Example Graph: y = x²")

    st.pyplot(fig)

# ------------------------
# SMARTBOT LOGIC
# ------------------------

def ask_ai(prompt):

    text = prompt.lower()

    # greetings
    if text in ["hi","hello","hey"]:
        return "Hello! I'm SmartBot AI. How can I help you today?"

    # identity
    if "who are you" in text:
        return "I am **SmartBot AI**, a friendly assistant that answers questions, solves math, and explains topics."

    # math command
    if text.startswith("solve:"):
        return solve_math(text.replace("solve:",""))

    # detect math
    if looks_like_math(text):
        return solve_math(text)

    # diagrams
    if "graph" in text or "diagram" in text:
        draw_graph()
        return "I created a graph diagram."

    # knowledge
    knowledge = search_knowledge(prompt)

    if knowledge:
        return knowledge

    # fallback
    return "That's an interesting question! Try asking about science, math, or history."

# ------------------------
# DISPLAY CHAT HISTORY
# ------------------------

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# ------------------------
# INPUT
# ------------------------

user_prompt = st.chat_input("Ask SmartBot something...")

if user_prompt:

    # store user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_prompt
    })

    with st.chat_message("user"):
        st.write(user_prompt)

    # generate response
    response = ask_ai(user_prompt)

    with st.chat_message("assistant"):
        st.write(response)

    # store response
    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })

# ------------------------
# SIDEBAR
# ------------------------

st.sidebar.title("SmartBot Examples")

st.sidebar.markdown("""
Questions:

What is photosynthesis  
Explain gravity  
Who invented computers  

Math:

2+2*10  
solve: 45*12  

Graphs:

draw graph
""")

# Clear chat button
if st.sidebar.button("Clear Chat"):
    st.session_state.messages = []
