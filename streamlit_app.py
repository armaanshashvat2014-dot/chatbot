import streamlit as st
import sympy as sp
import wikipedia
import matplotlib.pyplot as plt
from transformers import pipeline

st.set_page_config(page_title="SmartBot AI", layout="wide")

st.title("🧠 SmartBot AI")
st.caption("Your friendly AI helper for learning, questions, and problem solving.")

# Load AI model
@st.cache_resource
def load_model():
    return pipeline("text-generation", model="distilgpt2")

generator = load_model()

# memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------
# FUNCTIONS
# -----------------

def solve_math(expr):
    try:
        result = sp.sympify(expr)
        return f"Sure! The answer is **{result}**."
    except:
        return None


def wiki_search(topic):
    try:
        return "Here's what I found:\n\n" + wikipedia.summary(topic, sentences=3)
    except:
        return "Sorry, I couldn't find that topic. Maybe try another question?"


def draw_graph():
    fig, ax = plt.subplots()

    x = list(range(-10,10))
    y = [i*i for i in x]

    ax.plot(x,y)
    ax.set_title("Example Graph: y = x²")

    st.pyplot(fig)


def ask_ai(prompt):

    text = prompt.lower()

    if text.startswith("solve:"):
        return solve_math(text.replace("solve:",""))

    if text.startswith("wiki:"):
        return wiki_search(text.replace("wiki:",""))

    if "diagram" in text:
        draw_graph()
        return "I created a simple graph diagram for you."

    math = solve_math(text)
    if math:
        return math

    # Friendly system prompt
    friendly_prompt = f"""
You are SmartBot AI, a kind and helpful learning assistant.
Always respond politely and clearly.

User question: {prompt}
Answer:
"""

    result = generator(friendly_prompt, max_length=80)

    return result[0]["generated_text"].replace(friendly_prompt,"")


# -----------------
# CHAT DISPLAY
# -----------------

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])


# -----------------
# INPUT AREA
# -----------------

st.markdown("### 💬 Ask SmartBot a Question")

user_prompt = st.text_input(
    "Type your question here:",
    placeholder="Example: What is gravity? or solve: 25*12"
)

if st.button("Ask SmartBot") and user_prompt:

    st.session_state.messages.append({"role":"user","content":user_prompt})

    with st.chat_message("user"):
        st.write(user_prompt)

    response = ask_ai(user_prompt)

    with st.chat_message("assistant"):
        st.write(response)

    st.session_state.messages.append({"role":"assistant","content":response})


# -----------------
# SIDEBAR
# -----------------

st.sidebar.title("🧰 SmartBot Tools")

st.sidebar.markdown("""
Examplary commands:

solve: 25*12  
wiki: black hole  
diagram  
""")

st.sidebar.markdown("SmartBot tries to help politely and explain things clearly.")
