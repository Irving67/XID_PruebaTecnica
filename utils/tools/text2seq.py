from tensorflow.keras.preprocessing.sequence import pad_sequences


def text_2_seq(vector, max_tokens, tokenizer):
    """Este método genera un vector con un padding según la cantidad máxima de tokens

    Args:
        sentence (str): Vector a convertir según tokenizador y padding

    Returns:
        str: Vector con tokenización por diccionario y padding
    """

    try:
        # Transforma cada texto en una secuencia de valores enteros
        X_seq = tokenizer.texts_to_sequences(vector)

        # Especificamos la matriz (Con padding de posiciones iguales a maxlen)
        padded = pad_sequences(X_seq, padding='post', maxlen=max_tokens)
        return padded
    
    except Exception as err:
        return "Process Error: " + str(err)
