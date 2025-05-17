import streamlit as st
import pandas as pd
import bcampe

def mostrar():
  st.title("📊 Documentação da Biblioteca `bcampe`")
  
  st.markdown("""
  A biblioteca `bcampe` é uma ferramenta para criação rápida e eficiente de visualizações de dados com Plotly, permitindo gerar gráficos profissionais com poucas linhas de código.
  Ela oferece funções especializadas para os principais tipos de gráficos, com parâmetros inteligentes que simplificam a customização.
  """)
  
  st.header("⚙️ Funções Principais")
  
  with st.expander("1. `grafico_barras()`"):
      st.markdown("""
  Cria gráficos de barras horizontais ou verticais com diversas opções de customização.
  
  **Parâmetros principais**:
  - `df` (pd.DataFrame): Dados de entrada.
  - `var_categorica` (str): Coluna categórica.
  - `var_numerica` (str, opcional): Coluna numérica. Se None, conta ocorrências.
  - `cor`: Cor(es) das barras (str ou lista).
  - `titulo`: Título do gráfico.
  - `n`: Quantidade de categorias exibidas.
  - `orientacao`: 'h' (horizontal) ou 'v' (vertical).
  - `agregacao`: 'sum', 'mean', 'median'.
  - `abreviar_rotulos`: Abrevia rótulos longos.
  - `posicao_texto`: Posição dos valores nas barras.
  
  **Saída**: Gráfico de barras interativo (`go.Figure`)
      """)
  
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
  
  with st.expander("3. `grafico_pizza()`"):
      st.markdown("""
  Cria gráficos de pizza ou rosca com formatação avançada.
  
  **Parâmetros principais**:
  - `df`: DataFrame com os dados.
  - `var_categorica`: Coluna categórica.
  - `var_numerica`: Coluna numérica. Se None, conta ocorrências.
  - `outros`: Agrupa menores em "Outros".
  - `valor`: 'percentual', 'numero', etc.
  - `hole_size`: Define o tamanho do buraco central.
  
  **Saída**: Gráfico de pizza ou rosca com legenda interativa.
      """)
  
  with st.expander("4. `grafico_linha()`"):
      st.markdown("""
  Cria gráficos de linha com opção de preenchimento.
  
  **Parâmetros principais**:
  - `df`: DataFrame com os dados.
  - `periodo`: Coluna para eixo X (datas, por exemplo).
  - `var_numerica`: Coluna numérica para eixo Y.
  - `var_categorica`: Para filtragem.
  - `agregacao`: Método de agregação ('sum', etc).
  - `preenchimento`: Preenche a área sob a linha.
  
  **Saída**: Gráfico de linha com marcadores e preenchimento opcional.
      """)
  
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
  
  st.header(" Exemplo de Uso Básico")
  
  with st.echo():
      df = pd.DataFrame({
          'Categoria': ['A', 'B', 'C', 'D', 'E'],
          'Valores': [10, 25, 15, 30, 20]
      })
  
      fig = bcampe.grafico_barras(df, var_categorica='Categoria', var_numerica='Valores', titulo="grafico de barras")
      st.plotly_chart(fig, use_container_width=True)
  
  st.header("✅ Vantagens da Biblioteca")
  
  st.markdown("""
  1. **Sintaxe Simplificada**: Crie gráficos complexos com poucas linhas.  
  2. **Padrão Visual Consistente**: Design profissional sem esforço.  
  3. **Customização Fácil**: Parâmetros claros e objetivos.  
  4. **Tratamento Automático**:
     - Dados faltantes
     - Formatação de valores
     - Ajuste automático de rótulos  
  5. **Responsividade**: Gráficos adaptáveis a qualquer tela.
  
  A `bcampe` é ideal para **dashboards, análises exploratórias** e **relatórios interativos**, acelerando a construção de visualizações sem abrir mão da qualidade.
  """)
if __name__ == "__main__":
    mostrar()
