import streamlit as st
import pandas as pd
import streamlit as st
import plotly.express as px
from PIL import Image
import plotly.graph_objects as go
import locale

def mostrar():
    # Defina a localização para português do Brasil
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    ############ CSS ######
    import bcampe.estilos as est
    import bcampe.funcoes as func
    import bcampe.graficos as graf
    import bcampe.filtros as filt
    est.aplicar_css()
    est.titulo('Obras')
    config_graph=func.config_graph
############################# CARGA ############
    @st.cache_data
    def carregar_dados():
        resultado_final = pd.read_csv("./static/dados.csv", sep=";", encoding="utf-8")
        return resultado_final

    if 'df_original' not in st.session_state:
        st.session_state.df_original = carregar_dados()
    df_inicio = st.session_state.df_original.copy()
    df_inicio['Data_emissão_ne'] = pd.to_datetime(df_inicio['Data_emissão_ne'], errors='coerce')
    df_inicio = df_inicio[df_inicio['Data_emissão_ne'].dt.year == 2024]

    df_inicio['mes'] = df_inicio['Data_emissão_ne'].dt.month
    df_inicio['Ano'] = df_inicio['Data_emissão_ne'].dt.year

    # Inicializa o estado dos filtros se não estiverem no session_state
    if 'Empresa' not in st.session_state:
        st.session_state['Empresa'] = []
    if 'Cnpj' not in st.session_state:
        st.session_state['Cnpj'] = []
    if 'sigla_ajustada' not in st.session_state:
        st.session_state['sigla_ajustada'] = []
    

    # Função para redefinir os filtros
    def reset_filters():
        st.session_state['Empresa'] = []
        st.session_state['Cnpj'] = []
        st.session_state['sigla_ajustada'] = []
    # Função para filtrar os dados
    def filtra_dados(Empresa, Cnpj, sigla_ajustada):
        df_filtrado = df_inicio.copy()

        if Empresa:
            df_filtrado = df_filtrado[df_filtrado['Empresa'].isin(Empresa)]
        if Cnpj:
            df_filtrado = df_filtrado[df_filtrado['Cnpj'].isin(Cnpj)]
        if sigla_ajustada:
            df_filtrado = df_filtrado[df_filtrado['sigla_ajustada'].isin(sigla_ajustada)]

        st.session_state.df_filtrado = df_filtrado

    with st.container():
        col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 1, 1])  # Ajustando proporções
        with col1:
            Empresa = st.multiselect("Empresa:", sorted(map(str, df_inicio['Empresa'].unique().tolist())), 
                                    placeholder="Selecione uma Empresa", key="Empresa")
        with col2:
            Cnpj = st.multiselect("CNPJ:", sorted(map(str, df_inicio['Cnpj'].unique().tolist())), 
                                placeholder="Selecione um CNPJ", key="Cnpj")
        with col3:
            sigla_ajustada = st.multiselect("Unidade Gestora:", sorted(map(str, df_inicio['sigla_ajustada'].unique().tolist())), 
                                            placeholder="Selecione uma Unidade Gestora", key="sigla_ajustada")
        with col4:
            st.write("")
            st.write("")
            botao_filtro = st.button('Aplicar Filtros', key='botao_filtro')
        with col5:
            st.write("")
            st.write("")
            botao_reset = st.button(":red[Apagar Filtros]", on_click=reset_filters, key='botao_reset')

    # Aplicar filtros quando o botão for pressionado
    if botao_filtro:
        filtra_dados(Empresa, Cnpj, sigla_ajustada)

    # Gerenciar estado do dataframe filtrado
    if 'df_filtrado' not in st.session_state or botao_reset:
        st.session_state.df_filtrado = df_inicio.copy()

    df = st.session_state.df_filtrado

    
 ############################# CONSTRUÇAO DOS GRAFICOS ###########################################
    if not df.empty:
        # grafico 1
        grafico1 =graf.grafico_barras(df,var_categorica='Empresa',var_numerica='Despesas_empenhadas',hover_x='total',hover_y='empresa',titulo='Total de Despesas Empenhadas por Empresa',orientacao='h',n=7,abreviar_rotulos=True,max_caracteres=14)
        grafico1.update_layout(height=400)

        # Criar o gráfico com os meses formatados
        grafico2 = graf.grafico_linha(
            df, periodo='mes', var_numerica='Despesas_empenhadas',
            titulo='Total de Despesas Empenhadas por Mês', altura=350, preenchimento=True
        )
        grafico2.update_layout(xaxis=dict(tickangle=0))
        #grafico3
        graf3 = df.groupby('sigla_ajustada')['Nota_de_empenho'].nunique().reset_index(name='quantidade')
        grafico3 = graf.grafico_pizza(graf3, var_categorica='sigla_ajustada', var_numerica='quantidade',titulo='Notas de Empenho Distintas por Unidade Gestora',altura=450,valor="numero",n=5)
        grafico3.update_layout(title=dict(
                    text='Total de Notas de Empenho por Órgão',
                    y=0.95,  # Ajuste a posição vertical do título (0 a 1)
                    x=0.4,   # Centraliza o título
                    xanchor='center',
                    font=dict(size=15)
                    )
            )

        grafico3.update_traces(hoverlabel=dict(font_size=13))


        # grafico 4
        grafico4 = graf.grafico_barras_agrupadas(df,var_categorica='sigla_ajustada',var_numerica=['Despesas_empenhadas','Despesas_liquidadas','Despesas_pagas'],n=5,ordenado_por='Despesas_empenhadas',hover_y=['Despesas empenhadas','Despesas liquidadas','Despesas pagas'],titulo='Unidade Gestora por Total de Despesas Empenhadas')

        bins = [0, 1000, 5000, 10000, 50000, 100000, 1000000]
        labels = ['Menor que 1000', 'Entre 1000 e 5000', 'Entre 5000 e 10000', 
                'Entre 10000 e 50000', 'Entre 50000 e 100000', 'Entre 100000 e 1000000']

        df['faixa'] = pd.cut(df['Despesas_empenhadas'], bins=bins, labels=labels, right=False)

        contagem_faixa = df['faixa'].value_counts().reset_index()
        contagem_faixa.columns = ['faixa', 'quantidade']

        faixa_order = ['Menor que 1000', 'Entre 1000 e 5000', 'Entre 5000 e 10000', 
                    'Entre 10000 e 50000', 'Entre 50000 e 100000', 'Entre 100000 e 1000000']
        contagem_faixa['faixa'] = pd.Categorical(contagem_faixa['faixa'], categories=faixa_order, ordered=True)

        # Corrigir a ordenação para manter a sequência correta
        contagem_faixa = contagem_faixa.sort_values(by='faixa')

        # Corrigir o nome do parâmetro numérico
        grafico5 = graf.grafico_barras(contagem_faixa, var_categorica='faixa', var_numerica='quantidade',titulo='Quantidade de Notas por Faixa de Valor')

    else:
        grafico1 = grafico2 = grafico3 = grafico4 = grafico5 = None
########################################### LAYOUT ##################
    tab1, tab2 = st.tabs(["📈 Análises", "🗓️ Tabela Geral"])

    with tab1:
        kpi1_value = df['Despesas_empenhadas'].sum()
        kpi2_value = df['Despesas_pagas'].sum()
        kpi3_value = df['Nota_de_empenho'].nunique()
        kpi4_value = df['Despesas_liquidadas'].sum()
        # Layout das métricas no Streamlit
        kpi1, kpi2,kpi3,kpi4 = st.columns(4)

        # Exibir as métricas
        kpi1.metric("Total de Despesas Empenhadas", f"R$ {func.converte_br(kpi1_value)}")
        kpi2.metric("Total de Despesas Pagas", f"R$ {func.converte_br(kpi2_value)}")
        kpi3.metric("Nota de Empenho Distintas", f"{kpi3_value}")
        kpi4.metric("Total de Despesas Liquidadas", f"R$ {func.converte_br(kpi4_value)}")

        # Layout dos gráficos
        col1, col2,col3 = st.columns([1, 1, 1])
        with col1:
            st.plotly_chart(grafico1, use_container_width=True, config=config_graph)

        with col2:
            st.plotly_chart(grafico3, use_container_width=True, config=config_graph)

        with col3:
            st.plotly_chart(grafico4, use_container_width=True, config=config_graph)
        col4, col5 = st.columns([1, 1])       
        with col4:  
            st.plotly_chart(grafico2, use_container_width=True, config=config_graph)
        with  col5:
            st.plotly_chart(grafico5, use_container_width=True, config=config_graph)

    def tabela_geral(df):
        # Verifica se todas as colunas desejadas estão no DataFrame
        colunas_desejadas = [
            'Data_emissão_ne', 'Unidade_orçamentária','Empresa','sigla','Despesas_empenhadas', 
            'Despesas_liquidadas', 'Despesas_pagas','Subelemento', 'Cnpj', 'Nota_de_empenho', 
            'Histórico/objeto', 'Processo_(ne)'
        ]
        df_tab = df[colunas_desejadas].copy()
        return df_tab

    # Tab 2 - Cria layout e configurações da tabela
    with tab2:
        df_tab = tabela_geral(df)
        column_config=func.configurar_colunas(
            coluna_texto={
            'Nota_de_empenho':"Nota de Empenho",
            "sigla":"Unidade Gestora",
            "Unidade_orçamentária": "Unidade Orçamentária"
            },
            coluna_numerica={
            "Despesas_empenhadas": "Valor das Despesas Empenhadas",
            "Despesas_liquidadas":"Valor das Despesas Liquidadas",
            "Despesas_pagas":"Valor das Despesas Pagas"
            },
            coluna_data={
            'Data_emissão_ne':"Data de Emissão do NE"
            })
       
        # Exibe a tabela no Streamlit
        st.dataframe(df_tab,column_config=column_config,hide_index=True,width=1600,height=600,use_container_width=True)
        func.download_dataframe(df,file_name='Obras',file_format='xlsx')


