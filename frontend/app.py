import streamlit as st

from api.client import BackendClient
import uuid
import inspect

st.set_page_config(
    page_title="ResearchForge AI",
    page_icon="🔬",
)

st.title("🔬 ResearchForge AI")

client = BackendClient()
print(inspect.signature(BackendClient.chat))
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:

    with st.chat_message(
        message["role"],
    ):

        st.write(
            message["content"],
        )

        if (
            message["role"] == "assistant"
            and "sources" in message
            and message["sources"]
        ):

            with st.expander(
                "Sources",
            ):

                for source in message["sources"]:

                    st.markdown(
                        f"- [{source['name']}]({source['url']})"
                    )

prompt = st.chat_input(
    "Ask ResearchForge...",
)

if prompt:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt,
        }
    )

    with st.chat_message(
        "user",
    ):
        st.write(
            prompt,
        )

    with st.chat_message(
        "assistant",
    ):

        result = client.chat(
    session_id=st.session_state.session_id,
    message={
        "role": "user",
        "content": prompt,
    },
)

        st.write(
            result["response"],
        )

        if result["sources"]:

            with st.expander(
                "Sources",
            ):

                for source in result["sources"]:

                    st.markdown(
                        f"- [{source['name']}]({source['url']})"
                    )

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": result["response"],
            "sources": result["sources"],
        }
    )