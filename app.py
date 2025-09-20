import streamlit as st
from energy_agent import process_query
from datetime import datetime

# Set page config
st.set_page_config(
    page_title="Allen Works AI Assistant",
    page_icon="⚡",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .stTextInput > div > div > input {
        border-radius: 20px;
        padding: 12px;
    }
    .stButton>button {
        width: 100%;
        border-radius: 20px;
        height: 50px;
        font-weight: bold;
    }
    .chat-message {
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        align-items: flex-start;
    }
    .chat-message.user {
        background-color: #f0f2f6;
        margin-left: 20%;
    }
    .chat-message.assistant {
        background-color: #e6f3ff;
        margin-right: 20%;
    }
    .message-content {
        margin-left: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I'm your Energy Usage Assistant. How can I help you with your energy data today?"}
    ]

# Suggested questions
suggested_questions = [
    "Show me a summary of my energy usage",
    "What was my total electricity usage last month?",
    "How much did I spend on electricity last quarter?",
    "Compare my usage between January and March"
]

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Display suggested questions as buttons
st.write("### Try asking:")
cols = st.columns(2)
for i, question in enumerate(suggested_questions):
    if cols[i % 2].button(question, use_container_width=True):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": question})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(question)
        
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = process_query(question)
                st.markdown(response)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        # Rerun to update the chat
        st.rerun()

# Chat input
if prompt := st.chat_input("Ask about your energy usage..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = process_query(prompt)
            st.markdown(response)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Rerun to update the chat
    st.rerun()
