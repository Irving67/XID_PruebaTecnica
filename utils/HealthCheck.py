import logging

from flask_restful import Resource


# Configuración de logs
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s -  %(name)s - %(message)s'
)


class Health(Resource):

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def get(self):
        """Este método regresa un mensaje para demostrar que el servicio está
        dado de alta

        Returns:
            dict: Regresa una respuesta de "Servicio disponible" y status 200
        """

        result = {"status": "Serivcio disponible"}
        self.logger.info("Servicio Ok")

        return result, 200
