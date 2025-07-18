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


#### Predict

Este endpoint realiza una inferencia, y regresa la clase a la que pertence el texto enviado por el usuario (según el modelo que se haya seleccionado)

```http
  POST http://localhost:8000/MLSUM
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `model`  | `model` | **Obligatorio**. Nombre del archivo (modelo) a usar para realizar la predicción |
| `max_tokens`  | `str list` | **Obligatorio**. Número máximo de tokens (palabras) consideradas por texto, debe coincidir con el entrenamiento |
| `text`  | `str` | **Obligatorio**. Texto a evaluar |

Ejemplo:
```bash
{
    "model": "lstm_model_acc_35.6572.h5",
    "max_tokens": 300,
    "text": "De momento, no podemos responder a la pregunta frivolona que toda España se hace hoy, además de por qué bebí tanto anoche. ¿Qué cadena ganó en la retransmisión de las campanadas? Los sentimos, Sofres no ofrece hoy los datos por ser festivo. Los contendientes fueron el colegueo de Los Manolos, Manu Carreño y Manolo Lama (Cuatro), la gracia y juventud de los actores Antonio Garrido y Patricia Montero (Antena 3), el morboso dúo Sálvame, Javier Vázquez y Belén Esteban (Telecinco), el valor seguro de Anne Igartiburu en TVE-1 y el humor inteligente de Berto y Ana Morgade (La Sexta). Por primera vez en 13 años, Ramón García, el entrañable Ramontxu que aguantaba el frío como nadie bajo su capa, no estaba ante las cámaras. El menú para las últimas que los españoles vieron en el sistema analógico -el próximo 3 de abril todas las emisiones pasan a la TDT-, era de lo más variadito. La clásica TVE encargó por quinta vez la retransmisión a Anne Igartiburu, esta vez junto al actor Manuel Bandera, debutante. Entalladísima, escotadísima y de rojo Lorenzo Caprile, la sobria y correcta Igartiburu sobrevivió a duras penas al frío mientras todos sufríamos por ella. Antena 3, en cuya web se echan en falta los reflejos de destacar alguna referencia o vídeo resumen de lo sucedido anoche, viajó a la plaza del Obradoiro de Santiago de Compostela con motivo del nuevo año Xacobeo mientras Berto y Morgade daban en La Sexta hilarantes consejos para superar la resaca del día siguiente o cómo comportarse si toca visitar la casa de los suegros -ni rastro en su web, pero sí en las de sus fans. Cuatro, a la que tan buen resultado dio la Eurocopa, empezó desde el primer día a celebrar el año del Mundial de Fútbol con Carreño y Lama desplazados a Suráfrica. La Campos y la Esteban Sin datos en la mano, la impresión general es que el grueso de la audiencia vio las campanadas en TVE-1 por la fuerza de la tradición, pero muchos de los televidentes estaban con un ojo puesto en el pre y el post de Telecinco, con la Esteban en su salsa: una cabeza por encima de Jorge Javier gracias a sus taconazos, vestida de azul cobalto marca Versace, enseñando la liga roja y saludando a grito limpio a su hija -'Andrea te quiero'- padres, pareja y demás familia. Es muy posible que la cadena privada haya recortado distancias con La Primera, que el año pasado se llevó el gato al agua con más de 5,5 millones de personas y un 39% de cuota de pantalla. Según la encuesta no científica abierta en ELPAÍS.com, con 2.000 votos a las siete y media de la tarde, barrió la pública con un 56%, mientras que Telecinco se hizo con un 25% de la tarta. Las demás no llegaban ni al 10%. Más allá del sin vivir de saber qué pasó finalmente, aún hay más. Para todos los que se lo perdieron o, incluso, se quedaron con ganas de más, Telecinco explota el filón el sábado. María Teresa Campos presentará este sábado (18.00) en Telecinco un especial dedicado a Belén Esteban, en el que se revisará su (corta y polémica) biografía y el fenómeno mediático en el que la han convertido. Belén da la campanada ofrecerá además un making of de la retransmisión de las campanadas en Telecinco, así como los mejores momentos de la Nochevieja, unos vídeos que ya han colgado en su web, entregada hasta la extenuación al evento: los exóticos consejos para tener suerte el año que viene, el don de lenguas del premio Ondas 2009 al mejor presentador, que felicitó el año en todos los idiomas oficiales y la explicación de la colaboradora de cómo tomar las uvas. El espacio hará un repaso cronológico de la vida de la Esteban desde el momento en el que una completa desconocida comenzó a aparecer en los medios en 1998 como la novia de Jesulín de Ubrique hasta llegar a hoy en día, convertida en la princesa del pueblo, en concreto del popular madrileño distrito de San Blas donde vive, tal y como algunos la han calificado, y protagonista de portadas de revistas, diarios y portales web y de aparecer incluso entre los personajes más populares de Google. Junto a María Teresa Campos, estarán en el plató Patricia Pérez, presentadora del programa matinal de los sábados en Telecinco Vuélveme loca, quien ha conducido las campanadas en cuatro ocasiones, y los comentaristas Maribel Escalona, Emilio Pineda y José Manuel Parada."
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