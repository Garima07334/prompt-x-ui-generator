import streamlit as st
import textwrap
from groq import Groq
import streamlit.components.v1 as components

# =====================================
# 🔑 GROQ API KEY
# =====================================

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# =====================================
# ✅ STABLE GROQ MODEL
# =====================================
MODEL_NAME = "llama-3.1-8b-instant"

# =====================================
# 🔥 PROMPT ENHANCER + GOOGLE-STYLE INFO
# =====================================
@st.cache_data(show_spinner=False)
def enhance_and_search(user_prompt: str):

    combined_prompt = f"""
You are a search assistant.

TASKS:
1. Rewrite the user query into a clear, precise enhanced prompt.
2. Provide factual, neutral, Google-style information about the topic.

FORMAT STRICTLY AS:
ENHANCED_PROMPT:
<text>

TOPIC_INFORMATION:
<text>

USER QUERY:
{user_prompt}
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": textwrap.dedent(combined_prompt)}]
    ).choices[0].message.content

    enhanced = user_prompt
    info = response

    if "ENHANCED_PROMPT:" in response and "TOPIC_INFORMATION:" in response:
        enhanced = response.split("ENHANCED_PROMPT:")[1] \
                           .split("TOPIC_INFORMATION:")[0].strip()
        info = response.split("TOPIC_INFORMATION:")[1].strip()

    return enhanced, info


# =====================================
# 🎨 UI / WEBSITE GENERATION
# =====================================
def generate_ui_code(enhanced_prompt: str):

    ui_prompt = f"""
Generate a complete frontend UI based on the topic below.

Rules:
- Return ONLY valid HTML
- Include CSS inside <style>
- Include JS inside <script>
- Do NOT add explanations

TOPIC:
{enhanced_prompt}
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": textwrap.dedent(ui_prompt)}]
    )

    return response.choices[0].message.content


# =====================================
# 🌐 STREAMLIT UI
# =====================================
st.set_page_config(page_title="Prompt Enhancer + Smart Search", layout="wide")

st.title("✨ Prompt X UI Generator")
st.subheader("🚀A Hybrid AI Framework for Prompt Engineering and Automated UI Design🧩")

user_prompt = st.text_area(
    "Think it. Prompt it. Get it.",
    placeholder="search here...",
    height=120
)

generate_ui = st.checkbox("Generate UI / Website")

if st.button("Generate"):
    if not user_prompt.strip():
        st.warning("Please enter a query.")
    else:
        with st.spinner("Processing..."):
            enhanced_prompt, topic_info = enhance_and_search(user_prompt)

        st.markdown("### ✨ Enhanced Prompt")
        st.code(enhanced_prompt)

        st.markdown("### 📘 Topic Information")
        st.write(topic_info)

        if generate_ui:
            with st.spinner("Generating UI..."):
                ui_code = generate_ui_code(enhanced_prompt)

            st.markdown("### 🧩 Generated UI Code")
            st.code(ui_code, language="html")

            st.markdown("### 🎨 Live UI Preview")
            components.html(ui_code, height=550, scrolling=True)

