import streamlit as st

st.markdown(
    "<h1 style='text-align: center;'>Bem-vindo(a) ao GaViCash</h1>",
    unsafe_allow_html=True
)

left, middle, right = st.columns(3)

if st.button("CADASTRAR DESPESAS", use_container_width=True):
    st.switch_page("pages/expenses.py")

