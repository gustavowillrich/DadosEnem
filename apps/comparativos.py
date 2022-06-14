from pydoc import classname
from dash import dcc
import dash_bootstrap_components as dbc
from dash import html
import pandas as pd
import numpy as np
from dash.dependencies import Output, Input
from pkg_resources import add_activation_listener
import plotly.express as px
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd
from app import app
from app import con_banco
from app import log
import plotly.graph_objects as go
from dash import dash_table
from flask import request
from dash.exceptions import PreventUpdate

con = con_banco
cur = con.cursor()

def consultaBanco(escopo, locais, periodo, comparacao):
    view = 'view_media_nota_estado_ano'
    log.info(escopo)
    if escopo == 'estado':
        if comparacao == 'nota':
            view = 'view_media_nota_estado_ano'
        elif comparacao == 'genero':
            view = 'view_media_nota_estado_sexo'
        elif comparacao == 'etnia':
            view = 'view_media_nota_estado_etnia'
        elif comparacao == 'renda':
            view = 'view_media_nota_estado_renda'
        elif comparacao == 'tipo_escola':
            view = 'view_media_nota_estado_ano'
    elif escopo == 'microrregiao':
        if comparacao == 'nota':
            view = 'view_media_nota_microrregiao_ano'
        elif comparacao == 'genero':
            view = 'view_media_nota_microrregiao_sexo'
        elif comparacao == 'etnia':
            view = 'view_media_nota_microrregiao_raca'
        elif comparacao == 'renda':
            view = 'view_media_nota_microrregiao_renda'
        elif comparacao == 'tipo_escola':
            view = 'view_media_nota_microrregiao_ano'
    elif escopo == 'municipio':
        if comparacao == 'nota':
            view = 'view_media_nota_municipio_ano'
        elif comparacao == 'genero':
            view = 'view_media_nota_municipio_sexo'
        elif comparacao == 'etnia':
            view = 'view_media_nota_municipio_raca'
        elif comparacao == 'renda':
            view = 'view_media_nota_municipio_renda'
        elif comparacao == 'tipo_escola':
            view = 'view_media_nota_municipio_ano'
    elif escopo == 'regiao':
        if comparacao == 'nota':
            view = 'view_media_nota_regiao_ano'
        elif comparacao == 'genero':
            view = 'view_media_nota_regiao_sexo'
        elif comparacao == 'etnia':
            view = 'view_media_nota_regiao_raca'
        elif comparacao == 'renda':
            view = 'view_media_nota_regiao_renda'
        elif comparacao == 'tipo_escola':
            view = 'view_media_nota_regiao_ano'
    elif escopo == 'escola':
        if comparacao == 'nota':
            view = 'view_media_nota_escola_ano'
        elif comparacao == 'genero':
            view = 'view_media_nota_escola_sexo'
        elif comparacao == 'etnia':
            view = 'view_media_nota_escola_raca'
        elif comparacao == 'renda':
            view = 'view_media_nota_escola_renda'
        elif comparacao == 'tipo_escola':
            view = 'view_media_nota_escola_ano'


    return pd.read_sql_query("select * from " + view, con)  

data = consultaBanco('','','','')
log.info('zerou')

df_nota = data
df_regiao = data

escopo = dbc.Col([  # first column on second row
            html.H6("Escopo", className='text-center'),
            dbc.Card([
                dbc.CardBody([
                    dbc.RadioItems(
                        id="rdEscopo",
                        options=[
                            {"label": "Escola", "value": 'escola'},
                            {"label": "Município", "value": 'municipio'},
                            {"label": "Região", "value": 'regiao'},
                            {"label": "Microrregião", "value": 'microrregiao'},
                            {"label": "Estado", "value": 'estado'},
                        ],
                        value="estado"
                    ),
                    dcc.Loading(
                            id="ls-loading-output-2",
                            type="circle",
                    ),
                ])
            ], style={"height":"200px"})
    ])

regiao = dbc.Col([
        html.H6('Regiao', className='text-center'),
        dbc.Card([
            dbc.CardBody([
                dcc.Dropdown(
                    id="filtro-regiao",
                    #options=[
                    #    {"label": regiao, "value": regiao}
                    #    for regiao in np.sort(data.sigla_uf.unique())
                    #],
                    #value=['RS'],
                    clearable=False,
                    className="dropdown",
                    multi=True,
                ),
                html.Br(),
                dcc.Loading(
                    id="ls-loading-3",
                    children=[html.Div([html.Div(id="ls-loading-output-3")])],
                    type="circle",
                )
            ])
        ], style={"height":"200px"})
    ])

referencia = dbc.Col([
        html.H6('Referencia', className='text-center'),
        dbc.Card([
            dbc.CardBody([
                dbc.RadioItems(
                                id="rdfrmReferencia",
                                options=[
                                    {"label": "Nota", "value": 'nota'},
                                    {"label": "Gênero", "value": 'genero'},
                                    {"label": "Etnia", "value": 'etnia'},
                                    {"label": "Renda", "value": 'renda'},
                                ],
                                value='nota',
                            ),
            ], style={"height":"200px"})
        ])
    ], width={'offset': 0, 'order': 3})

filtro = dbc.Card([
            dbc.CardHeader(html.H5('Filtros', className='text-center')),
            dbc.CardBody([
                dbc.Row([escopo, regiao, referencia]),
            ]),
            dcc.Slider(
                id='slider-ano',
                min=data.nu_ano.min(),
                max=data.nu_ano.max(),
                step=None,
                
                marks={g: str(g) for g in data['nu_ano']},
                value=2019,
                updatemode='drag',
                included=False
            )
    ], className="border-dark")


graficoGeral = dbc.Col([
        html.H6('Média geral', className='text-center', style={'marginTop': '1em'}),
        dbc.Card([
            dbc.CardBody([
                dcc.Graph(id="grafico_geral", style={'vertical-align': 'middle'}),
            ])
        ]),
    ])

graficoCN = dbc.Col([
        html.H6('Ciências da natureza', className='text-center', style={'marginTop': '1em'}),
        dbc.Card([
            dbc.CardBody([
                dcc.Graph(id="grafico_cn", config={"displayModeBar": False},)
            ])
        ]),
    ], className="col-sm-6")

graficoCH = dbc.Col([
        html.H6('Ciências humanas', className='text-center', style={'marginTop': '1em'}),
        dbc.Card([
            dbc.CardBody([
                dcc.Graph(id="grafico_ch", config={"displayModeBar": False},)
            ])
        ]),
    ], className="col-sm-6")

graficoMT = dbc.Col([
        html.H6('Matemática', className='text-center', style={'marginTop': '1em'}),
        dbc.Card([
            dbc.CardBody([
                dcc.Graph(id="grafico_mt", config={"displayModeBar": False}, style={'vertical-align': 'middle'}),
            ])
        ]),
    ], className="col-sm-6")

graficoLC = dbc.Col([
        html.H6('Linguagens e códigos', className='text-center', style={'marginTop': '1em'}),
        dbc.Card([
            dbc.CardBody([
                dcc.Graph(id="grafico_lc", config={"displayModeBar": False}, style={'vertical-align': 'middle'}),
            ])
        ]),
    ], className="col-sm-6")

graficoRedacao = dbc.Col([
        html.H6('Redação', className='text-center', style={'marginTop': '1em'}),
        dbc.Card([
            dbc.CardBody([
                dcc.Graph(id="grafico_redacao", config={"displayModeBar": False},style={'vertical-align': 'middle'}),
            ])
        ],style={"margin": "0 auto", "width":"50%"}, ),
    ], )

graficos = dbc.Card([
            #dbc.CardHeader(html.H5('Filtros', className='text-center')),
            dbc.CardBody([
                dbc.Row(graficoGeral),
                dbc.Row([graficoCN, graficoCH]),
                dbc.Row([graficoMT, graficoLC]),
                dbc.Row(graficoRedacao),
            ]),
    ], className="border-dark")

titulo = html.Div(html.H2('Comparativos', style={"textAlign": "center"}), className="text-muted")

layout = dbc.Row([titulo, filtro], style={'marginBottom': '1em'}), dbc.Row(graficos)


#Seleção do escopo
@app.callback(
    [Output('filtro-regiao', 'options'),Output('filtro-regiao', 'value'),Output("ls-loading-output-2", "children")],
    [Input('rdEscopo', 'value')]
)
def definicao_escopo(value):
    
    df_regiao = []
    valor_padrao = []
    if value == 'estado':
        retornoSQL = pd.read_sql_query("select distinct(sigla_uf) as uf, nome_uf from regioes", con)
        opcoes = [{"label": row['nome_uf'], "value": row['uf']} for index, row in retornoSQL.iterrows()]
        valor_padrao = ['RS']
     

    elif value == 'microrregiao':
        retornoSQL = pd.read_sql_query("select distinct(codigo_microrregiao) as codigo_microrregiao, nome_microrregiao, sigla_uf from regioes order by sigla_uf, nome_microrregiao desc", con)
        #retornoSQL = retornoSQL.sort_values(by=['nome_microrregiao'],ascending=False)
        opcoes= [{"label": row['nome_microrregiao'] + ' - ' + row['sigla_uf'], "value": row['codigo_microrregiao']} for index, row in retornoSQL.iterrows()]
        valor_padrao = [43026]
    
    elif value == 'escola':
        retornoSQL = pd.read_sql_query("select distinct(co_escola)as codigo_escola, nome_escola, nome_municipio_uf from view_media_nota_escola_ano order by nome_escola desc", con)
        #retornoSQL = retornoSQL.sort_values(by=['nome_microrregiao'],ascending=False)
        opcoes= [{"label": row['nome_escola'] + ' - ' + row['nome_municipio_uf'], "value": row['codigo_escola']} for index, row in retornoSQL.iterrows()]
        valor_padrao = [43033474]

    elif value == 'municipio':
        retornoSQL = pd.read_sql_query("select distinct(codigo_municipio) as codigo_municipio, nome_municipio, sigla_uf from regioes order by sigla_uf, nome_municipio desc", con)
        #retornoSQL = retornoSQL.sort_values(by=['nome_microrregiao'],ascending=False)
        opcoes= [{"label": row['nome_municipio'] + ' - ' + row['sigla_uf'], "value": row['codigo_municipio']} for index, row in retornoSQL.iterrows()]
        valor_padrao = [4303905]
     
    elif value == 'regiao':
        retornoSQL = pd.read_sql_query("select distinct(nome_regiao) as nome_regiao from regioes order by nome_regiao desc", con)
        #retornoSQL = retornoSQL.sort_values(by=['nome_microrregiao'],ascending=False)
        opcoes= [{"label": row['nome_regiao'], "value": row['nome_regiao']} for index, row in retornoSQL.iterrows()]
        valor_padrao = ['Sul']

    else:
        opcoes = []
          
    return opcoes, valor_padrao, ''

def geraGrafico(tipoGrafico, df, x, y, cor, corBorda, tamanho, titulo, hover="sigla_uf"):
    grafico = px.scatter()

    if tipoGrafico == 'bolha':
        grafico = px.scatter(df, 
                             x=x, 
                             y=y, 
                             color=cor,
                             size=pd.cut(df[tamanho], bins = [0, 10000, 100000, 150000, 200000, 1000000, ], labels = [10, 20, 30, 40, 50]),
                             #hover_name=hover, 
                             symbol=corBorda, 
                             
                             symbol_sequence = ['circle', 'x', 'square', 'cross', 'diamond', 'triangle-up', 'triangle-down', 'triangle-left', 'triangle-right', 'triangle-ne', 'triangle-se', 'triangle-sw', 'triangle-nw', 'star', 'hexagram', 'star-triangle-up', 'star-triangle-down', 'star-square', 'star-diamond', 'diamond-tall', 'diamond-wide', 'hourglass', 'bowtie', 'circle-cross', 'circle-x', 'square-cross', 'square-x', 'diamond-cross', 'diamond-x', 'cross-thin', 'x-thin', 'asterisk', 'hash', 'y-up', 'y-down', 'y-left', 'y-right', 'line-ew', 'line-ns', 'line-ne', 'line-nw', 'arrow-up', 'arrow-down', 'arrow-left', 'arrow-right', 'arrow-bar-up', 'arrow-bar-down', 'arrow-bar-left', 'arrow-bar-right'], 
                             #hover_data={x:False,
                             #            y:':.2f',
                             #            tamanho:True,
                             #            marker_size:False,
                             #            cor:False},
                             custom_data=['num_participantes', hover],
                             labels={"nome_uf": "Estado", "sigla_uf": "Estado", "nome_microrregiao_uf":"Microrregião", "med_geral":"Nota média", "med_nota_cn":"Nota média", "med_nota_ch":"Nota média", "med_nota_mt":"Nota média", "med_nota_lc":"Nota média", "med_nota_redacao":"Nota média", "nome_escola":"Escola", "nome_municipio_uf":"Município", "nome_regiao":"Região", "tp_sexo":"Gênero", "med_idade":"Idade média", "tp_cor_raca":"Etnia", "qs_renda_familia":"Renda"})
        grafico.update_traces(hovertemplate='<b>%{customdata[1]}</b> <br><br>Idade média: %{x} <br>Nota média: %{y} <br>Num. Participantes: %{customdata[0]}')

        if titulo != "":
            grafico.update_layout(title=titulo)
            grafico.update_layout(title={'y':0.9,'x':0.5,'xanchor': 'center','yanchor': 'top'})

        #Deixa a escala facilitar ver as mudanças ao trocar de ano  
        grafico.update_xaxes(range=[16, 25])
        grafico.update_yaxes(range=[300, 800])

    elif tipoGrafico == 'barra':
        grafico = px.bar(df, x=x, y=y, color=cor, text=y)
        grafico.update_layout(barmode='group')
        grafico.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    return grafico


@app.callback(
    [   Output("grafico_geral", "figure"),
        Output("grafico_cn", "figure"), 
        Output("grafico_ch", "figure"), 
        Output("grafico_mt", "figure"), 
        Output("grafico_lc", "figure"),
        Output("grafico_redacao", "figure"),
        Output("ls-loading-output-3", "children")
    ],
    [
        Input("filtro-regiao", "value"),
        Input("slider-ano", "value"),
        Input('rdfrmReferencia', 'value'),
        Input('rdEscopo', 'value')
        
    ],
)
def update_charts(regiao, ano, referencia, escopo):
    log.info('Requisicao(Comparativos - update_charts): ' + str(request.__dict__))

    if len(regiao) == 0:
        raise PreventUpdate
    
    if regiao == []:
        grafico_nota_geral = px.scatter()
        grafico_nota_cn = px.scatter()
        grafico_nota_ch = px.scatter()
        grafico_nota_lc = px.scatter()
        grafico_nota_mt = px.scatter()
        grafico_nota_redacao = px.scatter()

        return grafico_nota_geral, grafico_nota_cn, grafico_nota_ch, grafico_nota_mt, grafico_nota_lc, grafico_nota_redacao
    
    tipoGrafico = 'bolha'
    
    hover = 'sigla_uf'
    #filtered_microrregiao = data_microrregiao[(data_microrregiao.sigla_uf.isin(microrregiaoUF))]
    log.info(referencia)
    df_nota = consultaBanco(escopo,'','',referencia)
    log.info(df_nota)
    log.info(escopo)
    if escopo == 'regiao':
        print(df_nota)
        filtered_data = df_nota[(df_nota.nome_regiao.isin(regiao))]
        print(df_nota)
        cor = "nome_regiao"
        hover='nome_regiao'
    elif escopo == 'municipio':
        filtered_data = df_nota[(df_nota.codigo_municipio.isin(regiao))]
        cor = "nome_municipio_uf"
        hover = 'nome_municipio_uf'
    elif escopo == 'escola':
        filtered_data = df_nota[(df_nota.co_escola.isin(regiao))]
        cor = "nome_escola"
        hover = 'nome_escola'
    elif escopo == 'microrregiao':
        filtered_data = df_nota[(df_nota.codigo_microrregiao.isin(regiao))]
        cor = "nome_microrregiao_uf"
        hover = 'nome_microrregiao_uf'
    else:
        filtered_data = df_nota[(df_nota.sigla_uf.isin(regiao))]
        cor = "nome_uf"
        hover = 'nome_uf'
        
    filtered_data = filtered_data[(df_nota.nu_ano.isin([ano]))]

    if referencia == 'nota':
        grafico_nota_geral = geraGrafico(tipoGrafico, filtered_data, "med_idade", "med_geral", cor, None, 'num_participantes', '',hover)
        grafico_nota_cn = geraGrafico(tipoGrafico, filtered_data, "med_idade", "med_nota_cn", cor, None, 'num_participantes', '',hover)
        grafico_nota_ch = geraGrafico(tipoGrafico, filtered_data, "med_idade", "med_nota_ch", cor, None, 'num_participantes', '',hover)
        grafico_nota_lc = geraGrafico(tipoGrafico, filtered_data, "med_idade", "med_nota_lc", cor, None, 'num_participantes', '',hover)
        grafico_nota_mt = geraGrafico(tipoGrafico, filtered_data, "med_idade", "med_nota_mt", cor, None, 'num_participantes', '',hover)
        grafico_nota_redacao = geraGrafico(tipoGrafico, filtered_data, "med_idade", "med_nota_redacao", cor, None, 'num_participantes', '',hover)
        #grafico_nota_geral.update_layout(hover_name="nome_uf")
    
    elif referencia == 'genero':
        titulo = 'Teste Genero'
        filtered_data = filtered_data.sort_values(by=['med_geral'],ascending=False)
        if escopo == 'regiao':
            if tipoGrafico == 'bolha':
                eixo_x = 'med_idade'
                grupo = "tp_sexo"
                hover='nome_regiao'
            else:
                eixo_x = 'nome_regiao'
                grupo = 'nome_regiao'
        elif escopo == 'municipio':
            if tipoGrafico == 'bolha':
                eixo_x = 'med_idade'
                grupo = "tp_sexo"
                hover = 'nome_municipio_uf'
            else:
                eixo_x = 'nome_municipio_uf'
                grupo = 'nome_municipio_uf'
        elif escopo == 'escola':
            if tipoGrafico == 'bolha':
                eixo_x = 'med_idade'
                grupo = "tp_sexo"
                hover = 'nome_escola'
            else:
                eixo_x = 'nome_escola'
                grupo = 'nome_escola'
        elif escopo == 'microrregiao':
            if tipoGrafico == 'bolha':
                eixo_x = 'med_idade'
                grupo = "tp_sexo"
                hover = 'nome_microrregiao_uf'
            else:
                eixo_x = 'nome_microrregiao_uf'
                grupo = 'nome_microrregiao_uf'
        else:
            if tipoGrafico == 'bolha':
                eixo_x = 'med_idade'
                grupo = "tp_sexo"
                hover = 'sigla_uf'
            else:
                eixo_x = 'sigla_uf'
                grupo = 'nome_uf'
        di = {'M': "Masculino", 'F': "Feminino"}
        filtered_data = filtered_data.replace({"tp_sexo": di})

        grafico_nota_geral = geraGrafico(tipoGrafico, filtered_data, eixo_x, "med_geral", hover, grupo, 'num_participantes', '', hover)
        grafico_nota_cn = geraGrafico(tipoGrafico, filtered_data, eixo_x, "med_nota_cn", hover, grupo, 'num_participantes', '', hover)
        grafico_nota_ch = geraGrafico(tipoGrafico, filtered_data, eixo_x, "med_nota_ch", hover, grupo, 'num_participantes', '', hover)
        grafico_nota_lc = geraGrafico(tipoGrafico, filtered_data, eixo_x, "med_nota_lc", hover, grupo, 'num_participantes', '', hover)
        grafico_nota_mt = geraGrafico(tipoGrafico, filtered_data, eixo_x, "med_nota_mt", hover, grupo, 'num_participantes', '', hover)
        grafico_nota_redacao = geraGrafico(tipoGrafico, filtered_data, eixo_x, "med_nota_redacao", hover, grupo, 'num_participantes', '', hover)
             
    elif referencia == 'etnia':
        filtered_data = filtered_data.sort_values(by=['med_geral'],ascending=False)
        if escopo == 'regiao':
            if tipoGrafico == 'bolha':
                eixo_x = 'med_idade'
                grupo = "tp_cor_raca"
                hover='nome_regiao'
            else:
                eixo_x = 'nome_regiao'
                grupo = 'nome_regiao'
        elif escopo == 'municipio':
            if tipoGrafico == 'bolha':
                eixo_x = 'med_idade'
                grupo = "tp_cor_raca"
                hover = 'nome_municipio_uf'
            else:
                eixo_x = 'nome_municipio_uf'
                grupo = 'nome_municipio_uf'
        elif escopo == 'microrregiao':
            if tipoGrafico == 'bolha':
                eixo_x = 'med_idade'
                grupo = "tp_cor_raca"
                hover = 'nome_microrregiao_uf'
            else:
                eixo_x = 'nome_microrregiao_uf'
                grupo = 'nome_microrregiao_uf'
        elif escopo == 'escola':
            if tipoGrafico == 'bolha':
                eixo_x = 'med_idade'
                grupo = "tp_cor_raca"
                hover = 'nome_escola'
            else:
                eixo_x = 'nome_escola'
                grupo = 'nome_escola'
        else:
            if tipoGrafico == 'bolha':
                eixo_x = 'med_idade'
                grupo = "tp_cor_raca"
                hover = 'sigla_uf'
            else:
                eixo_x = 'sigla_uf'
                grupo = 'nome_uf'
    
        di = {0: "Nao Declarado", 1: "Branco", 2: "Preta", 3: "Parda", 4: "Amarela", 5: "Indigena", 6: "Sem informacao"}
        filtered_data = filtered_data.replace({"tp_cor_raca": di})

        grafico_nota_geral = geraGrafico(tipoGrafico, filtered_data, eixo_x, "med_geral", hover, grupo, 'num_participantes', '', hover)
        grafico_nota_cn = geraGrafico(tipoGrafico, filtered_data, eixo_x, "med_nota_cn", hover, grupo, 'num_participantes', '', hover)
        grafico_nota_ch = geraGrafico(tipoGrafico, filtered_data, eixo_x, "med_nota_ch", hover, grupo, 'num_participantes', '', hover)
        grafico_nota_lc = geraGrafico(tipoGrafico, filtered_data, eixo_x, "med_nota_lc", hover, grupo, 'num_participantes', '', hover)
        grafico_nota_mt = geraGrafico(tipoGrafico, filtered_data, eixo_x, "med_nota_mt", hover, grupo, 'num_participantes', '', hover)
        grafico_nota_redacao = geraGrafico(tipoGrafico, filtered_data, eixo_x, "med_nota_redacao", hover, grupo, 'num_participantes', '', hover)

    elif referencia == 'renda':
        filtered_data = filtered_data.sort_values(by=['med_geral'],ascending=False)
        if escopo == 'regiao':
            if tipoGrafico == 'bolha':
                eixo_x = 'med_idade'
                grupo = "qs_renda_familia"
                hover='nome_regiao'
            else:
                eixo_x = 'nome_regiao'
                grupo = 'nome_regiao'
        elif escopo == 'municipio':
            if tipoGrafico == 'bolha':
                eixo_x = 'med_idade'
                grupo = "qs_renda_familia"
                hover = 'nome_municipio_uf'
            else:
                eixo_x = 'nome_municipio_uf'
                grupo = 'nome_municipio_uf'
        elif escopo == 'microrregiao':
            if tipoGrafico == 'bolha':
                eixo_x = 'med_idade'
                grupo = "qs_renda_familia"
                hover = 'nome_microrregiao_uf'
            else:
                eixo_x = 'nome_microrregiao_uf'
                grupo = 'nome_microrregiao_uf'
        elif escopo == 'escola':
            if tipoGrafico == 'bolha':
                eixo_x = 'med_idade'
                grupo = "qs_renda_familia"
                hover = 'nome_escola'
            else:
                eixo_x = 'nome_escola'
                grupo = 'nome_escola'
        else:
            if tipoGrafico == 'bolha':
                eixo_x = 'med_idade'
                grupo = "qs_renda_familia"
                hover = 'sigla_uf'
            else:
                eixo_x = 'sigla_uf'
                grupo = 'nome_uf'
        
        di = {'A': "Nenhuma renda", 'B': "Até 1 salário mínimo", 'C': "Até 1,5 salário mínimo", 'D': "Até 2 salários mínimos", 
        'E': "Até 2,5 salários mínimos", 'F': "Até 3 salários mínimos", 'G': "Até 4 salários mínimos", 'H': "Até 5 salários mínimos",
        'I': "Até 6 salários mínimos", 'J': "Até 7 salários mínimos", 'K': "Até 8 salários mínimos",'L': "Até 9 salários mínimos",
        'M': "Até 10 salários mínimos", 'N': "Até 12 salários mínimos", 'O': "Até 15 salários mínimos",'P': "Até 20 salários mínimos",
        'Q': "Mais de 20 salários mínimos"}
        filtered_data = filtered_data.replace({"qs_renda_familia": di})

        grafico_nota_geral = geraGrafico(tipoGrafico, filtered_data, eixo_x, "med_geral", hover, grupo, 'num_participantes', '', hover)
        grafico_nota_cn = geraGrafico(tipoGrafico, filtered_data, eixo_x, "med_nota_cn", hover, grupo, 'num_participantes', '', hover)
        grafico_nota_ch = geraGrafico(tipoGrafico, filtered_data, eixo_x, "med_nota_ch", hover, grupo, 'num_participantes', '', hover)
        grafico_nota_lc = geraGrafico(tipoGrafico, filtered_data, eixo_x, "med_nota_lc", hover, grupo, 'num_participantes', '', hover)
        grafico_nota_mt = geraGrafico(tipoGrafico, filtered_data, eixo_x, "med_nota_mt", hover, grupo, 'num_participantes', '', hover)
        grafico_nota_redacao = geraGrafico(tipoGrafico, filtered_data, eixo_x, "med_nota_redacao", hover, grupo, 'num_participantes', '', hover)
             

    elif referencia == 'tipo_escola':
        retorno = html.Div("tipo_escolaaaaa")

    

    return grafico_nota_geral, grafico_nota_cn, grafico_nota_ch, grafico_nota_mt, grafico_nota_lc, grafico_nota_redacao, ''

