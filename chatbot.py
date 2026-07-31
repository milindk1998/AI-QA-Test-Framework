import os
import json
from pathlib import Path
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

load_dotenv()

# Message storage configuration
MESSAGE_STORAGE_FILE = "ChatHistory.json"

def save_messages_to_json(messages: list, filepath: str = MESSAGE_STORAGE_FILE) -> None:
    try:
        with open(filepath, 'w') as f:
            json.dump(messages, f, indent=2)
    except Exception as e:
        print(f"Error saving messages: {e}")

def load_messages_from_json(filepath: str = MESSAGE_STORAGE_FILE) -> list:
    try:
        if Path(filepath).exists():
            with open(filepath, 'r') as f:
                return json.load(f)
    except Exception as e:
        print(f"Error loading messages: {e}")
    return []

# Initialize LangChain LLM with Groq configuration
llm = ChatOpenAI(
    api_key=os.getenv("grok_api_key"),
    base_url=os.getenv("base_url"),
    model=os.getenv("testmodel"),
    temperature=0,
    streaming=False
)

def ask_llm(prompt: str | list, message_history: list = None) -> str:
    if isinstance(prompt, list):
        return llm.invoke(prompt).content

    messages = [SystemMessage(content="You are a helpful assistant.")]

    # Rebuild history from JSON as typed message objects
    for msg in (message_history or []):
        if msg["role"] == "user":
            messages.append(HumanMessage(content=msg["content"]))
        elif msg["role"] == "assistant":
            messages.append(AIMessage(content=msg["content"]))

    messages.append(HumanMessage(content=prompt))
    return llm.invoke(messages).content


def run_streamlit_chatbot():
    import streamlit as st

    st.set_page_config(page_title="AI Chatbot", page_icon="🤖")
    st.title("🤖 Milind's Chatbot")
    st.markdown("In-Memory Chatbot developed by Milind Krishna | © 2026 (Powered by LangChain)")

    # Sidebar for controls
    st.sidebar.header("📊 Conversation Management")
    st.sidebar.markdown(f"**Note:** This Chatbot is powered by the model: `{os.getenv('testmodel')}`")
    
    # Initialize message history from JSON file (persistent across reloads)
    if "messages" not in st.session_state:
        st.session_state.messages = load_messages_from_json()
        if st.session_state.messages:
            st.sidebar.success(f"✅ Loaded {len(st.session_state.messages)} messages from history")
        else:
            st.sidebar.info("📝 No previous conversation history found")
    
    # Display conversation statistics
    msg_count = len(st.session_state.messages)
    user_msgs = sum(1 for m in st.session_state.messages if m["role"] == "user")
    assistant_msgs = sum(1 for m in st.session_state.messages if m["role"] == "assistant")
    
    st.sidebar.metric("Total Messages", msg_count)
    col1, col2 = st.sidebar.columns(2)
    col1.metric("User", user_msgs)
    col2.metric("Assistant", assistant_msgs)
    
    # Clear history button
    if st.sidebar.button("🗑️ Clear Conversation History"):
        st.session_state.messages = []
        save_messages_to_json([])
        st.sidebar.success("History cleared!")
        st.rerun()
    
    # Display all messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat input
    if prompt := st.chat_input("Ask me anything..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Get assistant response using full conversation history
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                # Pass all messages (from JSON + current session) to the LLM
                reply = ask_llm(prompt, st.session_state.messages)
            st.markdown(reply)

        # Add assistant message
        st.session_state.messages.append({"role": "assistant", "content": reply})
        
        # Save all messages to JSON file for persistence
        save_messages_to_json(st.session_state.messages)
        
        # Rerun to update the display and stats
        st.rerun()


if __name__ == "__main__":
    run_streamlit_chatbot()
