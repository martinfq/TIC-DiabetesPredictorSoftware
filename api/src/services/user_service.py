from repositories.users_repository import *
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

