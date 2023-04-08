import openai
import streamlit as st
from streamlit_chat import message

openai.api_key = st.secrets["api_key"]


def hide_style():
    return """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style>
        """


st.markdown(hide_style(), unsafe_allow_html=True)

st.title("CareChat")

if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []


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


def get_text():
    input_text = st.text_input("Patient: ")
    return input_text


# Placeholder for the text input widget
text_input_placeholder = st.empty()
user_input = text_input_placeholder.text_input("Patient: ")

submit_button = st.button("Ask")

if submit_button and user_input:
    context = "\n".join([f"Patient: {msg}" if i % 2 == 0 else f"Therapist: {msg}" for i, msg in
                         enumerate(st.session_state['past'] + st.session_state['generated'])])

    response = query(f"{context}\nPatient: {user_input}\nTherapist: ")

    st.session_state.past.append(user_input)
    st.session_state.generated.append(response)

    # Clear the text input after the message is submitted
    text_input_placeholder.text_input("Patient: ", value="", key="user_input")

if st.session_state['generated']:
    for i in range(len(st.session_state['generated']) - 1, -1, -1):
        message(st.session_state["generated"][i], key=f"{i}")
        message(st.session_state['past'][i], is_user=True, key=f"{i}_user")