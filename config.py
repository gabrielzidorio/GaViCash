#IMPORTS SECTION
import streamlit as st
import sqlite3 as db

# CREATE/CONNECT DATABASE
connect = db.connect('database/data.db', check_same_thread=False)
cursor = connect.cursor()

#PAGES SETTINGS
st.set_page_config(
    layout="centered",
    page_icon= "images/main-fav.png"
)

#PAGES DEFINITION
main = st.Page("pages/main.py", title="GaViCash") #incluirá dashboards e mostras tabela com despesas cadastradas até aqui
expenses = st.Page("pages/expenses.py", title="GaViCash - Cadastro de Despesas") #incluirá a aba despesas
# register = st.Page("pages/register.py", title="GaViCash - Cadastro de Despesas") #incluirá as abas cadastro e rankear
# login = st.Page("pages/login.py", title="Login")

#NAVIGATION
pages = st.navigation([main, expenses], position="hidden")
pages.run()
