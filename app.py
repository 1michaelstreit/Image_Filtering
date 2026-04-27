import streamlit as st

st.title("Filtering and Denoising")
x = st.slider("Choose a number", 0, 100, 50)
st.write("You chose", x)