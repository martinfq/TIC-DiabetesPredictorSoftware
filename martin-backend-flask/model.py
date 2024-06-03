import pickle

class ModeloML:
    def __init__(self, modelo_path):
        with open(modelo_path, 'rb') as model_file:
            self.modelo = pickle.load(model_file)

    def predecir(self, datos):
        try:
            resultado = self.modelo.predict([datos['feature']])[0]
            return resultado, None
        except Exception as e:
            return None, str(e)
