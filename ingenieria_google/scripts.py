import pandas as pd
import numpy as np
import ast
import os
import gcsfs
import re

path_metadata = 'gs://data-cruda/google-maps/metadata/meta_states.csv' 
df_metadata = pd.read_csv(path_metadata)

df_metadata.drop(columns=['description', 'address', 'longitude', 'latitude', 'price', 'hours', 'MISC', 'state', 'relative_results', 'url', 'num_of_reviews'], inplace=True)

def es_restaurant(categorias):
    restaurant = False
    for categoria in categorias:
        categoria_lower = categoria.lower()
        if 'seafood restaurant' in categoria_lower:
            restaurant = True 
    
    if restaurant:
        return categorias
    else:
        return None

# Función para convertir las cadenas en listas, manejando los valores nulos
def parse_list(str_value):
    try:
        array = ast.literal_eval(str_value)
        return es_restaurant(array)
    except (ValueError, SyntaxError):
        return None


df_metadata['category'] = df_metadata['category'].apply(parse_list)

df_metadata.dropna(subset=['category'], inplace=True)

df_metadata.rename(columns={'name': 'nombre_restaurant'}, inplace=True)

df_metadata.drop(columns=['category'], inplace=True)

# df_metadata.to_csv('data-cruda/data-preprocesada/restaurantes_google.csv', index=False)

path_poblacion = 'gs://data-cruda/estados/estados_poblacion.csv'
path_superficie = 'gs://data-cruda/estados/superficie_estado.csv'

df_poblacion = pd.read_csv(path_poblacion)
df_superficie = pd.read_csv(path_superficie)

estados_proyecto = ['Florida', 'Georgia', 'Maryland', 'Carolina del Sur', 'Carolina del Norte', 'Virginia']

mask_poblacion = df_poblacion['Estado'].isin(estados_proyecto)
mask_superficie = df_superficie['Estado'].isin(estados_proyecto)

df_poblacion = df_poblacion[mask_poblacion]
df_superficie = df_superficie[mask_superficie]


df_estados = pd.merge(df_superficie, df_poblacion, on='Estado')

df_estados.drop(columns=['Unnamed: 0_x', 'Descripcion', 'Unnamed: 0_y', 'Densudad', 'Porc'], inplace=True)
df_estados.rename(columns={ 'siglas'    : 'id_estado',
                            'Estado'    : 'estado',
                            'Poblacion' : 'poblacion',
                            'superficie': 'superficie_km2'}, inplace=True)

df_estados = df_estados[['id_estado', 'estado', 'superficie_km2', 'poblacion']]


path_carpeta_reviews = 'gs://data-cruda/google-maps/reviews/'
# path_restaurantes = 'data-cruda/data-preprocesada/restaurantes_google.csv'
# df_restaurantes = pd.read_csv(path_restaurantes)

def encontrar_estado(path):
    patron = r'\/([^/]+)\.parquet$'
    coincidencia = re.search(patron, path)
    return coincidencia.group(1)

# Crea un sistema de archivos GCS
credenciales = {
"type": "service_account",
"project_id": "proyecto-final-henry-397316",
"private_key_id": "6c67fe28b78e691a29afa013e3a825468b8475a2",
"private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC1j/xVTRN/TDiZ\nt4ZcwYZmZSVJPcIHWk+E40817BJR72Fy1u8mlXBKyFy9PwJN52JHfu5EvFaWBPmk\nqBdRacLPwHzsMwq53iWClYf3Xmh8qEtr+22DBm3zEZcygfykqQ04+7CLSslTlOeX\nDt2KuJtwokMrbUq6/FjdrVJybgkCCqFBZHVRrwqnWPtGzp26/a/LD67VbxzvNWRp\nnvE+WzDxoCkq1fWCuaJlKPObP5e69J4QYkzBiQKaNBS99z7cpgjYXesa9O0ayoo2\nu5taDUbP8BR+tR2xjGcKyhr+cMuMcOAq2T9UYHya9pwwK1Um6tgGSzslj8AA3koL\nAVkhLDBhAgMBAAECggEADFWsL+Nc8rtWkQ2IdvQS0bwHYh1sTsbnkMCcmK42ub2d\n4jO7QDogzIPQ1m6Eao8l/HN2ySapFJIL9RASXXk7lJT1fQUkB708JnigKcG5LtbZ\ndjbjmWYuFrhYNu82dGf5D6j8X8ovOUVsImAOfvvMW5o6c/soe4w56/14FMa9nUIb\n9ZRQVkkVLVoSO4HZzVYPo+DuBio6S0gZIuNhvkWYv/CvcfQwy8gbkpO82H5/fxOI\noXiKhVrSY4KwKawUVrX7uQfcDs22Tz/5ksjOChTU8aBKo/EhwlmKBSymzbi3W3W2\nvbZKx68hwwpQvT+TFW3Utg+Bd5HDcnV0ljbpuQ2vUQKBgQD8Vl0nzW3kxMYgbdsz\nI9i+/xj8zWYzF7E77T/43D9PII59VfshXPYJY+O1Q13/uha/iUGoeUtD4UR3JoPI\nN0W+3cyxLSvtjrGGQtr2WKqQBnu5fqg6fPvh1pbdSyd/WewkYrKU0L31jDtVW3W6\nvNIeQMIbxpL2vktqK85izDALjQKBgQC4MqLW6+FFtsPd9RnTjT5MbsjCmsFNV202\nK85E5QMeT92EgSO7NtPKrqDLVYXxTZEz+DJouGZkQlA2NXECdGhfCphLHvWIkSkM\nYV7ET1w3HXvaa99AV+2C9XNQbFehF66ZgfuDqocYNfW594QUD4rQDHnCaWaGIMVC\nXZu6IjDZJQKBgQDqHx9TfLDHnyLMl+DXNB04KOuAMvrt0L+qgFfoiEFdIzHRbGMS\n83N8BugRGC4wxPGySKFYtSF2G54whtWigFX/3z657NVjFg/0KDeMdXvbIYjN9IwV\nqDzzruxO6hn9eOs2XzSeCocVOkUazz8OQX8afq8aokVdFfZWzcoxtI2nSQKBgHOm\nd09x8pMO2ZO2nGyTNhZPSIXHHK8uwUdN4cin8XlKs87KNmEJX5jWY+bG375N8Wkr\n4JqXjNJOQIaIr1fXNuDViiFAYvFIEvnO+O1Q1plUTbsqF5YSnvGmoqxQGgTvFZUU\nY5Kbsw6kcpA8tBTUXVebPaeu/cwhLzkoBOqtJPZxAoGAFw5ZJEMCMShgAaxxFakT\nBvqv91qCRZmnublBheRsQkfe9k+3tfOk7Cqbu6dqdkAx2g8e3LhB7CLw/sxSR/ku\nQ1huRsHfkwnKqxDyjOiU+GhxWHc/s9SkfYg9010k8YIEwP+nqzDRpFGaM81lTM9T\n35jeN70j+ClR3fbzrXw0zNo=\n-----END PRIVATE KEY-----\n",
"client_email": "proyecto-final@proyecto-final-henry-397316.iam.gserviceaccount.com",
"client_id": "117580722272189124656",
"auth_uri": "https://accounts.google.com/o/oauth2/auth",
"token_uri": "https://oauth2.googleapis.com/token",
"auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
"client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/proyecto-final%40proyecto-final-henry-397316.iam.gserviceaccount.com",
"universe_domain": "googleapis.com"
}


fs = gcsfs.GCSFileSystem(project='proyecto-final-henry-397316', token=credenciales)

files = fs.ls(path_carpeta_reviews)

# files = os.listdir(path_carpeta_reviews) 

array_restaurantes = []
array_reviews = []


for file in files:
    if file.endswith('.parquet'):
        with fs.open(file, 'rb') as f:
            path_archivo = f'gs://{file}'

            reviews = pd.read_parquet(path_archivo)
            reviews.drop(columns=['name', 'user_id', 'pics', 'resp', 'text'], inplace=True)

            restaurantes = [restaurante for restaurante in df_metadata['gmap_id']]

            reviews = reviews[reviews['gmap_id'].isin(restaurantes)]

            reviews.rename(columns={'time': 'fecha',
                    'rating': 'valoracion',
                    'state': 'estado'}, inplace=True)

            reviews.drop_duplicates(inplace=True)
            cant_reviews = reviews.value_counts(subset='gmap_id')
            cant_reviews = pd.DataFrame(cant_reviews).reset_index()

            estado = reviews['estado'].reset_index(drop=True)[0]
            nombre_archivo = f'restaurantes_{estado}_google.csv'

            df_restaurante = pd.merge(cant_reviews, df_metadata, on='gmap_id', how='right')
            df_restaurante = df_restaurante[df_restaurante['estado'] == estado]
            array_restaurantes.append(df_restaurante)

            reviews.drop(columns=['estado'], inplace=True)
            array_reviews.append(reviews)


reviews_final = pd.concat(array_reviews, ignore_index=True)

restaurantes_final = pd.concat(array_restaurantes, ignore_index=True)
restaurantes_final.fillna(0, inplace=True)
restaurantes_final.rename(columns={'count': 'cant_reviews', 'avg_rating': 'valoracion_promedio', 'estado': 'id_estado'}, inplace=True)
restaurantes_final['cant_reviews'] = restaurantes_final['cant_reviews'].apply(lambda x: int(x))
restaurantes_final = restaurantes_final[['gmap_id', 'nombre_restaurant', 'id_estado', 'cant_reviews', 'valoracion_promedio']]

## A partir de este punto, comienza el cálculo de los KPIs. Los procesamientos iniciales a los dataframes ya concluyeron.

# Listado de funciones utiles
#Funcion que toma una cadena string con numeros y puntos y la devuelve como numero entero.
def str_num(cadena:set):
    var = str(cadena)
    var = var.replace(".","")
    return int(var)

# Funcion que recibe una cadena de caracteres con "," como separador y una subcadena. La funcion verifica que la subcadena se encuentre en la cadena
# y devuelve la subcadena y efectivamente la encontro, o devuelve "0" si dicha subcadena no se encuentra en la cadena.
def Tip_Com_Cat(cadena:str,tipo_comida:str):
    lista = cadena.split(",")
    for i in range(0,len(lista)):
        lista[i] = lista[i].strip()
    if tipo_comida in lista:
        return tipo_comida
    else:
        return "0"

# Funcion para calcular el conjunto de estadisticos estandar seleccionados segun la data remitida (cuartil 1, cuartil 2, cuartil 3, promedio y desv std).
def Gen_Estadisticos(data):
    q1 = np.percentile(data, 25)
    Mediana = np.percentile(data, 50)
    q3 = np.percentile(data, 75)
    mean = np.mean(data)
    std = np.std(data)
    minimo = min(data)
    maximo = max(data)
    return q1,Mediana,q3,mean,std,minimo,maximo

def Menor_de_tres(A,B,C):
    #Fun cion que usamos para comparar cual de los tres valores enviados es el minimo y en dependiendo de ello se devuelve:
    # 97 indicando que el valor minimo corresponde a la poblacion de 97%, 98 a la de 98% o 99 a la 99%.
    lista = [A,B,C]
    Min_inter = min(lista)
    P_99 = Min_inter / (C)
    P_98 = Min_inter / (B)
    P_97 = Min_inter / (A)
    if P_99 == 1:
        var = 99
    else:
        if P_98 == 1:
            var = 98
        else: var = 97
    return var

# Funcion para asignar el valor del indice de consumo max o prom del segmento al cual esta asociado un comercio
def Asignacion_DCP(segmento,seg_A,seg_B,seg_C):
    if segmento == 1:
        return seg_A
    else:
        if segmento == 2:
            return seg_B
        else:
            return seg_C

#Funcin con la cual se asigna un 1 o un 0 a la columna en la cual decimos si un comercio tiene o no una percepcio por encima del promedio
def Asig_Encima_Debajo(valor,segmento,prom_peq,prom_gr,prom_ext):
    if segmento == 1:
        if valor > prom_peq:
            return 1
        else: return 0
    elif segmento == 2:
        if valor > prom_gr:
            return 1
        else: return 0
    elif segmento == 3:
        if valor > prom_ext:
            return 1
        else: return 0    


## Cantidad de Restaurantes
def calcular_cant_rest(estado):
    return  restaurantes_final[restaurantes_final['id_estado'] == estado]['gmap_id'].count()

df_estados['cant_rest'] = df_estados['id_estado'].apply(calcular_cant_rest)

# Calculo de columna de CRE (Concentracion de Restaurantes por Estado)
df_estados['CRE'] = df_estados['cant_rest'] / (df_estados['superficie_km2'] / 1000)

# Calculo de columna de DCP (Densidad de consumo segun poblacion)
df_estados['DCP'] = (df_estados['poblacion'] / 1000) / df_estados['cant_rest']

# Calculo de columna de Segmentacion de comercio en el dataframe de restaurantes


data_umbrales = {'NC': {'mediana': 0,
                'reduccion': 0,
                'porc_reduccion': 94},
            'SC': {'mediana': 0,
                'reduccion': 0,
                'porc_reduccion': 91},
            'FL': {'mediana': 0,
                'reduccion': 0,
                'porc_reduccion': 91},
            'GA': {'mediana': 0,
                'reduccion': 0,
                'porc_reduccion': 93},
            'MD': {'mediana': 0,
                'reduccion': 0,
                'porc_reduccion': 86},
            'VA': {'mediana': 0,
                'reduccion': 0,
                'porc_reduccion': 94},}


for estado in df_estados['id_estado']:
    
    mask = restaurantes_final['id_estado'] == estado
    df_temp = restaurantes_final[mask]

    var = data_umbrales[estado]['porc_reduccion']
    reduccion = np.percentile(df_temp['cant_reviews'], var)
    
    df_reducido = df_temp[df_temp['cant_reviews'] <= reduccion]
    df_reducido = df_reducido[df_reducido['cant_reviews'] > 0]
    
    q1,mediana,q3,mean,std,minimo,maximo = Gen_Estadisticos(df_reducido.cant_reviews)
    
    data_umbrales[estado]['mediana'] = mediana
    data_umbrales[estado]['reduccion'] = reduccion

def Seg_comercios(valor,Partidor1,Partidor2):
    if valor <= Partidor1:
        var = 1
    elif valor <= Partidor2:
        var = 2
    else: 
        var = 3
    return var

def apply_transform(row, umbrales):
    estado = row['id_estado']
    cant_reviews = row['cant_reviews']
    for estado_umbral in umbrales:
        if estado_umbral == estado:
            reduccion = umbrales[estado_umbral]['reduccion']
            mediana = umbrales[estado_umbral]['mediana']
            return Seg_comercios(cant_reviews, mediana, reduccion)
    return cant_reviews

restaurantes_final['SEG_DCP'] = restaurantes_final.apply(lambda x: apply_transform(x, data_umbrales), axis=1)


# Calculo de las columnas de promedio y maximo de reviews por estado
def asig_Rev_Prom(estado, df):
    return df[df["id_estado"] == estado]["cant_reviews"].mean()

def asig_Rev_Max(estado, df):
    return df[df["id_estado"] == estado]["cant_reviews"].max()

df_estados["Rev_Prom"] = df_estados["id_estado"].apply(lambda x: asig_Rev_Prom(x, restaurantes_final) if True else x)
df_estados["Rev_Max"] = df_estados["id_estado"].apply(lambda x: asig_Rev_Max(x, restaurantes_final) if True else x)

df_estados["Ind_DCP_Prom"] = df_estados["Rev_Prom"] / df_estados["DCP"] 
df_estados["Ind_DCP_Max"] = df_estados["Rev_Max"] / df_estados["DCP"] 

# Calculo de maximo y promedio de reseñas por segmento y estado

def calcular_estadisticos_segmento(data, segmento):
    # Filtrar el DataFrame por el segmento dado
    data_segmento = data[data["SEG_DCP"] == segmento]

    # Calcular el valor máximo y el promedio de reseñas por estado
    resultados = data_segmento.groupby(["id_estado"])["cant_reviews"].agg(["mean", "max"]).reset_index()
    resultados.columns = ["id_estado", f"Ind_DCP_prom_seg_{segmento}", f"Ind_DCP_max_seg_{segmento}"]

    return resultados

estadisticos_seg_1 = calcular_estadisticos_segmento(restaurantes_final, 1)
estadisticos_seg_2 = calcular_estadisticos_segmento(restaurantes_final, 2)
estadisticos_seg_3 = calcular_estadisticos_segmento(restaurantes_final, 3)


dataframe_estadisticas_segmentos = pd.merge(estadisticos_seg_1, estadisticos_seg_2, on='id_estado')
dataframe_estadisticas_segmentos = pd.merge(dataframe_estadisticas_segmentos, estadisticos_seg_3, on='id_estado')
df_estados = pd.merge(df_estados, dataframe_estadisticas_segmentos, on='id_estado')

# Reduccion de las ultimas columnas agregadas por DCP para volverlas indices.
columnas = ["Ind_DCP_prom_seg_1", "Ind_DCP_max_seg_1", "Ind_DCP_prom_seg_2", "Ind_DCP_max_seg_2", "Ind_DCP_prom_seg_3", "Ind_DCP_max_seg_3"]

for columna in columnas:
    df_estados[columna] = df_estados[columna] / df_estados["DCP"]

# Calculo de las columnas de PEE_prom y PEE_max

promedio_valoracion_por_estado = restaurantes_final.groupby("id_estado")["valoracion_promedio"].mean().reset_index()
maximo_valoracion_por_estado = restaurantes_final.groupby('id_estado')['valoracion_promedio'].max().reset_index()

# Renombrar la columna resultante
promedio_valoracion_por_estado.columns = ["id_estado", "PEE_prom"]
maximo_valoracion_por_estado.columns = ['id_estado', 'PEE_max']

dataframe_pee_max_prom = pd.merge(promedio_valoracion_por_estado, maximo_valoracion_por_estado, on='id_estado')
dataframe_pee_max_prom

df_estados = pd.merge(df_estados, dataframe_pee_max_prom, on='id_estado')

#Calculo de las columnas de PEE_prom y PEE_max por estado

# Calcular el promedio de "valoracion_promedio" por estado y segmento
promedio_valoracion_por_estado_segmento = restaurantes_final.groupby(["id_estado", "SEG_DCP"])["valoracion_promedio"].mean().reset_index()

# Calcular el máximo de "valoracion_promedio" por estado y segmento
maximo_valoracion_por_estado_segmento = restaurantes_final.groupby(["id_estado", "SEG_DCP"])["valoracion_promedio"].max().reset_index()

# Renombrar las columnas resultantes
promedio_valoracion_por_estado_segmento.columns = ["id_estado", "SEG_DCP", "PEE_prom"]
maximo_valoracion_por_estado_segmento.columns = ["id_estado", "SEG_DCP", "PEE_max"]

# Pivotear los DataFrames para obtener el formato deseado
promedio_valoracion_por_estado_segmento = promedio_valoracion_por_estado_segmento.pivot(index="id_estado", columns="SEG_DCP", values="PEE_prom").reset_index()
maximo_valoracion_por_estado_segmento = maximo_valoracion_por_estado_segmento.pivot(index="id_estado", columns="SEG_DCP", values="PEE_max").reset_index()

# Renombrar las columnas de los DataFrames pivotados
promedio_valoracion_por_estado_segmento.columns = ["id_estado", "PEE_prom_seg_1", "PEE_prom_seg_2", "PEE_prom_seg_3"]
maximo_valoracion_por_estado_segmento.columns = ["id_estado", "PEE_max_seg_1", "PEE_max_seg_2", "PEE_max_seg_3"]

# Combinar los resultados en un solo DataFrame
resultados_pee = pd.merge(promedio_valoracion_por_estado_segmento, maximo_valoracion_por_estado_segmento, on="id_estado")

df_estados = pd.merge(df_estados, resultados_pee, on='id_estado')


# Normalizacion

def normalizacion(valor,minimo,maximo,base,min_base):
    var = min_base + (((valor - minimo) / (maximo - minimo)) * base)
    return var

lista_indices = ["Ind_DCP_prom_seg_1","Ind_DCP_prom_seg_2","Ind_DCP_prom_seg_3","Ind_DCP_max_seg_1","Ind_DCP_max_seg_2","Ind_DCP_max_seg_3"]
lista_ind_Nor = ["Ind_DCP_prom_seg_1_nor","Ind_DCP_prom_seg_2_nor","Ind_DCP_prom_seg_3_nor","Ind_DCP_max_seg_1_nor","Ind_DCP_max_seg_2_nor","Ind_DCP_max_seg_3_nor"]
for i in range(0,len(lista_indices)):
    minimo = df_estados[lista_indices[i]].min()
    maximo = df_estados[lista_indices[i]].max()
    df_estados[lista_ind_Nor[i]] = df_estados[lista_indices[i]].apply(lambda x:normalizacion(x,minimo,maximo,80,20) if True else x)


df_estados = df_estados[["id_estado","estado","superficie_km2","poblacion","cant_rest",
                        "CRE","DCP","Rev_Prom","Rev_Max","PEE_prom","PEE_max",
                        "Ind_DCP_Prom","Ind_DCP_Max",
                        "Ind_DCP_prom_seg_1","Ind_DCP_prom_seg_1_nor",
                        "Ind_DCP_prom_seg_2","Ind_DCP_prom_seg_2_nor",
                        "Ind_DCP_prom_seg_3","Ind_DCP_prom_seg_3_nor",
                        "Ind_DCP_max_seg_1","Ind_DCP_max_seg_1_nor",
                        "Ind_DCP_max_seg_2","Ind_DCP_max_seg_2_nor",
                        "Ind_DCP_max_seg_3","Ind_DCP_max_seg_3_nor",
                        "PEE_prom_seg_1","PEE_prom_seg_2","PEE_prom_seg_3",
                        "PEE_max_seg_1","PEE_max_seg_2","PEE_max_seg_3"]]



def calcular_cumple(row):
    estado = row["id_estado"]
    segmento = row["SEG_DCP"]
    cant_reviews = row["cant_reviews"]
    valoracion_promedio = row["valoracion_promedio"]
    rest_id = row['gmap_id']

    # Obtener los valores de DCP_prom y PEE_prom correspondientes al estado y segmento
    DCP_prom = df_estados[(df_estados["id_estado"] == estado)][f"Ind_DCP_prom_seg_{segmento}"].values[0]
    PEE_prom = df_estados[(df_estados["id_estado"] == estado)][f"PEE_prom_seg_{segmento}"].values[0]

    # Calcular las condiciones y asignar 1 o 0
    DCP_cumple = 1 if cant_reviews > DCP_prom else 0
    PEE_cumple = 1 if valoracion_promedio > PEE_prom else 0

    return pd.Series({'gmap_id': rest_id, "DCP_cumple": DCP_cumple, "PEE_cumple": PEE_cumple})


restaurantes_final = pd.merge(restaurantes_final, restaurantes_final.apply(calcular_cumple, axis=1), on='gmap_id')


reviews_final.to_csv('gs://data-procesada/google-maps/reviews_google.csv', index=False)
restaurantes_final.to_csv('gs://data-procesada/google-maps/restaurantes_google.csv', index=False)
df_estados.to_csv('gs://data-procesada/google-maps/estados_google.csv', index=False)