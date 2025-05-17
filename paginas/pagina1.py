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
    st.markdown(
        """
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@300;400;700&display=swap');

            * {
                font-family: 'Nunito', sans-serif;
            }
            .header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                border-bottom: 2px solid #052E59;
                padding-bottom: 10px;
            }
            .titulo-container {
                display: flex;
                flex-direction: column;
            }
            .titulo {
                font-size: 24px;
                font-weight: bold;
                color: #052E59;
            }
            .objetivo {
                font-size: 20px;
                font-weight: bold;
                color: #517496;
                margin-top: 5px;
            }
            .contato {
                font-size: 18px;
                font-weight: bold;
                color: #7A89B2;
                text-align: right;
            }
            .subtitulo {
                font-size: 20px;
                font-weight: 900; /* Extra Bold */
                margin-top: 20px;
                color: #517496;
            }
            .texto {
                font-size: 16px;
                color: #333333;
            }
        </style>
        
        <div class="header">
            <div class="titulo-container">
                <div class="titulo">Alan Bruno Soares Campello</div>
                <div class="objetivo">Objetivo: Analista de Dados</div>
            </div>
            <div class="contato">
                <b>Email:</b> <a href="https://mail.google.com/mail/?view=cm&fs=1&to=alancampiello@gmail.com&su=Oportunidade%20de%20Trabalho&body=Olá%20Alan,%20gostaria%20de%20falar%20sobre%20uma%20oportunidade%20de%20trabalho." target="_blank">alancampiello@gmail.com</a><br>
                <b>Contato:</b> <a href="https://api.whatsapp.com/send?phone=5521976103449" target="_blank">(21) 97610-3449</a>
            </div>
        </div>

        """,
        unsafe_allow_html=True
    )
    
    import bcampe.estilos as est
    est.aplicar_css()
    est.titulo('Currículo')
    st.markdown('<p class="subtitulo">📌 Resumo Profissional</p>', unsafe_allow_html=True)
    st.markdown(
        """
        <p class="texto">
        Analista de Dados com expertise em transformar dados complexos em insights estratégicos para impulsionar decisões orientadas por dados.
        Experiência sólida em processos de ETL (Extração, Transformação e Carga), criação de dashboards interativos e modelagem de dados.
        Proficiente em Python, SQL e Power BI, com atuação no desenvolvimento de soluções que otimizam processos e aumentam a eficiência operacional.
        </p>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<p class="subtitulo">📚 Formação Acadêmica</p>', unsafe_allow_html=True)
    st.markdown('<p class="texto"> Bacharelado em Estatística - Anhembi Morumbi (01/2021 - Em andamento)</p>', unsafe_allow_html=True)
    st.markdown('<p class="texto"> Tecnólogo em Ciência de Dados - UNINTER (06/2023 - Em andamento)</p>', unsafe_allow_html=True)

    st.markdown('<p class="subtitulo">💼 Experiência Profissional</p>', unsafe_allow_html=True)
    st.markdown('<p class="texto"><b>Controladoria Geral do Estado - CGE RJ</b> | Analista de Dados (12/2023 - Atual)</p>', unsafe_allow_html=True)
    st.markdown(
        """
        <ul class="texto">
            <li>Realizei a limpeza, transformação e organização de dados semiestruturados, assegurando maior qualidade e consistência para análises estratégicas, com o uso de ferramentas como Python e SQL.</li>
            <li>Desenvolvi a biblioteca BCAMPE (<a href="https://pypi.org/project/bcampe/">link</a>) em Python, que acelerou consideravelmente a criação de dashboards e relatórios.</li>
            <li>Criei dashboards e relatórios interativos com Python (Streamlit), aprimorando a visualização de indicadores e contribuindo para decisões mais ágeis e fundamentadas pelas áreas de negócio.</li>
            <li>realizei extraçao de dados via APIs, banco de dados e webscraping</li>
            <li>Realizei a migração de dashboards do Qlik Sense para soluções em Python (Streamlit), promovendo a modernização do ambiente de BI e gerando uma economia em licenças, ao adotar soluções open source.</li>
        </ul>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<p class="subtitulo">🛠 Habilidades Técnicas</p>', unsafe_allow_html=True)
    st.markdown(
        """
        <ul class="texto">
            <li><b>Ferramentas de Análise de Dados:</b> Python, SQL, Power BI, Excel</li>
            <li><b>Versionamento e Controle de Código:</b> GIT</li>
            <li><b>Visualização de Dados:</b> Streamlit, Power BI</li>
            <li><b>ETL (Extração, Transformação e Carga):</b> Experiência na coleta, tratamento e integração de dados de múltiplas fontes</li>
        </ul>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<p class="subtitulo">📜 Cursos e Certificações</p>', unsafe_allow_html=True)
    st.markdown(
    """
    <ul class="texto">
        <li><a href="https://drive.google.com/file/d/1Jr5gwH-FLaWa2QU0RNCRBck8wVgfKfWO/view?usp=sharing" target="_blank">Microsoft Power BI Para Business Intelligence e Data Science - DSA</a></li> 
        <li><a href="https://drive.google.com/file/d/1vw9CDuh10wCnvyVb3j-JlbSu7GzKAbLL/view?usp=sharing" target="_blank">Certificado Profissional de Google Data Analytics - Google</a></li> 
        <li><a href="https://drive.google.com/file/d/1fFpVucAPU8e3GoG6iseaxRCOdoQjcByg/view?usp=sharing" target="_blank">Fundamentos de Engenharia de Dados - DSA</a></li> 
    </ul>
    """,
    unsafe_allow_html=True
    )
