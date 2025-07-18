import os
import pickle
import logging

from flask_restful import Resource
from flask import request
from tensorflow.keras.models import load_model
import numpy as np

from utils.tools.stopwords import stopwords_filter
from utils.tools.lematizer import lematizer_tokens
from utils.tools.text2seq import text_2_seq

# Configuración de logs
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(message)s'
)


class Predict(Resource):
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def post(self):
        """
        Este método realiza una predicción utilizando un modelo previamente entrenado y un tokenizador.
        """
        try:
            # Leer el texto enviado por el usuario
            input_data = request.json
            model = input_data["model"]
            user_text = input_data["text"]
            max_tokens = input_data["max_tokens"]

            # Cargar el modelo desde la carpeta data
            model_path = 'data/' + model
            if not os.path.exists(model_path):
                raise FileNotFoundError(f"No se encontró el modelo en la ruta: {model_path}")
            model = load_model(model_path)

            # Cargar el tokenizador desde la carpeta data
            tokenizer_path = 'data/tokenizer.pkl'
            if not os.path.exists(tokenizer_path):
                raise FileNotFoundError(f"No se encontró el tokenizador en la ruta: {tokenizer_path}")
            with open(tokenizer_path, 'rb') as handle:
                tokenizer = pickle.load(handle)

            # Preprocesar el texto del usuario
            self.logger.info("Preprocesando el texto del usuario...")
            preprocessed_text = stopwords_filter(user_text)
            preprocessed_text = lematizer_tokens(preprocessed_text)

            # Convertir el texto a secuencia# Ajustar según el valor usado en el entrenamiento
            text_sequence = text_2_seq(preprocessed_text, max_tokens, tokenizer)

            # Asegurarse de que text_sequence sea un arreglo NumPy y tenga la forma correcta
            if not isinstance(text_sequence, np.ndarray):
                text_sequence = np.array(text_sequence)

            # Expandir dimensiones para incluir el batch (si es necesario)
            if len(text_sequence.shape) == 1:  # Si es un arreglo unidimensional
                text_sequence = np.expand_dims(text_sequence, axis=0)

            # Realizar la predicción
            self.logger.info("Realizando la predicción...")
            prediction = model.predict([text_sequence])
            predicted_class = prediction.argmax(axis=-1)

            #return str(preprocessed_text)
            return {"predicted_class": int(predicted_class), "confidence": float(prediction.max())}

        except Exception as err:
            self.logger.error(f"Error en la predicción: {str(err)}")
            return {"error": str(err)}
