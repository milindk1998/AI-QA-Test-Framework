import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("grok_api_key"), base_url=os.getenv("base_url"))

Model = os.getenv("testmodel")

def ask_llm(prompt: str) -> str:
    response = client.chat.completions.create(
        model=Model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
            ],
        temperature=0,
        stream=False
    )
    return response.choices[0].message.content


# using streamlit to create a simple chatbot interface
# command: streamlit run chatbot.py
# open in browser: http://localhost:8501

st.set_page_config(page_title="AI Chatbot", page_icon="🤖")
st.title("🤖 Milind's Chatbot")
st.markdown("Simple Chatbot developed by Milind Krishna | © 2026")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask me anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            reply = ask_llm(prompt)
        st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})
