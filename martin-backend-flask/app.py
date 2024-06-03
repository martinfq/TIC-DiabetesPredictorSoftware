from flask import Flask, request, jsonify
from model import ModeloML

# Crea una instancia de la aplicación Flask
app = Flask(__name__)

# Instancia el modelo de Machine Learning
modelo = ModeloML('model.pkl')

# Define el único endpoint
@app.route('/', methods=['POST'])
def index():
    # Obtiene los datos JSON del cuerpo de la solicitud
    data = request.json

    # Procesa los datos utilizando el modelo de Machine Learning
    resultado, error = modelo.predecir(data)

    if error:
        # Si hay un error en el modelo, devuelve un mensaje de error y un código de estado 400
        return jsonify({'error': error}), 400
    else:
        # Si no hay errores, devuelve el resultado como JSON y un código de estado 200
        return jsonify({'resultado': resultado}), 200


# Ejecuta la aplicación si este archivo se ejecuta directamente
if __name__ == '__main__':
    app.run(debug=True)
