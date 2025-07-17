from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Embedding, Dropout, BatchNormalization


def lstm(X_train_padded, embedding_matrix, y_train, X_test, y_test, epochs=20, batch_size=1):
    """
    Entrena un modelo LSTM con los datos proporcionados.

    Args:
        X_train_padded (np.ndarray): Datos de entrada preprocesados y con padding.
        embedding_matrix (np.ndarray): Matriz de embeddings preentrenados.
        y_train (np.ndarray): Etiquetas correspondientes a los datos de entrada.

    Returns:
        str: Mensaje indicando el resultado del entrenamiento.
    """

    try:
        model = Sequential()

        # Capa de embeddings preentrenados
        model.add(Embedding(input_dim=embedding_matrix.shape[0],
                            output_dim=embedding_matrix.shape[1],
                            weights=[embedding_matrix],
                            trainable=False))

        # Primera capa LSTM
        model.add(LSTM(256, return_sequences=True))
        model.add(Dropout(0.5))
        model.add(BatchNormalization())

        # Segunda capa LSTM
        model.add(LSTM(128, return_sequences=True))
        model.add(Dropout(0.5))
        model.add(BatchNormalization())

        # Tercera capa LSTM
        model.add(LSTM(64))
        model.add(Dropout(0.5))
        model.add(BatchNormalization())

        # Capa densa intermedia
        model.add(Dense(64, activation='relu'))
        model.add(Dropout(0.5))

        # Capa de salida
        model.add(Dense(y_train.shape[1], activation='softmax'))

        model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

        # Entrenamiento del modelo
        model.fit(X_train_padded, y_train,
                  epochs=epochs,
                  batch_size=batch_size,
                  validation_split=0.1)

        # Datos del entrenamiento
        print("Modelo LSTM entrenado exitosamente")
        print("Training Loss: {:.4f}".format(model.history.history['loss'][-1]))
        print("Training Accuracy: {:.2f}%".format(model.history.history['accuracy'][-1] * 100))

        final_accuracy = model.history.history['accuracy'][-1] * 100
        formatted_accuracy = f"{final_accuracy:.4f}"

        # Evaluación del modelo
        #test_loss, test_accuracy = model.evaluate(X_test, y_test)
        #print(f"Test Loss: {test_loss:.4f}, Test Accuracy: {test_accuracy:.4f}")

        return model, formatted_accuracy

    except Exception as err:
        return "Error al entrenar el modelo LSTM: " + str(err)
