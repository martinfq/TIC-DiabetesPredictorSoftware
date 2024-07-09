class Usuario:    
    def __init__(self, fechaNacimiento, genero, nombre, password):
        self.fechaNacimiento = fechaNacimiento
        self.genero = genero
        self.nombre = nombre
        self.password = password
    
#Minuscula, mayuscula, numero, caracter especial, longitud 8. 
#Genero M, F
#Nombre Caracteres 
#Fecha de nacimiento 
#Correo, Marshmallow
    def is_valid():
        if(fechaNacimiento is None or genero is None or nombre is None  or password is None):
            return False
        return True

    
    def data(self):
        return {
            "fechaNacimiento" : self.fechaNacimiento,
            "genero" : self.genero,
            "nombre" : self.nombre,
            "password" : self.password
        }
