from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField, IntegerField, SelectField, FloatField, DecimalField, BooleanField 
from wtforms.validators import DataRequired, Length, ValidationError, InputRequired
from extentions import db



class Register(FlaskForm):
    name = StringField(label="Nombre", validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder":"Nombre"})
    sede = StringField(label="Sede", validators=[InputRequired()], render_kw={"placeholder":"Sede"})
    email = EmailField(label="Correo", validators=[InputRequired()], render_kw={"placeholder":"Correo"})
    password = PasswordField(label="Contraseña", validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder":"Contraseña"})
    submit = SubmitField("Registrar")

    def validate_user(self, name):
        existing_name = db.usuarios.find_one({"name":name})

        if existing_name:
            raise ValidationError("El nombre ya existe. Por favor ingrese uno diferente")
        

class Login(FlaskForm):
    name = StringField(label="Nombre", validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder":"Nombre"})
    password = PasswordField(label="Contraseña", validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder":"Contraseña"})
    submit = SubmitField(label="Login")



# -----------------------> MANEJO CLIENTES <--------------------------

class FormClient(FlaskForm):
    nameCompany = StringField(label="Nombre de la compañía", render_kw={'placeholder':'Nombre Compañía'})
    nit = IntegerField(label="NIT")
    city = StringField(label="Ciudad donde radica", render_kw={'placeholder':'Ciudad donde radica'})
    quantity = IntegerField(label="Cantidad de producto")
    submit = SubmitField('Añadir')

class Asignacion(FlaskForm):
    asignar = SubmitField('Asignar')


# -----------------------> PRODUCTOS <--------------------------

class Productos(FlaskForm):
    tVehiculo = SelectField('Tipo Vehículo')
    mVehiculo = SelectField('Marca del Vehículo')
    rVehiculo = SelectField('Referencia del Vehiculo')
    submitb = SubmitField('Buscar')
    submit = SubmitField('Enviar') 


# -----------------------> CREAR VEHICULOS <-----------------------------

class VehiculoForm(FlaskForm):
    tipo_vehiculo = SelectField('Tipo de Vehiculo')
    marca = SelectField('Marca')
    modelo = SelectField('Modelo')#, validators=[DataRequired()], render_kw={'placeholder':'Modelo'})
    precio = IntegerField('Precio', validators=[DataRequired()], render_kw={'placeholder':'Precio'})
    submitn = SubmitField('Nuevo')
    submit = SubmitField('Crear')
    nuevo_modelo = StringField('Nuevo')
    check = BooleanField('Prueba', default=False)



