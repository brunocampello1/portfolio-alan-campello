import streamlit as st

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
    st.markdown("texto")