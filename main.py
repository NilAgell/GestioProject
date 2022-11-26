#imports
import streamlit as st
import pandas as pd
from io import StringIO

st.set_page_config(page_title= 'Dades INCASÒL',page_icon=":eyes:",initial_sidebar_state="collapsed",layout="wide",menu_items={
        'About': "# This is a project for visual analytics."
    })

col1,col2 = st.columns([4,1])
with col1:
    st.title("Conversió de les dades de INCASÒL pel portal de transparència")
with col2:
    st.image("1200px-INCASOL.svg.png")

"""
L'objectiu d'aquesta pàgina web es el de convertir les dades del sòl que té incasòl en la seva base de dades interna en dades comprensibles i útils per els usuaris finals.

Per a que l'aplicatiu funcioni correctament, s'ha de pujar un arxis .csv amb, com a mínim, aquestes columnes que us mostrem a continuació. 
Cal dir, però, que en el cas en que alguna d'aquestes columnes no estigui en el arxiu pujat, es mostrarà com a buida en el arxiu ja transformat.
"""

example = pd.read_csv("Example.csv",sep=";")
example = example[0:5]
example




uploaded_file = st.file_uploader("Adjunta siusplau el arxiu amb les dades extretes de la base de dades de incasòl.")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()

    # To convert to a string based IO:
    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))

    # To read file as string:
    string_data = stringio.read()

    # Can be used wherever a "file-like" object is accepted:
    data = pd.read_csv(uploaded_file,sep=",")

    df = pd.DataFrame()
    if 'codiUp' in data.columns:
        df['Identificador']= data['codiUp']
    else: 
        df['Identificador'] =None

    if 'nomMunicipi' in data.columns:
        df['Municipi']= data['nomMunicipi']
    else: 
        df['Municipi'] =None
            
    if 'codiMunicipi' in data.columns:
        df['Codi municipi']= data['codiMunicipi']
    else: 
        df['Codi municipi']= None
            
    if 'descripcioActuacio' in data.columns:
        df['Descripció'] = data['descripcioActuacio']
    else: 
        df['Descripció']= None

    if 'superficieRealSol' in data.columns:
        df['Superficie Real Sol']= data['superficieRealSol'].apply(lambda x: str('{:,.2f}'.format(float(x.replace(',', '.')))).replace('.',';').replace(',','.').replace(';', ','))
    else:    
        df['Superficie Real Sol']= None
            
    if 'estatUrbanisticDescription' in data.columns:
        df['Estat urbanístic'] = data['estatUrbanisticDescription']
    else: 
        df['Estat urbanístic']= None

    if 'comercialitzacio' in data.columns:
        df['Comercialització'] = data['comercialitzacio']
    else: 
        df['Comercialització']= None
            
    if 'dretPropietat' in data.columns:
        df['Dret de propietat'] = data['dretPropietat']
    else: 
        df['Dret de propietat']= None

    ####Quins valors haurien d'anar en el dataset???
    if 'Total valor cadastral' in data.columns:
        df['Valor cadastral del sól'] = data['Total valor cadastral']
    else: 
        df['Valor cadastral del sól']= None
    if 'COD_CLAS' in data.columns:
        df['Classificació'] = data['COD_CLAS']
    else: 
        df['Classificació']=None

    if 'X' in data.columns:
        df['Coordenades X']= data['X']
    else: 
        df['Coordenades X'] =None
            
    if 'Y' in data.columns:
        df['Coordenades Y']= data['Y']
    else: 
        df['Coordenades Y'] =None
  

    for i in range(len(df)):
        if df['Comercialització'][i] == "VERDADERO":
            df.loc[i,'Comercialització'] = 'Si'
        else:
            df.loc[i,'Comercialització'] = 'No'
            
    for i in range(len(df)):
        if df['Dret de propietat'][i] == "VERDADERO":
            df.loc[i,'Dret de propietat'] = 'Si'
        else:
            df.loc[i,'Dret de propietat'] = 'No'

    # converting to string dtype
    df['Codi municipi']= df['Codi municipi'].astype(str)
    df['Identificador']= df['Identificador'].astype(str)
    
    # width of output string
    width =5
    
    # calling method and overwriting series
    df['Codi municipi']= df['Codi municipi'].str.zfill(width)
    df['Identificador']= df['Identificador'].str.zfill(width)
    col1, col2= st.columns(2)
    with col1:

        """
        Identificador: Número de 7 xifres que permet identificar cada sòl.\n
        Municipi: Nom del municipi.\n
        Codi municipi: Número de 5 xifres que permet identificar el municipi.\n
        Descripció: Descripció del terreny.\n
        Superfície Real Sòl: Superfície en metres quadrats de sòl.\n
        Estat urbanístic: Estat actual del sòl.\n
        """
    with col2:

        """
        Comercialització: Determina si el sòl es poden utilitzar per la comercialització.\n
        Dret de propietat: Determina si INCASÒL es propietari dels sòl o no.\n
        Valor catastral del sól: Valor del sòl en el cadastre.\n
        Classificació: Classificació urbanística del sòl.\n
        Coordenades X: Coordenades X en el sistema de referència ETRS89.\n
        Coordenades Y: Coordenades Y en el sistema de referència ETRS89.
        """



    df

    @st.cache
    def convert_df(df):
        # IMPORTANT: Cache the conversion to prevent computation on every rerun
        return df.to_csv().encode('utf-8')

    csv = convert_df(df)

    name_file = st.text_input("A continuació, introdueix el nom amb el qual vols que es baixi el fixer (sense incloure-hi el .csv).",value="dadesINCASOLnetes")
    st.download_button(
        label="Descarregar les dades en format CSV",
        data=csv,
        file_name=name_file+".csv",
        mime='text/csv',
    )
   







