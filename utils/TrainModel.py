import logging

from flask_restful import Resource
from flask import request
import pandas as pd
from sklearn.model_selection import train_test_split


# Configuración de logs
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s -  %(name)s - %(message)s'
)


class TrainModel(Resource):

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def post(self):
        """
        Este servicio se encarga de entrenar el modelo para un conjunto de tipos de texto específicos

        Returns:
            string: Mensaje que muestra que se ha actualizado el DataSet
        """
        input_data = request.json
        topic_list = input_data["topic_list"]
        data_name = input_data["dataset_name"]

        (df_train, df_test) = self.get_examples(topic_list, data_name)

        return "OK"

    def get_examples(self, topic_list, data_name):
        """
        Este método toma un dataset y una lista de tópicos que se desean considerar para generar un
        dataset nuevo para el entrenamiento, y uno para el test de un modelo a entrenar

        Args:
        topic_list (list): Lista de strings con los tópicos a filtrar del dataset.
            Ejemplo: ["elpais actualidad", "internacional actualidad", "sociedad actualidad", "deportes actualidad"]
        dataset_name (str): Nombre del archivo CSV a cargar, incluyendo la extensión.
            Ejemplo: 'dataset.csv'

        Returns:
        tuple: Una tupla con dos DataFrames de pandas:
            - df_train (pd.DataFrame): Dataset de entrenamiento (80% de los datos)
            - df_test (pd.DataFrame): Dataset de prueba (20% de los datos) 
        """

        try:
            # Lectura del CSV en el directorio local y creación de Dataset simplificado
            df = pd.read_csv('../app/data/' + data_name)
            df_simple = df[['text', 'summary', 'topic', 'title']]

            # Filtramos solo los elementos del Dataset que contengan los tópicos de la lista
            df_topic = df_simple[df_simple['topic'].isin(topic_list)].copy()

            # Dividir manteniendo proporciones por topic
            df_train, df_test = train_test_split(
                df_topic, 
                test_size=0.2, 
                stratify=df_topic['topic'], 
                random_state=42
                )

            # Recuento de elementos por categoría
            for t in topic_list:
                self.logger.info("La cantidad de ejemplos de " + t + "es: Entrenamiento -> " + str((df_train['topic'] == t).sum()) + " Test -> " + str((df_test['topic'] == t).sum()))

            return (df_train, df_test)

        except Exception as err:
            return "Process Error: " + str(err)
