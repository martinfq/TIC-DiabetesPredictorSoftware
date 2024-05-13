from flask import Flask

# Crea una instancia de la aplicación Flask
app = Flask(__name__)

# Define el único endpoint
@app.route('/')
def index():
    return '¡Hola, mundo! Esta es mi primera aplicación Flask.'

# Ejecuta la aplicación si este archivo se ejecuta directamente
if __name__ == '__main__':
    app.run(debug=True)
