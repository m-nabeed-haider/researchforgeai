import streamlit as st

from api.client import BackendClient


st.set_page_config(
    page_title="ResearchForge AI",
    page_icon="🔬",
)

st.title("🔬 ResearchForge AI")

client = BackendClient()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

prompt = st.chat_input(
    "Ask ResearchForge..."
)

if prompt:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt,
        }
    )

    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):

        response = client.chat(
            st.session_state.messages,
        )

        st.write(response)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response,
        }
    )