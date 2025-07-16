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


