import streamlit as st
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
import streamlit.components.v1 as components
import bcampe.graficos as graf

from babel.numbers import format_currency, format_decimal
import math

def converte_br(numero):
    suf = {
        1e3: "K",
        1e6: "M",  # milhão
        1e9: "B",  # bilhão
        1e12: "T"  # trilhão
    }
    negativo = numero < 0
    numero = abs(numero)

    for s in reversed(sorted(suf.keys())):
        if numero >= s:
            # Arredonda para cima e divide pelo sufixo
            valor_arredondado = math.ceil(numero / s)
            # Formata como número inteiro
            valor_formatado = format_decimal(valor_arredondado, format="#,##0", locale='pt_BR')
            return f"{'-' if negativo else ''}{valor_formatado}{suf[s]}"

    # Se não se encaixar em nenhum sufixo, retorna o número formatado como moeda (sem casas decimais)
    return format_currency(numero, 'BRL', locale='pt_BR', format=u'¤#,##0', decimal_quantization=False)

def mostrar():
    def load_data():
        return pd.read_csv("./static/dados_relatorio1.csv", delimiter=',', encoding="utf-8")

    # Função para carregar os dados com cache
    @st.cache_data
    def carregar_dados():
        return load_data()

    # Carregar os dados usando a função com cache
    df = carregar_dados()

    # Inicializar o DataFrame no estado da sessão, se ainda não estiver definido
    if 'df_inicio' not in st.session_state:
        st.session_state.df_inicio = df.copy()
    df_inicio = st.session_state.df_inicio
    df_inicio['Data_emissão_ne'] = pd.to_datetime(df_inicio['Data_emissão_ne'], errors='coerce')
    df_inicio['Mes'] = df_inicio['Data_emissão_ne'].dt.month



    st.markdown("""
        <style>          
        /* Ocultar a barra superior do Streamlit */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* Alterar o fundo da página */
        /* Alterar o fundo do elemento específico */
        .appview-container.st-emotion-cache-1yiq2ps.ea3mdgi9 {
            background-color: rgb(237, 237, 237); /* Cor de fundo desejada */
        }
        .st-cc.st-bn.st-ar.st-cd.st-ce.st-cf{
        color: rgb(0, 0, 0);  /* Cor do placeholder */
        }   
        .css-hhhz79 e1fqkh3o2 { 
            color: rgb(0, 0, 0);  /* Cor desejada para o subheader */
        }
        
        /* Ajustar o posicionamento do bloco vertical */
        [data-testid="stVerticalBlock"] {
            margin-top: 0 !important; /* Remove o espaço acima do bloco */
            padding-top: 0 !important; /* Remove o preenchimento acima do bloco */
            position: relative; /* Garante que o elemento se posicione de forma relativa */
            top: 0; /* Move para o topo */
        }
        [data-testid="stHeaderActionElements"] {
            visibility: hidden;
            display: none;
        }
        [data-testid="StyledFullScreenButton"]{
            visibility: hidden;
            display: none;
        }
        </style>
        """, unsafe_allow_html=True)



    ############### cores ##############

    def generate_colors(num_categorias, color_palette): 
        colors = color_palette * (num_categorias // len(color_palette)) + color_palette[:num_categorias % len(color_palette)]
        return colors
    corazul = ['#052E59']
    corverde =['#355e2a']
    colors_base = ['#052E59','#517496']
    def configurar_layout(fig):
        fig.update_layout(
            paper_bgcolor='white',  # Cor de fundo do papel
            plot_bgcolor='white',   # Cor de fundo do gráfico
            font=dict(color='rgb(0, 0, 0)'),     # Cor da fonte
            xaxis=dict(title_font=dict(color='rgb(0, 0, 0)')),  
            yaxis=dict(title_font=dict(color='rgb(0, 0, 0)')),
            legend=dict(
                itemclick=False,  # Desativa o clique na legenda
                itemdoubleclick=False  # Desativa o duplo clique na legenda
            )   
        )
        return fig
    ###################################### CRIAÇÃO DE GRÁFICOS ###################################
    def grafico1(df):    
        # Agrupar e somar despesas por beneficiário, ordenando de forma decrescente
        graf1 = df.groupby('Nome')["Despesas_empenhadas"].sum().nlargest(10)  # Obter os 10 maiores valores
        entidade_top_1 = graf1.index[0]
        
        # Calcular o total de adiantamentos da entidade top 1
        total_diarias = graf1.values[0]  
        total_diarias = converte_br(total_diarias)

        # Gerar cores
        corgrafico1 = generate_colors(len(graf1), corazul)
        
        # Criar o gráfico
        fig = px.bar(
            x=graf1.values,              # Total de despesas no eixo X
            y=graf1.index,               # Nomes dos beneficiários no eixo Y
            orientation='h'
        )
        
        # Atualizar o layout do gráfico
        fig.update_layout(
            xaxis=dict(title=''),
            yaxis=dict(title='', autorange='reversed'),  # Inverte a ordem do eixo Y
            xaxis_fixedrange=True,
            yaxis_fixedrange=True
        )
        
        # Atualizar traços do gráfico
        fig.update_traces(
            marker=dict(color=corgrafico1),
            hovertemplate=("Nome: <b>%{y}</b><br>Total: <b>%{x}</b><br>"),
            hoverlabel=dict(font_size=13)
        )
        
        # Configurando o layout
        configurar_layout(fig)
        
        return fig, total_diarias, entidade_top_1
    # Gráfico 2 - Total de despesas empenhadas por ano
    import calendar

    def grafico2(df, ano_filtrado=None):
        # Dicionário com siglas dos meses em português
        meses_portugues = {
            1: "Jan", 2: "Fev", 3: "Mar", 4: "Abr", 5: "Mai", 6: "Jun",
            7: "Jul", 8: "Ago", 9: "Set", 10: "Out", 11: "Nov", 12: "Dez"
        }

        if ano_filtrado:
            df_filtrado = df[df['Ano'].isin(map(int, ano_filtrado))]  # Certifica-se de converter para int
            graf2 = df_filtrado.groupby('Mes')["Despesas_empenhadas"].sum()  # Agrupa por mês
            titulo_x = "Mês"
            # Converte números dos meses para siglas em português
            labels_x = [meses_portugues.get(m, m) for m in graf2.index]
        else:
            graf2 = df.groupby('Ano')["Despesas_empenhadas"].sum()  # Agrupa por ano
            titulo_x = "Ano"
            labels_x = graf2.index

        total_diarias = converte_br(graf2.sum())

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=labels_x,
            y=graf2.values,
            mode='lines+markers',
            fill='tozeroy',
            fillcolor='rgba(5, 46, 89, 0.35)',
            line=dict(color='#052E59'),
            marker=dict(color='#052E59', size=6),
            name='',
            hovertemplate=f"{titulo_x}: <b>%{{x}}</b><br>Total: <b>%{{customdata}}</b><br>",
            customdata=[converte_br(valor) for valor in graf2.values]
        ))

        fig.update_layout(
            xaxis=dict(title=titulo_x),
            yaxis=dict(title=None),
            xaxis_fixedrange=True,
            yaxis_fixedrange=True,
            height=360
        )
        configurar_layout(fig)

        return fig, total_diarias


    # Gráfico 3 - Notas de empenho distintas por unidade gestora
    def grafico3(df):
        graf4 = df.groupby('Sigla_unidade_gestora')['Nota_de_empenho'].nunique()        
        graf3 = df.groupby('Sigla_unidade_gestora')['Nota_de_empenho'].nunique().reset_index(name='quantidade')
        top_5_categorias = graf4.sort_values(ascending=False)[:7]
        fig = graf.grafico_pizza(graf3, var_categorica='Sigla_unidade_gestora', var_numerica='quantidade',altura=350,valor="numero",n=7)
        fig.update_layout(title=dict(
                    text='',
                    y=0.95,  # Ajuste a posição vertical do título (0 a 1)
                    x=0.4,   # Centraliza o título
                    xanchor='center',
                    font=dict(size=15)
                    )
            )

        fig.update_traces(hoverlabel=dict(font_size=13))

        configurar_layout(fig)
        # Calcular a unidade gestora com mais notas de empenho
        unidade_gestora_com_maior_ne = top_5_categorias.idxmax()
        valor = top_5_categorias.max()

        return fig, unidade_gestora_com_maior_ne, valor  # Retornar o gráfico e as informações necessárias

    # Gráfico 4 - Unidade gestora por total de despesas empenhadas
    def grafico4(df):
        graf4 = df.groupby('Sigla_unidade_gestora')[['Despesas_empenhadas', 'Despesas_liquidadas', 'Despesas_pagas']].sum().sort_values(by='Despesas_empenhadas', ascending=False).reset_index()[:5]
        
        # Inicializando uma lista para armazenar as informações
        unidades_gestoras = []

        # Capturando as informações das unidades gestoras
        for i in range(len(graf4)):
            unidade_gestora = graf4.iloc[i]['Sigla_unidade_gestora']
            valor_empenhado = graf4.iloc[i]['Despesas_empenhadas']
            valor_liquidado = graf4.iloc[i]['Despesas_liquidadas']
            valor_pago = graf4.iloc[i]['Despesas_pagas']
            
            unidades_gestoras.append((unidade_gestora, valor_empenhado, valor_liquidado, valor_pago))

        # Gerar gráfico
        cor = ['#052E59', '#517496', '#7A89B2']
        corgrafico4 = cor * len(graf4)

        fig = px.bar(
            graf4,
            x='Sigla_unidade_gestora',
            y=['Despesas_empenhadas', 'Despesas_liquidadas', 'Despesas_pagas'],
            color_discrete_sequence=corgrafico4,
            barmode='group'
        )
        fig.update_layout(
            xaxis=dict(title=''),
            yaxis=dict(title=''),  
            xaxis_fixedrange=True,
            yaxis_fixedrange=True
        )
        configurar_layout(fig)

        fig.for_each_trace(lambda trace: trace.update(name={
            'Despesas_empenhadas': 'Despesa Empenhada',
            'Despesas_liquidadas': 'Despesa Liquidada',
            'Despesas_pagas': 'Despesa Paga'
        }[trace.name]))

        fig.update_traces(
            hovertemplate="<b>%{x}</b><br>Total de despesas: R$%{y:,.2f}<extra></extra>",
            hoverlabel=dict(font_size=13)
        )
        configurar_layout(fig)

        return fig, unidades_gestoras



    # Gráfico 5 - Quantidade de Notas por Faixa de Valor
    def grafico5(df):
        bins = [0, 1000, 5000, 10000, 50000, 100000, 1000000]
        labels = [
        'Abaixo de R$ 1.000',
        'R$ 1.000 a R$ 5.000',
        'R$ 5.000 a R$ 10.000',
        'R$ 10.000 a R$ 50.000',
        'R$ 50.000 a R$ 100.000',
        'R$ 100.000 a R$ 1.000.000']

        df['faixa'] = pd.cut(df['Despesas_empenhadas'], bins=bins, labels=labels, right=False)

        # Count the occurrences in each faixa
        contagem_faixa = df['faixa'].value_counts().reset_index()
        contagem_faixa.columns = ['faixa', 'quantidade']
        
        # Calculate total notes and percentage
        total_notas = contagem_faixa['quantidade'].sum()
        contagem_faixa['percentual'] = (contagem_faixa['quantidade'] / total_notas) * 100

        # Get the faixa with the largest quantity using nlargest
        maior_faixa_row = contagem_faixa.nlargest(1, 'quantidade').iloc[0]
        maior_faixa = maior_faixa_row['faixa']
        numero_maior_faixa = maior_faixa_row['quantidade']
        percentual_maior_faixa = maior_faixa_row['percentual']

        # Sort the entire DataFrame in descending order for the graph
        contagem_faixa = contagem_faixa.sort_values(by='quantidade')

        corgrafico5 = generate_colors(len(contagem_faixa), corazul)

        fig = px.bar(contagem_faixa, x='quantidade', y='faixa', orientation='h', 
                    labels={'quantidade': 'Quantidade de Notas', 'faixa': 'Faixa de Valores'})

        fig.update_layout(xaxis_title='Quantidade de Notas', yaxis_title='Faixa de Valores')
        fig.update_traces(marker=dict(color=corgrafico5), 
                        hovertemplate=("Faixa: <b>%{y}</b><br>Total de Notas de Empenho: <b>%{x}</b>"))
        
        # Remove text labels inside the bars
        fig.for_each_trace(lambda trace: trace.update(text=[]))

        configurar_layout(fig)
        
        return fig, maior_faixa, numero_maior_faixa, percentual_maior_faixa

    ################################################# LAYOUT ################################################
    df_filtrado = df_inicio.copy()
    st.markdown("<h1 style='text-align: center;'>Relatório Despesas com Diárias</h1>", unsafe_allow_html=True)
    st.markdown("""
    <p style='text-align: left; font-family: Arial, sans-serif; font-size: 17px; font-weight: normal;'>
        Este relatório apresenta uma análise detalhada das despesas com diárias no Estado do Rio de Janeiro, visando oferecer uma visão clara e transparente dos gastos realizados.
        As diárias são valores pagos aos servidores públicos que se afastam de sua sede de trabalho para realizar atividades a serviço do estado, com o intuito de indenizar gastos com alimentação, hospedagem e locomoção.
        Com base em informações sistematizadas, nosso objetivo é garantir a transparência das despesas, promovendo a responsabilidade na gestão dos recursos públicos.
    </p>

    """, unsafe_allow_html=True)





    # Filtro de Ano
    if 'Ano' not in st.session_state:
        st.session_state['Ano'] = []

    ano = st.multiselect("", sorted(map(str, df_inicio['Ano'].unique())), placeholder="Selecione um ano")

    df_filtrado = df_inicio[df_inicio['Ano'].isin(map(int, ano))] if ano else df_inicio
    st.session_state['Ano'] = ano

    # Layout dos KPIs
    # Cálculo dos valores KPI
    kpi1_value = df_filtrado['Despesas_empenhadas'].sum()
    kpi2_value = df_filtrado['Despesas_pagas'].sum()
    kpi3_value = df_filtrado['Nota_de_empenho'].nunique()
    kpi4_value = df_filtrado['Despesas_liquidadas'].sum()
    # Layout das métricas no Streamlit
    kpi1, kpi2,kpi3,kpi4 = st.columns(4)

    # Exibir as métricas
    kpi1.metric("Total de despesas empenhadas", f"R$ {converte_br(kpi1_value)}")
    kpi2.metric("Total de despesas pagas", f"R$ {converte_br(kpi2_value)}")
    kpi3.metric("Nota de empenho distintas", f"{kpi3_value}")
    kpi4.metric("Total de despesas liquidadas", f"R$ {converte_br(kpi4_value)}")


    # Gráfico 4
    st.subheader("Unidade Gestora por Total de Despesas com Diárias")
    fig4, unidades_gestoras = grafico4(df_filtrado)

    if ano:
        mensagem = f"No ano de <b>{', '.join(ano)}</b>, "
    else:
        mensagem = ""

    # Coletar informações das unidades gestoras e construir a mensagem
    for i, (unidade_gestora, valor_empenhado, valor_liquidado, valor_pago) in enumerate(unidades_gestoras):
        if i == 0:
            mensagem += (f"A unidade gestora que mais investiu em diárias foi <b>{unidade_gestora}</b>, "
                        f"com um total empenhado de <b>{converte_br(valor_empenhado)}</b>. Deste valor, "
                        f"<b>{converte_br(valor_liquidado)}</b> foi liquidado e <b>{converte_br(valor_pago)}</b> já foi pago. ")
        elif i == 1:
            mensagem += (f"Em segundo lugar, a unidade gestora <b>{unidade_gestora}</b> empenhou <b>{converte_br(valor_empenhado)}</b>, "
                        f"dos quais <b>{converte_br(valor_liquidado)}</b> foram liquidados e <b>{converte_br(valor_pago)}</b> já pagos. ")
        elif i == 2:
            mensagem += (f"Na terceira posição, <b>{unidade_gestora}</b> registrou um empenho de <b>{converte_br(valor_empenhado)}</b>, "
                        f"com <b>{converte_br(valor_liquidado)}</b> liquidados e <b>{converte_br(valor_pago)}</b> pagos. ")

    # Exibir o texto final com uma única chamada de markdown
    st.markdown(f"""
        <p style='text-align:left; font-family: Arial, sans-serif; font-size: 17px; font-weight: normal;'>
            {mensagem}
        </p>
    """, unsafe_allow_html=True)

    # Exibir o gráfico
    st.plotly_chart(fig4, use_container_width=True)


    # Gráfico 2
    st.subheader("Total de Despesas com Diárias por Ano")

    fig, total_diarias = grafico2(df_filtrado, st.session_state['Ano'])

    # Texto descritivo
    if ano:
        st.markdown(f"""
        <p style='text-align:left; font-family: Arial, sans-serif; font-size: 17px; font-weight: normal;'>
            No ano de <b>{', '.join(ano)}</b>, o valor total empenhado em diárias foi de 
            <b>{total_diarias}</b>, demonstrando o compromisso com o financiamento de atividades a serviço do estado.
        </p>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <p style='text-align:left; font-family: Arial, sans-serif; font-size: 17px; font-weight: normal;'>
            O valor total empenhado em diárias foi de <b>{total_diarias}</b>, 
            evidenciando o apoio contínuo às atividades dos servidores públicos em suas funções.
        </p>
        """, unsafe_allow_html=True)

    st.plotly_chart(fig, use_container_width=True)


    # Gráfico 1
    st.subheader("Distribuição por Beneficiários de Diárias")

    # Obter os dados do gráfico e as variáveis necessárias
    fig1, total_adiantamentos, entidade_top_1 = grafico1(df_filtrado)

    # Texto descritivo para o gráfico
    if ano:
        st.markdown(f"""
            <p style='text-align:left; font-family: Arial, sans-serif; font-size: 17px; font-weight: normal;'>
                No ano de <b>{', '.join(ano)}</b>, a pessoa com o maior valor recebido em diárias foi 
                <b>{entidade_top_1}</b>, totalizando <b>{total_adiantamentos}</b>. Esse repasse reflete a importância do suporte 
                financeiro aos servidores que se afastam de sua sede para desempenhar suas funções.
            </p>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <p style='text-align:left; font-family: Arial, sans-serif; font-size: 17px; font-weight: normal;'>
                A pessoa com o maior valor recebido em diárias foi <b>{entidade_top_1}</b>, 
                com um total de <b>{total_adiantamentos}</b>. Esse repasse reforça o compromisso com o apoio financeiro aos servidores em suas atividades.
            </p>
        """, unsafe_allow_html=True)

    # Exibir o gráfico
    st.plotly_chart(fig1, use_container_width=True)

    # Gráfico 3
    st.subheader("Notas de Empenho Distintas por Unidade Gestora")
    fig3, unidade_gestora_com_maior_ne, valor = grafico3(df_filtrado)

    # Texto descritivo para o gráfico
    if ano:
        st.markdown(f"""
        <p style='text-align:left; font-family: Arial, sans-serif; font-size: 17px; font-weight: normal;'>
            No ano de <b>{', '.join(ano)}</b>, a unidade gestora com o maior número de notas de empenho foi <b>{unidade_gestora_com_maior_ne}</b>, 
            totalizando <b>{valor}</b> notas de empenho distintas. 
        </p>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <p style='text-align:left; font-family: Arial, sans-serif; font-size: 17px; font-weight: normal;'>
            A unidade gestora com o maior número de notas de empenho foi <b>{unidade_gestora_com_maior_ne}</b>, 
            totalizando <b>{valor}</b> notas de empenho distintas. 
        </p>
        """, unsafe_allow_html=True)

    st.plotly_chart(fig3, use_container_width=True)


    # Gráfico 5
    st.subheader("Quantidade de Notas por Faixa de Valor de Diárias")
    fig5, maior_faixa, numero_maior_faixa, percentual_maior_faixa = grafico5(df_filtrado)

    if ano:
        st.markdown(f"""
        <p style='text-align:left; font-family: Arial, sans-serif; font-size: 17px; font-weight: normal;'>
            No ano de <b>{', '.join(ano)}</b>, as notas de empenho estavam predominantemente concentradas na faixa de <b>{maior_faixa}</b>, 
            representando um total de <b>{numero_maior_faixa}</b> notas de empenho, o que corresponde a <b>{percentual_maior_faixa:.2f}%</b> do total.
        </p>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <p style='text-align:left; font-family: Arial, sans-serif; font-size: 17px; font-weight: normal;'>
            As notas de empenho estão predominantemente concentradas na faixa de <b>{maior_faixa}</b>, 
            representando um total de <b>{numero_maior_faixa}</b> notas de empenho, o que corresponde a <b>{percentual_maior_faixa:.2f}%</b> do total.
        </p>
        """, unsafe_allow_html=True)

    st.plotly_chart(fig5, use_container_width=True)
