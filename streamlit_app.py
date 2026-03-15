import streamlit as st
import sympy as sp
import wikipedia
import matplotlib.pyplot as plt
from transformers import pipeline

st.set_page_config(page_title="SmartBot AI", layout="wide")

st.title("🧠 SmartBot AI")
st.caption("A friendly AI assistant that helps answer questions and solve problems.")

# Load AI model
@st.cache_resource
def load_model():
    return pipeline("text-generation", model="distilgpt2")

generator = load_model()

# Memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------
# Math Solver
# -----------------------

def solve_math(expr):
    try:
        result = sp.sympify(expr)
        return f"Sure! The answer is **{result}**."
    except:
        return None

# -----------------------
# Knowledge Search
# -----------------------

def search_knowledge(question):

    try:
        return wikipedia.summary(question, sentences=3)
    except:
        return None

# -----------------------
# Diagram Generator
# -----------------------

def draw_graph():

    fig, ax = plt.subplots()

    x = list(range(-10,10))
    y = [i*i for i in x]

    ax.plot(x,y)
    ax.set_title("Example Graph: y = x²")

    st.pyplot(fig)

# -----------------------
# AI Brain
# -----------------------

def ask_ai(prompt):

    text = prompt.lower()

    # identity
    if "who are you" in text:
        return "I am **SmartBot AI**, a friendly assistant designed to help with learning, questions, and problem solving."

    # greetings
    if text in ["hi","hello","hey"]:
        return "Hello! I'm SmartBot AI. How can I help you today?"

    # math command
    if text.startswith("solve:"):
        return solve_math(text.replace("solve:",""))

    # detect math automatically
    math = solve_math(text)
    if math:
        return math

    # diagram
    if "graph" in text or "diagram" in text:
        draw_graph()
        return "I created a simple graph diagram for you."

    # knowledge search
    knowledge = search_knowledge(prompt)
    if knowledge:
        return knowledge

    # fallback AI response
    result = generator(
        prompt,
        max_length=60,
        do_sample=True,
        temperature=0.7,
        repetition_penalty=1.5
    )

    answer = result[0]["generated_text"]

    return answer.replace(prompt,"")

# -----------------------
# Display chat
# -----------------------

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# -----------------------
# Input box
# -----------------------

st.markdown("### 💬 Ask SmartBot a Question")

user_prompt = st.text_input(
    "Type your question:",
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

# -----------------------
# Sidebar
# -----------------------

st.sidebar.title("🧰 SmartBot Tools")

st.sidebar.markdown("""
Examples you can try:

solve: 45*12  
What is photosynthesis  
Who invented computers  
Draw graph  
""")
