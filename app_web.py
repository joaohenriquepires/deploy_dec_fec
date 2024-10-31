# Streamlit
import streamlit as st
from streamlit_option_menu import option_menu    # menu para sidebar do streamlit

# Analise de Dados
import pandas as pd
import numpy as np
from datetime import datetime
import calendar
import plotly.express as px
from tabelas_graficos import base_dec_polo_enel, base_fec_polo_enel, base_meta_dec_aneel_polos, base_meta_fec_aneel_polos
from tabelas_graficos import base_dec, base_fec
from tabelas_graficos import base_meta_aneel_conjuntos, base_conjuntos

# Titulo - subtitulo
st.set_page_config( 
    page_title='DEC-FEC Enel Rio',
    page_icon='📊',
    layout='wide'
)

### Sidebar Superior ###
st.sidebar.image('https://upload.wikimedia.org/wikipedia/commons/thumb/2/22/Enel_Group_logo.svg/1024px-Enel_Group_logo.svg.png', use_column_width=True)
st.sidebar.title('DEC-FEC Enel Rio')

# customizar a sidebar
with st.sidebar:

    # menu de seleção
    selected = option_menu(

        # titulo
        'Menu',

        # opções de navegação
        ['Enel Rio', 'Polos - YTD', 'Polos - LTM', 'Conjuntos', 'Listagem Conjuntos'],

        # Icones para o menu das opções
        icons=['bar-chart-fill', 'bar-chart-fill', 'bar-chart-fill', 'bar-chart-fill', 'bar-chart-fill'],

        # icone do menu principal
        menu_icon='cast',

        # Seleção padrão
        default_index=0,

        # Estilos
        styles={
            'menu-title' : {'font-size' : '17px'}, # Diminui o tamanho da fonte do título
            'menu-icon': {'display': 'none'},  # Remove o ícone do título
            'icon': {'font-size': '12px'},  # Estilo dos ícones
            'nav-link': {
                'font-size': '13px',  # Tamanho da fonte dos itens do menu
                '--hover-color': '#7f9ee3',  # Cor de fundo ao passar o mouse
            },
            'nav-link-selected': {'background-color': '#082d7c'},  # Cor de fundo do item selecionado
        }
    )




# Filtros
lista_ano = ['24'] #, '23']
lista_polos = ['Campos', 'Lagos', 'Macaé', 'Magé', 'Niterói', 'Noroeste', 'São Gonçalo', 'Serrana', 'Sul']




# Navegação das paginas
if selected == 'Enel Rio':
    
    # Titulo da pagina
    st.title('Indicadores Enel Rio')

    st.write('---')

    # Tabela
    col1, col2, col3 = st.columns(3)

    with col1:
        selecione_ano = st.selectbox('Ano', lista_ano, index=None)
    
    # tabelas para geração dos graficos    
    base_dec_polo_enel_ano = base_dec_polo_enel[base_dec_polo_enel['Meses'].str.contains(f'/{selecione_ano}')]
    base_dec_polo_enel_ano = base_dec_polo_enel_ano.iloc[:, [0] + list(range(-3, 0))]
    base_dec_polo_enel_ano_transformado = pd.melt(base_dec_polo_enel_ano, id_vars=['Meses'], var_name='UT', value_name='DEC')
    totais_por_mes_polo_enel_ano_dec = base_dec_polo_enel_ano_transformado.groupby('UT')['DEC'].sum().reset_index()

    base_fec_polo_enel_ano = base_fec_polo_enel[base_fec_polo_enel['Meses'].str.contains(f'/{selecione_ano}')]
    base_fec_polo_enel_ano = base_fec_polo_enel_ano.iloc[:, [0] + list(range(-3, 0))]
    base_fec_polo_enel_ano_transformado = pd.melt(base_fec_polo_enel_ano, id_vars=['Meses'], var_name='UT', value_name='FEC')
    totais_por_mes_polo_enel_ano_fec = base_fec_polo_enel_ano_transformado.groupby('UT')['FEC'].sum().reset_index()




    # tabelas para geração dos graficos 
    base_dec_polos = base_dec_polo_enel.iloc[:, :-3]
    base_dec_polos = base_dec_polos[base_dec_polos['Meses'].str.contains(f'/{selecione_ano}')]
    base_dec_polos_transformado = pd.melt(base_dec_polos, id_vars=['Meses'], var_name='Polos', value_name='DEC')
    totais_por_mes_polos_dec = base_dec_polos_transformado.groupby('Polos')['DEC'].sum().reset_index()
    totais_por_mes_polos_dec = totais_por_mes_polos_dec.merge(base_meta_dec_aneel_polos[['DEC POLO', '2024']], left_on='Polos', right_on='DEC POLO', how='left')
    totais_por_mes_polos_dec.rename(columns = {'2024':'Meta DEC Ano'}, inplace = True)
    totais_por_mes_polos_dec = totais_por_mes_polos_dec.drop(columns=['DEC POLO'])
    totais_por_mes_polos_dec['Meta DEC Ano'] = totais_por_mes_polos_dec['Meta DEC Ano'].str.replace(',', '.').astype(float)
    base_dec_polos_transformado['Meses_Ordenados'] = pd.to_datetime(base_dec_polos_transformado['Meses'], format='%b/%y')
    base_dec_polos_transformado = base_dec_polos_transformado.sort_values(by=['Meses_Ordenados', 'Polos']).drop(columns=['Meses_Ordenados'])
    base_dec_polos_transformado = base_dec_polos_transformado[['Polos', 'Meses', 'DEC']].reset_index(drop=True)

    base_fec_polos = base_fec_polo_enel.iloc[:, :-3]
    base_fec_polos = base_fec_polos[base_fec_polos['Meses'].str.contains(f'/{selecione_ano}')]
    base_fec_polos_transformado = pd.melt(base_fec_polos, id_vars=['Meses'], var_name='Polos', value_name='FEC')
    totais_por_mes_polos_fec = base_fec_polos_transformado.groupby('Polos')['FEC'].sum().reset_index()
    totais_por_mes_polos_fec = totais_por_mes_polos_fec.merge(base_meta_fec_aneel_polos[['FEC POLO', '2024']], left_on='Polos', right_on='FEC POLO', how='left')
    totais_por_mes_polos_fec.rename(columns = {'2024':'Meta FEC Ano'}, inplace = True)
    totais_por_mes_polos_fec = totais_por_mes_polos_fec.drop(columns=['FEC POLO'])
    base_fec_polos_transformado['Meses_Ordenados'] = pd.to_datetime(base_fec_polos_transformado['Meses'], format='%b/%y')
    base_fec_polos_transformado = base_fec_polos_transformado.sort_values(by=['Meses_Ordenados', 'Polos']).drop(columns=['Meses_Ordenados'])
    base_fec_polos_transformado = base_fec_polos_transformado[['Polos', 'Meses', 'FEC']].reset_index(drop=True)




    # Polos acima e abaixo do DEC-FEC
    dec_acima = totais_por_mes_polos_dec[totais_por_mes_polos_dec['DEC'] > totais_por_mes_polos_dec['Meta DEC Ano']].shape[0]
    dec_abaixo = totais_por_mes_polos_dec[totais_por_mes_polos_dec['DEC'] <= totais_por_mes_polos_dec['Meta DEC Ano']].shape[0]
    fec_acima = totais_por_mes_polos_fec[totais_por_mes_polos_fec['FEC'] > totais_por_mes_polos_fec['Meta FEC Ano']].shape[0]
    fec_abaixo = totais_por_mes_polos_fec[totais_por_mes_polos_fec['FEC'] <= totais_por_mes_polos_fec['Meta FEC Ano']].shape[0]




    col1, col2 = st.columns(2)

    # Gráficos de dec-fec enel rio 
    graf_dec_ut_enel = px.bar(base_dec_polo_enel_ano_transformado, x='UT', y='DEC', color='Meses', title='DEC', width=430, height=380)
    graf_dec_ut_enel.update_layout(
        title_x=0.5,
        xaxis_title='',  # Remove o título do eixo x
        yaxis_title='',  # Remove o título do eixo y
        legend=dict(
            orientation="h",  # Define a orientação horizontal
            yanchor="bottom",  # Ancorar a legenda na parte inferior
            y=-0.8,           # Ajustar a posição vertical da legenda
            xanchor="center",  # Ancorar horizontalmente no centro
            x=0.5),
        annotations=[dict(
            x=row['UT'],
            y=row['DEC'],
            text=f"{row['DEC']:.2f}", # Formata o valor com duas casas decimais
            showarrow=False, 
            font=dict(size=12),
            xanchor='center', 
            yanchor='bottom') for index, row in totais_por_mes_polo_enel_ano_dec.iterrows()])

    graf_fec_ut_enel = px.bar(base_fec_polo_enel_ano_transformado, x='UT', y='FEC', color='Meses', title='FEC', width=430, height=380)
    graf_fec_ut_enel.update_layout(
        title_x=0.5,
        xaxis_title='',  # Remove o título do eixo x
        yaxis_title='',  # Remove o título do eixo y
        legend=dict(
            orientation="h",  # Define a orientação horizontal
            yanchor="bottom",  # Ancorar a legenda na parte inferior
            y=-0.8,           # Ajustar a posição vertical da legenda
            xanchor="center",  # Ancorar horizontalmente no centro
            x=0.5),
        annotations=[dict(
            x=row['UT'],
            y=row['FEC'],
            text=f"{row['FEC']:.2f}", # Formata o valor com duas casas decimais
            showarrow=False, 
            font=dict(size=12),
            xanchor='center', 
            yanchor='bottom') for index, row in totais_por_mes_polo_enel_ano_fec.iterrows()])

    col1.plotly_chart(graf_dec_ut_enel)
    col2.plotly_chart(graf_fec_ut_enel)


    st.write('---')


    # Frame para incluir os big numerbs
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.subheader('DEC')
    col4.subheader('FEC')
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric('Polos Acima Limite', dec_acima)

    with col2:
        st.metric('Polos Abaixo Limite', dec_abaixo)

    with col4:
        st.metric('Polos Acima Limite', fec_acima)

    with col5:
        st.metric('Polos Abaixo Limite', fec_abaixo)




    col3, col4 = st.columns(2)

    # Gráficos de dec-fec polos
    graf_dec_polos = px.bar(base_dec_polos_transformado, x='Polos', y='DEC', color='Meses', title='DEC', width=430, height=400)
    graf_dec_polos.update_layout(
        title_x=0.5,
        xaxis_title='',  # Remove o título do eixo x
        yaxis_title='',  # Remove o título do eixo y
        legend=dict(
            orientation="h",  # Define a orientação horizontal
            yanchor="bottom",  # Ancorar a legenda na parte inferior
            y=-0.85,           # Ajustar a posição vertical da legenda
            xanchor="center",  # Ancorar horizontalmente no centro
            x=0.5),
        annotations=[dict(
            x=row['Polos'],
            y=row['DEC'],
            text=f"{row['DEC']:.2f}", # Formata o valor com duas casas decimais
            showarrow=False, 
            font=dict(size=12),
            xanchor='center', 
            yanchor='bottom') for index, row in totais_por_mes_polos_dec.iterrows()])
    graf_dec_polos.add_scatter(x=base_dec_polos_transformado['Polos'], y=totais_por_mes_polos_dec['Meta DEC Ano'], mode="lines+markers+text", name="Meta DEC", line=dict(color="black", dash="dash"), text=totais_por_mes_polos_dec['Meta DEC Ano'], textposition="top center", textfont=dict(color='black'))


    graf_fec_polos = px.bar(base_fec_polos_transformado, x='Polos', y='FEC', color='Meses', title='FEC', width=430, height=400)
    graf_fec_polos.update_layout(
        title_x=0.5,
        xaxis_title='',  # Remove o título do eixo x
        yaxis_title='',  # Remove o título do eixo y
        legend=dict(
            orientation="h",  # Define a orientação horizontal
            yanchor="bottom",  # Ancorar a legenda na parte inferior
            y=-0.85,           # Ajustar a posição vertical da legenda
            xanchor="center",  # Ancorar horizontalmente no centro
            x=0.5),
        annotations=[dict(
            x=row['Polos'],
            y=row['FEC'],
            text=f"{row['FEC']:.2f}", # Formata o valor com duas casas decimais
            showarrow=False, 
            font=dict(size=12),
            xanchor='center', 
            yanchor='bottom') for index, row in totais_por_mes_polos_fec.iterrows()])
    graf_fec_polos.add_scatter(x=base_fec_polos_transformado['Polos'], y=totais_por_mes_polos_fec['Meta FEC Ano'], mode="lines+markers+text", name="Meta FEC", line=dict(color="black", dash="dash"), text=totais_por_mes_polos_fec['Meta FEC Ano'], textposition="top center", textfont=dict(color='black'))

    col3.plotly_chart(graf_dec_polos)
    col4.plotly_chart(graf_fec_polos)




    # rodapé 
    st.markdown(
        '''
            <hr style='border: 1px solid #d3d3d3;'/>
            <p style='text-align: center; color: gray;'>
                Análise DEC-FEC Enel Rio | Dados fornecidos por OyM Rio | Desenvolvido por João Henrique Pires | © 2024
            </p>
        ''',
        unsafe_allow_html=True
    )



# Navegação das paginas
if selected == 'Polos - YTD':

    # Titulo da pagina
    st.title('Indicadores Polos - YTD')

    st.write('---')

    # Tabela
    col1, col2, col3 = st.columns(3)

    with col1:
        selecione_polo = st.selectbox('Polo', lista_polos, index=None)

    with col2:
        selecione_ano = st.selectbox('Ano', lista_ano, index=None)
    

    base_dec_polo = pd.merge(base_dec, base_conjuntos, on='Conjunto', how='left')
    colunas_para_mover_dec = base_dec_polo.columns[-3:].tolist() #extraindo as ultimas 3 colunas que vieram do merge
    base_dec_menor = base_dec_polo.drop(columns=colunas_para_mover_dec) #removendo as colunas da base original
    base_dec_novo = pd.concat([base_dec_menor.iloc[:, :1], base_dec_polo[colunas_para_mover_dec], base_dec_menor.iloc[:, 1:]], axis=1) #inserindo as colunas na posição específica
    base_dec_polo = base_dec_novo.copy()

    base_fec_polo = pd.merge(base_fec, base_conjuntos, on='Conjunto', how='left')
    colunas_para_mover_fec = base_fec_polo.columns[-3:].tolist() #extraindo as ultimas 3 colunas que vieram do merge
    base_fec_menor = base_fec_polo.drop(columns=colunas_para_mover_fec) #removendo as colunas da base original
    base_fec_novo = pd.concat([base_fec_menor.iloc[:, :1], base_fec_polo[colunas_para_mover_fec], base_fec_menor.iloc[:, 1:]], axis=1) #inserindo as colunas na posição específica
    base_fec_polo = base_fec_novo.copy()

    base_dec_polo_filtro = base_dec_polo[base_dec_polo['Regional'] == selecione_polo] # filtrando o DF pelo polo escolhido
    primeira_coluna_dec = base_dec_polo_filtro.iloc[:, [0]] # pegando a primeira coluna do DF filtrado
    colunas_ano_filtrado_dec = base_dec_polo_filtro.filter(like=f'{selecione_ano}') # pegando o DF no ano escolhido
    df_resultado_dec = pd.concat([primeira_coluna_dec, colunas_ano_filtrado_dec], axis=1).reset_index(drop=True)
    df_transformado_dec = pd.melt(df_resultado_dec, id_vars=['Conjunto'], var_name='Mês', value_name='DEC')
    totais_por_mes_dec = df_transformado_dec.groupby('Conjunto')['DEC'].sum().reset_index()
    totais_por_mes_dec = totais_por_mes_dec.merge(base_meta_aneel_conjuntos[['Conjunto', 'DEC']], on='Conjunto').rename(columns={'DEC_x':'DEC','DEC_y':'Meta DEC'})

    base_fec_polo_filtro = base_fec_polo[base_fec_polo['Regional'] == selecione_polo]
    primeira_coluna_fec = base_fec_polo_filtro.iloc[:, [0]]
    colunas_ano_filtrado_fec = base_fec_polo_filtro.filter(like=f'{selecione_ano}')
    df_resultado_fec = pd.concat([primeira_coluna_fec, colunas_ano_filtrado_fec], axis=1).reset_index(drop=True)
    df_transformado_fec = pd.melt(df_resultado_fec, id_vars=['Conjunto'], var_name='Mês', value_name='FEC')
    totais_por_mes_fec = df_transformado_fec.groupby('Conjunto')['FEC'].sum().reset_index()
    totais_por_mes_fec = totais_por_mes_fec.merge(base_meta_aneel_conjuntos[['Conjunto', 'FEC']], on='Conjunto').rename(columns={'FEC_x':'FEC','FEC_y':'Meta FEC'})




    # Quantidade de colunas bases DEC e FEC
    qtd_cols = base_dec.shape[1]
    meses = {'jan': 1, 'fev': 2, 'mar': 3, 'abr': 4, 'mai': 5, 'jun': 6, 'jul': 7, 'ago': 8, 'set': 9, 'out': 10, 'nov': 11, 'dez': 12}
    ultima_coluna = base_dec.columns[-1]
    abreviatura_mes = ultima_coluna[:3]
    numero_ultimo_mes = meses[abreviatura_mes]

    data_atual = datetime.now()
    dia_do_ano = data_atual.timetuple().tm_yday
    total_dias_ano = 366 if calendar.isleap(data_atual.year) else 365
    percentual_ano = (dia_do_ano / total_dias_ano)


    # Criação de base DEC/FEC Análises
    base_dec_analises = pd.DataFrame()
    base_dec_analises = base_dec[['Conjunto']]
    # Cálculo de DEC acumulado ano
    base_dec_analises['DEC Acumulado - 2024'] = base_dec.iloc[:, (qtd_cols - numero_ultimo_mes):].sum(axis=1)
    # Merge para pegar a meta Aneel
    base_dec_analises = pd.merge(base_dec_analises, base_meta_aneel_conjuntos[['Conjunto', 'DEC']], on='Conjunto', how='left')
    base_dec_analises.rename(columns = {'DEC':'Meta Aneel DEC'}, inplace = True)
    # Criação de coluna "% Consumido da Meta Anual"
    base_dec_analises['% Consumido da Meta Anual'] = base_dec_analises['DEC Acumulado - 2024'] / base_dec_analises['Meta Aneel DEC']
    # Cálculo DEC TAM
    base_dec_analises['DEC TAM'] = base_dec.iloc[:, qtd_cols - 12:].sum(axis=1)
    # Criação de coluna "% Consumido TAM"
    base_dec_analises['% Consumido TAM'] = base_dec_analises['DEC TAM'] / base_dec_analises['Meta Aneel DEC']

    base_fec_analises = pd.DataFrame()
    base_fec_analises = base_fec[['Conjunto']]
    # Cálculo de FEC acumulado ano
    base_fec_analises['FEC Acumulado - 2024'] = base_fec.iloc[:, (qtd_cols - numero_ultimo_mes):].sum(axis=1)
    # Merge para pegar a meta Aneel
    base_fec_analises = pd.merge(base_fec_analises, base_meta_aneel_conjuntos[['Conjunto', 'FEC']], on='Conjunto', how='left')
    base_fec_analises.rename(columns = {'FEC':'Meta Aneel FEC'}, inplace = True)
    # Criação de coluna "% Consumido da Meta Anual"
    base_fec_analises['% Consumido da Meta Anual'] = base_fec_analises['FEC Acumulado - 2024'] / base_fec_analises['Meta Aneel FEC']
    # Cálculo FEC TAM
    base_fec_analises['FEC TAM'] = base_fec.iloc[:, qtd_cols - 12:].sum(axis=1)
    # Criação de coluna "% Consumido TAM"
    base_fec_analises['% Consumido TAM'] = base_fec_analises['FEC TAM'] / base_fec_analises['Meta Aneel FEC']


    base_dec_analises_com_polo = base_dec_analises.merge(base_conjuntos[['Conjunto', 'Regional']], on='Conjunto')
    base_dec_analise_ytd = base_dec_analises_com_polo[base_dec_analises_com_polo['Regional'] == selecione_polo]
    base_dec_analise_ytd = base_dec_analise_ytd.sort_values(by='% Consumido da Meta Anual', ascending=True)
    def definir_cor_DEC_ytd(valor):
        if valor > 1:
            return 'DEC Irreversível'
        elif percentual_ano <= valor <= 1:
            return 'DEC em Atenção'
        else:
            return 'DEC Controlado'
    base_dec_analise_ytd['Status DEC YTD'] = base_dec_analise_ytd['% Consumido da Meta Anual'].apply(definir_cor_DEC_ytd)

    base_fec_analises_com_polo = base_fec_analises.merge(base_conjuntos[['Conjunto', 'Regional']], on='Conjunto')
    base_fec_analise_ytd = base_fec_analises_com_polo[base_fec_analises_com_polo['Regional'] == selecione_polo]
    base_fec_analise_ytd = base_fec_analise_ytd.sort_values(by='% Consumido da Meta Anual', ascending=True)
    def definir_cor_FEC_ytd(valor):
        if valor > 1:
            return 'FEC Irreversível'
        elif percentual_ano <= valor <= 1:
            return 'FEC em Atenção'
        else:
            return 'FEC Controlado'
    base_fec_analise_ytd['Status FEC YTD'] = base_fec_analise_ytd['% Consumido da Meta Anual'].apply(definir_cor_FEC_ytd)




    num_dec_controlado = base_dec_analise_ytd['Status DEC YTD'].value_counts().get('DEC Controlado', 0)
    num_dec_atencao = base_dec_analise_ytd['Status DEC YTD'].value_counts().get('DEC em Atenção', 0)
    num_dec_irreversivel = base_dec_analise_ytd['Status DEC YTD'].value_counts().get('DEC Irreversível', 0)

    num_fec_controlado = base_fec_analise_ytd['Status FEC YTD'].value_counts().get('FEC Controlado', 0)
    num_fec_atencao = base_fec_analise_ytd['Status FEC YTD'].value_counts().get('FEC em Atenção', 0)
    num_fec_irreversivel = base_fec_analise_ytd['Status FEC YTD'].value_counts().get('FEC Irreversível', 0)


    col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
    col1.subheader('DEC')
    col5.subheader('FEC')
    col1, col2, col3, col4, col5, col6, col7 = st.columns(7)

    col1.metric(label="Normal", value=f"{num_dec_controlado}")
    col2.metric(label="Em Atenção", value=f"{num_dec_atencao}")
    col3.metric(label="Crítico", value=f"{num_dec_irreversivel}")
    col5.metric(label="Normal", value=f"{num_fec_controlado}")
    col6.metric(label="Em Atenção", value=f"{num_fec_atencao}")
    col7.metric(label="Crítico", value=f"{num_fec_irreversivel}")



    col1, col2 = st.columns(2)

    # Gráficos de dec-fec
    graf_dec_conjuntos = px.bar(df_transformado_dec, x='Conjunto', y='DEC', color='Mês', title='DEC YTD', width=430)
    graf_dec_conjuntos.update_layout(
        title_x=0.5,
        xaxis_title='',  # Remove o título do eixo x
        yaxis_title='',  # Remove o título do eixo y
        legend=dict(
            orientation="h",  # Define a orientação horizontal
            yanchor="bottom",  # Ancorar a legenda na parte inferior
            y=-0.9,           # Ajustar a posição vertical da legenda
            xanchor="center",  # Ancorar horizontalmente no centro
            x=0.5),
        annotations=[dict(
            x=row['Conjunto'],
            y=row['DEC'],
            text=f"{row['DEC']:.2f}", # Formata o valor com duas casas decimais
            showarrow=False, 
            font=dict(size=12),
            xanchor='center', 
            yanchor='bottom') for index, row in totais_por_mes_dec.iterrows()])
    graf_dec_conjuntos.add_scatter(x=df_transformado_dec['Conjunto'], y=totais_por_mes_dec['Meta DEC'], mode="lines+markers+text", name="Meta DEC", line=dict(color="black", dash="dash"), text=totais_por_mes_dec['Meta DEC'], textposition="top center", textfont=dict(color='black'))

    graf_fec_conjuntos = px.bar(df_transformado_fec, x='Conjunto', y='FEC', color='Mês', title='FEC YTD', width=430)
    graf_fec_conjuntos.update_layout(
        title_x=0.5,
        xaxis_title='',  # Remove o título do eixo x
        yaxis_title='',  # Remove o título do eixo y
        legend=dict(
            orientation="h",  # Define a orientação horizontal
            yanchor="bottom",  # Ancorar a legenda na parte inferior
            y=-0.9,           # Ajustar a posição vertical da legenda
            xanchor="center",  # Ancorar horizontalmente no centro
            x=0.5),
        annotations=[dict(
            x=row['Conjunto'],
            y=row['FEC'],
            text=f"{row['FEC']:.2f}", # Formata o valor com duas casas decimais
            showarrow=False, 
            font=dict(size=12),
            xanchor='center', 
            yanchor='bottom') for index, row in totais_por_mes_fec.iterrows()])
    graf_fec_conjuntos.add_scatter(x=df_transformado_fec['Conjunto'], y=totais_por_mes_fec['Meta FEC'], mode="lines+markers+text", name="Meta FEC", line=dict(color="black", dash="dash"), text=totais_por_mes_fec['Meta FEC'], textposition="top center", textfont=dict(color='black'))

    col1.plotly_chart(graf_dec_conjuntos)
    col2.plotly_chart(graf_fec_conjuntos)




    col1, col2 = st.columns(2)

    # Gráficos de % dec-fec ytd
    graf_dec_conjuntos_ytd = px.bar(base_dec_analise_ytd, x='% Consumido da Meta Anual' , y='Conjunto', title='DEC YTD 2024',
                                    orientation='h', text=base_dec_analise_ytd['% Consumido da Meta Anual'], width=430, height=400,
                                    color='Status DEC YTD', color_discrete_map={'DEC Irreversível': 'red', 'DEC em Atenção': 'yellow', 'DEC Controlado': 'green'})
    graf_dec_conjuntos_ytd.update_traces(texttemplate='%{text:.2%}', textposition='inside')
    graf_dec_conjuntos_ytd.update_layout(xaxis_title='', yaxis_title='', title_x=0.5,
        legend=dict(
        orientation="h",  # Define a orientação horizontal
        yanchor="bottom",  # Ancorar a legenda na parte inferior
        y=-0.4,           # Ajustar a posição vertical da legenda
        xanchor="center",  # Ancorar horizontalmente no centro
        x=0.5))

    graf_fec_conjuntos_ytd = px.bar(base_fec_analise_ytd, x='% Consumido da Meta Anual' , y='Conjunto', title='FEC YTD 2024',
                                    orientation='h', text=base_fec_analise_ytd['% Consumido da Meta Anual'], width=430, height=400,
                                    color='Status FEC YTD', color_discrete_map={'FEC Irreversível': 'red', 'FEC em Atenção': 'yellow', 'FEC Controlado': 'green'})
    graf_fec_conjuntos_ytd.update_traces(texttemplate='%{text:.2%}', textposition='inside')
    graf_fec_conjuntos_ytd.update_layout(xaxis_title='', yaxis_title='', title_x=0.5,
        legend=dict(
        orientation="h",  # Define a orientação horizontal
        yanchor="bottom",  # Ancorar a legenda na parte inferior
        y=-0.4,           # Ajustar a posição vertical da legenda
        xanchor="center",  # Ancorar horizontalmente no centro
        x=0.5))
    
    col1.plotly_chart(graf_dec_conjuntos_ytd)
    col2.plotly_chart(graf_fec_conjuntos_ytd)


    # rodapé 
    st.markdown(
        '''
            <hr style='border: 1px solid #d3d3d3;'/>
            <p style='text-align: center; color: gray;'>
                Análise DEC-FEC Enel Rio | Dados fornecidos por OyM Rio | Desenvolvido por João Henrique Pires | © 2024
            </p>
        ''',
        unsafe_allow_html=True
    )



# Navegação das paginas
if selected == 'Polos - LTM':

    # Titulo da pagina
    st.title('Indicadores Polos - LTM')

    st.write('---')

    # Tabela
    col1, col2, col3 = st.columns(3)

    with col1:
        selecione_polo = st.selectbox('Polo', lista_polos, index=None)


    base_dec_polo = pd.merge(base_dec, base_conjuntos, on='Conjunto', how='left')
    colunas_para_mover_dec = base_dec_polo.columns[-3:].tolist() #extraindo as ultimas 3 colunas que vieram do merge
    base_dec_menor = base_dec_polo.drop(columns=colunas_para_mover_dec) #removendo as colunas da base original
    base_dec_novo = pd.concat([base_dec_menor.iloc[:, :1], base_dec_polo[colunas_para_mover_dec], base_dec_menor.iloc[:, 1:]], axis=1) #inserindo as colunas na posição específica
    base_dec_polo = base_dec_novo.copy()

    base_fec_polo = pd.merge(base_fec, base_conjuntos, on='Conjunto', how='left')
    colunas_para_mover_fec = base_fec_polo.columns[-3:].tolist() #extraindo as ultimas 3 colunas que vieram do merge
    base_fec_menor = base_fec_polo.drop(columns=colunas_para_mover_fec) #removendo as colunas da base original
    base_fec_novo = pd.concat([base_fec_menor.iloc[:, :1], base_fec_polo[colunas_para_mover_fec], base_fec_menor.iloc[:, 1:]], axis=1) #inserindo as colunas na posição específica
    base_fec_polo = base_fec_novo.copy()

    base_dec_polo_filtro = base_dec_polo[base_dec_polo['Regional'] == selecione_polo] # filtrando o DF pelo polo escolhido
    primeira_coluna_dec = base_dec_polo_filtro.iloc[:, [0]] # pegando a primeira coluna do DF filtrado
    colunas_ano_filtrado_dec = base_dec_polo_filtro.iloc[:, list(range(-12, 0))] # pegando as ultimas 12 colunas (ltm)
    df_resultado_dec = pd.concat([primeira_coluna_dec, colunas_ano_filtrado_dec], axis=1).reset_index(drop=True)
    df_transformado_dec = pd.melt(df_resultado_dec, id_vars=['Conjunto'], var_name='Mês', value_name='DEC')
    totais_por_mes_dec = df_transformado_dec.groupby('Conjunto')['DEC'].sum().reset_index()
    totais_por_mes_dec = totais_por_mes_dec.merge(base_meta_aneel_conjuntos[['Conjunto', 'DEC']], on='Conjunto').rename(columns={'DEC_x':'DEC','DEC_y':'Meta DEC'})

    base_fec_polo_filtro = base_fec_polo[base_fec_polo['Regional'] == selecione_polo]
    primeira_coluna_fec = base_fec_polo_filtro.iloc[:, [0]] # pegando a primeira coluna do DF filtrado
    colunas_ano_filtrado_fec = base_fec_polo_filtro.iloc[:, list(range(-12, 0))] # pegando as ultimas 12 colunas (ltm)
    df_resultado_fec = pd.concat([primeira_coluna_fec, colunas_ano_filtrado_fec], axis=1).reset_index(drop=True)
    df_transformado_fec = pd.melt(df_resultado_fec, id_vars=['Conjunto'], var_name='Mês', value_name='FEC')
    totais_por_mes_fec = df_transformado_fec.groupby('Conjunto')['FEC'].sum().reset_index()
    totais_por_mes_fec = totais_por_mes_fec.merge(base_meta_aneel_conjuntos[['Conjunto', 'FEC']], on='Conjunto').rename(columns={'FEC_x':'FEC','FEC_y':'Meta FEC'})


    # Quantidade de colunas bases DEC e FEC
    qtd_cols = base_dec.shape[1]
    meses = {'jan': 1, 'fev': 2, 'mar': 3, 'abr': 4, 'mai': 5, 'jun': 6, 'jul': 7, 'ago': 8, 'set': 9, 'out': 10, 'nov': 11, 'dez': 12}
    ultima_coluna = base_dec.columns[-1]
    abreviatura_mes = ultima_coluna[:3]
    numero_ultimo_mes = meses[abreviatura_mes]

    data_atual = datetime.now()
    dia_do_ano = data_atual.timetuple().tm_yday
    total_dias_ano = 366 if calendar.isleap(data_atual.year) else 365
    percentual_ano = (dia_do_ano / total_dias_ano)


    # Criação de base DEC/FEC Análises
    base_dec_analises = pd.DataFrame()
    base_dec_analises = base_dec[['Conjunto']]
    # Cálculo de DEC acumulado ano
    base_dec_analises['DEC Acumulado - 2024'] = base_dec.iloc[:, (qtd_cols - numero_ultimo_mes):].sum(axis=1)
    # Merge para pegar a meta Aneel
    base_dec_analises = pd.merge(base_dec_analises, base_meta_aneel_conjuntos[['Conjunto', 'DEC']], on='Conjunto', how='left')
    base_dec_analises.rename(columns = {'DEC':'Meta Aneel DEC'}, inplace = True)
    # Criação de coluna "% Consumido da Meta Anual"
    base_dec_analises['% Consumido da Meta Anual'] = base_dec_analises['DEC Acumulado - 2024'] / base_dec_analises['Meta Aneel DEC']
    # Cálculo DEC TAM
    base_dec_analises['DEC TAM'] = base_dec.iloc[:, qtd_cols - 12:].sum(axis=1)
    # Criação de coluna "% Consumido TAM"
    base_dec_analises['% Consumido TAM'] = base_dec_analises['DEC TAM'] / base_dec_analises['Meta Aneel DEC']

    base_fec_analises = pd.DataFrame()
    base_fec_analises = base_fec[['Conjunto']]
    # Cálculo de FEC acumulado ano
    base_fec_analises['FEC Acumulado - 2024'] = base_fec.iloc[:, (qtd_cols - numero_ultimo_mes):].sum(axis=1)
    # Merge para pegar a meta Aneel
    base_fec_analises = pd.merge(base_fec_analises, base_meta_aneel_conjuntos[['Conjunto', 'FEC']], on='Conjunto', how='left')
    base_fec_analises.rename(columns = {'FEC':'Meta Aneel FEC'}, inplace = True)
    # Criação de coluna "% Consumido da Meta Anual"
    base_fec_analises['% Consumido da Meta Anual'] = base_fec_analises['FEC Acumulado - 2024'] / base_fec_analises['Meta Aneel FEC']
    # Cálculo FEC TAM
    base_fec_analises['FEC TAM'] = base_fec.iloc[:, qtd_cols - 12:].sum(axis=1)
    # Criação de coluna "% Consumido TAM"
    base_fec_analises['% Consumido TAM'] = base_fec_analises['FEC TAM'] / base_fec_analises['Meta Aneel FEC']


    base_dec_analises_com_polo = base_dec_analises.merge(base_conjuntos[['Conjunto', 'Regional']], on='Conjunto')
    base_dec_analise_ytd = base_dec_analises_com_polo[base_dec_analises_com_polo['Regional'] == selecione_polo]
    base_dec_analise_ytd = base_dec_analise_ytd.sort_values(by='% Consumido da Meta Anual', ascending=True)
    def definir_cor_DEC_ytd(valor):
        if valor > 1:
            return 'DEC Irreversível'
        elif percentual_ano <= valor <= 1:
            return 'DEC em Atenção'
        else:
            return 'DEC Controlado'
    base_dec_analise_ytd['Status DEC YTD'] = base_dec_analise_ytd['% Consumido da Meta Anual'].apply(definir_cor_DEC_ytd)

    base_fec_analises_com_polo = base_fec_analises.merge(base_conjuntos[['Conjunto', 'Regional']], on='Conjunto')
    base_fec_analise_ytd = base_fec_analises_com_polo[base_fec_analises_com_polo['Regional'] == selecione_polo]
    base_fec_analise_ytd = base_fec_analise_ytd.sort_values(by='% Consumido da Meta Anual', ascending=True)
    def definir_cor_FEC_ytd(valor):
        if valor > 1:
            return 'FEC Irreversível'
        elif percentual_ano <= valor <= 1:
            return 'FEC em Atenção'
        else:
            return 'FEC Controlado'
    base_fec_analise_ytd['Status FEC YTD'] = base_fec_analise_ytd['% Consumido da Meta Anual'].apply(definir_cor_FEC_ytd)


    base_dec_analise_tam = base_dec_analise_ytd.sort_values(by='% Consumido TAM', ascending=True)
    def definir_cor_DEC_tam(valor):
        if valor >= 1.4:
            return 'Conjunto Crítico'
        elif valor < 1:
            return 'Conjunto Normal'
        else:
            return 'Conjunto em Atenção'
    base_dec_analise_tam['Status DEC TAM'] = base_dec_analise_tam['% Consumido TAM'].apply(definir_cor_DEC_tam)

    base_fec_analise_tam = base_fec_analise_ytd.sort_values(by='% Consumido TAM', ascending=True)
    def definir_cor_FEC_tam(valor):
        if valor >= 1.22:
            return 'Conjunto Crítico'
        elif valor < 1:
            return 'Conjunto Normal'
        else:
            return 'Conjunto em Atenção'
    base_fec_analise_tam['Status FEC TAM'] = base_fec_analise_tam['% Consumido TAM'].apply(definir_cor_FEC_tam)




    num_dec_controlado = base_dec_analise_tam['Status DEC TAM'].value_counts().get('Conjunto Normal', 0)
    num_dec_atencao = base_dec_analise_tam['Status DEC TAM'].value_counts().get('Conjunto em Atenção', 0)
    num_dec_irreversivel = base_dec_analise_tam['Status DEC TAM'].value_counts().get('Conjunto Crítico', 0)

    num_fec_controlado = base_fec_analise_tam['Status FEC TAM'].value_counts().get('Conjunto Normal', 0)
    num_fec_atencao = base_fec_analise_tam['Status FEC TAM'].value_counts().get('Conjunto em Atenção', 0)
    num_fec_irreversivel = base_fec_analise_tam['Status FEC TAM'].value_counts().get('Conjunto Crítico', 0)


    col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
    col1.subheader('DEC')
    col5.subheader('FEC')
    col1, col2, col3, col4, col5, col6, col7 = st.columns(7)

    col1.metric(label="Normal", value=f"{num_dec_controlado}")
    col2.metric(label="Em Atenção", value=f"{num_dec_atencao}")
    col3.metric(label="Crítico", value=f"{num_dec_irreversivel}")
    col5.metric(label="Normal", value=f"{num_fec_controlado}")
    col6.metric(label="Em Atenção", value=f"{num_fec_atencao}")
    col7.metric(label="Crítico", value=f"{num_fec_irreversivel}")




    col1, col2 = st.columns(2)

    # Gráficos de dec-fec
    graf_dec_conjuntos = px.bar(df_transformado_dec, x='Conjunto', y='DEC', color='Mês', title='DEC LTM 2024', width=430)
    graf_dec_conjuntos.update_layout(
        title_x=0.5,
        xaxis_title='',  # Remove o título do eixo x
        yaxis_title='',  # Remove o título do eixo y
        legend=dict(
            orientation="h",  # Define a orientação horizontal
            yanchor="bottom",  # Ancorar a legenda na parte inferior
            y=-0.9,           # Ajustar a posição vertical da legenda
            xanchor="center",  # Ancorar horizontalmente no centro
            x=0.5),
        annotations=[dict(
            x=row['Conjunto'],
            y=row['DEC'],
            text=f"{row['DEC']:.2f}", # Formata o valor com duas casas decimais
            showarrow=False, 
            font=dict(size=12),
            xanchor='center', 
            yanchor='bottom') for index, row in totais_por_mes_dec.iterrows()])
    graf_dec_conjuntos.add_scatter(x=df_transformado_dec['Conjunto'], y=totais_por_mes_dec['Meta DEC'], mode="lines+markers+text", name="Meta DEC", line=dict(color="black", dash="dash"), text=totais_por_mes_dec['Meta DEC'], textposition="top center", textfont=dict(color='black'))

    graf_fec_conjuntos = px.bar(df_transformado_fec, x='Conjunto', y='FEC', color='Mês', title='FEC LTM 2024', width=430)
    graf_fec_conjuntos.update_layout(
        title_x=0.5,
        xaxis_title='',  # Remove o título do eixo x
        yaxis_title='',  # Remove o título do eixo y
        legend=dict(
            orientation="h",  # Define a orientação horizontal
            yanchor="bottom",  # Ancorar a legenda na parte inferior
            y=-0.9,           # Ajustar a posição vertical da legenda
            xanchor="center",  # Ancorar horizontalmente no centro
            x=0.5),
        annotations=[dict(
            x=row['Conjunto'],
            y=row['FEC'],
            text=f"{row['FEC']:.2f}", # Formata o valor com duas casas decimais
            showarrow=False, 
            font=dict(size=12),
            xanchor='center', 
            yanchor='bottom') for index, row in totais_por_mes_fec.iterrows()])
    graf_fec_conjuntos.add_scatter(x=df_transformado_fec['Conjunto'], y=totais_por_mes_fec['Meta FEC'], mode="lines+markers+text", name="Meta FEC", line=dict(color="black", dash="dash"), text=totais_por_mes_fec['Meta FEC'], textposition="top center", textfont=dict(color='black'))

    col1.plotly_chart(graf_dec_conjuntos)
    col2.plotly_chart(graf_fec_conjuntos)




    col1, col2 = st.columns(2)


    # Gráficos de % dec-fec tam
    graf_dec_conjuntos_tam = px.bar(base_dec_analise_tam, x='% Consumido TAM', y='Conjunto', title='DEC LTM 2024',
                                    orientation='h', text=base_dec_analise_tam['% Consumido TAM'], width=430, height=400,
                                    color='Status DEC TAM', color_discrete_map={'Conjunto Crítico': 'red', 'Conjunto em Atenção': 'yellow', 'Conjunto Normal': 'green'})
    graf_dec_conjuntos_tam.update_traces(texttemplate='%{text:.2%}', textposition='inside')
    graf_dec_conjuntos_tam.update_layout(xaxis_title='', yaxis_title='', title_x=0.5,
        legend=dict(
        orientation="h",  # Define a orientação horizontal
        yanchor="bottom",  # Ancorar a legenda na parte inferior
        y=-0.6,           # Ajustar a posição vertical da legenda
        xanchor="center",  # Ancorar horizontalmente no centro
        x=0.5))


    # Gráficos de % dec-fec tam
    graf_fec_conjuntos_tam = px.bar(base_fec_analise_tam, x='% Consumido TAM', y='Conjunto', title='FEC LTM 2024',
                                    orientation='h', text=base_fec_analise_tam['% Consumido TAM'], width=430, height=400,
                                    color='Status FEC TAM', color_discrete_map={'Conjunto Crítico': 'red', 'Conjunto em Atenção': 'yellow', 'Conjunto Normal': 'green'})
    graf_fec_conjuntos_tam.update_traces(texttemplate='%{text:.2%}', textposition='inside')
    graf_fec_conjuntos_tam.update_layout(xaxis_title='', yaxis_title='', title_x=0.5,
        legend=dict(
        orientation="h",  # Define a orientação horizontal
        yanchor="bottom",  # Ancorar a legenda na parte inferior
        y=-0.6,           # Ajustar a posição vertical da legenda
        xanchor="center",  # Ancorar horizontalmente no centro
        x=0.5))


    col1.plotly_chart(graf_dec_conjuntos_tam)
    col2.plotly_chart(graf_fec_conjuntos_tam)




    # rodapé 
    st.markdown(
        '''
            <hr style='border: 1px solid #d3d3d3;'/>
            <p style='text-align: center; color: gray;'>
                Análise DEC-FEC Enel Rio | Dados fornecidos por OyM Rio | Desenvolvido por João Henrique Pires | © 2024
            </p>
        ''',
        unsafe_allow_html=True
    )



# Navegação das paginas
if selected == 'Conjuntos':

    # Titulo da pagina
    st.title('Indicadores Conjuntos')

    st.write('---')


    qtd_cols = base_dec.shape[1]
    meses = {'jan': 1, 'fev': 2, 'mar': 3, 'abr': 4, 'mai': 5, 'jun': 6, 'jul': 7, 'ago': 8, 'set': 9, 'out': 10, 'nov': 11, 'dez': 12}
    ultima_coluna = base_dec.columns[-1]
    abreviatura_mes = ultima_coluna[:3]
    numero_ultimo_mes = meses[abreviatura_mes]


    # Criação de base DEC/FEC Análises
    base_dec_analises = pd.DataFrame()
    base_dec_analises = base_dec[['Conjunto']]
    # Cálculo de DEC acumulado ano
    base_dec_analises['DEC Acumulado - 2024'] = base_dec.iloc[:, (qtd_cols - numero_ultimo_mes):].sum(axis=1)
    # Merge para pegar a meta Aneel
    base_dec_analises = pd.merge(base_dec_analises, base_meta_aneel_conjuntos[['Conjunto', 'DEC']], on='Conjunto', how='left')
    base_dec_analises.rename(columns = {'DEC':'Meta Aneel DEC'}, inplace = True)
    # Criação de coluna "% Consumido da Meta Anual"
    base_dec_analises['% Consumido da Meta Anual'] = base_dec_analises['DEC Acumulado - 2024'] / base_dec_analises['Meta Aneel DEC']
    # Cálculo DEC TAM
    base_dec_analises['DEC TAM'] = base_dec.iloc[:, qtd_cols - 12:].sum(axis=1)
    # Criação de coluna "% Consumido TAM"
    base_dec_analises['% Consumido TAM'] = base_dec_analises['DEC TAM'] / base_dec_analises['Meta Aneel DEC']

    base_fec_analises = pd.DataFrame()
    base_fec_analises = base_fec[['Conjunto']]
    # Cálculo de FEC acumulado ano
    base_fec_analises['FEC Acumulado - 2024'] = base_fec.iloc[:, (qtd_cols - numero_ultimo_mes):].sum(axis=1)
    # Merge para pegar a meta Aneel
    base_fec_analises = pd.merge(base_fec_analises, base_meta_aneel_conjuntos[['Conjunto', 'FEC']], on='Conjunto', how='left')
    base_fec_analises.rename(columns = {'FEC':'Meta Aneel FEC'}, inplace = True)
    # Criação de coluna "% Consumido da Meta Anual"
    base_fec_analises['% Consumido da Meta Anual'] = base_fec_analises['FEC Acumulado - 2024'] / base_fec_analises['Meta Aneel FEC']
    # Cálculo FEC TAM
    base_fec_analises['FEC TAM'] = base_fec.iloc[:, qtd_cols - 12:].sum(axis=1)
    # Criação de coluna "% Consumido TAM"
    base_fec_analises['% Consumido TAM'] = base_fec_analises['FEC TAM'] / base_fec_analises['Meta Aneel FEC']


    # DF estado dos Conjuntos 2024
    base_estado_conjuntos_dec = base_dec.iloc[:, [0] + list(range(14, qtd_cols))] # quando mudar o ano, alterar o 14 para 26
    base_estado_conjuntos_dec_TAM = base_estado_conjuntos_dec.iloc[:, 1:]
    base_estado_conjuntos_dec_TAM = base_estado_conjuntos_dec_TAM.rolling(window=12, axis=1).sum()
    base_estado_conjuntos_dec_TAM['Conjunto'] = base_estado_conjuntos_dec['Conjunto']
    base_estado_conjuntos_dec_TAM = base_estado_conjuntos_dec_TAM.drop(base_estado_conjuntos_dec_TAM.columns[:11], axis=1)
    base_estado_conjuntos_dec_TAM = base_estado_conjuntos_dec_TAM[['Conjunto'] + [col for col in base_estado_conjuntos_dec_TAM.columns if col != 'Conjunto']]
    base_estado_conjuntos_dec_TAM.columns = [base_estado_conjuntos_dec_TAM.columns[0]] + [f"TAM {col}" for col in base_estado_conjuntos_dec_TAM.columns[1:]]


    # DF estado dos Conjuntos 2024
    base_estado_conjuntos_fec = base_fec.iloc[:, [0] + list(range(14, qtd_cols))] # quando mudar o ano, alterar o 14 para 26
    base_estado_conjuntos_fec_TAM = base_estado_conjuntos_fec.iloc[:, 1:]
    base_estado_conjuntos_fec_TAM = base_estado_conjuntos_fec_TAM.rolling(window=12, axis=1).sum()
    base_estado_conjuntos_fec_TAM['Conjunto'] = base_estado_conjuntos_fec['Conjunto']
    base_estado_conjuntos_fec_TAM = base_estado_conjuntos_fec_TAM.drop(base_estado_conjuntos_fec_TAM.columns[:11], axis=1)
    base_estado_conjuntos_fec_TAM = base_estado_conjuntos_fec_TAM[['Conjunto'] + [col for col in base_estado_conjuntos_fec_TAM.columns if col != 'Conjunto']]
    base_estado_conjuntos_fec_TAM.columns = [base_estado_conjuntos_fec_TAM.columns[0]] + [f"TAM {col}" for col in base_estado_conjuntos_fec_TAM.columns[1:]]


    # Criando DF com o estado do conjunto em 2024
    base_estado_conjuntos_dec = pd.DataFrame()
    base_estado_conjuntos_dec['Conjunto'] = base_conjuntos['Conjunto']
    base_estado_conjuntos_dec.insert(loc=1, column='Meta Aneel DEC', value=base_dec_analises['Meta Aneel DEC'])
    for coluna in base_estado_conjuntos_dec_TAM.columns[1:]:
        base_estado_conjuntos_dec[f'{coluna}'] = base_estado_conjuntos_dec_TAM[coluna] / base_estado_conjuntos_dec['Meta Aneel DEC']
    for coluna in base_estado_conjuntos_dec.columns[2:]:
        base_estado_conjuntos_dec[coluna] = np.where(base_estado_conjuntos_dec[coluna] < 1, 'Normal',
                                            np.where(base_estado_conjuntos_dec[coluna] <= 1.4, 'Atenção',
                                            'Crítico'))
    base_estado_conjuntos_dec = base_estado_conjuntos_dec.drop('Meta Aneel DEC', axis=1)
    base_estado_conjuntos_dec.columns = base_estado_conjuntos_dec.columns.str.replace('TAM ', '', regex=False)

    # Criando DF com o estado do conjunto em 2024
    base_estado_conjuntos_fec = pd.DataFrame()
    base_estado_conjuntos_fec['Conjunto'] = base_conjuntos['Conjunto']
    base_estado_conjuntos_fec.insert(loc=1, column='Meta Aneel FEC', value=base_fec_analises['Meta Aneel FEC'])
    for coluna in base_estado_conjuntos_fec_TAM.columns[1:]:
        base_estado_conjuntos_fec[f'{coluna}'] = base_estado_conjuntos_fec_TAM[coluna] / base_estado_conjuntos_fec['Meta Aneel FEC']
    for coluna in base_estado_conjuntos_fec.columns[2:]:
        base_estado_conjuntos_fec[coluna] = np.where(base_estado_conjuntos_fec[coluna] < 1, 'Normal',
                                            np.where(base_estado_conjuntos_fec[coluna] <= 1.22, 'Atenção',
                                            'Crítico'))
    base_estado_conjuntos_fec = base_estado_conjuntos_fec.drop('Meta Aneel FEC', axis=1)
    base_estado_conjuntos_fec.columns = base_estado_conjuntos_fec.columns.str.replace('TAM ', '', regex=False)


    meses_ano = ['jan/24', 'fev/24', 'mar/24', 'abr/24', 'mai/24', 'jun/24', 'jul/24', 'ago/24', 'set/24', 'out/24', 'nov/24', 'dez/24']
    ordem_colunas = meses_ano[0:(base_estado_conjuntos_dec.shape[1] - 1)]
    ordem_categorias = ['Normal', 'Atenção', 'Crítico']


    base_estado_conjuntos_dec_melt = pd.melt(base_estado_conjuntos_dec, id_vars=['Conjunto'], var_name='Mês', value_name='Estado Conjunto')
    base_estado_conjuntos_dec_consolidado = pd.crosstab(base_estado_conjuntos_dec_melt['Estado Conjunto'], base_estado_conjuntos_dec_melt['Mês'])
    base_estado_conjuntos_dec_consolidado_DF = pd.DataFrame(base_estado_conjuntos_dec_consolidado)
    base_estado_conjuntos_dec_consolidado_DF = base_estado_conjuntos_dec_consolidado_DF[ordem_colunas]
    base_estado_conjuntos_dec_consolidado_DF = base_estado_conjuntos_dec_consolidado_DF.reset_index()
    base_estado_conjuntos_dec_consolidado_DF['Estado Conjunto'] = pd.Categorical(base_estado_conjuntos_dec_consolidado_DF['Estado Conjunto'], categories=ordem_categorias, ordered=True)
    base_estado_conjuntos_dec_consolidado_DF = base_estado_conjuntos_dec_consolidado_DF.sort_values(by='Estado Conjunto')

    base_estado_conjuntos_fec_melt = pd.melt(base_estado_conjuntos_fec, id_vars=['Conjunto'], var_name='Mês', value_name='Estado Conjunto')
    base_estado_conjuntos_fec_consolidado = pd.crosstab(base_estado_conjuntos_fec_melt['Estado Conjunto'], base_estado_conjuntos_fec_melt['Mês'])
    base_estado_conjuntos_fec_consolidado_DF = pd.DataFrame(base_estado_conjuntos_fec_consolidado)
    base_estado_conjuntos_fec_consolidado_DF = base_estado_conjuntos_fec_consolidado_DF[ordem_colunas]
    base_estado_conjuntos_fec_consolidado_DF = base_estado_conjuntos_fec_consolidado_DF.reset_index()
    base_estado_conjuntos_fec_consolidado_DF['Estado Conjunto'] = pd.Categorical(base_estado_conjuntos_fec_consolidado_DF['Estado Conjunto'], categories=ordem_categorias, ordered=True)
    base_estado_conjuntos_fec_consolidado_DF = base_estado_conjuntos_fec_consolidado_DF.sort_values(by='Estado Conjunto')


    base_estado_conjuntos_dec_consolidado_DF_melt = base_estado_conjuntos_dec_consolidado_DF.melt(id_vars=['Estado Conjunto'], var_name='Mês', value_name='Num Conjuntos')

    base_estado_conjuntos_fec_consolidado_DF_melt = base_estado_conjuntos_fec_consolidado_DF.melt(id_vars=['Estado Conjunto'], var_name='Mês', value_name='Num Conjuntos')



    metrica_conjuntos_dec_ultimas_col = pd.DataFrame(base_estado_conjuntos_dec_consolidado_DF.iloc[:, [0, -2, -1]].copy())
    metrica_conjuntos_dec_ultimas_col['Delta Mês'] = metrica_conjuntos_dec_ultimas_col.iloc[:, -1] - metrica_conjuntos_dec_ultimas_col.iloc[:, -2]
    metrica_conjuntos_dec_ultimas_col['% Mês'] = ((metrica_conjuntos_dec_ultimas_col.iloc[:, -2] - metrica_conjuntos_dec_ultimas_col.iloc[:, -3]) / metrica_conjuntos_dec_ultimas_col.iloc[:, -3]) * 100

    metrica_conjuntos_fec_ultimas_col = pd.DataFrame(base_estado_conjuntos_fec_consolidado_DF.iloc[:, [0, -2, -1]].copy())
    metrica_conjuntos_fec_ultimas_col['Delta Mês'] = metrica_conjuntos_fec_ultimas_col.iloc[:, -1] - metrica_conjuntos_fec_ultimas_col.iloc[:, -2]
    metrica_conjuntos_fec_ultimas_col['% Mês'] = ((metrica_conjuntos_fec_ultimas_col.iloc[:, -2] - metrica_conjuntos_fec_ultimas_col.iloc[:, -3]) / metrica_conjuntos_fec_ultimas_col.iloc[:, -3]) * 100


    st.header("DEC")

    col1, col2, col3 = st.columns(3)

    col1.metric(label="Conjuntos Normais", value=f"{metrica_conjuntos_dec_ultimas_col.iloc[0, -3]}", delta=f"{metrica_conjuntos_dec_ultimas_col.iloc[0, -2]} Conjuntos ({metrica_conjuntos_dec_ultimas_col.iloc[0, -1]:.1f}%)")
    col2.metric(label="Conjuntos em Atenção", value=f"{metrica_conjuntos_dec_ultimas_col.iloc[1, -3]}", delta=f"{metrica_conjuntos_dec_ultimas_col.iloc[1, -2]} Conjuntos ({metrica_conjuntos_dec_ultimas_col.iloc[1, -1]:.1f}%)", delta_color="inverse")
    col3.metric(label="Conjuntos Críticos", value=f"{metrica_conjuntos_dec_ultimas_col.iloc[2, -3]}", delta=f"{metrica_conjuntos_dec_ultimas_col.iloc[2, -2]} Conjuntos ({metrica_conjuntos_dec_ultimas_col.iloc[2, -1]:.1f}%)", delta_color="inverse")

    graf_base_estado_conjuntos_dec_consolidado_DF_melt = px.bar(base_estado_conjuntos_dec_consolidado_DF_melt, x="Mês", y="Num Conjuntos", width=860, height=300,
                                                                color="Estado Conjunto", text=base_estado_conjuntos_dec_consolidado_DF_melt['Num Conjuntos'],
                                                                color_discrete_map={'Crítico': 'FireBrick', 'Atenção': 'Gold', 'Normal': 'DarkGreen'})
    graf_base_estado_conjuntos_dec_consolidado_DF_melt.update_layout(xaxis_title='', yaxis_title='', title_x=0.5, title_text='',
        legend=dict(
        orientation="h",  # Define a orientação horizontal
        yanchor="bottom",  # Ancorar a legenda na parte inferior
        y=-0.5,           # Ajustar a posição vertical da legenda
        xanchor="center",  # Ancorar horizontalmente no centro
        x=0.5))

    with st.container():
        graf_base_estado_conjuntos_dec_consolidado_DF_melt

    
    st.write('---')


    st.header("FEC")

    col1, col2, col3 = st.columns(3)

    metrica_conjuntos_fec_ultimas_col = pd.DataFrame(base_estado_conjuntos_fec_consolidado_DF.iloc[:, [0, -2, -1]].copy())
    metrica_conjuntos_fec_ultimas_col['Delta Mês'] = metrica_conjuntos_fec_ultimas_col.iloc[:, -1] - metrica_conjuntos_fec_ultimas_col.iloc[:, -2]
    metrica_conjuntos_fec_ultimas_col['% Mês'] = ((metrica_conjuntos_fec_ultimas_col.iloc[:, -2] - metrica_conjuntos_fec_ultimas_col.iloc[:, -3]) / metrica_conjuntos_fec_ultimas_col.iloc[:, -3]) * 100

    col1.metric(label="Conjuntos Normais", value=f"{metrica_conjuntos_fec_ultimas_col.iloc[0, -3]}", delta=f"{metrica_conjuntos_fec_ultimas_col.iloc[0, -2]} Conjuntos ({metrica_conjuntos_fec_ultimas_col.iloc[0, -1]:.1f}%)")
    col2.metric(label="Conjuntos em Atenção", value=f"{metrica_conjuntos_fec_ultimas_col.iloc[1, -3]}", delta=f"{metrica_conjuntos_fec_ultimas_col.iloc[1, -2]} Conjuntos ({metrica_conjuntos_fec_ultimas_col.iloc[1, -1]:.1f}%)", delta_color="inverse")
    col3.metric(label="Conjuntos Críticos", value=f"{metrica_conjuntos_fec_ultimas_col.iloc[2, -3]}", delta=f"{metrica_conjuntos_fec_ultimas_col.iloc[2, -2]} Conjuntos ({metrica_conjuntos_fec_ultimas_col.iloc[2, -1]:.1f}%)", delta_color="inverse")

    graf_base_estado_conjuntos_fec_consolidado_DF_melt = px.bar(base_estado_conjuntos_fec_consolidado_DF_melt, x="Mês", y="Num Conjuntos", width=860, height=300,
                                                                color="Estado Conjunto", text=base_estado_conjuntos_fec_consolidado_DF_melt['Num Conjuntos'],
                                                                color_discrete_map={'Crítico': 'FireBrick', 'Atenção': 'Gold', 'Normal': 'DarkGreen'})
    graf_base_estado_conjuntos_fec_consolidado_DF_melt.update_layout(xaxis_title='', yaxis_title='', title_x=0.5, title_text='',
        legend=dict(
        orientation="h",  # Define a orientação horizontal
        yanchor="bottom",  # Ancorar a legenda na parte inferior
        y=-0.5,           # Ajustar a posição vertical da legenda
        xanchor="center",  # Ancorar horizontalmente no centro
        x=0.5))

    with st.container():
        graf_base_estado_conjuntos_fec_consolidado_DF_melt




    # rodapé 
    st.markdown(
        '''
            <hr style='border: 1px solid #d3d3d3;'/>
            <p style='text-align: center; color: gray;'>
                Análise DEC-FEC Enel Rio | Dados fornecidos por OyM Rio | Desenvolvido por João Henrique Pires | © 2024
            </p>
        ''',
        unsafe_allow_html=True
    )



# Navegação das paginas
if selected == 'Listagem Conjuntos':

    # Titulo da pagina
    st.title('Listagem Conjuntos - EDRJ')

    st.write('---')


    # Quantidade de colunas bases DEC e FEC
    qtd_cols = base_dec.shape[1]
    meses = {'jan': 1, 'fev': 2, 'mar': 3, 'abr': 4, 'mai': 5, 'jun': 6, 'jul': 7, 'ago': 8, 'set': 9, 'out': 10, 'nov': 11, 'dez': 12}
    ultima_coluna = base_dec.columns[-1]
    abreviatura_mes = ultima_coluna[:3]
    numero_ultimo_mes = meses[abreviatura_mes]

    data_atual = datetime.now()
    dia_do_ano = data_atual.timetuple().tm_yday
    total_dias_ano = 366 if calendar.isleap(data_atual.year) else 365
    percentual_ano = (dia_do_ano / total_dias_ano)


    # Criação de base DEC/FEC Análises
    base_dec_analises = pd.DataFrame()
    base_dec_analises = base_dec[['Conjunto']]
    # Cálculo de DEC acumulado ano
    base_dec_analises['DEC Acumulado - 2024'] = base_dec.iloc[:, (qtd_cols - numero_ultimo_mes):].sum(axis=1)
    # Merge para pegar a meta Aneel
    base_dec_analises = pd.merge(base_dec_analises, base_meta_aneel_conjuntos[['Conjunto', 'DEC']], on='Conjunto', how='left')
    base_dec_analises.rename(columns = {'DEC':'Meta Aneel DEC'}, inplace = True)
    # Criação de coluna "% Consumido da Meta Anual"
    base_dec_analises['% Consumido da Meta Anual'] = base_dec_analises['DEC Acumulado - 2024'] / base_dec_analises['Meta Aneel DEC']
    # Cálculo DEC TAM
    base_dec_analises['DEC TAM'] = base_dec.iloc[:, qtd_cols - 12:].sum(axis=1)
    # Criação de coluna "% Consumido TAM"
    base_dec_analises['% Consumido TAM'] = base_dec_analises['DEC TAM'] / base_dec_analises['Meta Aneel DEC']

    base_fec_analises = pd.DataFrame()
    base_fec_analises = base_fec[['Conjunto']]
    # Cálculo de FEC acumulado ano
    base_fec_analises['FEC Acumulado - 2024'] = base_fec.iloc[:, (qtd_cols - numero_ultimo_mes):].sum(axis=1)
    # Merge para pegar a meta Aneel
    base_fec_analises = pd.merge(base_fec_analises, base_meta_aneel_conjuntos[['Conjunto', 'FEC']], on='Conjunto', how='left')
    base_fec_analises.rename(columns = {'FEC':'Meta Aneel FEC'}, inplace = True)
    # Criação de coluna "% Consumido da Meta Anual"
    base_fec_analises['% Consumido da Meta Anual'] = base_fec_analises['FEC Acumulado - 2024'] / base_fec_analises['Meta Aneel FEC']
    # Cálculo FEC TAM
    base_fec_analises['FEC TAM'] = base_fec.iloc[:, qtd_cols - 12:].sum(axis=1)
    # Criação de coluna "% Consumido TAM"
    base_fec_analises['% Consumido TAM'] = base_fec_analises['FEC TAM'] / base_fec_analises['Meta Aneel FEC']


    base_dec_analises_com_polo = base_dec_analises.merge(base_conjuntos[['Conjunto', 'Regional']], on='Conjunto')

    base_fec_analises_com_polo = base_fec_analises.merge(base_conjuntos[['Conjunto', 'Regional']], on='Conjunto')


    base_dec_analises_com_polo_tam = base_dec_analises_com_polo.sort_values(by='% Consumido TAM', ascending=True)
    def definir_cor_DEC_tam(valor):
        if valor >= 1.4:
            return 'Conjunto Crítico'
        elif valor < 1:
            return 'Conjunto Normal'
        else:
            return 'Conjunto em Atenção'
    base_dec_analises_com_polo_tam['Status DEC TAM'] = base_dec_analises_com_polo_tam['% Consumido TAM'].apply(definir_cor_DEC_tam)

    base_fec_analises_com_polo_tam = base_fec_analises_com_polo.sort_values(by='% Consumido TAM', ascending=True)
    def definir_cor_FEC_tam(valor):
        if valor >= 1.22:
            return 'Conjunto Crítico'
        elif valor < 1:
            return 'Conjunto Normal'
        else:
            return 'Conjunto em Atenção'
    base_fec_analises_com_polo_tam['Status FEC TAM'] = base_fec_analises_com_polo_tam['% Consumido TAM'].apply(definir_cor_FEC_tam)


    base_dec_analises_com_polo_ytd = base_dec_analises_com_polo.sort_values(by='% Consumido da Meta Anual', ascending=True)
    def definir_cor_DEC_ytd(valor):
        if valor > 1:
            return 'DEC Irreversível'
        elif percentual_ano <= valor <= 1:
            return 'DEC em Atenção'
        else:
            return 'DEC Controlado'
    base_dec_analises_com_polo_ytd['Status DEC YTD'] = base_dec_analises_com_polo_ytd['% Consumido da Meta Anual'].apply(definir_cor_DEC_ytd)

    base_fec_analises_com_polo_ytd = base_fec_analises_com_polo.sort_values(by='% Consumido da Meta Anual', ascending=True)
    def definir_cor_FEC_ytd(valor):
        if valor > 1:
            return 'FEC Irreversível'
        elif percentual_ano <= valor <= 1:
            return 'FEC em Atenção'
        else:
            return 'FEC Controlado'
    base_fec_analises_com_polo_ytd['Status FEC YTD'] = base_fec_analises_com_polo_ytd['% Consumido da Meta Anual'].apply(definir_cor_FEC_ytd)





    graf_dec_conjuntos_horizontal_tam = px.bar(base_dec_analises_com_polo_tam, x='% Consumido TAM', y='Conjunto', orientation='h',
                                            text=base_dec_analises_com_polo_tam['% Consumido TAM'],
                                            width=860, height=1600, color='Status DEC TAM',
                                            color_discrete_map={'Conjunto Crítico': 'FireBrick', 'Conjunto em Atenção': 'gold', 'Conjunto Normal': 'darkgreen'})
    graf_dec_conjuntos_horizontal_tam.update_traces(texttemplate='%{text:.2%}', textposition='auto',
                                                    textfont=dict(size=24))
    graf_dec_conjuntos_horizontal_tam.update_layout(xaxis_title='', yaxis_title='', title_x=0.5, title_text='',
        yaxis=dict(tickfont=dict(size=10)),
        legend=dict(
        orientation="h",  # Define a orientação horizontal
        yanchor="bottom",  # Ancorar a legenda na parte inferior
        y=-0.1,           # Ajustar a posição vertical da legenda
        xanchor="center",  # Ancorar horizontalmente no centro
        x=0.5))


    graf_fec_conjuntos_horizontal_tam = px.bar(base_fec_analises_com_polo_tam, x='% Consumido TAM', y='Conjunto', orientation='h',
                                            text=base_fec_analises_com_polo_tam['% Consumido TAM'],
                                            width=860, height=1600, color='Status FEC TAM',
                                            color_discrete_map={'Conjunto Crítico': 'FireBrick', 'Conjunto em Atenção': 'gold', 'Conjunto Normal': 'darkgreen'})
    graf_fec_conjuntos_horizontal_tam.update_traces(texttemplate='%{text:.2%}', textposition='auto',
                                                    textfont=dict(size=24))
    graf_fec_conjuntos_horizontal_tam.update_layout(xaxis_title='', yaxis_title='', title_x=0.5, title_text='',
        yaxis=dict(tickfont=dict(size=10)),
        legend=dict(
        orientation="h",  # Define a orientação horizontal
        yanchor="bottom",  # Ancorar a legenda na parte inferior
        y=-0.1,           # Ajustar a posição vertical da legenda
        xanchor="center",  # Ancorar horizontalmente no centro
        x=0.5))




    graf_dec_conjuntos_horizontal_ytd = px.bar(base_dec_analises_com_polo_ytd, x='% Consumido da Meta Anual', y='Conjunto', orientation='h',
                                            text=base_dec_analises_com_polo_ytd['% Consumido da Meta Anual'],
                                            width=860, height=1600, color='Status DEC YTD',
                                            color_discrete_map={'DEC Irreversível': 'FireBrick', 'DEC em Atenção': 'gold', 'DEC Controlado': 'darkgreen'})
    graf_dec_conjuntos_horizontal_ytd.update_traces(texttemplate='%{text:.2%}', textposition='auto',
                                                    textfont=dict(size=24))
    graf_dec_conjuntos_horizontal_ytd.update_layout(xaxis_title='', yaxis_title='', title_x=0.5, title_text='',
        yaxis=dict(tickfont=dict(size=10)),
        legend=dict(
        orientation="h",  # Define a orientação horizontal
        yanchor="bottom",  # Ancorar a legenda na parte inferior
        y=-0.05,           # Ajustar a posição vertical da legenda
        xanchor="center",  # Ancorar horizontalmente no centro
        x=0.5))
    

    graf_fec_conjuntos_horizontal_ytd = px.bar(base_fec_analises_com_polo_ytd, x='% Consumido da Meta Anual', y='Conjunto', orientation='h',
                                            text=base_fec_analises_com_polo_ytd['% Consumido da Meta Anual'],
                                            width=860, height=1600, color='Status FEC YTD',
                                            color_discrete_map={'FEC Irreversível': 'FireBrick', 'FEC em Atenção': 'gold', 'FEC Controlado': 'darkgreen'})
    graf_fec_conjuntos_horizontal_ytd.update_traces(texttemplate='%{text:.2%}', textposition='auto',
                                                    textfont=dict(size=24))
    graf_fec_conjuntos_horizontal_ytd.update_layout(xaxis_title='', yaxis_title='', title_x=0.5, title_text='',
        yaxis=dict(tickfont=dict(size=10)),
        legend=dict(
        orientation="h",  # Define a orientação horizontal
        yanchor="bottom",  # Ancorar a legenda na parte inferior
        y=-0.05,           # Ajustar a posição vertical da legenda
        xanchor="center",  # Ancorar horizontalmente no centro
        x=0.5))
   



    col1, col2, col3 = st.columns(3)
    col1.subheader('Conjuntos DEC YTD')
    col3.subheader('Conjuntos FEC YTD')

    col1, col2 = st.columns(2)

    col1.plotly_chart(graf_dec_conjuntos_horizontal_ytd)
    col2.plotly_chart(graf_fec_conjuntos_horizontal_ytd)


    st.write('---')


    col1, col2, col3 = st.columns(3)
    col1.subheader('Conjuntos DEC LTM')
    col3.subheader('Conjuntos FEC LTM')

    col1, col2 = st.columns(2)

    col1.plotly_chart(graf_dec_conjuntos_horizontal_tam)
    col2.plotly_chart(graf_fec_conjuntos_horizontal_tam)



        # rodapé 
    st.markdown(
        '''
            <hr style='border: 1px solid #d3d3d3;'/>
            <p style='text-align: center; color: gray;'>
                Análise DEC-FEC Enel Rio | Dados fornecidos por OyM Rio | Desenvolvido por João Henrique Pires | © 2024
            </p>
        ''',
        unsafe_allow_html=True
    )