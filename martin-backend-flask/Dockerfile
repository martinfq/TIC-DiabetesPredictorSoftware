# Usa Python 3.12 como imagen base
FROM python:3.12-bookworm

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

RUN apt-get update

# Copia los archivos de la aplicación al contenedor
COPY . .

# Instala las dependencias de la aplicación
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto 5000 (el predeterminado de Flask)
EXPOSE 5000

# Comando de entrada predeterminado para iniciar Gunicorn
# Cambiamos el puerto a 5000 en el binding de Gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:create_app()"]
