# Librerías de dependencia
from flask import Flask
from flask_restful import Api
from flask_swagger_ui import get_swaggerui_blueprint

# Dependencias dentro del proyecto
from utils.HealthCheck import Health
from utils.MLSUM_Get import MLSUM_Get
from utils.TrainModel import TrainModel
from utils.Predict import Predict

# Inicializamos la aplicación de Flask
app = Flask(__name__)
api = Api(app)

# Endpoints (servicios)
api.add_resource(Health, "/", endpoint="health")
api.add_resource(MLSUM_Get, "/MLSUM",
                 endpoint="MLSUM")
api.add_resource(TrainModel, "/train_model",
                 endpoint="train_model")
api.add_resource(Predict, "/predict",
                 endpoint="predict")

# Configuración del swagger
SWAGGER_URL = '/docs'
API_URL = '/static/swagger.json'

SWAGGER_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "llm API"
    }
)
app.register_blueprint(SWAGGER_BLUEPRINT, url_prefix=SWAGGER_URL)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
