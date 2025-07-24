import streamlit as st
import sqlite3 as db
import datetime as dt
import time

st.set_page_config(layout="wide")

# CONSTANTES
DATABASE = ".database/data.db"

# CONFIGURAÇÕES DO SQLITE
## CREATE/CONNECT DATABASE (IF NOT EXISTS)
connect = db.connect(DATABASE, check_same_thread=False)
cursor = connect.cursor()


# SELECT ALL FROM DESPESAS AND PUT ON A VARIABLE
cursor.execute("SELECT * FROM despesas")
dados_banco = cursor.fetchall()

nomes_colunas = [desc[0] for desc in cursor.description]
nomes_colunas.remove("id")

ids = [linha[0] for linha in dados_banco]

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
                    "0": st.column_config.NumberColumn(
                        "ID"
                    ),
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

# CAIXA PARA CONFIRMAR ALTERAÇÃO
@st.dialog("ALTERAÇÃO DE DADOS")
def atualizar_valor():
    campo_editado = st.selectbox("Campo a atualizar", nomes_colunas)
    novo_valor = st.text_input("Novo valor", placeholder="Ex.: 24/08/2012")
    id_linha = st.selectbox("ID da linha", ids)
    if st.button("CONFIRMAR", use_container_width=True):
        st.session_state.atualizar = {"campo_editado": campo_editado, "novo_valor": novo_valor, "id_linha": id_linha}
        st.rerun()
    if st.button("CANCELAR", use_container_width=True, type="primary"):
        st.rerun()

if "atualizar" not in st.session_state:
    if st.button("EDITAR VALOR", type="primary", use_container_width=True):
        atualizar_valor()
else:
    query = f"UPDATE despesas SET {st.session_state.atualizar["campo_editado"]} = ? WHERE id = ?"
    cursor.execute(query, (st.session_state.atualizar["novo_valor"], st.session_state.atualizar["id_linha"]))
    connect.commit()
    st.toast("VALOR ATUALIZADO COM SUCESSO!")

#     st.button("EXCLUIR VALOR", use_container_width=True)
