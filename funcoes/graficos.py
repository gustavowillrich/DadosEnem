
from enum import Enum
import enum
import json
from urllib.request import urlopen
import plotly.express as px

class Escopo(Enum):
    Nacional = 1
    Regiao = 2
    Estado = 3
    Microrregiao = 4
    Municipio = 5
    Escola = 6
    
class Grafico:
    centroMapaUF = {
                    'AC': [-8.77, -70.55],
                    'AL': [-9.62, -36.82],
                    'AM': [-3.47, -65.10],
                    'AP': [1.41, -51.77],
                    'BA': [-13.29, -41.71],
                    'CE': [-5.20, -39.53],
                    'DF': [-15.83, -47.86],
                    'ES': [-19.19, -40.34],
                    'GO': [-15.98, -49.86],
                    'MA': [-5.42, -45.44],
                    'MT': [-12.64, -55.42],
                    'MS': [-20.51, -54.54],
                    'MG': [-18.10, -44.38],
                    'PA': [-3.79, -52.48],
                    'PB': [-7.28, -36.72],
                    'PR': [-24.89, -51.55],
                    'PE': [-8.38, -37.86],
                    'PI': [-6.60, -42.28],
                    'RJ': [-22.25, -42.66],
                    'RN': [-5.81, -36.59],
                    'RO': [-10.83, -63.34],
                    'RS': [-30.17, -53.50],
                    'RR': [1.99, -61.33],
                    'SC': [-27.45, -50.95],
                    'SE': [-10.57, -37.45],
                    'SP': [-22.19, -48.79],
                    'TO': [-9.46, -48.26]
                } 

    def __init__(self):
       self.geojson   = ''


    def mapa(self, escopo, local, dataframe, cor, legenda, titulo, hover_name, locations, tipoMapa="open-street-map", animacao=False):           
        if escopo == Escopo.Nacional:
            centro={"lat": -29.9372173370, "lon": -51.2331220782}
            zoom=4
            
        elif escopo == Escopo.Estado:
            centro = {"lat": -15.48, "lon": -54.00}
            zoom   = 2.7
            print('gera mapa')
            if type(self.geojson) == str:
                print('carrougou mapa')
                self.geojson   = json.load(open('datasets/mapas/uf.json'))
            mapa = self.geojson

                
            #locations = 'codigo_municipio'
            featureidkey = 'properties.GEOCODIGO'
            #hover_name = 'nome_municipio_uf'
            hover_data = {hover_name:False, cor:True, cor:':.', locations:False}
            
            
            """hover_data={'species':False, # remove species from hover data
                            'sepal_length':':.2f', # customize hover for column of y attribute
                            'petal_width':True, # add other column, default formatting
                            'sepal_width':':.2f', # add other column, customized formatting
                            # data not in dataframe, default formatting
                            'suppl_1': np.random.random(len(df)),
                            # data not in dataframe, customized formatting
                            'suppl_2': (':.3f', np.random.random(len(df)))
                        })"""
        elif escopo == Escopo.Microrregiao:
            centro = {"lat": self.centroMapaUF[local][0], "lon": self.centroMapaUF[local][1]}
            zoom   = 5
            mapa   = json.load(open('datasets/mapas/microrregiao.json'))
            
        elif escopo == Escopo.Municipio:
            centro = {"lat": self.centroMapaUF[local][0], "lon": self.centroMapaUF[local][1]}
            zoom   = 5
            mapa   = json.load(open('datasets/mapas/municipio-' + local + '.json'))
            locations = 'codigo_municipio'
            featureidkey = 'properties.id'
            hover_name = 'nome_municipio_uf'
            hover_data = {hover_name:False, cor:True, locations:False}
        else:
            centro={"lat": -15.5477299222, "lon": -47.4139605285}
            zoom=3
            
        if animacao:
            animation_frame = "nu_ano"
        else:
            animation_frame = None
            
        grafico = px.choropleth_mapbox(dataframe, geojson=mapa, 
                                    locations=locations, 
                                    color=cor,
                                    color_continuous_scale="bluyl", #greens aggrnyl
                                    range_color=(dataframe[cor].min(), dataframe[cor].max()),
                                    featureidkey=featureidkey,
                                    mapbox_style=tipoMapa,
                                    zoom=zoom, 
                                    center = centro, 
                                    animation_frame=animation_frame,
                                    opacity=0.3,
                                    color_continuous_midpoint=dataframe[cor].max(),
                                    labels={cor:legenda},
                                    hover_name = hover_name, 
                                    hover_data = hover_data
                                    )
        grafico.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        return grafico

    def barras(self, escopo, local, dataframe, cor, legenda, titulo, hover_name, locations, tipoMapa="open-street-map",legenda_x='', animacao=False):
        dataframe = dataframe.sort_values(by=[cor])
        hover_data = {hover_name:False, cor:True, locations:False}
        if legenda_x == '':
            legenda_x = hover_name
        grafico = px.bar(dataframe, 
                         y=cor, 
                         x=legenda_x, 
                         text_auto='.2s', 
                         title=titulo,
                         labels={cor:legenda},
                         color_continuous_scale="bluyl",
                         color_continuous_midpoint=dataframe[cor].max(),
                         color=cor,
                         hover_name = hover_name, 
                         hover_data = hover_data,
                         range_y=(dataframe[cor].min()-10, dataframe[cor].max()+10)
                         )
        grafico.update_yaxes(visible=False, showticklabels=False)
        #grafico.update_xaxes(visible=False, showticklabels=True)
        grafico.update_layout(margin={"r":0,"l":0,"b":0},xaxis_title=None)
        return grafico