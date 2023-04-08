import openai
import streamlit as st
from streamlit_chat import message

# Set up the OpenAI API key
openai.api_key = st.secrets["api_key"]


def hide_style():
    # Hides the Streamlit menu and footer
    return """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style>
        """


st.markdown(hide_style(), unsafe_allow_html=True)

# Add a brief explanation of the app
st.title("CareChat")
st.write("Welcome to CareChat, an AI-powered therapy chatbot. Enter your messages below to get started.")


if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []


def query(prompt):
    # Send a query to the OpenAI API and return the response
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=200,  # Increase the number of max_tokens for longer responses
        n=1,
        stop=None,
        temperature=0.7,  # Try adjusting the temperature for different responses
    )
    return response.choices[0].text.strip()


def get_text():
    # Get the user's input from the text input widget
    input_text = st.text_input("Patient: ")
    return input_text


# Add some shadow text to the text input box for better visual cue
text_input_placeholder = st.empty()
user_input = text_input_placeholder.text_input("Patient: ", value="", key="user_input", placeholder="Type your message here...")

submit_button = st.button("Ask")

if submit_button and user_input:
    context = "\n".join([f"Patient: {msg}" if i % 2 == 0 else f"Therapist: {msg}" for i, msg in
                         enumerate(st.session_state['past'] + st.session_state['generated'])])

    try:
        response = query(f"{context}\nPatient: {user_input}\nTherapist: ")
    except Exception as e:
        st.write(f"Error: {e}")
        response = "Sorry, there was an error processing your message."

    st.session_state.past.append(user_input)
    st.session_state.generated.append(response)

    # Clear the text input after the message is submitted
    text_input_placeholder.text_input("Patient: ", value="", key="user_input")

if st.session_state['generated']:
    for i in range(len(st.session_state['generated']) - 1,
