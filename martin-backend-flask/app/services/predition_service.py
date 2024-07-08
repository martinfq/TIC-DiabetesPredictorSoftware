from ..services.models import ModeloML

modelo = ModeloML('model.pkl')


def process_data(data):
    return modelo.predecir(data)
