import logging
import os

from datasets import load_dataset
from flask_restful import Resource
from flask import request
import pandas as pd


# Configuración de logs
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s -  %(name)s - %(message)s'
)


class MLSUM_Get(Resource):

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def post(self):
        """
        Este servicio, escribe en el directorio local /data el dataset de  MLSUM
        con el nombre indicado por el usuario. Es un dataset que contiene noticias por categorías.

        Args:
        train_split_per (int): Porcentaje del dataset de entrenamiento a descargar.
            Debe ser un número entre 1 y 100. Ejemplo: 10 descarga el 10% del dataset.
        dataset_name (str): Nombre del archivo CSV a crear (con extensión .csv).
            Ejemplo: "mlsum_spanish_news.csv"
    
        Returns:
        str: Mensaje de confirmación indicando número total de registros descargados y ruta completa donde se guardó el archivo
        """
        input_data = request.json
        percent = input_data["train_split_per"]
        data_name = input_data["dataset_name"]
        split_arg = "train[:" + str(percent) + "%]"

        try:
            self.logger.info("Descargando dataset desde Hugging Faces")

            dataset = load_dataset("mlsum", "es", split=split_arg, trust_remote_code=True)
            # Acceder al conjunto de entrenamiento
            texts = dataset['text']
            summaries = dataset['summary']
            topics = dataset['topic']
            urls = dataset['url']
            dates = dataset['date']
            titles = dataset['title']

            self.logger.info("Dataset Descargado correctamente")

            df = pd.DataFrame(
                {
                    'text': texts,
                    'summary': summaries, 
                    'topic': topics,
                    'url': urls,
                    'title': titles,
                    'date': dates
                    }
                )

            self.logger.info("Escribiendo archivo en el directorio local")
            
            # Guardado del DataFrame
            cwd = os.getcwd()
            path = cwd + "/data/" + data_name
            df.to_csv(path)

            self.logger.info("Archivo escrito con éxito")

            return "Se escribió el nuevo dataset con " + str(len(df)) + " registros. En " + str(path)

        except Exception as err:
            return "Process Error: " + str(err)
