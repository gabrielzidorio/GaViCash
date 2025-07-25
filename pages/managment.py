import streamlit as st
import sqlite3 as db
import datetime as dt
import unicodedata as uni

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

st.html(
    "<p style='text-align: center; font-size: 2.5em; margin-bottom:-50px; font-weight:bold'>Gerenciar Despesas</p>"
)
st.divider()

# Função para remover acentos de uma string
def remover_acentos(texto):
    return uni.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('ASCII')

# SHOW DATABASE DATA 
st.dataframe(dados_banco, hide_index=True, row_height=55, height=588, use_container_width=True, 
            column_config={
                    "0": st.column_config.NumberColumn(
                        "ID"
                    ),
                    "1": st.column_config.DateColumn(
                        "DATA",
                        format="DD [de] MMM[. de] YYYY",
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

# POP-UP DE EDIÇÃO
@st.dialog("ALTERAÇÃO DE DADOS")
def atualizar_valor():
    campo_editado = st.selectbox("Campo a atualizar", nomes_colunas)
    novo_valor = st.text_input("Novo valor", placeholder="Ex.: 24/08/2012")
    id_linha = st.selectbox("ID da linha", ids)
    
    if st.button("CONFIRMAR", use_container_width=True):
        st.session_state.atualizar = {"campo_editado": campo_editado, "novo_valor": novo_valor, "id_linha": id_linha}
        st.rerun()
        st.set_page_config(layout="wide")
    if st.button("CANCELAR", use_container_width=True, type="primary"):
        st.rerun()
        st.set_page_config(layout="wide")

col1, col2 = st.columns(2)
with col1:
    if "atualizar" not in st.session_state:
        if st.button("EDITAR DESPESA", type="primary", use_container_width=True):
            atualizar_valor()
    else:
        # VALIDA OS DADOS E OS PERSISTE NO BANCO CASO ESTEJAM CERTOS
        erro = False
        campo_editado = st.session_state.atualizar["campo_editado"]
        novo_valor = st.session_state.atualizar["novo_valor"]
        id_linha = st.session_state.atualizar["id_linha"]

        del st.session_state.atualizar  # Limpa o estado para evitar re-execução

        if campo_editado == "data":
            try:
                novo_valor = dt.datetime.strptime(novo_valor, "%d/%m/%Y").date()
            except ValueError:
                st.error("Data inválida! Use o formato DD/MM/YYYY.")
                erro = True
        elif campo_editado == "valor":
            try:
                novo_valor = float(novo_valor.replace(",", ".")) # Aceita "," no número float
            except ValueError:
                st.error("O valor informado é inválido!")
                erro = True
        elif type(novo_valor) == str:
            novo_valor = novo_valor.upper().strip()
            novo_valor = remover_acentos(novo_valor)

        if not erro:
            query = f"UPDATE despesas SET {campo_editado} = ? WHERE id = ?"
            cursor.execute(query, (novo_valor, id_linha))
            connect.commit()
            st.rerun()
            st.set_page_config(layout="wide")
            st.toast("DESPESA ATUALIZADA COM SUCESSO!")

# POP-UP DE EXCLUSÃO
@st.dialog("EXCLUSÃO DE DADOS")
def excluir_valor():
    id_linha = st.selectbox("ID da despesa", ids)
    
    if st.button("CONFIRMAR", use_container_width=True):
        st.session_state.excluir = {"id_linha": id_linha}
        st.rerun()
        st.set_page_config(layout="wide")
    if st.button("CANCELAR", use_container_width=True, type="primary"):
        st.rerun()
        st.set_page_config(layout="wide")

with col2:
    if "excluir" not in st.session_state:
        if st.button("EXCLUIR DESPESA", type="secondary", use_container_width=True):
            excluir_valor()
    else:
        id_linha = st.session_state.excluir["id_linha"]

        cursor.execute("DELETE FROM despesas WHERE id = ?", (id_linha,))
        connect.commit()

        del st.session_state.excluir  # Limpa o estado para evitar re-execução

        st.rerun()
        st.set_page_config(layout="wide")
        st.toast("DESPESA ATUALIZADA COM SUCESSO!")

if st.button("VOLTAR", use_container_width=True):
    st.switch_page("pages/main.py")
