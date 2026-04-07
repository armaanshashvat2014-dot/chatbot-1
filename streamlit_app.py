import streamlit as st
from g4f.client import Client
import g4f

# --- Page Configuration ---
st.set_page_config(
    page_title="Complex Global AI",
    page_icon="🌍",
    layout="centered"
)

st.title("🌍 Complex Global AI")
st.markdown("### Unlimited Global Intelligence | No API Keys")

# Initialize the Global Client
client = Client()

# --- Session State for Chat History ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "I am Complex AI. I have access to global knowledge. Ask me anything about Math, Science, History, or Code."}
    ]

# Display Global Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# --- User Input Logic ---
if prompt := st.chat_input("Enter your question here..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # Generate Global Response
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        
        try:
            # We use gpt-4o for "Global" level intelligence
            stream = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            )

            for chunk in stream:
                if chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    full_response += content
                    response_placeholder.markdown(full_response + "▌")
            
            response_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})

        except Exception as e:
            st.error("The global provider is busy. Trying an alternative route...")
            try:
                # Fallback to a secondary global model if GPT-4o is throttled
                response = g4f.ChatCompletion.create(
                    model=g4f.models.default,
                    messages=[{"role": "user", "content": prompt}],
                )
                st.write(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e2:
                st.error("Global connection failed. Please try again in 5 seconds.")
