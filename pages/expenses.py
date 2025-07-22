import streamlit as st
from datetime import date
import sqlite3 as db
import unicodedata as uni

# CONFIGURAÇÕES DO SQLITE
## CREATE/CONNECT DATABASE (IF NOT EXISTS)
connect = db.connect('.database/data.db', check_same_thread=False)
cursor = connect.cursor()

## CREATE TABLE (IF NOT EXISTS)
cursor.execute("""
CREATE TABLE IF NOT EXISTS despesas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data TEXT NOT NULL,           
    item TEXT NOT NULL,
    valor REAL NOT NULL,
    parcelas INTEGER NOT NULL,
    responsavel TEXT NOT NULL,
    recorrente TEXT NOT NULL
)
""")

st.markdown(
    "<h1 style='text-align: center;'>Cadastrar Despesas</h1>",
    unsafe_allow_html=True
)

erro = False # Flag para identificar erros nos inputs do forms

def remover_acentos(texto):
    return uni.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('ASCII')

with st.form("Despesa", clear_on_submit=True, border=False, ):
    data = st.date_input("Data", date.today(), format="DD/MM/YYYY")
    item = st.text_input("Item", placeholder="Ex.: NETFLIX") # deixar o texto maiúsculo depois de enviar
    valor = st.text_input("Valor", placeholder="Ex. 19,90")
    parcelas = st.selectbox("Número de parcelas", ["","À VISTA", 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]) # quando for à vista, o valor enviado será zero na validação
    responsavel = st.selectbox("Responsável", ["","GABRIEL", "VITÓRIA"])
    recorrente = st.radio("É uma despesa recorrente?", ["SIM", "NÂO"], index=None,horizontal=True, help="Despesas que ocorrem mensalmente, como Netflix, aluguel, etc.")
    # pagamento = st.selectbox("Forma de pagamento (*)", ["","DINHEIRO / PIX", "XP", "ITAÚ", "BRADESCO", "SANTANDER"])
    # tipo_gasto = st.selectbox("Tipo de gasto", ["","FIXO", "VARIÁVEL"])
    cadastrado = st.form_submit_button("Cadastrar", use_container_width=True, type="primary")

    if cadastrado:
        # Trata as variáveis
        data = data.strftime('%d/%m/%Y')
        item = item.upper().strip()
        item = remover_acentos(item)
        responsavel = remover_acentos(responsavel)
        recorrente = remover_acentos(recorrente)
        valor = valor.strip()
        if parcelas == "À VISTA":
            parcelas = 0
        
        # Valida os dados
        if responsavel == "" or parcelas == "" or valor == "" or item == "" or recorrente == None:
            erro = True
            st.error("Por favor, preencha todos os campos")

        if not erro:
            try:
                valor = float(valor.replace(",", ".")) # Aceita "," no número float
                valor = format(valor, ".2f").replace(".", ",") # Deixa o número no padrão brasileiro
            except ValueError:
                erro = True
                st.error("O campo \"Valor\" possui caracteres inválidos!")

        if not erro:
            cursor.execute("""
                INSERT INTO DESPESAS (data, item, valor, parcelas, responsavel, recorrente)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (data, item, valor, parcelas, responsavel, recorrente))
            connect.commit()
            st.success("Despesa registrada com sucesso!")

        st.session_state.clear()

if st.button("VOLTAR", use_container_width=True):
    st.switch_page("pages/main.py")