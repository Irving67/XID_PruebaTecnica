import re

import nltk

from nltk.tokenize import RegexpTokenizer
from nltk.tokenize.treebank import TreebankWordDetokenizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from tensorflow.keras.preprocessing.text import Tokenizer


nltk.download('stopwords')
nltk.download('punkt_tab')
stop_words = stopwords.words('spanish')


def stopwords_filter(sentence):
    """Este método filtra las stopwords de un texto

    Args:
        sentence (str): Texto a filtrar

    Returns:
        str: Texto en minúculas, sin stop words, y sin números o caracteres especiales
    """

    try:
        # Filtrado de stopword
        tokens = word_tokenize(sentence.lower())
        texto_filtrado = ' '.join([palabra for palabra in tokens if(palabra not in stop_words and len(palabra) > 2)])

        # Remover acentos
        texto_filtrado = texto_filtrado.replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u")
        # Remover espacios múltiples
        texto_filtrado = re.sub(r'\s+', ' ', texto_filtrado)
        # Filtrado de signos de puntuación
        tokenizer = RegexpTokenizer(r'[a-zñ]+')
        # Tokenización del resultado
        result = tokenizer.tokenize(texto_filtrado)
        # Agregar al arreglo los textos "destokenizados" (Como texto nuevamente)
        return str(TreebankWordDetokenizer().detokenize(result))
    
    except Exception as err:
        return "Process Error: " + str(err)
