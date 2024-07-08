import os
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'you-will-never-guess')
    MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/Tesis')
    DEBUG = True