import re, hashlib
from datetime import datetime


class Usuario:    
    def __init__(self, fechaNacimiento, genero, nombre, last_name, email, password):
        self.fechaNacimiento = fechaNacimiento
        self.genero = genero
        self.nombre = nombre
        self.last_name = last_name
        self.email  = email
        self.password = password
    

    def is_valid(self):

        try:
            #Email
            if not re.match("^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", self.email):
                return False

            #Password
            if not re.match("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!#@$])[A-Za-z\d!#@$]{8,}$", self.password):
                return False

            #Nombre
            if not re.match("^[A-Za-z]+$", self.nombre):
                return False

            #Last Name
            if not re.match("^[A-Za-z]+$", self.last_name):
                return False

            #Genero
            self.genero = self.genero.upper()
            if self.genero != "M" and self.genero != "F":
                return False

            #Fecha
            if not re.match("^\d{4}-\d{1,2}-\d{1,2}$", self.fechaNacimiento):
                return False

            try:
                datetime.strptime(self.fechaNacimiento, '%Y-%m-%d')
            except ValueError:
                return False

            self.password = hashlib.sha256(self.password.encode()).hexdigest()
        except Exception as e:
            return False   
        
        return True

    
    def data(self):
        return {
            "fechaNacimiento" : self.fechaNacimiento,
            "genero" : self.genero,
            "nombre" : self.nombre,
            "email"  : self.email,
            "password" : self.password
        }
