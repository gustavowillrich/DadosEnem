import json
from urllib.request import urlopen
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from  funcoes.graficos import Escopo, Grafico
from app import app
from app import con_banco

mapa_presenca = Grafico()
df_presenca_estado_total = ''

df_presenca = pd.read_sql_query("select * from view_numero_participantes_nacional", con_banco)
df_presenca_presentes = df_presenca.query('situacao == "presente"')
df_presenca_ausentes = df_presenca.query('situacao == "ausente" | situacao == "nulo"').groupby(["nu_ano"]).sum().reset_index()
df_presenca_parciais = df_presenca.query('situacao == "parcial"').groupby(["nu_ano"]).sum().reset_index()
df_presenca_eliminados = df_presenca.query('situacao == "eliminado"').groupby(["nu_ano"]).sum().reset_index()


total_participantes = df_presenca.groupby(["nu_ano"])["num_participantes"].sum().reset_index()


#data_microrregiao = pd.read_sql_query("select * from view_media_nota_microrregiao_ano", con_banco)
#filtered_microrregiao = data_microrregiao
#df_nota = data

#df_presenca_estado = pd.read_sql_query("select * from view_numero_participantes_estado", con_banco)
#mapa_participantes = geraMapa('', df_presenca_estado, "med_idade", "med_geral", 'num_participantes', None, 'num_participantes', 'Media geral','')

df = df_presenca_presentes
df = df.sort_values(by="nu_ano")
fig = px.line(df, x='nu_ano', y='num_participantes', color='situacao')

figNumeroParticipantesSituacao = go.Figure()
figNumeroParticipantesSituacao.add_trace(go.Scatter(x=df['nu_ano'], y=df['num_participantes'], name="Presentes", line_shape='spline'))

df = df_presenca_ausentes
figNumeroParticipantesSituacao.add_trace(go.Scatter(x=df['nu_ano'], y=df['num_participantes'], name="Ausentes", line_shape='spline'))

df = df_presenca_eliminados
figNumeroParticipantesSituacao.add_trace(go.Scatter(x=df['nu_ano'], y=df['num_participantes'], name="Eliminados", line_shape='spline'))

df = df_presenca_parciais
figNumeroParticipantesSituacao.add_trace(go.Scatter(x=df['nu_ano'], y=df['num_participantes'], name="Apenas 1 dia", line_shape='spline'))

figNumeroParticipantesSituacao.update_layout(title='Número de participantes por situação',
                   xaxis_title='Ano',
                   yaxis_title='Número de participantes',
                   xaxis=dict(tickformat='d'))

'''fig.add_trace(go.Scatter(x=x, y=y + 5, name="spline",
                    text=["tweak line smoothness<br>with 'smoothing' in line object"],
                    hoverinfo='text+name',
                    line_shape='spline'))


fig.update_traces(hoverinfo='text+name', mode='lines+markers')
fig.update_layout(legend=dict(y=0.5, traceorder='reversed', font_size=16))'''


df2 = total_participantes
#print('=====df2====')
#print(df2.reset_index()['nu_ano'])
#figNumeroParticipantes = px.line(df2.reset_index(), x='nu_ano', y="num_participantes", title='Número de participantes')

figNumeroParticipantes = go.Figure()
figNumeroParticipantes.add_trace(go.Scatter(x=df2['nu_ano'], y=df2['num_participantes'], name="Total", line_shape='spline'))
figNumeroParticipantes.update_layout(title='Número de participantes',
                   xaxis_title='Ano',
                   yaxis_title='Número de participantes',
                   xaxis=dict(tickformat='d'))



df_nota_media = pd.read_sql_query("""SELECT nu_ano, 
	   AVG(med_nota_cn) AS med_nota_cn,
	   AVG(med_nota_ch) AS med_nota_ch,
	   AVG(med_nota_lc) AS med_nota_lc,
	   AVG(med_nota_mt) AS med_nota_mt,
	   AVG(med_nota_redacao) AS med_nota_redacao
  FROM view_media_nota_estado_ano
GROUP BY nu_ano""", con_banco)
df_nota_media = df_nota_media.sort_values(by="nu_ano")
#media_nacional_geral = df_nota_media.mean(axis=0)

#media_nacional_geral = [df_nota_media['nu_ano'], ((df_nota_media['med_nota_cn'] + df_nota_media['med_nota_ch'] + df_nota_media['med_nota_lc'] + df_nota_media['med_nota_mt'] + df_nota_media['med_nota_redacao']) /5)]
df_nota_media['media_geral']= df_nota_media.iloc[:, -5:].mean(axis=1)

#print(df_nota_media) # ====Validar se esta faendo certo====
#print('PaginaENEM') 

figNotaMedia = go.Figure()
figNotaMedia.add_trace(go.Scatter(x=df_nota_media['nu_ano'], y=df_nota_media['med_nota_cn'], name="Ciências da Natureza", line_shape='spline'))
figNotaMedia.add_trace(go.Scatter(x=df_nota_media['nu_ano'], y=df_nota_media['med_nota_ch'], name="Ciências Humanas", line_shape='spline'))
figNotaMedia.add_trace(go.Scatter(x=df_nota_media['nu_ano'], y=df_nota_media['med_nota_lc'], name="Linguagens e Códigos", line_shape='spline'))
figNotaMedia.add_trace(go.Scatter(x=df_nota_media['nu_ano'], y=df_nota_media['med_nota_mt'], name="Matemática", line_shape='spline'))
figNotaMedia.add_trace(go.Scatter(x=df_nota_media['nu_ano'], y=df_nota_media['med_nota_redacao'], name="Redação", line_shape='spline'))
figNotaMedia.update_layout(title='Nota media nacional por area de conhecimento',
                   xaxis_title='Ano',
                   yaxis_title='Nota',
                   xaxis=dict(tickformat='d'))

figNotaMediaGeral = go.Figure()
figNotaMediaGeral.add_trace(go.Scatter(x=df_nota_media['nu_ano'], y=df_nota_media['media_geral'], name="Geral", line_shape='spline'))
figNotaMediaGeral.update_layout(title='Nota media nacional',
                   xaxis_title='Ano',
                   yaxis_title='Nota',
                   xaxis=dict(tickformat='d'))

###################################
#
#  Layout HTML
#

layout = html.Div([
    html.Div(
    className="text-muted",
    children=[
    html.H2('Evolução do ENEM', style={"textAlign": "center"}),
    ]),

    html.Div(className="container-fluid", children=[  
        #Linha 1                                            
        html.Div(className="row", children=[
            #Coluna 1
            html.Div(className="col-sm-6", children=[
                html.Div(className="card", children=[
                    html.Div(className="card-body", children=[
                        dcc.Graph(id = "grafico_cn", 
                                figure = figNumeroParticipantes, 
                                config = {"displayModeBar": False}
                                ),
                    ]),
                ]),
            ]),
                     
            #Coluna 2       
            html.Div(className="col-sm-6", children=[
                html.Div(className="card", children=[
                    html.Div(className="card-body", children=[
                        dcc.Graph(id = "grafico_ch123", 
                                  figure = figNumeroParticipantesSituacao
                                 ),
                    ]),
                ]),
            ]),                      
        ]),
        
        #Linha 2                                                  
        html.Div(className="row", children=[
            #Coluna 1
            html.Div(className="col-sm-6", children=[
                html.Div(className="card", children=[
                    html.Div(className="card-body", children=[
                        dcc.Graph(id = "grafico_mt", 
                                  figure = figNotaMediaGeral, 
                                  config = {"displayModeBar": False}
                                 ),
                    ]),
                ]),
            ]),
                     
            #Coluna 2       
            html.Div(className="col-sm-6", children=[
                html.Div(className="card", children=[
                    html.Div(className="card-body", children=[
                        dcc.Graph(id = "grafico_lc", 
                                  figure = figNotaMedia
                                 ),
                    ]),
                ]),
            ]),                      
        ]),
        
        #Linha 3
        html.Div(className="row", children=[
            #Coluna 1
            html.Div(className="card", children=[
                dcc.Loading(id = "ls-loading-4", children=[html.Div([html.Div(id="ls-loading-output-4")])], type="circle"),
                html.Div(id='titulo_mapa', className="card-title", children=['Mapa']),
                html.Div(className="card-body", children=[
                    
                    html.Div(className="container-fluid", children=[
                        html.Div(className="row", children=[
                            html.Div(className="col-xs-6 col-md-6", children=[
                                dcc.Graph(id = "mapa", 
                                        #figure = grafico_mapa, 
                                        config = {"displayModeBar": False}
                                        ),
                                
                            ]),
                        
                  
                            
                            #Coluna 2       
                            html.Div(className="col-xs-6 col-md-6", children=[
                                #html.Div(className="card", children=[
                                    #html.Div(className="card-body", children=[
                                        dcc.Graph(id = "grafico_barras", 
                                                #figure = grafico_barras_mapa
                                                ),
                                    #]),
                                #]),
                            ]),
                        ]),
                        html.Div(className="row", children=([
                            dcc.Slider(id = 'slider-anoaaa',
                                    min=df.nu_ano.min(),
                                    max=df.nu_ano.max(),
                                    step=None,
                                    marks={g: str(g) for g in df['nu_ano']},
                                    value=2020,
                                    updatemode='drag',
                                    included=False
                            )
                        ])),
                    ]),
                ]),  
            ]),                    
        ]), 

    ]),
])


@app.callback(
    [   
        Output("mapa", "figure"),
        Output("grafico_barras", "figure"),
        Output("titulo_mapa", "children"),
        Output("ls-loading-output-4", "children")
    ],
    [
        Input("slider-anoaaa", "value"),  
    ],
)
def update_charts(ano):
    global mapa_presenca, df_presenca_estado_total
    ###################################
    #
    #  Mapa nacional
    #
    #Total Participantes
    """if type(df_presenca_estado_total) == str:
        df_presenca_estado_total = pd.read_sql_query("select *,(select distinct(sigla_uf) from regioes where codigo_uf = part.codigo_uf) as sigla_uf from view_numero_participantes_estado part where situacao = 'presente'", con_banco)
    df_presenca_estado = df_presenca_estado_total[(df_presenca_estado_total.nu_ano.isin([ano]))]
    
    #df_presenca_estado = pd.read_sql_query("select * from view_numero_participantes_estado where situacao = 'presente' and nu_ano = " + str(ano), con_banco)
    grafico_mapa = mapa_presenca.mapa(Escopo.Estado, '', df_presenca_estado, 'num_participantes', 'Participantes', '',hover_name = 'nome_uf', locations = 'codigo_uf',  tipoMapa='white-bg')
    grafico_barras_mapa = mapa_presenca.barras(Escopo.Estado, '', df_presenca_estado, 'num_participantes', 'Participantes', '',hover_name = 'nome_uf',legenda_x='sigla_uf', locations = 'codigo_uf',  tipoMapa='white-bg')
    """
    
    #Media nota
    if type(df_presenca_estado_total) == str:
        df_presenca_estado_total = pd.read_sql_query("select * from view_media_nota_estado_ano", con_banco)
    df_presenca_estado = df_presenca_estado_total[(df_presenca_estado_total.nu_ano.isin([ano]))]
    
    grafico_mapa = mapa_presenca.mapa(Escopo.Estado, '', df_presenca_estado, 'med_geral', 'Nota Media', '',hover_name = 'nome_uf', locations = 'co_uf_prova',  tipoMapa='white-bg')
    grafico_barras_mapa = mapa_presenca.barras(Escopo.Estado, '', df_presenca_estado, 'med_geral', 'Nota Media', '',hover_name = 'nome_uf',legenda_x='sigla_uf', locations = 'co_uf_prova',  tipoMapa='white-bg')

    return grafico_mapa, grafico_barras_mapa, 'Nota média por UF em ' + str(ano), ''