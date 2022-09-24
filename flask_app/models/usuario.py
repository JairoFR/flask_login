import os
import re
from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.base_modelo import BaseModelo
from flask_bcrypt import Bcrypt        


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User(BaseModelo): #Cambiar a nombre de modelo en singular  

    modelo = 'usuarios' #nombre de tabla
    columnas_tabla = ['usuario', 'nombre', 'apellido', 'email', 'password'] #campos de columnas sin creted_at y update_at

    def __init__( self , data ):
        self.id = data['id']
        self.nombre= data['usuario']  
        self.apellido = data['nombre']
        self.email = data['apellido']
        self.created_at = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    

    @classmethod
    def get_by_email(cls, data):
        
        query = "SELECT * FROM usuarios WHERE  email = %(dato)s"
        data = { 'dato' : data }
        results = connectToMySQL(os.environ.get("BASE_DATOS_NOMBRE")).query_db(query, data)
    
        # no se encontró un usuario coincidente
        if len(results) < 1:
            return False
        return cls(results[0])

    @staticmethod
    def validar(data):  

        # query = "SELECT * FROM validaciones WHERE email = %(email)s;"
        # results = connectToMySQL(os.environ.get("BASE_DATOS_NOMBRE")).query_db(query,data)

        # if len(results) >= 1:
        #     flash("Email ya existe.","error")
        #     is_valid=False

        is_valid = True
        if len(data['usuario']) <= 2:
            flash(f'El usuario  no puede ser menor a 2', 'error')
            is_valid = False
        
        if len(data['nombre']) <= 2:
            flash(f'El nombre no puede ser menor a 2', 'error')
            is_valid = False

        if len(data['apellido']) < 2:
            is_valid = False
            flash("El apellido no puede ser menor a 2", 'error')

        if not EMAIL_REGEX.match(data['email']): 
            flash("Direccion de email invalida!","error")
            is_valid = False
        
        if data['password'] != data['cpassword']:
            is_valid = False
            flash("Las contraseñas no coinciden!","error")
        
        if len(data['password']) < 8:
            is_valid = False
            flash("La contraseña debe tener minimo de 8 caracteres", 'error')

        return is_valid


