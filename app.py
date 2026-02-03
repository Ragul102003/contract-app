import streamlit as st

st.title("Contract Risk Checker")

file = st.file_uploader("Upload contract (.txt)", type=["txt"])

if file:
    text = file.read().decode()
    st.write(text)

    if "penalty" in text.lower():
        st.error("High Risk: Penalty clause found")
    else:
        st.success("Low Risk Contract")
