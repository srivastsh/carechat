import streamlit as st
import openai
from streamlit_chat import message

openai.api_key = st.secrets["api_key"]

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.title("CareChat")

st.write("""
CareChat is an AI-powered chatbot designed to serve as a virtual therapist, providing users
with someone to listen and offer support. The chatbot leverages OpenAI's GPT-4 to generate 
meaningful and contextually relevant responses based on the user's input, creating a safe
space for users to express their thoughts and feelings.
""")

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
    input_text = st.text_input("", placeholder="How are you feeling?")
    return input_text

user_input = get_text()
submit_button = st.button("Ask")

if submit_button and user_input:
    context = "\n".join([f"Patient: {msg}" if i % 2 == 0 else f"Therapist: {msg}" for i, msg in enumerate(st.session_state['past'] + st.session_state['generated'])])

    response = query(f"{context}\nPatient: {user_input}\nTherapist: ")

    st.session_state.past.append(user_input)
    st.session_state.generated.append(response)

if st.session_state['generated']:
    for i in range(len(st.session_state['generated']) - 1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')