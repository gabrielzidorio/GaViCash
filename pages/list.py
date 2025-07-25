import streamlit as st
import sqlite3 as db
import datetime as dt
import pandas as pd

st.set_page_config(layout="wide")

# CONSTANTES
DATABASE = ".database/data.db"

tab1, tab2 = st.tabs(["VISUALIZAR", "EDITAR"])

# CONFIGURAÇÕES DO SQLITE
## CREATE/CONNECT DATABASE (IF NOT EXISTS)
connect = db.connect(DATABASE, check_same_thread=False)
cursor = connect.cursor()

with tab1:
    # SELECT ALL FROM DESPESAS AND PUT ON A VARIABLE
    cursor.execute("SELECT * FROM despesas")
    dados_banco = cursor.fetchall()

    dados_local = [] # Array criado para não haver repetição de busca no banco na tab2

    for linha in dados_banco:
        data_formatada = list(linha)
        try:
            data_formatada[1] = dt.datetime.strptime(linha[1], "%Y-%m-%d").date() # Converte o campo data de string para date
        except ValueError as e:
            print(f"Erro ao converter data: {linha[1]} → {e}")
        dados_local.append(tuple(data_formatada))

    # SHOW DATABASE DATA 
    st.dataframe(dados_local, hide_index=True, row_height=55, height=588, use_container_width=True, 
                column_config={
                        "0": None,
                        "1": st.column_config.DateColumn(
                            "DATA",
                            format="localized",
                            help="Data da compra"
                        ),
                        "2": st.column_config.TextColumn(
                            "PRODUTO",
                            help="Produto adquirido"
                        ),
                        "3": st.column_config.NumberColumn(
                            "VALOR",
                            help="Valor da compra",
                            format="dollar"
                        ),
                        "4": st.column_config.NumberColumn(
                            "PARCELAS",
                            help="Número de parcelas"
                        ),
                        "5": st.column_config.TextColumn(
                            "RESPONSÁVEL",
                            help="Pessoa que pagou pelo produto"
                        ),
                        "6": st.column_config.TextColumn(
                            "RECORRENTE",
                            help="Compra mensal"
                        )
                    })

with tab2: 
    dados_local_editado = st.data_editor(dados_local, hide_index=True, row_height=55, height=588, use_container_width=True, num_rows="dynamic", key="de_edit", 
                column_config={
                        "0": None,
                        "1": st.column_config.DateColumn(
                            "DATA",
                            format="localized",
                            help="Data da compra"
                        ),
                        "2": st.column_config.TextColumn(
                            "PRODUTO",
                            help="Produto adquirido"
                        ),
                        "3": st.column_config.NumberColumn(
                            "VALOR",
                            help="Valor da compra",
                            format="dollar"
                        ),
                        "4": st.column_config.NumberColumn(
                            "PARCELAS",
                            help="Número de parcelas"
                        ),
                        "5": st.column_config.TextColumn(
                            "RESPONSÁVEL",
                            help="Pessoa que pagou pelo produto"
                        ),
                        "6": st.column_config.TextColumn(
                            "RECORRENTE",
                            help="Compra mensal"
                        )
                    })
    
    # EDIÇÃO E EXCLUSÃO DE DADOS
    ids_originais = set(dados_local[0])
    ids_editados = set(dados_local_editado[0])
    ids_excluidos = ids_originais - ids_editados
    
    for id_del in ids_excluidos:
        st.text(id_del)
        cursor.execute("DELETE FROM despesas WHERE id = ?", (id_del,))
        connect.commit()
        