import streamlit as st
from paginas import pagina1, pagina2
from dashboard import dashboard1
from relatorio import relatorio1
from biblioteca import biblioteca
import bcampe.estilos as bi
from streamlit.components.v1 import html

# Função para injetar JavaScript e manter expanders abertos
def inject_js():
    js_code = """
    <script>
    document.addEventListener('DOMContentLoaded', function() {
        const sidebar = document.querySelector('[data-testid="stSidebar"]');
        if (sidebar) {
            const expanders = sidebar.querySelectorAll('.streamlit-expander');
            expanders.forEach(expander => {
                const isClosed = expander.querySelector('[aria-expanded="false"]');
                if (isClosed) {
                    expander.querySelector('summary').click();
                }
            });
        }
    });
    </script>
    """
    html(js_code, height=0, width=0)

# Configuração do sidebar
st.sidebar.title("Menu")

# Inicializa a variável de sessão se ainda não existir
if "pagina" not in st.session_state:
    st.session_state.pagina = "Currículo"

# Seção Currículo
if st.sidebar.button("📄 Currículo"):
    st.session_state.pagina = "Currículo"

# Seção Dashboards
with st.sidebar.expander("📊 Dashboards"):
    if st.button("Obras do Estado"):
        st.session_state.pagina = "Dash 1"

# Seção Relatórios
with st.sidebar.expander("📄 Relatórios"):
    if st.button("Despesas com Diárias"):
        st.session_state.pagina = "Relatório 1"
if st.sidebar.button("Biblioteca"):
    st.session_state.pagina = "Biblioteca"
# Seção Sistemas
with st.sidebar.expander("🖥️ Sistemas"):
    if st.button("Simulador de Investimentos"):
        st.session_state.pagina = "Simulador de Investimentos"

# Injeta o JavaScript após configurar o sidebar
inject_js()

# Exibição da página selecionada
if st.session_state.pagina == "Currículo":
    pagina1.mostrar()
if st.session_state.pagina == "Biblioteca":
    Biblioteca.mostrar()
elif st.session_state.pagina == "Simulador de Investimentos":
    pagina2.mostrar()
elif st.session_state.pagina == "Dash 1":
    dashboard1.mostrar()
elif st.session_state.pagina == "Relatório 1":
    relatorio1.mostrar()
