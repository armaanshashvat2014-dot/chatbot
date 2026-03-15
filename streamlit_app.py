import streamlit as st
import sympy as sp
import wikipedia
import matplotlib.pyplot as plt
from transformers import pipeline

st.set_page_config(page_title="SmartBot AI", layout="wide")

st.title("🧠 SmartBot AI")
st.caption("A friendly AI assistant for learning, questions, and problem solving.")

# Load open-source AI model
@st.cache_resource
def load_model():
    return pipeline(
        "text-generation",
        model="distilgpt2"
    )

generator = load_model()

# Chat memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# -------------------------
# MATH SOLVER
# -------------------------

def solve_math(expr):
    try:
        result = sp.sympify(expr)
        return f"Sure! The answer is **{result}**."
    except:
        return None

# -------------------------
# WIKIPEDIA SEARCH
# -------------------------

def wiki_search(topic):
    try:
        return "Here is what I found:\n\n" + wikipedia.summary(topic, sentences=3)
    except:
        return "Sorry, I couldn't find that topic. Please try asking in another way."

# -------------------------
# DIAGRAM GENERATOR
# -------------------------

def draw_graph():

    fig, ax = plt.subplots()

    x = list(range(-10,10))
    y = [i*i for i in x]

    ax.plot(x,y)
    ax.set_title("Example Graph: y = x²")

    st.pyplot(fig)

# -------------------------
# SMART AI BRAIN
# -------------------------

def ask_ai(prompt):

    text = prompt.lower()

    # identity
    if "who are you" in text:
        return "I am **SmartBot AI**, your friendly assistant. I help answer questions, solve math problems, explain science, and assist with learning."

    # greeting
    if text in ["hi","hello","hey"]:
        return "Hello! I'm SmartBot AI. How can I help you today?"

    # math command
    if text.startswith("solve:"):
        return solve_math(text.replace("solve:",""))

    # wikipedia command
    if text.startswith("wiki:"):
        return wiki_search(text.replace("wiki:",""))

    # diagram
    if "diagram" in text or "graph" in text:
        draw_graph()
        return "I created a simple graph diagram for you."

    # detect math automatically
    math = solve_math(text)
    if math:
        return math

    # AI response
    prompt_text = f"""
You are SmartBot AI, a kind, intelligent assistant for students.
Always respond clearly, politely, and helpfully.

User question: {prompt}
Answer:
"""

    result = generator(
        prompt_text,
        max_length=80,
        do_sample=True,
        temperature=0.7,
        repetition_penalty=1.5
    )

    answer = result[0]["generated_text"]

    return answer.replace(prompt_text,"")

# -------------------------
# CHAT DISPLAY
# -------------------------

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# -------------------------
# QUESTION INPUT
# -------------------------

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

# -------------------------
# SIDEBAR
# -------------------------

st.sidebar.title("🧰 SmartBot Tools")

st.sidebar.markdown("""
Example commands you can try:

solve: 25*12  
wiki: solar system  
draw graph  

Or ask normal questions like:

• What is gravity?  
• Who invented computers?  
• Explain photosynthesis  
""")
