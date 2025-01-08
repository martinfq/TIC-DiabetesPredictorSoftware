from flask import Flask, jsonify
from app import create_app

app = create_app()

# Manejo de errores global
@app.errorhandler(401)
def unauthorized_error(e):
    return jsonify({"message": str(e)}), 401

@app.errorhandler(500)
def internal_server_error(e):
    return jsonify({"message": "Ocurrió un error en el servidor"}), 500

if __name__ == "__main__":
    app.run(debug=True)