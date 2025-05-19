from ..services.models import ModeloML

modelo = ModeloML('modelANN.pkl', 'scalerANN.pkl')


def process_data(data):
    return modelo.predecir_ann(data)
