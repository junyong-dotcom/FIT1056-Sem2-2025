import streamlit as st

st.title("Hello, Streamlit!")

name = st.text_input("Enter your name")

if st.button("Greet"):
    st.write(f"Hello, {name}! 👋 Welcome to Streamlit!")