import dash
from dash.dependencies import Input, Output, State
from dash import dcc
from dash import html
from app import app
import dash_table
import pandas as pd
import dash_bootstrap_components as dbc


layout = dbc.Container([
            html.Div(
            className="text-muted",
            children=[
            html.H2('DadosENEM', style={"textAlign": "center"}),
            ]),
    
    
    
    
html.P('Esta plataforma é resultado do trabalho de conclusão do curso de Ciência da Computaçao desenvolvido por Gustavo Willrich, e tem como objetivo facilitar a visualização dos resultados do ENEM apresentando as médias gerais e as notas por área de conhecimento dos inscritos no ENEM de 2013 a 2020. Tambem permite a comparação entre escolas, municípios, estados, entre outros.'),

html.P('O trabalho detalha a mudança na estrutura dos microdados ao longo dos anos e o processo adotado para importação desses microdados e o desenvolvimento da plataforma.'),

html.P('Todos os códigos-fonte da plataforma e os scritps utilizados na importação dos dados estão disponíveis no endereço: https://github.com/gustavowillrich/DadosEnem.')], fluid=True)