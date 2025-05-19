import json
import pickle
import numpy as np


class ModeloML:
    def __init__(self, model_path, scaler_path):
        with open(model_path, 'rb') as file:
            self.model = pickle.load(file)
        with open(scaler_path, 'rb') as file:
            self.scaler = pickle.load(file)

    def predecir_pruebas(self, data):
        try:
            print((data['feature']))
            resultado = self.model.predict([data['feature']])[0]
            return resultado, None
        except Exception as e:
            return None, str(e)

    def predecir_ann(self, data):
        try:
            np_x = np.array(data)
            x_new = self.scaler.transform(np_x.reshape(1, -1))
            resultado = self.model.predict(x_new)
            print(resultado)
            # json_obj = {0: round(float(resultado[0][0]), 4), 1: round(float(resultado[0][1]), 4)}
            # json_string = json.dumps(json_obj)
            return [round(float(resultado[0][0]), 4), round(float(resultado[0][1]), 4)] , None
        except Exception as e:
            return None, str(e)
