import pickle

class ModeloML:
    def __init__(self, model_path):
        with open(model_path, 'rb') as file:
            self.model = pickle.load(file)

    def predecir(self, data):
        try:
            resultado = self.model.predict([data['feature']])[0]
            return resultado, None
        except Exception as e:
            return None, str(e)