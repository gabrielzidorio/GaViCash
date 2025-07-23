#IMPORTS SECTION
import streamlit as st

#PAGES SETTINGS
st.set_page_config(
    layout="centered",
    page_icon= "images/main-fav.png"
)

#PAGES DEFINITION
main = st.Page("pages/main.py", title="GaViCash") #incluirá dashboards e mostras tabela com despesas cadastradas até aqui
expenses = st.Page("pages/expenses.py", title="GaViCash - Cadastro de Despesas") #incluirá a aba despesas
list = st.Page("pages/list.py", title="GaViCash - Despesas") #incluirá a aba despesas
# register = st.Page("pages/register.py", title="GaViCash - Cadastro de Despesas") #incluirá as abas cadastro e rankear
# login = st.Page("pages/login.py", title="Login")

#MENU
st.sidebar.image("images/main-fav.png")

if st.sidebar.button("PÁGINA INICIAL", use_container_width=True, type="tertiary"):
    st.switch_page("pages/main.py")

if st.sidebar.button("CADASTRAR DESPESAS", use_container_width=True, type="tertiary"):
    st.switch_page("pages/expenses.py")

if st.sidebar.button("LISTA DE DESPESAS", use_container_width=True, type="tertiary"):
    st.switch_page("pages/list.py")

#NAVIGATION
pages = st.navigation([main, expenses, list], position="hidden")
pages.run()
