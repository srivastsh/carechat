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

if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []

def query(messages):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    return response.choices[0].text.strip()
def get_text():
    input_text = st.text_input("Patient: ")
    return input_text

user_input = get_text()
submit_button = st.button("Ask")

if submit_button and user_input:
    messages = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]

    for i, msg in enumerate(st.session_state['past'] + st.session_state['generated']):
        role = "Patient" if i % 2 == 0 else "Therapist"
        messages.append({"role": role, "content": msg})

    messages.append({"role": "Patient", "content": user_input})
    response = query(messages)

    st.session_state.past.append(user_input)
    st.session_state.generated.append(response)

if st.session_state['generated']:
    for i in range(len(st.session_state['generated']) - 1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
