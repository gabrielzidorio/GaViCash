import streamlit as st
import validate_email as ve
import streamlit_authenticator as stauth
import sqlite3 as db

# CONSTANTES
DATABASE = ".database/data.db"

# CONFIGURAÇÕES DO SQLITE
## CREATE/CONNECT DATABASE (IF NOT EXISTS)
connect = db.connect(DATABASE, check_same_thread=False)
cursor = connect.cursor()

## CREATE TABLE (IF NOT EXISTS)
cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT NOT NULL,           
        senha TEXT NOT NULL,
        email TEXT NOT NULL
    )
""")

st.html(
    "<p style='text-align: center; font-size: 2em; margin-bottom:-50px; font-weight:bold'>Cadastro de usuário</p>"
)
st.divider()

erro = False

with st.form("register_form", border=False, clear_on_submit=True):
    username = st.text_input("Usuário", placeholder="Digite seu nome de usuário")
    password = st.text_input("Senha", type="password", help="Mínimo de 8 caractéres", placeholder="Digite sua senha")
    confirm_password = st.text_input("Confirmar senha", type="password", placeholder="Confirme sua senha")
    email = st.text_input("Email", placeholder="Informe um email válido")
    cadastrado = st.form_submit_button("CADASTRAR", use_container_width=True, type="primary")
    
    if cadastrado:
        if username and password and confirm_password and email:
            if password != confirm_password:
                st.error("As senhas não coincidem!")
                erro = True

            if len(password) < 8:
                st.error("A senha não atende aos requisitos!")
                erro = True

            email_valido = ve.validate_email(email)

            if not email_valido:
                st.error("Informe um email válido!")
                erro = True
        else:
            st.error("Preencha todos os campos!")
            erro = True
    
        if not erro:
            username = username.lower().strip()
            password = password.strip()
            hashed_password = stauth.Hasher.hash(password)
            email = email.lower().strip()

            cursor.execute("""
                INSERT INTO usuarios (usuario, senha, email)
                VALUES (?, ?, ?)
            """, (username, hashed_password, email))
            connect.commit()
            connect.close()            

            st.success("Usuário cadastrado com sucesso!")

if st.button("JÁ POSSUO UMA CONTA", use_container_width=True, type="tertiary"):
    st.switch_page("pages/login.py")
