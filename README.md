
## Reviews de Google por Estado

Inicialmente, se nos proporcionan datos de reseñas de Google organizados por estado. Estos datos se presentan en forma de archivos JSON, que no son tabulares por naturaleza.

En el script `reviews_state.ipynb`, hemos desarrollado un algoritmo que permite recorrer cada carpeta correspondiente a un estado y seleccionar cada archivo JSON. Luego, integramos todos estos archivos en un único archivo final para cada estado.

A continuación, creamos un DataFrame utilizando la biblioteca Pandas a partir de este archivo, y agregamos un campo "State" que contiene la abreviatura del estado. Además, convertimos el formato de tiempo de milisegundos a una fecha legible.

Finalmente, almacenamos el archivo resultante en formato Parquet para reducir su tamaño en megabytes (MB).

## Metadata de Sitios en Google

Los datos de Metadata de Sitios en Google se presentan en archivos JSON separados por comercio. Cada archivo contiene información relevante, como Nombre, Id, Cantidad de Reseñas, Calificación, Longitud, Latitud, Dirección y otros datos relacionados con cada comercio.

En el script `estados_meta_google.ipynb`, cargamos cada archivo en un DataFrame y realizamos una eliminación inicial de datos duplicados. Luego, creamos una columna "estados" y asignamos la abreviatura del estado al que pertenece, basándonos en la información de dirección proporcionada en los datos.

Dado que el DataFrame contiene información de todos los estados, generamos un filtro para seleccionar los comercios de los estados preseleccionados. Posteriormente, creamos un nuevo DataFrame que contiene solo los comercios correspondientes a cada estado en cada archivo JSON.

En última instancia, creamos un DataFrame final que contiene los comercios seleccionados por estado en cada archivo JSON.

## API de YELP

En un análisis preliminar de los datos de YELP, observamos que el archivo que contenía información sobre negocios en el territorio nacional se centraba principalmente en el estado de Florida.

Debido a esta limitación, decidimos obtener información adicional mediante el consumo de la API de YELP.

- Esta API permite un máximo de 1000 resultados por consulta.
- Para realizar una consulta, ingresamos una abreviatura o nombre de ciudad para especificar la ubicación deseada.
- Para utilizar la API, primero generamos una API_KEY registrándonos en YELP y debemos agregar "Bearer" antes de la API_KEY en las solicitudes.
- La API nos proporciona un código inicial para generar consultas desde otro entorno, y un código de respuesta exitosa es "200".
- El formato de respuesta de la API es JSON.

## Google Function - API YELP

Después de consumir la API de YELP, fue necesario automatizar el proceso de búsqueda y almacenamiento de datos utilizando Google Cloud Platform.

Google Functions permitió la implementación de nuestro script de Python para consumir la API y almacenar los datos en Google Storage. Desde Google Storage, podemos acceder a los datos para realizar análisis o crear modelos de recomendación.

- Google Functions es un servicio en la nube que permite la implementación de scripts.
- Puede ejecutarse de manera automatizada y sin problemas.
- Permite asignar recursos de RAM y CPU según las necesidades de la tarea.
- Ofrece entornos de ejecución para Python, Node, Go y otros lenguajes.
- El archivo "main.py" ejecuta nuestra Function con la tarea a realizar, y en "requirements.txt" se declaran las bibliotecas necesarias.

Para obtener una descripción detallada de cómo implementamos Google Functions para obtener los datos de YELP y almacenarlos en un Bucket de Google Storage, consulte el archivo "FuncionYelp.ipynb".

### Stack Tecnologico
![Stack Tecnologico](./Imagenes/stack_tecnologico.jpg)