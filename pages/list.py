import streamlit as st
import sqlite3 as db

# CONSTANTES
DATABASE = ".database/data.db"

# CONFIGURAÇÕES DO SQLITE
## CREATE/CONNECT DATABASE (IF NOT EXISTS)
connect = db.connect(DATABASE, check_same_thread=False)
cursor = connect.cursor()

st.dataframe(cursor.execute("""
                SELECT data, item, valor, parcelas, responsavel, recorrente FROM despesas;
            """), hide_index=True)

