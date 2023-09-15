import streamlit as st
import folium as fl
import streamlit_folium as sf
from sklearn.metrics import jaccard_score
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

def app():
    st.write('Portal de Consultas')

df= pd.read_csv('Yelp_Seafood_Final (3).csv')
st.image("Logo.jpeg", width=150) 


#st.markdown("# Portal de Consultas")
st.sidebar.header("Portal de Consultas")

uploaded_files = st.sidebar.file_uploader("Cargar archivo CSV", accept_multiple_files=True)
for uploaded_file in uploaded_files:
    bytes_data = uploaded_file.read()
    st.write("filename:", uploaded_file.name)
    st.write(bytes_data)


st.header('Potencial de Inversión en el Sureste USA')
st.caption('Consulta por: ')
title = st.text_input('1. Tipo de Comida', 'Seafood', key='tipo_de_comida')
#Definir una función para calcular la similitud de Jaccard promedio por estado
def calcular_similitud_jaccard(df):
    estados = ['Florida', 'Georgia', 'Maryland', 'North Carolina', 'South Carolina', 'Virginia']
    resultados = []

    for estado in estados:
        # Filtrar datos por estado
        estado_data = df[df['state_full'] == estado]
        if estado_data.empty:
            continue
        # Filtrar restaurantes con categoría 'Seafood'
        seafood_data = estado_data[estado_data['categories'] == 'Seafood']
        # Calcular el número de restaurantes con categoría 'Seafood' utilizando la similitud de Jaccard
        if len(estado_data) > 0:
            jaccard_similarity = len(seafood_data) / len(estado_data)
        else:
            jaccard_similarity = 0.0
        resultados.append({'Estado': estado, 'Restaurantes Seafood': len(seafood_data), 'Similitud': jaccard_similarity})

    return pd.DataFrame(resultados)
# Botón para calcular y mostrar las recomendaciones
if st.button('Obtener Recomendaciones'):
# Obtener los resultados
   resultados_similitud_jaccard = calcular_similitud_jaccard(df)
# Botón para calcular y mostrar las recomendaciones
# Mostrar los resultados en una tabla
   st.subheader('Similitud Estado:')
   st.write(resultados_similitud_jaccard)


st.header('Top 5 de Restaurantes')
st.caption('Consulta por: ')
option = st.selectbox(
    '2. Seleccione el Estado',
    ('Florida','Georgia','Maryland','North Carolina','South Carolina','Virginia'))
title_top5 = st.text_input('2. Tipo de Comida', 'Seafood')

@st.cache_data
def restaurantes(state_full, categories):
     # Convertir a minúsculas
     state_full = state_full.lower()
     categories = categories.lower()
     # Filtrar 
     resultados = df[(df['state_full'].str.lower() == state_full) & (df['categories'].str.lower() == categories) 
                     & (df['review_count'] > 187)]
     # Ordenar 
     resultados = resultados.sort_values(by=['rating'], ascending=False).head(5)
     resultados = resultados[['rating','SEG_DCP','name','review_count']]
     # Convertir a lista de diccionarios
     resultados = resultados.to_dict(orient='records')
     return resultados

if st.button('Buscar Restaurantes'):
     resultados_top5 = restaurantes(option, title_top5)
     if resultados_top5:
         st.subheader(f'Top 5 de restaurantes en el Estado de {option}')
         for i, restaurante in enumerate(resultados_top5):
             st.write(f'{i + 1}. Estrellas: {restaurante["rating"]}, Nombre: {restaurante["name"]},  Segmento: {restaurante["SEG_DCP"]}, Reseñas: {restaurante["review_count"]}')
     else:
         st.write('No se encontraron restaurantes en el estado y tipo de comida seleccionados.')


st.header('Ubicación geográfica')
st.caption('Consulta por: ')
option3 = st.selectbox(
    '3. Seleccione el Estado',
    ('Florida','Georgia','Maryland','North Carolina','South Carolina','Virginia'))
title3 = st.text_input('3. Tipo de Comida ', 'Seafood')

@st.cache_data
def restaurantes(state_full, categories):
    state_full = state_full.lower()
    categories = categories.lower()
    top5 = df[(df['state_full'].str.lower() == state_full) & 
              (df['categories'].str.lower() == categories) & 
              (df['review_count'] > 187)].nlargest(5, 'rating')
    if top5.empty:
        return "No se encontraron restaurantes en el estado y tipo de comida seleccionados."
    # Mapa
    mapa = fl.Map(location=[top5.iloc[0]['latitude'], top5.iloc[0]['longitude']], zoom_start=4)
    for index, restaurante in top5.iterrows():
        fl.Marker(
            location=[restaurante['latitude'], restaurante['longitude']],
            popup=fl.Popup(f"{restaurante['name']} - {restaurante['rating']} estrellas - {restaurante['id']} id",max_width=110),
            tooltip=f"{restaurante['name']} - {restaurante['rating']} estrellas - {restaurante['id']} id",
            icon=fl.Icon(icon_color="pink",icon="utensils",prefix="fa")
        ).add_to(mapa)
        # Incrusta el mapa en la aplicación de Streamlit
    sf.folium_static(mapa)
if option3 and title3:
    if st.button('Buscar'):
        st.subheader(f'Mapa de restaurantes en el Estado de {option3}')
        restaurantes(option3, title3)  # Llama a la función para mostrar el mapa


st.header('Detalle de Ubicación')
st.caption('Consulta por: ')
option = st.selectbox(
    '4. Seleccione el Estado',
    ('Florida','Georgia','Maryland','North Carolina','South Carolina','Virginia'))
title_top5 = st.text_input('4. Tipo de Comida + Click boton Imprimir', 'Seafood')
@st.cache_data
def restaurantes(state_full, categories):
    state_full = state_full.lower()
    categories = categories.lower()
    resultados = df[(df['state_full'].str.lower() == state_full) & (df['categories'].str.lower() == categories) 
                    & (df['review_count'] > 187)]
    resultados = resultados.sort_values(by=['rating'], ascending=False).head(5)
    resultados = resultados[['id','name','city','latitude','longitude']]
    resultados = resultados.to_dict(orient='records')
    return resultados

# Imprimir lista top 5 cuando se haga clic en el botón
if st.sidebar.button('Imprimir Ubicación'):
    resultados_top5 = restaurantes(option, title_top5)
    if resultados_top5:
        st.subheader(f'Estado {option}')
        for restaurante in resultados_top5:
            st.write(f'Id: {restaurante["id"]}, Nombre: {restaurante["name"]}, Ciudad: {restaurante["city"]}, Latitud: {restaurante["latitude"]}, Longitud: {restaurante["longitude"]}')
    else:
        st.write('No se encontraron restaurantes en el estado y tipo de comida seleccionados.')


st.header('Similitud Competitiva') 
id_rest1 = st.text_input('Ingrese el ID del primer restaurante:', key='id_rest1')
id_rest2 = st.text_input('Ingrese el ID del segundo restaurante:', key='id_rest2')
try:
    id_rest1 = int(id_rest1)
    id_rest2 = int(id_rest2)
    st.write(f'IDs ingresados: {id_rest1}, {id_rest2}')
except ValueError:
    st.write('Por favor, ingrese un número válido.')

# Función para calcular el coeficiente de jaccard
def jaccard_similarity(rest1, rest2):
    set_rest1 = set(rest1)
    set_rest2 = set(rest2)
    intersection = len(set_rest1.intersection(set_rest2))
    union = len(set_rest1.union(set_rest2))
    return intersection / union if union != 0 else 0

def calcular_similitud(df, id_rest1, id_rest2):
    rest1 = df[df['id'] == id_rest1][['city','SEG_DCP','categories','DCP_Cumple','PEE_Cumple','Prom_SEG_PEE','latitude','longitude']].values[0].tolist()
    rest2 = df[df['id'] == id_rest2][['city','SEG_DCP','categories','DCP_Cumple','PEE_Cumple','Prom_SEG_PEE','latitude','longitude']].values[0].tolist()  
    similitud = jaccard_similarity(rest1, rest2)
    return similitud
    
if st.button('Calcular Similitud'):
    try:
        id_rest1 = int(id_rest1)
        id_rest2 = int(id_rest2)
        similitud = calcular_similitud(df, id_rest1, id_rest2)
        st.subheader('Resultado:')
        st.write(f'Similitud entre los restaurantes ID {id_rest1} y ID {id_rest2}: <span style="color: darkblue;">{similitud:.2f}</span>', unsafe_allow_html=True)
    except ValueError:
        st.write('Por favor, ingrese IDs válidos antes de calcular la similitud.')