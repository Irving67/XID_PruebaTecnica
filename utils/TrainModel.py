import logging
import os
import pickle

from flask_restful import Resource
from flask import request
from tensorflow.keras.preprocessing.text import Tokenizer
import pandas as pd
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical  # Importar to_categorical


from utils.tools.lematizer import lematizer_tokens
from utils.tools.lstm import lstm
from utils.tools.stopwords import stopwords_filter
from utils.tools.text2seq import text_2_seq
from utils.tools.getembeddings import get_embeddings


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
            self.max_tokens = input_data["max_tokens"]
            self.batch_size_train = input_data["batch_size_train"]
            self.epochs = input_data["epochs"]

            # Obtenemos los nuevos datasets solo con la información de los tópicos deseados al 80% y 20%
            df_train, df_test = self.get_examples(topic_list, data_name)

            # Preprocesamiento de la información
            preprocess_train = self.preprocess_pipeline(df_train)
            preprocess_test = self.preprocess_pipeline(df_test)

            concat_df = pd.concat([preprocess_train, preprocess_test])

            # Obtenemos la secuencia de texto con un padding
            tokenizer = Tokenizer()
            # Validar que concat_df["text"] es una lista de textos
            if not isinstance(concat_df["text"], pd.Series) or not all(isinstance(text, str) for text in concat_df["text"]):
                raise ValueError("La columna 'text' de concat_df debe contener únicamente cadenas de texto.")

            tokenizer.fit_on_texts(concat_df["text"])

            # Si se desea guardar el tokenizador, se puede hacer con pickle o joblib
            with open('data/tokenizer.pkl', 'wb') as handle:
                pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)

            self.logger.info("Tamaño del vocabulario: " + str(len(tokenizer.word_index)))

            preprocess_train["text"] = preprocess_train["text"].apply(lambda tokens: " ".join(tokens) if isinstance(tokens, list) else tokens)
            preprocess_test["text"] = preprocess_test["text"].apply(lambda tokens: " ".join(tokens) if isinstance(tokens, list) else tokens)

            X_train = [text_2_seq(x, self.max_tokens, tokenizer) for x in preprocess_train["text"]]
            X_test = [text_2_seq(x, self.max_tokens, tokenizer) for x in preprocess_test["text"]]

            # Vemos los tópicos únicos
            unique_topics = topic_list
            self.logger.info("Tópicos únicos encontrados: " + str(unique_topics))

            # Crear un diccionario para mapear los tópicos únicos a índices
            topic_to_index = {topic: idx for idx, topic in enumerate(unique_topics)}

            # Mapear la columna 'output' a índices usando el diccionario
            preprocess_train["output"] = preprocess_train["output"].map(topic_to_index)
            preprocess_test["output"] = preprocess_test["output"].map(topic_to_index)

            # Generar One-Hot Encoding para y_train y y_test
            y_train = to_categorical(preprocess_train["output"].values, num_classes=len(unique_topics))
            y_test = to_categorical(preprocess_test["output"].values, num_classes=len(unique_topics))

            X_train_padded, embedding_matrix = get_embeddings(X_train, y_train, tokenizer)

            self.logger.info("Iniciando el entrenamiento del modelo LSTM...")
            model, accuracy = lstm(X_train_padded, embedding_matrix, y_train, X_test, y_test, self.epochs, self.batch_size_train)
            self.logger.info("Entrenamiento terminado de manera correcta...")

            # Se almacena el modelo para futuras interacciones
            model_filename = f"data/lstm_model_acc_{accuracy}.h5"
            model.save(model_filename)
            self.logger.info(f"Modelo almacenado en {model_filename}")

            return "Entrenamiento exitodso del modelo"

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
            # Verificar si la ruta existe
            file_path = '../app/data/' + data_name
            if not os.path.exists(file_path):
                file_path = 'data/' + data_name  # Ruta alternativa
            
            df = pd.read_csv(file_path)
            df_simple = df[['text', 'summary', 'topic', 'title']]

            # Filtramos solo los elementos del Dataset que contengan las palabras clave de la lista
            pattern = '|'.join(topic_list)  # Crear un patrón con las palabras clave separadas por "|"
            df_topic = df_simple[df_simple['topic'].str.contains(pattern, case=False, na=False)].copy()

            for element in df_topic['topic']:
                for t in topic_list:
                    if t in element:
                        df_topic['topic'] = df_topic['topic'].replace(element, t)

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
            # ----------------------------------------------
            # Pipeline de transformaciones y limpieza
            # ----------------------------------------------
            # Filtrado de StopWords
            df['text'] = df['text'].apply(stopwords_filter)
            # Lematización del Texto y lo tokenizamos
            df['text'] = df['text'].apply(lematizer_tokens) 

            new_df = pd.DataFrame({
                'text': df["text"],
                'topic': df['topic'],
                'output': df['topic']
                })

            return new_df

        except Exception as err:
            return "Process Error: " + str(err)
