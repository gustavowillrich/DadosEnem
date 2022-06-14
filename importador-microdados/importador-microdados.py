import psycopg2
import psycopg2.extras
import csv
from time import gmtime, strftime
import pandas as pd
import numpy as np
import unicodedata
import sys
from datetime import datetime

# Verifica se um arquivo foi informado
if len(sys.argv) <= 1:
    print("Informe um arquivo de microdados no ENEM!")
    print("exemplo: " + sys.argv[0] + " microdados_enem2019.csv")
    exit(1)

# Parametros
arquivo=sys.argv[1]

con = psycopg2.connect(host='127.0.0.1', database='enem', user='enem', password='fsa2Lkd#jfklsd5jM')
cur = con.cursor()

chunk_size=50000
batch_no=0
for df in pd.read_csv(arquivo, sep=None, encoding = "ISO-8859-1", chunksize=chunk_size, iterator=True):
    if batch_no == 0:
        ano = int(df.iloc[0]['NU_ANO'])
        print(ano)
    
    batch_no += 1
    print(batch_no)

    #Remover acentuação dos cabeçalho
    for column in df.columns.values:
        df = df.rename(columns={column: str(unicodedata.normalize('NFKD', column).encode('ascii','ignore').decode('utf-8'))})

    """if ano <= 2012:
        df = df.rename(columns={'COD_MUNICIPIO_INSC': 'CO_MUNICIPIO_RESIDENCIA'})
        df = df.rename(columns={'??? Vou ter que converter sigla em codigo': 'CO_UF_RESIDENCIA'})
        df = df.rename(columns={'IDADE': 'NU_IDADE'})
        df = df.rename(columns={'ST_CONCLUSAO': 'TP_ST_CONCLUSAO'})
        df = df.rename(columns={'IN_TP_ENSINO': 'TP_ENSINO'})
        df = df.rename(columns={'PK_COD_ENTIDADE': 'CO_ESCOLA'})
        df = df.rename(columns={'COD_MUNICIPIO_ESC': 'CO_MUNICIPIO_ESC'})
        df = df.rename(columns={'??? Vou ter que converter sigla em codigo': 'CO_UF_ESC'})
        df = df.rename(columns={'ID_DEPENDENCIA_ADM': 'TP_DEPENDENCIA_ADM_ESC'})
        df = df.rename(columns={'ID_LOCALIZACAO': 'TP_LOCALIZACAO_ESC'})
        df = df.rename(columns={'SIT_FUNC': 'TP_SIT_FUNC_ESC'})
        df = df.rename(columns={'COD_MUNICIPIO_PROVA': 'CO_MUNICIPIO_PROVA'})
        df = df.rename(columns={'??? Vou ter que converter sigla em codigo': 'CO_UF_PROVA'})
        df = df.rename(columns={'IN_PRESENCA_CN': 'TP_PRESENCA_CN'})
        df = df.rename(columns={'IN_PRESENCA_CH': 'TP_PRESENCA_CH'})
        df = df.rename(columns={'IN_PRESENCA_LC': 'TP_PRESENCA_LC'})
        df = df.rename(columns={'IN_PRESENCA_MT': 'TP_PRESENCA_MT'})
        df = df.rename(columns={'NU_NT_CN': 'NU_NOTA_CN'})
        df = df.rename(columns={'NU_NT_CH': 'NU_NOTA_CH'})
        df = df.rename(columns={'NU_NT_LC': 'NU_NOTA_LC'})
        df = df.rename(columns={'NU_NT_MT': 'NU_NOTA_MT'})
        df = df.rename(columns={'IN_STATUS_REDACAO': 'TP_STATUS_REDACAO'})
        df = df.rename(columns={'ANO_CONCLUIU': 'TP_ANO_CONCLUIU'})
        df = df.rename(columns={'NACIONALIDADE___Não tem': 'TP_NACIONALIDADE'})
        df = df.rename(columns={'COD_MUNICIPIO_NASCIMENTO___Não tem': 'CO_MUNICIPIO_NASCIMENTO'})
        df = df.rename(columns={'COD_UF_NASCIMENTO___Não tem': 'CO_UF_NASCIMENTO'})
    elif ano <= 2014:
        df = df.rename(columns={'COD_MUNICIPIO_RESIDENCIA': 'CO_MUNICIPIO_RESIDENCIA'})
        df = df.rename(columns={'COD_UF_RESIDENCIA': 'CO_UF_RESIDENCIA'})
        df = df.rename(columns={'IDADE': 'NU_IDADE'})
        df = df.rename(columns={'ST_CONCLUSAO': 'TP_ST_CONCLUSAO'})
        df = df.rename(columns={'IN_TP_ENSINO': 'TP_ENSINO'})
        df = df.rename(columns={'COD_ESCOLA': 'CO_ESCOLA'})
        df = df.rename(columns={'COD_MUNICIPIO_ESC': 'CO_MUNICIPIO_ESC'})
        df = df.rename(columns={'COD_UF_ESC': 'CO_UF_ESC'})
        df = df.rename(columns={'ID_DEPENDENCIA_ADM_ESC': 'TP_DEPENDENCIA_ADM_ESC'})
        df = df.rename(columns={'ID_LOCALIZACAO_ESC': 'TP_LOCALIZACAO_ESC'})
        df = df.rename(columns={'SIT_FUNC_ESC': 'TP_SIT_FUNC_ESC'})
        df = df.rename(columns={'COD_MUNICIPIO_PROVA': 'CO_MUNICIPIO_PROVA'})
        df = df.rename(columns={'COD_UF_PROVA': 'CO_UF_PROVA'})
        df = df.rename(columns={'IN_PRESENCA_CN': 'TP_PRESENCA_CN'})
        df = df.rename(columns={'IN_PRESENCA_CH': 'TP_PRESENCA_CH'})
        df = df.rename(columns={'IN_PRESENCA_LC': 'TP_PRESENCA_LC'})
        df = df.rename(columns={'IN_PRESENCA_MT': 'TP_PRESENCA_MT'})
        df = df.rename(columns={'NOTA_CN': 'NU_NOTA_CN'})
        df = df.rename(columns={'NOTA_CH': 'NU_NOTA_CH'})
        df = df.rename(columns={'NOTA_LC': 'NU_NOTA_LC'})
        df = df.rename(columns={'NOTA_MT': 'NU_NOTA_MT'})
        df = df.rename(columns={'IN_STATUS_REDACAO': 'TP_STATUS_REDACAO'})
        df = df.rename(columns={'ANO_CONCLUIU': 'TP_ANO_CONCLUIU'})
        df = df.rename(columns={'NACIONALIDADE': 'TP_NACIONALIDADE'})
        df = df.rename(columns={'COD_MUNICIPIO_NASCIMENTO': 'CO_MUNICIPIO_NASCIMENTO'})
        df = df.rename(columns={'COD_UF_NASCIMENTO': 'CO_UF_NASCIMENTO'})"""
  
    #Ajusta campos binarios
    df = df.replace({"IN_TREINEIRO": {1: True, 0: False}}).fillna(np.nan)
    df = df.replace({"IN_BAIXA_VISAO": {1: True, 0: False}}).fillna(np.nan)
    df = df.replace({"IN_CEGUEIRA": {1: True, 0: False}}).fillna(np.nan)
    df = df.replace({"IN_SURDEZ": {1: True, 0: False}}).fillna(np.nan)
    df = df.replace({"IN_DEFICIENCIA_AUDITIVA": {1: True, 0: False}}).fillna(np.nan)
    df = df.replace({"IN_SURDO_CEGUEIRA": {1: True, 0: False}}).fillna(np.nan)
    df = df.replace({"IN_DEFICIENCIA_FISICA": {1: True, 0: False}}).fillna(np.nan)
    df = df.replace({"IN_DEFICIENCIA_MENTAL": {1: True, 0: False}}).fillna(np.nan)
    df = df.replace({"IN_DEFICIT_ATENCAO": {1: True, 0: False}}).fillna(np.nan)
    df = df.replace({"IN_DISLEXIA": {1: True, 0: False}}).fillna(np.nan)
    df = df.replace({"IN_DISCALCULIA": {1: True, 0: False}}).fillna(np.nan)
    df = df.replace({"IN_AUTISMO": {1: True, 0: False}}).fillna(np.nan)
    df = df.replace({"IN_VISAO_MONOCULAR": {1: True, 0: False}}).fillna(np.nan)
    df = df.replace({"IN_OUTRA_DEF": {1: True, 0: False}}).fillna(np.nan)
    df = df.replace({"IN_GESTANTE": {1: True, 0: False}}).fillna(np.nan)
    df = df.replace({"IN_LACTANTE": {1: True, 0: False}}).fillna(np.nan)
    df = df.replace({"IN_IDOSO": {1: True, 0: False}}).fillna(np.nan)
    df = df.replace({"IN_ESTUDA_CLASSE_HOSPITALAR": {1: True, 0: False}})
    df = df.replace({"IN_SEM_RECURSO": {1: True, 0: False}}).fillna(np.nan)
    df = df.replace({"IN_BRAILLE": {1: True, 0: False}}).fillna(np.nan)
    df = df.replace({"IN_AMPLIADA_24": {1: True, 0: False}}).fillna(np.nan)
    df = df.replace({"IN_AMPLIADA_18": {1: True, 0: False}}).fillna(np.nan)
    df = df.replace({"IN_LEDOR": {1: True, 0: False}}).fillna(np.nan)
    df = df.replace({"IN_ACESSO": {1: True, 0: False}}).fillna(np.nan)
    df = df.replace({"IN_TRANSCRICAO": {1: True, 0: False}}).fillna(np.nan)
    df = df.replace({"IN_LIBRAS": {1: True, 0: False}}).fillna(np.nan)
    df = df.replace({"IN_LEITURA_LABIAL": {1: True, 0: False}}).fillna(np.nan)
    df = df.replace({"IN_MESA_CADEIRA_RODAS": {1: True, 0: False}}).fillna(np.nan)
    df = df.replace({"IN_MESA_CADEIRA_SEPARADA": {1: True, 0: False}}).fillna(np.nan)
    df = df.replace({"IN_APOIO_PERNA": {1: True, 0: False}}).fillna(np.nan)
    df = df.replace({"IN_GUIA_INTERPRETE": {1: True, 0: False}}).fillna(np.nan)
    df = df.replace({"IN_COMPUTADOR": {1: True, 0: False}}).fillna(np.nan)
    df = df.replace({"IN_CADEIRA_ESPECIAL": {1: True, 0: False}}).fillna(np.nan)
    df = df.replace({"IN_CADEIRA_CANHOTO": {1: True, 0: False}}).fillna(np.nan)
    df = df.replace({"IN_CADEIRA_ACOLCHOADA": {1: True, 0: False}}).fillna(np.nan)
    df = df.replace({"IN_PROVA_DEITADO": {1: True, 0: False}}).fillna(np.nan)
    df = df.replace({"IN_MOBILIARIO_OBESO": {1: True, 0: False}}).fillna(np.nan)
    df = df.replace({"IN_LAMINA_OVERLAY": {1: True, 0: False}}).fillna(np.nan)
    df = df.replace({"IN_PROTETOR_AURICULAR": {1: True, 0: False}}).fillna(np.nan)
    df = df.replace({"IN_MEDIDOR_GLICOSE": {1: True, 0: False}}).fillna(np.nan)
    df = df.replace({"IN_MAQUINA_BRAILE": {1: True, 0: False}}).fillna(np.nan)
    df = df.replace({"IN_SOROBAN": {1: True, 0: False}}).fillna(np.nan)
    df = df.replace({"IN_MARCA_PASSO": {1: True, 0: False}}).fillna(np.nan)
    df = df.replace({"IN_SONDA": {1: True, 0: False}}).fillna(np.nan)
    df = df.replace({"IN_MEDICAMENTOS": {1: True, 0: False}}).fillna(np.nan)
    df = df.replace({"IN_SALA_INDIVIDUAL": {1: True, 0: False}}).fillna(np.nan)
    df = df.replace({"IN_SALA_ESPECIAL": {1: True, 0: False}}).fillna(np.nan)
    df = df.replace({"IN_SALA_ACOMPANHANTE": {1: True, 0: False}}).fillna(np.nan)
    df = df.replace({"IN_MOBILIARIO_ESPECIFICO": {1: True, 0: False}}).fillna(np.nan)
    df = df.replace({"IN_MATERIAL_ESPECIFICO": {1: True, 0: False}}).fillna(np.nan)
    df = df.replace({"IN_NOME_SOCIAL": {1: True, 0: False}}).fillna(np.nan)
    df = df.replace({"IN_TEMPO_ADICIONAL": {1: True, 0: False}}).fillna(np.nan)
    
    #Padroniza ano de conclusao do ensino medio
    if ano in [2018, 2017, 2016, 2015, 2014, 2013]:
        df = df.replace({"TP_ESTADO_CIVIL": {0: 1, 
                                            1: 2, 
                                            2: 3, 
                                            3: 4}})
        
        if ano in [2014, 2013]:
            df = df.rename(columns={'COD_MUNICIPIO_RESIDENCIA': 'CO_MUNICIPIO_RESIDENCIA'})
            df = df.rename(columns={'COD_UF_RESIDENCIA': 'CO_UF_RESIDENCIA'})
            df = df.rename(columns={'IDADE': 'NU_IDADE'})
            df = df.rename(columns={'ST_CONCLUSAO': 'TP_ST_CONCLUSAO'})
            df = df.rename(columns={'IN_TP_ENSINO': 'TP_ENSINO'})
            df = df.rename(columns={'COD_ESCOLA': 'CO_ESCOLA'})
            df = df.rename(columns={'COD_MUNICIPIO_ESC': 'CO_MUNICIPIO_ESC'})
            df = df.rename(columns={'COD_UF_ESC': 'CO_UF_ESC'})
            df = df.rename(columns={'ID_DEPENDENCIA_ADM_ESC': 'TP_DEPENDENCIA_ADM_ESC'})
            df = df.rename(columns={'ID_LOCALIZACAO_ESC': 'TP_LOCALIZACAO_ESC'})
            df = df.rename(columns={'SIT_FUNC_ESC': 'TP_SIT_FUNC_ESC'})
            df = df.rename(columns={'COD_MUNICIPIO_PROVA': 'CO_MUNICIPIO_PROVA'})
            df = df.rename(columns={'COD_UF_PROVA': 'CO_UF_PROVA'})
            df = df.rename(columns={'IN_PRESENCA_CN': 'TP_PRESENCA_CN'})
            df = df.rename(columns={'IN_PRESENCA_CH': 'TP_PRESENCA_CH'})
            df = df.rename(columns={'IN_PRESENCA_LC': 'TP_PRESENCA_LC'})
            df = df.rename(columns={'IN_PRESENCA_MT': 'TP_PRESENCA_MT'})
            df = df.rename(columns={'NOTA_CN': 'NU_NOTA_CN'})
            df = df.rename(columns={'NOTA_CH': 'NU_NOTA_CH'})
            df = df.rename(columns={'NOTA_LC': 'NU_NOTA_LC'})
            df = df.rename(columns={'NOTA_MT': 'NU_NOTA_MT'})
            df = df.rename(columns={'IN_STATUS_REDACAO': 'TP_STATUS_REDACAO'})
            df = df.rename(columns={'ANO_CONCLUIU': 'TP_ANO_CONCLUIU'})
            df = df.rename(columns={'NACIONALIDADE': 'TP_NACIONALIDADE'})
            df = df.rename(columns={'COD_MUNICIPIO_NASCIMENTO': 'CO_MUNICIPIO_NASCIMENTO'})
            df = df.rename(columns={'COD_UF_NASCIMENTO': 'CO_UF_NASCIMENTO'})
            
            df = df.replace({"TP_ANO_CONCLUIU": {2014: 14, 
                                                 2013: 13, 
                                                 2012: 12, 
                                                 2011: 11, 
                                                 2010: 10, 
                                                 2009: 9, 
                                                 2008: 8, 
                                                 2007: 7, 
                                                 2006: 1}})
            
            #Tipo de escola
            df = df.replace({"TP_ESCOLA": {1: 2, 
                                           2: 3}})
            
            #Tipo de ensino, epecial, eja
            df = df.replace({"TP_ENSINO": {2: 3, 
                                           4: 2}})
            
            #Status redacao
            df = df.replace({"TP_STATUS_REDACAO": {1: 4, 
                                                   3: 6,
                                                   4: 7,
                                                   5: 8,
                                                   6: 60,
                                                   7: 1,
                                                   9: 5,
                                                   10: 3,
                                                   11: 9}})

            
        
        elif ano in [2016, 2015]:
            df = df.replace({"TP_ANO_CONCLUIU": {1: 15, 
                                                2: 14, 
                                                3: 13, 
                                                4: 12, 
                                                5: 11, 
                                                6: 10, 
                                                7: 9, 
                                                8: 8, 
                                                9: 7, 
                                                10: 1}})
        elif ano == 2017:
            df = df.replace({"TP_ANO_CONCLUIU": {1: 16, 
                                                2: 15, 
                                                3: 14, 
                                                4: 13, 
                                                5: 12, 
                                                6: 11, 
                                                7: 10, 
                                                8: 9, 
                                                9: 8, 
                                                10: 7, 
                                                11: 1}})
        elif ano == 2018:
            df = df.replace({"TP_ANO_CONCLUIU": {1: 17, 
                                                2: 16, 
                                                3: 15, 
                                                4: 14, 
                                                5: 13, 
                                                6: 12, 
                                                7: 11, 
                                                8: 10, 
                                                9: 9, 
                                                10: 8, 
                                                11: 7, 
                                                12: 1}})
    elif ano == 2019:
        df = df.replace({"TP_ANO_CONCLUIU": {1: 18, 
                                            2: 17, 
                                            3: 16, 
                                            4: 15, 
                                            5: 14, 
                                            6: 13, 
                                            7: 12, 
                                            8: 11, 
                                            9: 10, 
                                            10: 9, 
                                            11: 8, 
                                            12: 7, 
                                            13: 1}})
    elif ano == 2020:
        df = df.replace({"TP_ANO_CONCLUIU": {1: 19, 
                                            2: 18, 
                                            3: 17, 
                                            4: 16, 
                                            5: 15, 
                                            6: 14, 
                                            7: 13, 
                                            8: 12, 
                                            9: 11, 
                                            10: 10, 
                                            11: 9, 
                                            12: 8, 
                                            13: 7,
                                            14: 1}})
        
        df = df.replace({"TP_FAIXA_ETARIA": {1: 16, 
                                            2: 17, 
                                            3: 18, 
                                            4: 19, 
                                            5: 20, 
                                            6: 21, 
                                            7: 22, 
                                            8: 23, 
                                            9: 24, 
                                            10: 25, 
                                            11: 28, 
                                            12: 33, 
                                            13: 38,
                                            14: 43,
                                            15: 48,
                                            16: 53,
                                            17: 58,
                                            18: 63,
                                            19: 68,
                                            20: 73}})
        df = df.rename(columns={'TP_FAIXA_ETARIA': 'NU_IDADE'})
    
    #Padroniza o questionario socioeconomico
    df = df.rename(columns={'Q001': 'QS_ESCOLARIDADE_PAI'})
    df = df.rename(columns={'Q002': 'QS_ESCOLARIDADE_MAE'}) 
    
    if ano >= 2015:
        df = df.rename(columns={'Q005': 'QS_NUMERO_PESSOAS_RESIDENCIA'})
        df = df.rename(columns={'Q006': 'QS_RENDA_FAMILIA'})
        df = df.rename(columns={'Q007': 'QS_EMPREGADO_DOMESTICO'})
        df = df.rename(columns={'Q008': 'QS_NUMERO_BANHEIROS'})
        df = df.rename(columns={'Q009': 'QS_NUMERO_QUARTOS'}).fillna(np.nan)
        df = df.rename(columns={'Q010': 'QS_NUMERO_CARROS'})
        df = df.rename(columns={'Q011': 'QS_NUMERO_MOTOS'}).fillna(np.nan)
        df = df.rename(columns={'Q012': 'QS_NUMERO_GELADEIRA'}).fillna(np.nan)
        df = df.rename(columns={'Q013': 'QS_NUMERO_FREEZER'}).fillna(np.nan)
        df = df.rename(columns={'Q014': 'QS_NUMERO_LAVADORA_ROUPA'})
        df = df.rename(columns={'Q015': 'QS_NUMERO_SECADORA_ROUPA'}).fillna(np.nan)
        df = df.rename(columns={'Q016': 'QS_NUMERO_MICROONDAS'}).fillna(np.nan)
        df = df.rename(columns={'Q017': 'QS_NUMERO_LAVADORA_LOUCA'}).fillna(np.nan)
        df = df.rename(columns={'Q018': 'QS_ASPIRADOR_PO'})
        df = df.replace({"QS_ASPIRADOR_PO": {'A': False, 'B': True}})
        df = df.rename(columns={'Q019': 'QS_NUMERO_TELEVISAO'})
        df = df.rename(columns={'Q020': 'QS_DVD'})
        df = df.replace({"QS_DVD": {'A': False, 'B': False}})
        df = df.rename(columns={'Q021': 'QS_TV_ASSINATURA'})
        df = df.replace({"QS_TV_ASSINATURA": {'A': False, 'B': True}})
        df = df.rename(columns={'Q022': 'QS_NUMERO_CELULAR'})
        df = df.rename(columns={'Q023': 'QS_TELEFONE_FIXO'})
        df = df.replace({"QS_TELEFONE_FIXO": {'A': False, 'B': True}})
        df = df.rename(columns={'Q024': 'QS_NUMERO_COMPUTADOR'})
        df = df.rename(columns={'Q025': 'QS_INTERNET'})
        df = df.replace({"QS_INTERNET": {'A': False, 'B': True}})
        
        
    elif ano in [2014, 2013]:
        df = df.rename(columns={'Q003': 'QS_RENDA_FAMILIA'})
        df = df.rename(columns={'Q004': 'QS_NUMERO_PESSOAS_RESIDENCIA'})
        
        df = df.rename(columns={'Q007': 'QS_NUMERO_TELEVISAO'})
        df = df.replace({"QS_NUMERO_TELEVISAO": {"A": "B", 
                                                 "B": "C", 
                                                 "C": "D", 
                                                 "D": "A"}})
        df = df.rename(columns={'Q008': 'QS_DVD'})
        df = df.replace({"QS_DVD": {'A': True, 'B': True, 'C': True, 'D': False}})
        
        df = df.rename(columns={'Q010': 'QS_NUMERO_COMPUTADOR'})
        df = df.replace({"QS_NUMERO_COMPUTADOR": {"A": "B", 
                                                  "B": "C", 
                                                  "C": "D", 
                                                  "D": "A"}})
        
        df = df.rename(columns={'Q011': 'QS_NUMERO_AUTOMOVEL'})
        df = df.replace({"QS_NUMERO_AUTOMOVEL": {"A": "B", 
                                                 "B": "C", 
                                                 "C": "D", 
                                                 "D": "A"}})
        
        df = df.rename(columns={'Q012': 'QS_NUMERO_LAVADORA_ROUPA'})
        df = df.replace({"QS_NUMERO_LAVADORA_ROUPA": {"A": "B", 
                                                      "B": "C", 
                                                      "C": "D", 
                                                      "D": "A"}})
        
        df = df.rename(columns={'Q013': 'QS_NUMERO_GELADEIRA'}).fillna(np.nan)
        df = df.replace({"QS_NUMERO_GELADEIRA": {"A": "B", 
                                                 "B": "C", 
                                                 "C": "D", 
                                                 "D": "A"}})
        
        df = df.rename(columns={'Q014': 'QS_NUMERO_FREEZER'}).fillna(np.nan)
        df = df.replace({"QS_NUMERO_FREEZER": {"A": "B", 
                                                 "B": "C", 
                                                 "C": "D", 
                                                 "D": "A"}})
                
        df = df.rename(columns={'Q015': 'QS_TELEFONE_FIXO'})
        df = df.replace({"QS_TELEFONE_FIXO": {'A': True, 'B': True, 'C': True, 'D': False}})
        
        df = df.rename(columns={'Q016': 'QS_NUMERO_CELULAR'})
        df = df.replace({"QS_NUMERO_CELULAR": {"A": "B", 
                                               "B": "C", 
                                               "C": "D", 
                                               "D": "A"}})
        
        df = df.rename(columns={'Q017': 'QS_INTERNET'})
        df = df.replace({"QS_INTERNET": {'A': True, 'B': True, 'C': True, 'D': False}})
        
        df = df.rename(columns={'Q018': 'QS_TV_ASSINATURA'})
        df = df.replace({"QS_TV_ASSINATURA": {'A': True, 'B': True, 'C': True, 'D': False}})
        
        df = df.rename(columns={'Q019': 'QS_ASPIRADOR_PO'})
        df = df.replace({"QS_ASPIRADOR_PO": {'A': True, 'B': True, 'C': True, 'D': False}})
        
        df = df.rename(columns={'Q020': 'QS_EMPREGADO_DOMESTICO'})
        df = df.replace({"QS_EMPREGADO_DOMESTICO": {'A': 'B', 
                                                    'B': 'B', 
                                                    'C': 'B', 
                                                    'D': 'A'}})
        
        df = df.rename(columns={'Q021': 'QS_NUMERO_BANHEIROS'})
        df = df.replace({"QS_NUMERO_CELULAR": {"A": "B", 
                                               "B": "C", 
                                               "C": "D", 
                                               "D": "A"}})

        
        df = df.replace({"QS_ESCOLARIDADE_PAI": {"F": "E", 
                                                 "G": "F", 
                                                 "H": "G", 
                                                 "I": "H"}})
        
        df = df.replace({"QS_ESCOLARIDADE_MAE": {"F": "E", 
                                                 "G": "F", 
                                                 "H": "G", 
                                                 "I": "H"}})
        

    
    #Busca apenas os campos que serao importados, descartando qualquer outro campo adicional
    df = df.loc[:, df.columns.isin(list(["NU_INSCRICAO",
            "NU_ANO", 
            "CO_MUNICIPIO_RESIDENCIA", 
            "CO_UF_RESIDENCIA", 
            "NU_IDADE", 
            "TP_SEXO", 
            "TP_ESTADO_CIVIL",
            "TP_COR_RACA",
            "TP_NACIONALIDADE",
            "CO_MUNICIPIO_NASCIMENTO",
            "CO_UF_NASCIMENTO",
            "TP_ST_CONCLUSAO",
            "TP_ANO_CONCLUIU",
            "TP_ESCOLA",
            "TP_ENSINO",
            "IN_TREINEIRO",
            "CO_ESCOLA",
            "CO_MUNICIPIO_ESC",
            "CO_UF_ESC",
            "TP_DEPENDENCIA_ADM_ESC",
            "TP_LOCALIZACAO_ESC",
            "TP_SIT_FUNC_ESC",
            "IN_BAIXA_VISAO",
            "IN_CEGUEIRA",
            "IN_SURDEZ",
            "IN_DEFICIENCIA_AUDITIVA",
            "IN_SURDO_CEGUEIRA",
            "IN_DEFICIENCIA_FISICA",
            "IN_DEFICIENCIA_MENTAL",
            "IN_DEFICIT_ATENCAO",
            "IN_DISLEXIA",
            "IN_DISCALCULIA",
            "IN_AUTISMO",
            "IN_VISAO_MONOCULAR",
            "IN_OUTRA_DEF",
            "IN_GESTANTE",
            "IN_LACTANTE",
            "IN_IDOSO",
            "IN_ESTUDA_CLASSE_HOSPITALAR",
            "IN_SEM_RECURSO",
            "IN_BRAILLE",
            "IN_AMPLIADA_24",
            "IN_AMPLIADA_18",
            "IN_LEDOR",
            "IN_ACESSO",
            "IN_TRANSCRICAO",
            "IN_LIBRAS",
            "IN_LEITURA_LABIAL",
            "IN_MESA_CADEIRA_RODAS",
            "IN_MESA_CADEIRA_SEPARADA",
            "IN_APOIO_PERNA",
            "IN_GUIA_INTERPRETE",
            "IN_COMPUTADOR",
            "IN_CADEIRA_ESPECIAL",
            "IN_CADEIRA_CANHOTO",
            "IN_CADEIRA_ACOLCHOADA",
            "IN_PROVA_DEITADO",
            "IN_MOBILIARIO_OBESO",
            "IN_LAMINA_OVERLAY",
            "IN_PROTETOR_AURICULAR",
            "IN_MEDIDOR_GLICOSE",
            "IN_MAQUINA_BRAILE",
            "IN_SOROBAN",
            "IN_MARCA_PASSO",
            "IN_SONDA",
            "IN_MEDICAMENTOS",
            "IN_SALA_INDIVIDUAL",
            "IN_SALA_ESPECIAL",
            "IN_SALA_ACOMPANHANTE",
            "IN_MOBILIARIO_ESPECIFICO",
            "IN_MATERIAL_ESPECIFICO",
            "IN_NOME_SOCIAL",
            "CO_MUNICIPIO_PROVA",
            "CO_UF_PROVA",
            "TP_PRESENCA_CN",
            "TP_PRESENCA_CH",
            "TP_PRESENCA_LC",
            "TP_PRESENCA_MT",
            "NU_NOTA_CN",
            "NU_NOTA_CH",
            "NU_NOTA_LC",
            "NU_NOTA_MT",
            "TP_LINGUA",
            "TP_STATUS_REDACAO",
            "NU_NOTA_COMP1",
            "NU_NOTA_COMP2",
            "NU_NOTA_COMP3",
            "NU_NOTA_COMP4",
            "NU_NOTA_COMP5",
            "NU_NOTA_REDACAO",
            "QS_ESCOLARIDADE_PAI",
            "QS_ESCOLARIDADE_MAE",
            "QS_NUMERO_PESSOAS_RESIDENCIA",
            "QS_RENDA_FAMILIA",
            "QS_EMPREGADO_DOMESTICO",
            "QS_NUMERO_BANHEIROS",
            "QS_NUMERO_QUARTOS",
            "QS_NUMERO_CARROS",
            "QS_NUMERO_MOTOS",
            "QS_NUMERO_AUTOMOVEL",
            "QS_NUMERO_GELADEIRA",
            "QS_NUMERO_FREEZER",
            "QS_NUMERO_LAVADORA_ROUPA",
            "QS_NUMERO_SECADORA_ROUPA",
            "QS_NUMERO_MICROONDAS",
            "QS_NUMERO_LAVADORA_LOUCA",
            "QS_ASPIRADOR_PO",
            "QS_NUMERO_TELEVISAO",
            "QS_DVD",
            "QS_TV_ASSINATURA",
            "QS_NUMERO_CELULAR",
            "QS_TELEFONE_FIXO",
            "QS_NUMERO_COMPUTADOR",
            "IN_TEMPO_ADICIONAL",
            "QS_INTERNET" ]))]

    df = df.replace({np.nan: None})
    # df is the dataframe
    if len(df) > 0:
        df_columns = list(df)
        # create (col1,col2,...)
        columns = ",".join(df_columns)
      
        # create VALUES('%s', '%s',...) one '%s' per column
        values = "VALUES({})".format(",".join(["%s" for _ in df_columns])) 

        
        #create INSERT INTO table (columns) VALUES('%s',...)
        '''np.set_printoptions(threshold=sys.maxsize)
        print(columns)
        print(values)
        print(df.values)
        print('--------------')'''
        insert_stmt = "INSERT INTO {} ({}) {}".format('microdados',columns, values)

        pd.set_option('display.max_columns', None)
        
        #print(insert_stmt, df.head())
        #pd.set_option('display.max_columns', 200)
    
        cur = con.cursor()
        psycopg2.extras.execute_batch(cur, insert_stmt, df.values)
        con.commit()
        cur.close()
        print('Commit - ' + datetime.now().strftime("%d/%m/%Y %H:%M:%S"))

print('Fim')
