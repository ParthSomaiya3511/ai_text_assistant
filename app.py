import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os
import time

# ======================================================
# LOAD ENVIRONMENT VARIABLES
# ======================================================

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")


# =========================================
# PAGE CONFIG
# =========================================

st.set_page_config(
    page_title="AI Assistant Pro",
    page_icon="🤖",
    layout="wide"
)

# =========================================
# LOAD CSS
# =========================================

def load_css():

    with open("assets/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# ======================================================
# SESSION STATE
# ======================================================

if "history" not in st.session_state:
    st.session_state.history = []

# ======================================================
# CHECK API KEY
# ======================================================

if not GROQ_API_KEY:
    st.error("❌ GROQ_API_KEY not found in .env file")
    st.stop()

# ======================================================
# INITIALIZE GROQ CLIENT
# ======================================================

client = Groq(api_key=GROQ_API_KEY)

# ======================================================
# SIDEBAR
# ======================================================

with st.sidebar:

    st.title("🤖 AI Assistant Pro")

    st.markdown("---")

    st.success("🚀 Powered by Llama 3")

    # ==============================================
    # TONE SELECTOR
    # ==============================================

    tone = st.selectbox(
        "🎭 Select AI Tone",
        [
            "Professional",
            "Friendly",
            "Creative",
            "Beginner",
            "Motivational"
        ]
    )

    # ==============================================
    # PROMPT TEMPLATES
    # ==============================================

    st.markdown("---")

    st.subheader("⚡ Prompt Templates")

    template = st.selectbox(
        "Choose Template",
        [
            "None",
            "Instagram Caption",
            "Blog Introduction",
            "YouTube Script",
            "Business Email",
            "Motivational Quote",
            "Explain Python"
        ]
    )

    # ==============================================
    # CLEAR HISTORY
    # ==============================================

    st.markdown("---")

    if st.button("🗑 Clear Chat History"):
        st.session_state.history = []
        st.rerun()

# ======================================================
# TEMPLATE CONTENT
# ======================================================

template_text = ""

if template == "Instagram Caption":
    template_text = "Write an engaging Instagram caption for a travel photo."

elif template == "Blog Introduction":
    template_text = "Write a professional blog introduction about Artificial Intelligence."

elif template == "YouTube Script":
    template_text = "Write a YouTube video intro about AI tools."

elif template == "Business Email":
    template_text = "Write a professional email to a client."

elif template == "Motivational Quote":
    template_text = "Write a motivational quote for students."

elif template == "Explain Python":
    template_text = "Explain Python programming for beginners."

# ======================================================
# TITLE
# ======================================================

st.markdown(
    '<div class="main-title">🤖 AI Assistant Pro</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">Advanced AI UI using Streamlit + Llama3 + Groq</div>',
    unsafe_allow_html=True
)

# ======================================================
# TABS
# ======================================================

tab1, tab2 = st.tabs(["💬 AI Assistant", "📜 Chat History"])

# ======================================================
# TAB 1
# ======================================================

with tab1:

    # ==============================================
    # USER INPUT
    # ==============================================

    user_text = st.text_area(
        "✍️ Enter Your Prompt",
        value=template_text,
        height=220,
        placeholder="Type your text here..."
    )

    # ==============================================
    # TASK SELECTION
    # ==============================================

    task = st.selectbox(
        "🧠 Select AI Task",
        [
            "Summarize",
            "Rewrite",
            "Explain",
            "Generate Ideas",
            "Translate",
            "Write Content"
        ]
    )

    # ==============================================
    # BUTTONS
    # ==============================================

    col1, col2 = st.columns(2)

    with col1:
        generate = st.button("🚀 Generate Response")

    with col2:
        clear = st.button("❌ Clear History")

    # ==============================================
    # CLEAR INPUT
    # ==============================================

    if clear:
        st.rerun()

    # ==============================================
    # GENERATE RESPONSE
    # ==============================================

    if generate:

        if not user_text.strip():
            st.warning("⚠️ Please enter some text")
            st.stop()

        prompt = f"""
        Tone: {tone}

        Task: {task}

        User Input:
        {user_text}

        Generate a high-quality AI response.
        """

        try:

            with st.spinner("🤖 AI is generating response..."):

                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=0.7,
                    max_tokens=1200
                )

                ai_response = response.choices[0].message.content

            # ==========================================
            # TYPING ANIMATION
            # ==========================================

            st.markdown("## ✅ AI Response")

            placeholder = st.empty()

            full_response = ""

            for char in ai_response:
                full_response += char

                placeholder.markdown(
                    f"""
                    <div class="response-box">
                    {full_response}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                time.sleep(0.002)

            # ==========================================
            # SAVE CHAT HISTORY
            # ==========================================

            st.session_state.history.append({
                "user": user_text,
                "ai": ai_response
            })

            # ==========================================
            # RESPONSE STATS
            # ==========================================

            st.markdown("## 📊 Response Statistics")

            c1, c2, c3 = st.columns(3)

            c1.metric("Words", len(ai_response.split()))
            c2.metric("Characters", len(ai_response))
            c3.metric("Lines", len(ai_response.splitlines()))

            # ==========================================
            # COPY SECTION
            # ==========================================

            st.markdown("## 📋 Copy Response")

            st.code(ai_response)

            # ==========================================
            # DOWNLOAD BUTTON
            # ==========================================

            st.download_button(
                label="📥 Download Response",
                data=ai_response,
                file_name="ai_response.txt",
                mime="text/plain"
            )

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

# ======================================================
# TAB 2 CHAT HISTORY
# ======================================================

with tab2:

    st.subheader("📜 Previous AI Conversations")

    if len(st.session_state.history) == 0:

        st.info("No chat history yet")

    else:

        for chat in reversed(st.session_state.history):

            st.markdown(
                f"""
                <div class="user-chat">
                👤 <b>User:</b><br><br>
                {chat['user']}
                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown(
                f"""
                <div class="ai-chat">
                🤖 <b>AI:</b><br><br>
                {chat['ai']}
                </div>
                """,
                unsafe_allow_html=True
            )

# ======================================================
# FOOTER
# ======================================================

st.markdown("---")

st.markdown(
    """
    <center>
        <p style="color:gray;">
            Built with ❤️ using Streamlit + Groq + Llama3
        </p>
    </center>
    """,
    unsafe_allow_html=True
)