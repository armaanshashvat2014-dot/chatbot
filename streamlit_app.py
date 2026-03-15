import streamlit as st
import sympy as sp
import wikipedia
import matplotlib.pyplot as plt
from transformers import pipeline

st.set_page_config(page_title="SmartBot AI", layout="wide")

# TITLE
st.title("🧠 SmartBot AI")
st.subheader("Ask questions, solve math, search knowledge, and generate diagrams.")

# Load open-source AI model
@st.cache_resource
def load_model():
    return pipeline("text-generation", model="distilgpt2")

generator = load_model()

# Memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# -------------------
# FUNCTIONS
# -------------------

def solve_math(expr):
    try:
        result = sp.sympify(expr)
        return f"Answer: {result}"
    except:
        return None


def wiki_search(topic):
    try:
        return wikipedia.summary(topic, sentences=3)
    except:
        return "Topic not found."


def draw_graph():
    fig, ax = plt.subplots()

    x = list(range(-10, 10))
    y = [i * i for i in x]

    ax.plot(x, y)
    ax.set_title("Graph: y = x²")

    st.pyplot(fig)


def ask_ai(prompt):

    # math
    if prompt.startswith("solve:"):
        return solve_math(prompt.replace("solve:", ""))

    # wikipedia
    if prompt.startswith("wiki:"):
        return wiki_search(prompt.replace("wiki:", ""))

    # diagram
    if prompt.startswith("diagram"):
        draw_graph()
        return "Diagram generated."

    # auto math detect
    math = solve_math(prompt)
    if math:
        return math

    # AI response
    result = generator(prompt, max_length=60)
    return result[0]["generated_text"]


# -------------------
# CHAT DISPLAY
# -------------------

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])


# -------------------
# QUESTION BOX
# -------------------

st.markdown("### 💬 Ask SmartBot a Question")

user_prompt = st.text_input(
    "Type your question here:",
    placeholder="Example: What is gravity? or solve: 25*12"
)

if st.button("Ask SmartBot") and user_prompt:

    st.session_state.messages.append({"role": "user", "content": user_prompt})

    with st.chat_message("user"):
        st.write(user_prompt)

    response = ask_ai(user_prompt)

    with st.chat_message("assistant"):
        st.write(response)

    st.session_state.messages.append({"role": "assistant", "content": response})


# -------------------
# SIDEBAR TOOLS
# -------------------

st.sidebar.title("🧰 SmartBot Tools")

st.sidebar.markdown("""
Examples:

solve: 2+2*10  
wiki: black hole  
diagram  
""")
