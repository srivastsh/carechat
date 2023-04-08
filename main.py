import openai
import streamlit as st
from streamlit_chat import message

# Set up OpenAI API key
openai.api_key = st.secrets["api_key"]

# Hide Streamlit menu and footer
def hide_style():
    return """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style>
        """
st.markdown(hide_style(), unsafe_allow_html=True)

# Set up title and explanation
st.title("CareChat")
st.write("Welcome to CareChat, a therapy chatbot powered by OpenAI's GPT-3. This chatbot is designed to help you talk through your thoughts and feelings in a safe, non-judgmental environment. Simply type your message in the text box below and hit 'Ask' to get started.")

# Set up session state for past messages and generated responses
if 'generated' not in st.session_state:
    st.session_state['generated'] = []
if 'past' not in st.session_state:
    st.session_state['past'] = []

# Define function to query OpenAI API
def query(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response.choices[0].text.strip()

# Set up text input widget for user input
text_input_placeholder = st.empty()
user_input = text_input_placeholder.text_input("Type your message here...", key="user_input")

# Set up submit button
submit_button = st.button("Ask")

# Process user input and generate response
if submit_button and user_input:
    context = "\n".join([f"Patient: {msg}" if i % 2 == 0 else f"Therapist: {msg}" for i, msg in
                         enumerate(st.session_state['past'] + st.session_state['generated'])])
    response = query(f"{context}\nPatient: {user_input}\nTherapist: ")
    st.session_state.past.append(user_input)
    st.session_state.generated.append(response)
    # Clear the text input after the message is submitted
    text_input_placeholder.text_input("Type your message here...", value="", key="user_input")

# Display past messages and generated responses
if st.session_state['generated']:
    for i in range(len(st.session_state['generated']) - 1, -1, -1):
        message(st.session_state["generated"][i], key=f"{i}", is_shadow=True)
        message(st.session_state['past'][i], is_user=True, key=f"{i}_user", is_shadow=True)
