import spacy

# Cargar el modelo en español
nlp = spacy.load("es_core_news_md")


def lematizer_tokens(text):
    """Este método lematiza las palabras para llevarlas a su forma raiz

    Args:
        sentence (str): Texto a lematizar

    Returns:
        str: Texto lematizado
    """

    try:
        # Tokenización del texto:
        doc = nlp(text)

        # Extraer los lemmas
        lemmas = [token.lemma_ for token in doc]

        # Convertir de vuelta a texto
        texto_lematizado = ' '.join(lemmas) 

        return texto_lematizado
    
    except Exception as err:
        return "Process Error: " + str(err)
