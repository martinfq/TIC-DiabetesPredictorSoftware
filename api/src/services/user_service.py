from repositories.users_repository import *
from datetime import datetime
import hashlib, jwt


class UserService:
    def crear_usuario(self, usuario):
        
        #VALIDACION DEL DOMINIO DE LOS CAMPOS
        if not usuario.is_valid():
            return 'CUERPO DE LA SOLICITUD INCORRECTO.', 400

        #VALIDACION PARA ASEGURAR UNICIDAD DE USUARIO
        if self.usuario_existe(usuario.email):
            return 'ERROR. YA EXISTE UN USUARIO CON ESTE CORREO', 400

        resultado = crear_usuario(usuario)
        return "Correcto funcionamiento", resultado

    
    def generar_tokenSession(self, email, password):
       
        if email is None or password is None:
            return 'CREDENCIALES INCORRECTAS.', 400

        credenciales = validar_credenciales(email, password)
        if not self.usuario_existe(email) or not credenciales:
            return 'CREDENCIALES INCORRECTAS.', 400

        #CREACION DEL TOKEN DE USUARIO
        token_session = jwt.encode({'email': email, 'id' : credenciales[1]}, "passPrueba", algorithm='HS256')
        return token_session, 200


    def usuario_existe(self, email):
        return usuario_creado(email)


    def datos_usuario(self, user_id):
        datos_usuario = obtener_datos_usuario(user_id)
        if(datos_usuario == None):
            return 'EL USUARIO NO EXISTE', 400

        datos_usuario["age"] = self.calcular_edad(datos_usuario["age"])
        return datos_usuario, 200

    
    def calcular_edad(self, fechaNacimiento):
        fechaNacimiento = datetime.strptime(fechaNacimiento, "%Y-%m-%d")
        fechaActual = datetime.now()
        edad = fechaActual.year - fechaNacimiento.year
        if (fechaActual.month, fechaActual.day) < (fechaNacimiento.month, fechaNacimiento.day):
            edad -= 1
        return str(edad)