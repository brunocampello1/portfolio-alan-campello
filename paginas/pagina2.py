import streamlit as st



# Estiliza o iframe para ocupar 100% da largura
def mostrar():
    st.markdown(
    """
    <style>
        /* Esconde o menu de hambúrguer */
        header {visibility: hidden;}

        /* Esconde o rodapé do Streamlit */
        footer {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True
    )
    st.markdown(
        """
        <style>
            .iframe-container {
                width: 100%;
                height: 1000px;
                display: flex;
                justify-content: center;
            }
            iframe {
                width: 100%;
                height: 100%;
                border: none;
            }
        </style>
        <div class="iframe-container">
            <iframe src="https://brunocampello1.github.io/calculadora/"></iframe>
        </div>
        """,
        unsafe_allow_html=True
    )