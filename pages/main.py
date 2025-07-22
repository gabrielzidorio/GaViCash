import streamlit as st

left, middle, right = st.columns(3)

st.markdown(
    "<h1 style='text-align: center;'>Bem-vindo(a) ao GaViCash</h1>",
    unsafe_allow_html=True
)

with right:
    if st.button("CADASTRAR GASTOS"):
        st.switch_page("pages/expenses.py")