import logging

from flask_restful import Resource
from flask import request
import pandas as pd
from sklearn.model_selection import train_test_split

from utils.tools.stopwords import stopwords_filter


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
        try:
            input_data = request.json
            topic_list = input_data["topic_list"]
            data_name = input_data["dataset_name"]

            # Obtenemos los nuevos datasets solo con la información de los tópicos deseados al 80% y 20%
            self.logger.info(self.get_examples(topic_list, data_name))
            df_train, df_test = self.get_examples(topic_list, data_name)

            # Preprocesamiento de la información
            preprocess_train = self.preprocess_pipeline(df_train)
            preprocess_test = self.preprocess_pipeline(df_test)

            return preprocess_train["text"]
        
        except Exception as err:
            return "Process Error: " + str(err)

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
        tuple: Dos DataFrames de pandas:
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

            return df_train, df_test

        except Exception as err:
            return "Process Error: " + str(err)

    def preprocess_pipeline(self, df):
        """
        Aquí se realiza el preprocesamiento del texto en los dataframes correspondientes
        """

        self.logger.info("Preprocesando el Dataframe")
        
        try:
            # Vemos los tópicos únicos
            unique_topics = df['topic'].unique()
            topic_to_number = {topic: i+1 for i, topic in enumerate(unique_topics)}

            df['text_filtered'] = df['text'].apply(stopwords_filter)

            new_df = pd.DataFrame({
                'text': df['text_filtered'],
                'topic': df['topic'],
                'output': df['topic'].map(topic_to_number)
                })

            return new_df

        except Exception as err:
            return "Process Error: " + str(err)
