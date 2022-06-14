import dash
import dash_bootstrap_components as dbc
import psycopg2
import logging
from logging.handlers import TimedRotatingFileHandler

# define file handler and set formatter
file_handler = logging.FileHandler('logDadosENEM.log')
formatter    = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s')
handler = TimedRotatingFileHandler('logDadosENEM.log', when="midnight", interval=1)
handler.suffix = "%Y%m%d"
handler.setFormatter(formatter)
#file_handler.setFormatter(formatter)





# meta_tags are required for the app layout to be mobile responsive
app = dash.Dash(__name__, suppress_callback_exceptions=True,
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}],
                external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP]
                )
app.title = 'DadosENEM'
server = app.server

logFlask = logging.getLogger('werkzeug')
logFlask.setLevel(logging.DEBUG)
logFlask.addHandler(handler)

log = logging.getLogger(__name__)  
log.setLevel(logging.DEBUG)
log.addHandler(handler)


#Parametros do banco de dados
db_host='127.0.0.1'
db_database='enem'
db_usuario='enem'
db_senha='fsa2Lkd#jfklsd5jM'

con_banco = psycopg2.connect(host=db_host, database=db_database, user=db_usuario, password=db_senha)
