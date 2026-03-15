import streamlit as st
import sympy as sp
import wikipedia
import matplotlib.pyplot as plt
import re

st.set_page_config(page_title="SmartBot AI", layout="wide")

st.title("🧠 SmartBot AI")
st.caption("A friendly assistant that answers questions, explains topics, and solves math.")

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
# GRAPH GENERATOR
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

    if "who are you" in text:
        return "I am **SmartBot AI**, a friendly assistant that helps answer questions, explain topics, and solve math problems."

    if text in ["hi","hello","hey"]:
        return "Hello! I'm SmartBot AI. How can I help you today?"

    if text.startswith("solve:"):
        return solve_math(text.replace("solve:",""))

    if looks_like_math(text):
        return solve_math(text)

    if "graph" in text or "diagram" in text:
        draw_graph()
        return "I created a graph diagram."

    knowledge = search_knowledge(prompt)

    if knowledge:
        return knowledge

    return "That's an interesting question! Try asking about science, math, or history."

# ------------------------
# DISPLAY CHAT
# ------------------------

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# ------------------------
# INPUT AREA
# ------------------------

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

# ------------------------
# SIDEBAR
# ------------------------

st.sidebar.title("Examples")

st.sidebar.markdown("""
Try asking:

What is photosynthesis  
Explain gravity  
Who invented computers  

Math:

2+2*10  
solve: 45*12  

Graphs:

draw graph
""")
