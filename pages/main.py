import streamlit as st
import sqlite3 as db

# CONSTANTES
DATABASE = ".database/data.db"

# CONFIGURAÇÕES DO SQLITE
## CREATE/CONNECT DATABASE (IF NOT EXISTS)
connect = db.connect(DATABASE, check_same_thread=False)
cursor = connect.cursor()

## CREATE TABLE (IF NOT EXISTS)
cursor.execute("""
    CREATE TABLE IF NOT EXISTS despesas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data TEXT NOT NULL,           
        produto TEXT NOT NULL,
        valor REAL NOT NULL,
        parcelas INTEGER NOT NULL,
        responsavel TEXT NOT NULL,
        recorrente TEXT NOT NULL
    )
""")

# GATHERING NECESSARY DATA FROM DATABASE
## VALOR TOTAL
cursor.execute("""
                SELECT SUM(valor) FROM despesas;
            """)
valor_total = cursor.fetchall()[0][0]

if valor_total == None:
    valor_total = 0

valor_total_formatado = f"R$ {valor_total:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

## VALOR POR RESPONSÁVEL
### GABRIEL
cursor.execute("""
                SELECT SUM(valor) FROM despesas WHERE responsavel='GABRIEL';
            """)
valor_gabriel = cursor.fetchall()[0][0]

if valor_gabriel == None:
    valor_gabriel = 0

valor_gabriel_formatado = f"R$ {valor_gabriel:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

### VITORIA
cursor.execute("""
                SELECT SUM(valor) FROM despesas WHERE responsavel='VITORIA';
            """)
valor_vitoria = cursor.fetchall()[0][0]

if valor_vitoria == None:
    valor_vitoria = 0

valor_vitoria_formatado = f"R$ {valor_vitoria:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# CALCULA PORCENTAGENS E DIZ QUEM PAGA QUANTO
porcentagem = 7293.95 / (7293.95+4717)

gabriel_paga = valor_total * porcentagem
gabriel_paga_formatado = f"R$ {gabriel_paga:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

vitoria_paga = valor_total - gabriel_paga
vitoria_paga_formatado = f"R$ {vitoria_paga:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# CALCULA QUANTO DEVE SER TRANSFERIDO E QUEM DEVE TRANSFERIR
diferenca_gabriel = valor_gabriel - gabriel_paga
diferenca_vitoria = valor_vitoria - vitoria_paga

devedor = ""

if diferenca_gabriel < 0:
    devedor = "GABRIEL"
elif diferenca_vitoria < 0:
    devedor = "VITORIA"

diferenca_gabriel_formatado = f"R$ {abs(diferenca_gabriel):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
diferenca_vitoria_formatado = f"R$ {abs(diferenca_vitoria):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# 7.293,95 - full
# 6293,95 - full - alim
# 1000 - alim


# 4.717 - full
# 4.537,14 - full - pnr
# 179,86 pnr

kpi = st.metric("TOTAL", valor_total_formatado, help="Valor total de despesas cadastradas até o momento.", border=True)

b, c = st.columns(2)
d, e = st.columns(2)
st.container()
b.metric("GABRIEL PAGOU", valor_gabriel_formatado, border=True)
c.metric("VITÓRIA PAGOU", valor_vitoria_formatado, border=True)
d.metric("PARTE DO GABRIEL", gabriel_paga_formatado, border=True)
e.metric("PARTE DA VITÓRIA", vitoria_paga_formatado, border=True)

if devedor == "GABRIEL":
    st.warning(f"**{devedor}** DEVE TRANSFERIR **{diferenca_gabriel_formatado}** PARA **VITÓRIA**")
elif devedor == "VITORIA":
    st.warning(f"**{devedor}** DEVE TRANSFERIR **{diferenca_vitoria_formatado}** PARA **GABRIEL**")
else:
    st.success("Nenhum valor precisa ser transferido!")

col1, col2 = st.columns(2)
with col1:
    if st.button("CADASTRAR DESPESAS", use_container_width=True):
        st.switch_page("pages/expenses.py")

with col2:
    if st.button("GERENCIAR DESPESAS", use_container_width=True):
        st.switch_page("pages/managment.py")
