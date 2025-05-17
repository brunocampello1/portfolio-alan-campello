import streamlit as st
from streamlit.components.v1 import html
from paginas import pagina1, pagina2
from dashboard import dashboard1
from relatorio import relatorio1
import bcampe.estilos as bi

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

# Sidebar
st.sidebar.title("Menu")

# Inicializa a variável de sessão
if "pagina" not in st.session_state:
    st.session_state.pagina = "Currículo"

# Botões
if st.sidebar.button("📄 Currículo"):
    st.session_state.pagina = "Currículo"
    st.experimental_rerun()

with st.sidebar.expander("📊 Dashboards"):
    if st.button("Obras do Estado"):
        st.session_state.pagina = "Dash 1"
        st.experimental_rerun()

with st.sidebar.expander("📄 Relatórios"):
    if st.button("Despesas com Diárias"):
        st.session_state.pagina = "Relatório 1"
        st.experimental_rerun()

with st.sidebar.expander("🖥️ Sistemas"):
    if st.button("Simulador de Investimentos"):
        st.session_state.pagina = "Simulador de Investimentos"
        st.experimental_rerun()

# Injeta JS
inject_js()

# Exibição da página
if st.session_state.pagina == "Currículo":
    bi.titulo("curriculo")
    pagina1.mostrar()
elif st.session_state.pagina == "Simulador de Investimentos":
    pagina2.mostrar()
elif st.session_state.pagina == "Dash 1":
    dashboard1.mostrar()
elif st.session_state.pagina == "Relatório 1":
    relatorio1.mostrar()
