import streamlit as st
import sqlite3 as db
import pandas as pd

st.set_page_config(layout="wide")

# CONSTANTES
DATABASE = ".database/data.db"

tab1, tab2 = st.tabs(["VISUALIZAR", "EDITAR"])

with tab1:
    # CONFIGURAÇÕES DO SQLITE
    ## CREATE/CONNECT DATABASE (IF NOT EXISTS)
    connect = db.connect(DATABASE, check_same_thread=False)
    cursor = connect.cursor()

    # SELECT ALL FROM DESPESAS AND PUT ON A VARIABLE
    df = cursor.execute("SELECT * FROM despesas")


    # SHOW DATABASE DATA 
    st.dataframe(df, hide_index=True, row_height=55, height=588, use_container_width=True, 
                column_config={
                        "id": None,
                        "data": st.column_config.DateColumn(
                            "DATA",
                            help="Data da compra"
                        ),
                        "item": st.column_config.TextColumn(
                            "PRODUTO",
                            help="Produto adquirido"
                        ),
                        "valor": st.column_config.NumberColumn(
                            "VALOR",
                            help="Valor da compra",
                            format="dollar"
                        ),
                        "parcelas": st.column_config.NumberColumn(
                            "PARCELAS",
                            help="Número de parcelas"
                        ),
                        "responsavel": st.column_config.TextColumn(
                            "RESPONSÁVEL",
                            help="Pessoa que pagou pelo produto"
                        ),
                        "recorrente": st.column_config.TextColumn(
                            "RECORRENTE",
                            help="Compra mensal"
                        )
                    })

with tab2:
    # CONFIGURAÇÕES DO SQLITE
    ## CREATE/CONNECT DATABASE (IF NOT EXISTS)
    connect = db.connect(DATABASE, check_same_thread=False)
    cursor = connect.cursor()

    # SELECT ALL FROM DESPESAS AND PUT ON A VARIABLE
    df = cursor.execute("SELECT * FROM despesas")

    # EDIT ROWS FROM DATABASE DATA 
    st.data_editor(df, hide_index=True, row_height=55, height=588, use_container_width=True, key="de_edit", 
                column_config={
                        "id": None,
                        "data": st.column_config.DateColumn(
                            "DATA",
                            help="Data da compra"
                        ),
                        "item": st.column_config.TextColumn(
                            "PRODUTO",
                            help="Produto adquirido"
                        ),
                        "valor": st.column_config.NumberColumn(
                            "VALOR",
                            help="Valor da compra",
                            format="dollar"
                        ),
                        "parcelas": st.column_config.NumberColumn(
                            "PARCELAS",
                            help="Número de parcelas"
                        ),
                        "responsavel": st.column_config.TextColumn(
                            "RESPONSÁVEL",
                            help="Pessoa que pagou pelo produto"
                        ),
                        "recorrente": st.column_config.TextColumn(
                            "RECORRENTE",
                            help="Compra mensal"
                        )
                    })
