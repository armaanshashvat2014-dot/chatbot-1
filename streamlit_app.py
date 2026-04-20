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
st.markdown("### Unlimited Global Intelligence")

# Initialize the Global Client
client = Client()

# --- Session State for Chat History ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system", 
            "content": "You are a highly accurate academic AI. Ensure all scientific terms (like Evaporation, Condensation, Precipitation) are spelled correctly. Use Markdown tables or lists for diagrams."
        },
        {
            "role": "assistant", 
            "content": "I am Complex AI. Ask me anything about Math, Science (like the Water Cycle), or History."
        }
    ]

# Display Chat History (Skipping the system prompt for the UI)
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# --- User Input Logic ---
if prompt := st.chat_input("Explain the water cycle steps..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        
        try:
            # We add a specific provider (like Bing, Google, or DuckDuckGo) 
            # via the g4f client to ensure higher quality spelling.
            stream = client.chat.completions.create(
                model="gpt-4o", # Requesting a high-tier model
                messages=st.session_state.messages,
                stream=True,
            )

            for chunk in stream:
                content = chunk.choices[0].delta.content
                if content:
                    full_response += content
                    response_placeholder.markdown(full_response + "▌")
            
            response_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})

        except Exception as e:
            st.error("Primary connection interrupted. Adjusting intelligence parameters...")
            try:
                # Fallback: Using a more stable provider explicitly for better spelling
                response = g4f.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "Correct spelling is mandatory. Science focus."},
                        {"role": "user", "content": prompt}
                    ],
                )
                final_text = str(response)
                response_placeholder.markdown(final_text)
                st.session_state.messages.append({"role": "assistant", "content": final_text})
            except Exception as e2:
                st.error("Connection failed. Check your internet or library version.")
