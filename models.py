from flask_login import UserMixin
from extentions import db




class CreateUser(UserMixin):
    def __init__(self, _id, name, sede, email, password):
        
        self._id = _id
        self.name = name
        self.sede = sede
        self.email = email
        self.password = password

    @staticmethod
    def is_email_registered(email):

        user = db.usuarios.find_one({"email":email})
        return user is not None


class User(UserMixin):
    def __init__(self, user_json):
        self.user_json = user_json

    def get_id(self):
        object_id = self.user_json.get('_id')
        return str(object_id)
    

# -----------------------------> CLIENTES < ------------------------------

class Client:
    def __init__(self, _id, nameCompany, nit, city, quantity):
        self._id = _id
        self.nameCompany = nameCompany
        self.nit = nit
        self.city = city
        self.quantity = quantity 

    
class Cotizar:
    def __init__(self, _id, tVheiculo, mVehiculo, rVehiculo):

        self._id = _id
        self.tVehiculo = tVheiculo
        self.mVehiculo = mVehiculo
        self.rVehiculo = rVehiculo


# ----------------------> PRODUCTOS <--------------------------------------

class tVehiculo:
    def __init__(self, _id, tipo):

        self._id = _id
        self.tipo = tipo 

class mVehiculo:
    def __init__(self, _id, nombre, vehiculo_id):
        self._id = _id
        self.nombre = nombre
        self.vehiculo_id = vehiculo_id


class nModelo:
    def __init__(self, _id, nombre):

        self._id = _id 
        self.nombre = nombre