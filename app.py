import streamlit as st
import ollama

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Intelligent Customer Support Chatbot",
    page_icon="🤖",
    layout="wide"
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

/* Main application */
.stApp {
    background-color: #f5f7fb;
}

/* Main content */
.main .block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* Title */
.title {
    text-align: center;
    font-size: 38px;
    font-weight: 700;
    color: #202124 !important;
    margin-bottom: 5px;
}

/* Subtitle */
.subtitle {
    text-align: center;
    font-size: 17px;
    color: #5f6368 !important;
    margin-bottom: 25px;
}

/* User message */
.user-message {
    background-color: #dbeafe !important;
    color: #111827 !important;
    padding: 16px;
    border-radius: 14px;
    margin: 12px 0;
    border: 1px solid #bfdbfe;
    font-size: 16px;
    line-height: 1.6;
}

/* Assistant message */
.bot-message {
    background-color: #ffffff !important;
    color: #111827 !important;
    padding: 16px;
    border-radius: 14px;
    margin: 12px 0;
    border: 1px solid #d1d5db;
    font-size: 16px;
    line-height: 1.6;
}

/* Message headings */
.user-message b {
    color: #1d4ed8 !important;
}

.bot-message b {
    color: #7c3aed !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #ffffff !important;
}

/* Sidebar text */
section[data-testid="stSidebar"] * {
    color: #202124;
}

/* Chat input */
.stChatInputContainer {
    background-color: #f5f7fb !important;
}

/* Info box */
div[data-testid="stAlert"] {
    color: #202124 !important;
}

/* Buttons */
.stButton > button {
    border-radius: 10px;
    font-weight: 600;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# TITLE
# =========================================================

st.markdown(
    '<div class="title">🤖 Intelligent Customer Support Chatbot</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">AI-powered customer support using Ollama</div>',
    unsafe_allow_html=True
)

# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.header("⚙️ Chatbot Settings")

    model = st.selectbox(
        "Select AI Model",
        ["llama3.2:3b"]
    )

    st.markdown("---")

    st.subheader("📌 Support Categories")

    st.write("🛒 Orders")
    st.write("💳 Payments")
    st.write("🚚 Delivery")
    st.write("🔄 Returns & Refunds")
    st.write("📦 Products")
    st.write("👤 Account")
    st.write("❓ General Help")

    st.markdown("---")

    if st.button("🗑️ Clear Chat", use_container_width=True):

        st.session_state.messages = []

        st.rerun()

# =========================================================
# CHAT HISTORY
# =========================================================

if "messages" not in st.session_state:

    st.session_state.messages = []

# =========================================================
# SYSTEM INSTRUCTION
# =========================================================

system_prompt = """
You are an intelligent customer support chatbot.

Your job is to provide helpful, friendly and professional
customer support.

You can help customers with:

- Orders
- Payments
- Delivery
- Returns
- Refunds
- Products
- Account related questions
- General customer support

Rules:

1. Be polite and professional.
2. Give simple and clear answers.
3. Keep answers reasonably short.
4. If information is missing, ask the customer for it.
5. Never invent order numbers or transaction details.
6. Never invent company policies.
7. If you don't know something, honestly say so.
8. Try to solve the customer's problem step by step.
"""

# =========================================================
# WELCOME MESSAGE
# =========================================================

if len(st.session_state.messages) == 0:

    st.markdown(
        """
        <div class="bot-message">
        🤖 <b>Support Assistant</b><br><br>
        Hello! 👋 Welcome to Intelligent Customer Support.
        <br><br>
        I can help you with orders, payments, delivery,
        returns, refunds and general questions.
        <br><br>
        How can I help you today?
        </div>
        """,
        unsafe_allow_html=True
    )

# =========================================================
# DISPLAY CHAT HISTORY
# =========================================================

for message in st.session_state.messages:

    if message["role"] == "user":

        st.markdown(
            f"""
            <div class="user-message">
                👤 <b>You</b><br><br>
                {message["content"]}
            </div>
            """,
            unsafe_allow_html=True
        )

    elif message["role"] == "assistant":

        st.markdown(
            f"""
            <div class="bot-message">
                🤖 <b>Support Assistant</b><br><br>
                {message["content"]}
            </div>
            """,
            unsafe_allow_html=True
        )

# =========================================================
# USER INPUT
# =========================================================

user_input = st.chat_input(
    "Type your customer support question..."
)

# =========================================================
# PROCESS USER MESSAGE
# =========================================================

if user_input:

    # Add user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    # Create conversation for Ollama
    conversation = [
        {
            "role": "system",
            "content": system_prompt
        }
    ]

    for message in st.session_state.messages:

        conversation.append(
            {
                "role": message["role"],
                "content": message["content"]
            }
        )

    # Generate AI response
    with st.spinner("🤖 Thinking..."):

        try:

            response = ollama.chat(
                model=model,
                messages=conversation
            )

            answer = response["message"]["content"]

        except Exception as e:

            answer = """
❌ I couldn't connect to Ollama.

Please make sure:

1. Ollama is installed.
2. Ollama is running.
3. The model `llama3.2:3b` is installed.

Run this command in CMD:

ollama pull llama3.2:3b
"""

    # Add AI response
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )

    # Refresh page
    st.rerun()

# =========================================================
# FOOTER
# =========================================================

st.markdown("---")

st.markdown(
    """
    <div style="text-align:center; color:#6b7280;">
        🤖 <b>Intelligent Customer Support Chatbot</b>
        <br>
        Powered by Ollama & Llama 3.2
    </div>
    """,
    unsafe_allow_html=True
)