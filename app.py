import streamlit as st
from paginas import pagina1, pagina2
from dashboard import dashboard1, dashboard2
from relatorio import relatorio1, relatorio2

st.sidebar.title("Menu")

# Inicializa a variável de sessão se ainda não existir
if "pagina" not in st.session_state:
    st.session_state.pagina = "Currículo"


# Seção Currículo e Sistemas
if st.sidebar.button("📄 Currículo"):
    st.session_state.pagina = "Currículo"
# Seção Dashboards (apenas Dash 1 e Dash 2)
with st.sidebar.expander("📊 Dashboards"):
    if st.button("Dashboard 1"):
        st.session_state.pagina = "Dash 1"
    if st.button("Dashboard 2"):
        st.session_state.pagina = "Dash 2"

# Seção Relatórios (apenas Relatório 1 e Relatório 2)
with st.sidebar.expander("📄 Relatórios"):
    if st.button("Relatório 1"):
        st.session_state.pagina = "Relatório 1"
    if st.button("Relatório 2"):
        st.session_state.pagina = "Relatório 2"
with st.sidebar.expander("🖥️ Sistemas"):
    if st.button("Simulador de Investimentos"):
        st.session_state.pagina = "Simulador de Investimentos"

# Exibir a página correspondente no corpo principal
if st.session_state.pagina == "Currículo":
    pagina1.mostrar()
elif st.session_state.pagina == "Simulador de Investimentos":
    pagina2.mostrar()
elif st.session_state.pagina == "Dash 1":
    dashboard1.mostrar()
elif st.session_state.pagina == "Dash 2":
    dashboard2.mostrar()
elif st.session_state.pagina == "Relatório 1":
    relatorio1.mostrar()
elif st.session_state.pagina == "Relatório 2":
    relatorio2.mostrar()
