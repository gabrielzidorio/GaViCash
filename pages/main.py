import streamlit as st
import sqlite3 as db
#import pandas as pd

# CONSTANTES
DATABASE = ".database/data.db"

# CONFIGURAÇÕES DO SQLITE
## CREATE/CONNECT DATABASE (IF NOT EXISTS)
connect = db.connect(DATABASE, check_same_thread=False)
cursor = connect.cursor()

# GATHERING NECESSARY DATA FROM DATABASE
cursor.execute("""
                SELECT SUM(valor) FROM despesas;
            """)
valor_total = cursor.fetchall()[0][0]
valor_total = f"R$ {valor_total:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# CASTING DATA FROM DATABASE TO USEFUL TYPES
#valor_total = float(valor_total)

left, right = st.columns([1, 1])

st.html(
    "<h1 style='text-align: center; font-size:2.5em;'>Bem-vindo(a) ao GaViCash</h1>"
)

if st.button("CADASTRAR DESPESAS", use_container_width=True):
    st.switch_page("pages/expenses.py")

st.metric("TOTAL", valor_total, help="Valor total de despesas cadastradas até o momento.")

with left:
    st.write("teste")

with right:
    st.write("teste2")