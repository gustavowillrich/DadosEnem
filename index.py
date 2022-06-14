from urllib import response
from dash import dcc
import dash_bootstrap_components as dbc
from dash import html
from dash.dependencies import Input, Output
from flask import request


# Connect to main app.py file
from app import app
from app import server
from app import log

# Connect to your app pages
from apps import comparativos, enem, sobre

header = dbc.Card(dbc.Row([
            dbc.Col([
                    #dcc.Location(id='url2', refresh=False),
                    html.Img(src='/assets/logo.png', style={"margin-left": "2rem", "margin-top": "2rem", "width": "200px", "height": "auto"}),
                ]),
            dbc.Col(dbc.Nav([
                    dbc.NavItem(dbc.NavLink("ENEM", active="exact", href="/")),
                    dbc.NavItem(dbc.NavLink("Comparativos", active="exact", href="/apps/comparativos")),
                    dbc.NavItem(dbc.NavLink("Sobre", active="exact", href="/apps/sobre")),
                    #dcc.Link(dbc.Button("ENEM",size="lg", color="primary", className="mr-1"), href="/apps/enem"),
                    #dcc.Link(dbc.Button("Comparativos",size="lg", color="primary", className="mr-1"), href="/apps/comparativos"),
                    #dcc.Link(dbc.Button("Sobre",size="lg", color="primary", className="mr-1"), href="/apps/sobre"),
                    ],
                    fill=True,pills=True, style={"position":"absolute","bottom":"0px", "right":"0px"}),
                       
                    
            )
        ]),style={"height":"150px", "margin-left": "3rem", "margin-right": "2rem", "margin-bottom": "0rem", "border": "none"})

            

content = html.Div(id='page-content', style={"margin-left": "3rem", "margin-right": "2rem"})

app.layout = html.Div([dcc.Location(id="url"), header, html.Hr(), content])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    print(pathname)
    log.info('Requisicao: ' + str(request.__dict__))
    if pathname == '/':
        return enem.layout
    if pathname == '/apps/comparativos':
        return comparativos.layout
    if pathname == '/apps/sobre':
        return sobre.layout
    else:
        return "Pagina não encontrada!"

@app.callback(Output('target', 'children'), [Input('input', 'value')])
def get_ip(value):
    print(value)
    return html.Div(request.remote_addr)

if __name__ == '__main__':
    app.run_server(debug=False, host='0.0.0.0',port=443, ssl_context=('fullchain1.pem', 'privkey1.pem'))
