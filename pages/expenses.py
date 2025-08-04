import streamlit as st
from datetime import date
import sqlite3 as db
import unicodedata as uni
import streamlit_option_menu as som

# CONSTANTES
DATABASE = ".database/data.db"

# CONFIGURAÇÕES DO SQLITE
## CREATE/CONNECT DATABASE (IF NOT EXISTS)
connect = db.connect(DATABASE, check_same_thread=False)
cursor = connect.cursor()

pagina = som.option_menu(
    menu_title=None,
    options=["INÍCIO", "CADASTRAR", "GERENCIAR", "DESCONECTAR"],
    icons=["house-door", "plus-circle-dotted", "clipboard-data", "box-arrow-right"],
    default_index=(1),
    orientation="horizontal",
    styles={
        "container": {
            "padding": "0!important",
            "background-color": "#0E1117",
        },
        "icon": {
            "color": "white",
            "font-size": "18px"
        },
        "nav-link": {
            "font-size": "13px",
            "text-align": "center",
            "margin": "0px",
            "--hover-color": "#262730",
        },
        "nav-link-selected": {
            "background-color": "#2e7d32",
        },
    }
)

if pagina == "INÍCIO":
    st.switch_page("pages/main.py")
if pagina == "GERENCIAR":
    st.switch_page("pages/managment.py")

# st.html(
#     "<p style='text-align: center; font-size: 2.5em; margin-bottom:-50px; font-weight:bold'>Cadastrar Despesas</p>"
# )

# st.divider()

vazio = False # Flag para identificar se algum campo está vazio.
erro = False # Flag para identificar erros nos inputs do forms.
sucesso = False # Flag que identifica se os dados foram enviados


def remover_acentos(texto):
    return uni.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('ASCII')

with st.form("formDespesa", clear_on_submit=True, border=True):
    st.html("<p style='font-size:1.5em; text-align:center; margin-bottom:0px'>Cadastro de despesas</p>")
    data = st.date_input("Data", date.today(), format="DD/MM/YYYY")
    produto = st.text_input("Produto", placeholder="Ex.: NETFLIX") # deixar o texto maiúsculo depois de enviar
    valor = st.text_input("Valor", placeholder="Ex. 19,90")
    parcelas = st.selectbox("Número de parcelas", ["","À VISTA", 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]) # quando for à vista, o valor enviado será zero na validação
    responsavel = st.radio("Responsável", ["GABRIEL", "VITÓRIA"], index=None, horizontal=True , help="Quem pagou pelo item")
    recorrente = st.radio("Despesa recorrente", ["SIM", "NÃO"], index=None,horizontal=True, help="Despesas que ocorrem mensalmente, como Netflix, aluguel, etc.")
    cadastrado = st.form_submit_button("CADASTRAR", use_container_width=True, type="primary")
    container_form = st.container() # Para separar a lógica dos elementos visíveis na tela

    if cadastrado:
        # Checa se os campos estão preenchidos
        if responsavel == "" or parcelas == "" or valor == "" or produto == "" or recorrente == None:
            vazio = True

        # Trata as variáveis
        if not vazio:
            # data = data.strftime('%d/%m/%Y')
            produto = produto.upper().strip()
            produto = remover_acentos(produto)
            responsavel = remover_acentos(responsavel)
            recorrente = remover_acentos(recorrente)
            valor = valor.strip()
            if parcelas == "À VISTA":
                parcelas = 1

            try:
                valor = float(valor.replace(",", ".")) # Aceita "," no número float
            except ValueError:
                erro = True

            # Salva os dados no banco
            if not erro:
                cursor.execute("""
                    INSERT INTO DESPESAS (data, produto, valor, parcelas, responsavel, recorrente)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (data, produto, valor, parcelas, responsavel, recorrente))
                connect.commit()
                connect.close()
                sucesso = True

# left, right = st.columns(2)

# with left:
#     if st.button("VOLTAR", use_container_width=True):
#         st.switch_page("pages/main.py")

# with right:
#     if st.button("GERENCIAR", use_container_width=True):
#         st.switch_page("pages/managment.py")

if erro:
    st.error("O campo \"Valor\" possui caracteres inválidos!")

if vazio:
    st.error("Por favor, preencha todos os campos")

if sucesso:
    st.success("Despesa registrada com sucesso!")
