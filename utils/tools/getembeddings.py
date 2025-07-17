import numpy as np
from tensorflow.keras.preprocessing.sequence import pad_sequences
import spacy

# Cargar el modelo de spaCy
nlp = spacy.load("es_core_news_md")


def get_embeddings(X_train, y_train, tokenizer, embedding_dim=300):
    """
    Entrena un modelo de machine learning con los datos proporcionados.

    Args:
        X_train (list): Lista de secuencias de texto tokenizadas.
        y_train (list): Lista de etiquetas correspondientes a las secuencias de texto.
        tokenizer (Tokenizer): Tokenizador utilizado para generar las secuencias.
        spacy_model (str): Nombre del modelo de spaCy a usar para los embeddings.
        embedding_dim (int): Dimensión de los embeddings preentrenados.

    Returns:
        str: Mensaje indicando el resultado del entrenamiento.
    """
    try:
        # Crear la matriz de embeddings
        vocab_size = len(tokenizer.word_index) + 1
        embedding_matrix = np.zeros((vocab_size, embedding_dim))
        for word, i in tokenizer.word_index.items():
            # Obtener el vector del modelo de spaCy
            if word in nlp.vocab:
                embedding_vector = nlp.vocab[word].vector
                if embedding_vector is not None and len(embedding_vector) > 0:
                    embedding_matrix[i] = embedding_vector

        # Asegurarse de que las secuencias tengan la misma longitud
        max_length = max(len(seq) for seq in X_train)
        X_train_padded = pad_sequences(X_train, maxlen=max_length, padding='post')

        # Aquí se implementaría el código para entrenar el modelo
        print("X_train_padded shape:", X_train_padded.shape)
        print("y_train shape:", y_train.shape)
        print("Embedding matrix shape:", embedding_matrix.shape)

        return X_train_padded, embedding_matrix

    except Exception as err:
        return "Error al entrenar el modelo: " + str(err)