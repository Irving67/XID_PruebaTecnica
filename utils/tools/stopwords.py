import re

import nltk

from nltk.tokenize import RegexpTokenizer
from nltk.tokenize.treebank import TreebankWordDetokenizer
from nltk.corpus import stopwords
from tensorflow.keras.preprocessing.text import Tokenizer


nltk.download('stopwords')
stop_words = stopwords.words('spanish')


def stopwords_filter(sentence):
    """Este método filtra las stopwords de un texto
    """

    try:
        # Filtrado de stopword
        for stopword in stop_words:
            sentence = sentence.replace(" " + stopword + " ", " ")
        sentence = sentence.replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u")
                
        # Remover espacios múltiples
        sentence = re.sub(r'\s+', ' ', sentence)
        # Convertir todo a minúsculas
        sentence = sentence.lower()
        # Filtrado de signos de puntuación
        tokenizer = RegexpTokenizer(r'\w+')
        # Tokenización del resultado
        result = tokenizer.tokenize(sentence)
        # Agregar al arreglo los textos "destokenizados" (Como texto nuevamente)
        return str(TreebankWordDetokenizer().detokenize(result))
    
    except Exception as err:
        return "Process Error: " + str(err)
