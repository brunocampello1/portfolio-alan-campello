import streamlit as st
import pandas as pd
import bcampe.graficos as graf
import bcampe.estilos as est

def mostrar():
    est.aplicar_css()
    est.titulo('Documentação da Biblioteca bcampe')

    st.markdown("""
    A biblioteca `bcampe` é uma ferramenta para criação rápida e eficiente de visualizações de dados, permitindo gerar gráficos profissionais com poucas linhas de código.
    Ela oferece funções especializadas para os principais tipos de gráficos, com parâmetros inteligentes que simplificam a customização.
    """)
    
    st.code("pip install bcampe==0.94", language="bash")
    
    st.markdown("[bcampe 0.94 no PyPI](https://pypi.org/project/bcampe/0.94/)")
    st.header("⚙️ Funções Principais")
    
    with st.expander("1. `grafico_barras()`"):
        st.markdown("""
    Cria gráficos de barras horizontais ou verticais com diversas opções de customização.
    
    **Parâmetros**:
    - `df` (pd.DataFrame): DataFrame com os dados  
    - `var_categorica` (str): Nome da coluna categórica  
    - `var_numerica` (str, opcional): Nome da coluna numérica. Se None, fará contagem de ocorrências  
    - `cor` (list, opcional): Lista de cores para o gráfico  
    - `titulo` (str, opcional): Título do gráfico  
    - `n` (int, opcional): Quantidade de categorias a exibir (padrão: 5)  
    - `orientacao` (str, opcional): Orientação do gráfico ('h' para horizontal, 'v' para vertical)  
    - `agregacao` (str, opcional): Tipo de agregação a ser usada. Pode ser 'sum', 'mean', 'median'  
    - `hover_x` (str, opcional): Nome do eixo x no hover  
    - `hover_y` (str, opcional): Nome do eixo y no hover  
    - `abreviar_rotulos` (bool, opcional): Se True, abrevia os rótulos do gráfico  
    - `max_caracteres` (int, opcional): Número máximo de caracteres permitidos nos rótulos  
    - `posicao_texto` (str, opcional): Posição dos valores nas barras ('inside', 'outside', 'auto' ou None para ocultar)  
    - `altura` (int, opcional): Altura total do gráfico em pixels (padrão: 420)  
    - `ordenacao_eixo` (list, opcional): Lista manual com ordem específica das categorias. Se informado, sobrescreve a ordenação automática  
    
    **Saída**: Gráfico de barras interativo (`go.Figure`)
    """)
        
        st.markdown("### Exemplo: Top 5 produtos mais vendidos")
        with st.echo():
            df_barras = pd.DataFrame({
                'Produto': ['Notebook', 'Smartphone', 'Tablet', 'Monitor', 'Teclado'],
                'Vendas': [350, 500, 220, 180, 150]
            })
            fig_barras = graf.grafico_barras(df_barras, var_categorica='Produto', var_numerica='Vendas',
                                            titulo="Top 5 Produtos Mais Vendidos", orientacao="h")
            st.plotly_chart(fig_barras, use_container_width=True)

    with st.expander("2. `grafico_barras_agrupadas()`"):
        st.markdown("""
    Cria gráficos de barras agrupadas para comparar múltiplas variáveis numéricas.
    
    **Parâmetros principais**:
    - `df`: DataFrame com os dados.
    - `var_categorica`: Coluna categórica base.
    - `var_numerica`: Lista de colunas numéricas.
    - `n`: Número de categorias exibidas.
    - `cor`: Lista de cores.
    - `ordenado_por`: Coluna para ordenação.
    
    **Saída**: Gráfico interativo com barras agrupadas lado a lado.
        """)
        st.markdown("### Exemplo: Comparativo de vendas por trimestre")
        with st.echo():
            df_agrupadas = pd.DataFrame({
                'Categoria': ['Notebook', 'Smartphone', 'Tablet'],
                '1º Trim.': [120, 200, 100],
                '2º Trim.': [150, 220, 110],
                '3º Trim.': [130, 210, 105]
            })
            fig_agrupadas = graf.grafico_barras_agrupadas(df_agrupadas, var_categorica='Categoria',
                                                        var_numerica=['1º Trim.', '2º Trim.', '3º Trim.'],
                                                        titulo="Vendas por Trimestre")
            st.plotly_chart(fig_agrupadas, use_container_width=True)
    
    with st.expander("3. `grafico_pizza()`"):
        st.markdown("""
    Cria gráficos de pizza ou rosca com formatação avançada.

    **Parâmetros principais**:
    - df (pd.DataFrame): DataFrame contendo os dados.
    - var_categorica (str): Nome da coluna categórica para agrupar os dados e criar as fatias do gráfico.
    - var_numerica (str, opcional): Nome da coluna numérica para calcular os valores das fatias. Se None, conta a frequência das categorias.
    - outros (bool, opcional): Se True, categorias menores que não estão entre as top `n` são agrupadas em "Outros". Se False, exibe apenas as top `n` categorias.
    - n (int, opcional): Número de categorias principais a serem exibidas. Categorias além desse número são agrupadas em "Outros" se `outros=True`.
    - colors_base (list, opcional): Lista de cores personalizadas para as fatias do gráfico. Se None, as cores são geradas automaticamente.
    - cor_outros (str, opcional): Cor da fatia "Outros". Se None, usa a última cor de `colors_base`.
    - cores_categoria (list, opcional): Lista de cores específicas para cada categoria. Se fornecida, sobrescreve `colors_base`.
    - titulo (str, opcional): Título do gráfico.
    - valor (str, opcional): Tipo de valor exibido nas fatias. Pode ser "percentual", "numero", "percentual+numero" ou "label".
    - hole_size (float, opcional): Tamanho do buraco central do gráfico (0 a 1). Um valor de 0.5 cria um gráfico de rosca.
    - altura (int, opcional): Altura do gráfico em pixels.
    - expessura_linha (float, opcional): Espessura da linha que separa as fatias do gráfico.
    - cor_linha (str, opcional): Cor da linha que separa as fatias do gráfico.
    - hover_cat (str, opcional): Nome customizado para a categoria no hover.
    - hover_num (str, opcional): Nome customizado para o valor numérico no hover.
    - cor_gradiente (str, opcional): Cor base para gerar o gradiente de cores automaticamente.

    **Saída**: Gráfico de pizza ou rosca com legenda interativa.
        """)
        st.markdown("### Exemplo: Distribuição de usuários por plataforma")
        with st.echo():
            df_pizza = pd.DataFrame({
                'Plataforma': ['Android', 'iOS', 'Web', 'Windows', 'MacOS'],
                'Usuários': [5000, 3000, 2000, 1500, 1000]
            })
            fig_pizza = graf.grafico_pizza(df_pizza, var_categorica='Plataforma', var_numerica='Usuários',
                                        titulo="Usuários por Plataforma", valor="percentual+numero", n=4, outros=True)
            st.plotly_chart(fig_pizza, use_container_width=True)

    with st.expander("4. `grafico_linha()`"):
        st.markdown("""
    Cria gráficos de linha ou de Área.

    **Parâmetros principais**:
    - df (pd.DataFrame): DataFrame contendo os dados.
    - periodo (str): Nome da coluna usada para agrupar os dados no eixo X (ex: 'mes', 'ano').
    - var_numerica (str, opcional): Nome da coluna numérica a ser plotada (ex: 'Despesas_empenhadas').
    - var_categorica (str, opcional): Nome da coluna categórica para filtragem (ex: 'Categoria').
    - categoria (str, opcional): Valor específico da var_categorica para filtrar os dados.
    - agregacao (str, opcional): Método de agregação ('sum', 'mean', 'median'). Padrão: 'sum'.
    - cor_linha (str, opcional): Cor da linha do gráfico. Padrão: '#052E59'.
    - hover_x (str, opcional): Nome do eixo X exibido no hover. Padrão: 'Ano'.
    - hover_y (str, opcional): Nome do eixo Y exibido no hover. Padrão: 'Total'.
    - titulo (str, opcional): Título do gráfico.
    - preenchimento (bool, opcional): Se True, preenche a área abaixo da linha. Padrão: False.
    - cor_preenchimento (str, opcional): Cor do preenchimento. Se None, ajusta com base na cor_linha.
    - opacidade (float, opcional): Opacidade do preenchimento (0 a 1). Padrão: 0.35.
    - altura (int, opcional): Altura do gráfico em pixels. Padrão: 350.

    **Saída**: Gráfico de linha com marcadores e preenchimento opcional.
        """)
        st.markdown("### Exemplo: Evolução de faturamento anual")
        with st.echo():
            df_linha = pd.DataFrame({
                'Ano': ['2019', '2020', '2021', '2022', '2023'],
                'Faturamento': [1.2, 1.8, 2.1, 2.6, 3.0]
            })
            fig_linha = graf.grafico_linha(df_linha, periodo='Ano', var_numerica='Faturamento',
                                        titulo="Faturamento Anual (em milhões)", preenchimento=True)
            st.plotly_chart(fig_linha, use_container_width=True)
    
    with st.expander("5. `grafico_dispersao()`"):
        st.markdown("""
    Cria gráficos de dispersão para analisar relações entre variáveis.
    
    **Parâmetros principais**:
    - `df`: DataFrame com os dados.
    - `var_numericaX` / `var_numericaY`: Eixos X e Y.
    - `log_x`: Escala logarítmica no eixo X.
    - `custom_data`: Dados extras no hover.
    
    **Saída**: Gráfico de dispersão com hover customizado e escala ajustável.
        """)
    
        st.markdown("### Exemplo: Correlação entre investimento e lucro")
        with st.echo():
            df_disp = pd.DataFrame({
                'Investimento': [10, 15, 20, 25, 30],
                'Lucro': [2, 3, 5, 6, 8]
            })
            fig_disp = graf.grafico_dispersao(df_disp, var_numericaX='Investimento', var_numericaY='Lucro',
                                            title="Relação entre Investimento e Lucro")
            st.plotly_chart(fig_disp, use_container_width=True)
    
    st.header("Vantagens da Biblioteca")
    
    st.markdown("""
    1. **Sintaxe Simplificada**: Crie gráficos complexos com poucas linhas.  
    2. **Padrão Visual Consistente**: Design profissional sem esforço.  
    3. **Customização Fácil**: Parâmetros claros e objetivos.    
    4. **Responsividade**: Gráficos adaptáveis a qualquer tela.
    
    A `bcampe` é ideal para **dashboards, análises exploratórias** e **relatórios interativos**, acelerando a construção de visualizações sem abrir mão da qualidade.
    """)

if __name__ == "__main__":
    mostrar()
