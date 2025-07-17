# Clasificador de textos "Noticias Globales"

El presente proyecto pretende ser un centro de trabajo (suit de desarrollo) que permita el entrenamiento de modelos para la clasificación de noticias de diferentes tipos, basadas en el dataset "mlsum" de HuggingFaces en su versión en Español.


## Authors

- [@IrvingUribe](https://github.com/Irving67/)


## Installation

#### Creamos una imagen de docker 
```bash
docker build -t azteca:1.0.0 .
```

#### Corremos la imagen de Docker
```bash
docker run -p 8000:8000 azteca:1.0.0
```

Deberías de ver el siguiente mensaje en pantalla
```bash
* Running on all addresses (0.0.0.0)
* Running on https://localhost:8000
```
    
## API Reference

Una vez levantado el servicio, dispondrás de varios endpoints con los que podrás interactuar con el servicio:

#### Health Check

Este endpoint, al invocarlo, regresa un estatus "Ok" si el servicio está dado de alta

```http
  GET http://localhost:8000/
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
|           |          | No se requieren argumentos |

#### MLSUM

Este endpoint, se encarga de descargar y particionar una parte dle dataser MLSUM de Hugging Faces en español que contiene noticias en español separadas por categorías. Con el campo 'train_split_per' ouedes definir el porcentaje de dicisión del dataset que deseas.

```http
  POST http://localhost:8000/MLSUM
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `dataset_name`  | `string` | **Obligatorio**. Nombre del archivo donde quieres guasdar el df |
| `train_split_per`  | `int` | **Obligatorio**. Valor numérico del 0 al 100 del % de split deseado para los datos de entrenamiento |

Ejemplo:
```bash
{
    "dataset_name": "dataset.csv",
    "train_split_per": 2
}
```

#### Train Model

Este endpoint realiza el entrenamiento de un modelo de clasificación utilizando una red lstm y bajo los parámetros de entrenamiento dfinidos por el usuario, por ejemplo, la cantidad de épocas de entrenamiento definidas por el usuario, y el batchsize definido

```http
  POST http://localhost:8000/MLSUM
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `dataset_name`  | `string` | **Obligatorio**. Nombre del archivo (dataframe) a usar para entrenar |
| `topic_list`  | `str list` | **Obligatorio**. Lista de las categorías con las que se quiere entrenar |
| `max_tokens`  | `str list` | **Obligatorio**. Número máximo de tokens (palabras) consideradas por texto |
| `batch_size_train`  | `str list` | **Obligatorio**. Batch size para el entrenamiento del modelo |
| `epochs`  | `str list` | **Obligatorio**. Cantidad de épocas para el entrenamiento del modelo |

Ejemplo:
```bash
{
    "dataset_name": "dataset.csv",
    "topic_list": [
        "deportes",
        "economia",
        "cultura",
        "internacional"
    ],
    "max_tokens": 300,
    "batch_size_train": 4,
    "epochs": 10
}
```


# Áreas de mejora.

Al momento de entrega de este proyecto, se cuenta con algunos puntos muy importantes tales como, el entrenamiento de un modelo basado en redes lstm, la creación de un dataset sintético para las categorías seleccionadas por el usuario, y la parametrización de algunas cosas como el entrenamiento del modelo, mismo que tiene un pipeline de preprocesamiento. Todo esto acompañado de buenas prácticas de desarrollo.

Si se contara con una mayor tiempo para trabajar en este servicio, se visualizan varios puntos que podrían mejorar todo el proceso, entre los cuales, se destacan:

- Aplicación de más mecanismos de preprocesamiento como aplicar tf-idf para filtrado de palabras rleevantes
- Mejora en la implementación de los logs (Mas de ellos en procesos de inicio y finalización de actividades)
- Parametrización de algunos otros puntos como las rutas de almacenamiento de modelos y tokenizadores
- La experimentación con mas fuentes de embeddings como glove, o word2vect
- Uso de un dataset mas grande, ya que los accuracys obtenidos pueden ser relativamente bajos debido a que se tiene una alta variabilidad en los datos, pero también se tiene una baja muestra en comparación al total de datos que se pueden obtener (También se necesita un equipo poderoso para ello o una instancia de procesamiento de pago)
- Mejoras generales en la estructura del código, encapsulando mas procesos que pueden ser comunes o esclables a lo largo del entrenamiento y manipulación de los modelos

QUEDA PENDIENTE LA INTEGRACIÓN DEL ENDPOINT PARA EL PREDICT DEL MODELO, SE SUBIRÁ EN LA SIGUIENTE PR LO ANTES POSIBLE.