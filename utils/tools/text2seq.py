from tensorflow.keras.preprocessing.sequence import pad_sequences


def text_2_seq(vector, max_tokens, tokenizer):
    """Este método genera un vector con un padding según la cantidad máxima de tokens

    Args:
        sentence (str): Vector a convertir según tokenizador y padding

    Returns:
        str: Vector con tokenización por diccionario y padding
    """

    try:
        # Si el vector es una lista, lo convertimos a string
        if isinstance(vector, list):
            vector = " ".join(vector)

        # Transforma cada texto en una secuencia de valores enteros
        return tokenizer.texts_to_sequences([vector])[0][:max_tokens]

    except Exception as err:
        return "Process Error: " + str(err)
