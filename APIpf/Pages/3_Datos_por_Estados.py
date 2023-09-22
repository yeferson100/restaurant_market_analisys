import streamlit as st
import pandas as pd

def app():
    st.write('Datos por Estados')

df= pd.read_csv('Yelp_Estados.csv')
st.image("Logo.jpeg", width=150) 

#st.markdown("# Datos por Estados")
st.sidebar.header("Datos por Estados")

st.header('Análisis de Indicadores')
txt = st.text_area('Descripción', '''
    PEE_Prom:  Cantidad de Restaurantes por Territorio
    PEE_Max:  Valor Maximo de Percepcion del Comercio
    Rev_Prom:  Promedio de Review_Count
    Rev_Max:  Maximo de Review_Count
    Ind_DCP_Prom:  Índice de DCP Promedio
    Ind_DCP_Max:  Índice de DCP Máximo
    ''')

st.caption('Consulta por: ')
option = st.selectbox(
    '4. Seleccione el Estado',
    ('Florida', 'Georgia', 'Maryland', 'Carolina del Norte', 'Carolina del Sur', 'Virginia'))

@st.cache_data
def estados(estado: str):
    #estado = estado.lower()
    resultados = df[df['estado'] == estado]
    columnas_de_interes = ['Ind_DCP_Prom', 'Ind_DCP_Max', 'PEE_Prom', 'PEE_Max', 'Rev_Prom', 'Rev_Max']
    resultados = resultados[columnas_de_interes]
    return resultados

if st.button('Buscar'):
    resultados_top5 = estados(option)
    if not resultados_top5.empty:
        st.subheader(f'Estado de {option}')
        for i, estado in resultados_top5.iterrows():
            st.write(f'{i + 1}. PEE_Prom: <span style="color: darkblue;"> {estado["PEE_Prom"]} </span>,' 
                     f'PEE_Max: <span style="color: darkblue;"> {estado["PEE_Max"]} </span>,'
                     f'Ind_DCP_Prom: <span style="color: darkblue;"> {estado["Ind_DCP_Prom"]} </span>,'
                     f'Ind_DCP_Max: <span style="color: darkblue;"> {estado["Ind_DCP_Max"]} </span>,'
                     f'Rev_Prom: <span style="color: darkblue;"> {estado["Rev_Prom"]} </span>,'
                     f'Rev_Max: <span style="color: darkblue;"> {estado["Rev_Max"]} </span>',unsafe_allow_html=True)
    else:
        st.write('No se encontraron restaurantes en el estado y tipo de comida seleccionados.')



st.header('Indicadores de Inversión en Restaurantes por Estado')
txt = st.text_area('Descripción', '''
    CRE (Cantidad de Restaurantes por Territorio): Esta métrica representa la cantidad de restaurantes en un área específica. Se calcula por cada 100 metros cuadrados y ayuda a identificar la densidad de restaurantes en un territorio.
    DCP (Densidad de Consumo Potencial según Población): Este indicador refleja la relación entre la densidad de consumidores potenciales y la población en un estado. Cuanto mayor sea el valor, mayor será la densidad de consumidores potenciales en comparación con la población.
    ''')
st.caption('Consulta por: ')
option = st.selectbox(
    '5. Seleccione el Estado',
    ('Florida', 'Georgia', 'Maryland', 'Carolina del Norte', 'Carolina del Sur', 'Virginia'))

def territorio(estado):
    # Filtra por estado especificado
    estado_filtrado = df[df['estado'] == estado]
    # Sumar la columna CRE y DCP en ese estado
    media_cre = estado_filtrado['CRE'].mean()
    media_dcp = estado_filtrado['DCP'].mean()

    return {   
        f'Concentracion de restaurantes en el Estado de {estado}' : media_cre , 
        f'Consumo potencial en el Estado de {estado}' : media_dcp }

if st.button('Consultar'):  # Agrega un botón para iniciar la consulta
    resultado = territorio(option) 
    # Mostrar los resultados
    st.write(f'Concentración de restaurantes en el Estado de {option}:', 
             f'<span style="color: darkblue;"> {resultado[f"Concentracion de restaurantes en el Estado de {option}"]}</span>',unsafe_allow_html=True)
    st.write(f'Consumo potencial en el Estado de {option}:',
             f'<span style="color: darkblue;"> {resultado[f"Consumo potencial en el Estado de {option}"]}</span>',unsafe_allow_html=True)

if __name__ == "__main__":
    app()         
