from flask import Blueprint, render_template, session, redirect, url_for, request
from flask_login import login_user, current_user
from flask_login import login_required
from babel.numbers import format_currency

from forms import FormClient, Productos
from models import Client, Cotizar
from extentions import db
import uuid

blpd = Blueprint("appDash", __name__, template_folder="./templates", static_folder="./static")


@blpd.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = FormClient()

    name = current_user.user_json.get('name') # current user hereda a partir de la clase User
    di = current_user.user_json.get('_id')

    clients = db['clientes']
    clientAct = clients.find()

    #Validar cliente disponible
    nClient = list(db.clientes.find({}))

      
    
    return render_template('dashboard.html', name=name, di=di, form=form, clientes=clientAct)


# Ensure responses aren't cached / Para no permitir acceder a la sesión después de cerrar
@blpd.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response


# ---------------------------------------------> CRUD VISTA USUARIO <--------------------------------------------------------

@blpd.route('/client', methods=['GET', 'POST'])
def addClient():
    form = FormClient()

    if request.method == 'POST':
        nameCompany = request.form['nameCompany']
        nit = request.form['nit']
        city = request.form['city']
        quantity = request.form['quantity']
        _id = str(uuid.uuid4())

        new_client = Client(_id, nameCompany, nit, city, quantity)
        db.clientes.insert_one(new_client.__dict__)

        return redirect('/dashboard')
    
    return render_template('dashboard.html', form=form)


# ASIGNAR CLIENTE A USUARIO -------------------------------------------------------------------------------

@blpd.route('/asignar_cliente/<cliente_id>')
def asignar_cliente(cliente_id):
    # Verifica que el usuario esté autenticado
    if not current_user.is_authenticated:
        return redirect(url_for('login'))  # O redirige a la página de inicio de sesión

    # Convierte el ID del cliente a ObjectId
   

    # Actualiza el cliente en la base de datos asignando el usuario actual
    db.clientes.update_one({'_id': cliente_id}, {'$set': {'usuario_id': current_user.user_json.get('_id')}})

    return redirect('/dashboard')

    

# VISTA PERFIL

@blpd.route('/perfil', methods=['GET', 'POST'])
def perfil():

    
    name = current_user.user_json.get('name')
    sede = current_user.user_json.get('sede')
    email = current_user.user_json.get('email')

    user_id = current_user.user_json.get('_id')

    clients = db['clientes']
    clientesAct = clients.find({'usuario_id':user_id})

    #list(db.clientes.find_one({'usuario_id':user_id}))

    


    return render_template('perfil.html', name=name, sede=sede, email=email, clientes=clientesAct)



# CREAR OPERACIÓN PARA SOLTAR CLIENTE

@blpd.route('/soltar_cliente/<cliente_id>')
def soltar_cliente(cliente_id):
    

    cliente = db.clientes.find_one({'_id': cliente_id})
    # Actualiza el cliente en la base de datos eliminando el campo 'usuario_id'
    if cliente and cliente.get('usuario_id') == current_user.user_json.get('_id'):
        db.clientes.update_one({'_id': cliente_id}, {'$unset': {'usuario_id': 1}})


    # MANEJO PARA QUE ME REDIRIJA A LA RUTA DEPENDIENDO DESDE DONDE SUELTE EL CLIENTE

    origin = request.args.get('origin', 'dashboard')

    if origin == 'perfil':
        return redirect('/perfil')
    elif origin == 'dashboard':
        return redirect('/dashboard')
    else:
        # Tratamiento de casos no manejados
        return redirect('/dashboard')


# CREANDO FUNCION PARA COTIZAR

@blpd.route('/cotizar/<cliente_id>', methods = ['GET', 'POST'])
def cotizar(cliente_id):
    form = Productos()
    
    cliente = db.clientes.find_one({"_id": cliente_id})

    usuario = db.usuarios.find_one({"_id":current_user.user_json.get('_id')})

    tipo = db.vehiculos.find()
    marca = db.marca.find()
    refe = db.modelo.find()


    #form.tipo_vehiculo.choices = [str(vehiculo['tipo']) for vehiculo in opciones]

    form.tVehiculo.choices = [vehiculo['tipo'] for vehiculo in tipo]
    form.mVehiculo.choices = [marc['nombre'] for marc in marca]
    form.rVehiculo.choices = [ref['nombre'] for ref in refe]


    if request.method == 'POST' and form.validate():

        if form.submitb.data:

            rVehiculo = request.form['rVehiculo']

            precio_doc = db.precioUn.find_one({'nombre_modelo': rVehiculo})
            precio = precio_doc['valor'] if precio_doc else 'Precio no disponible'
            format_precio = format_currency(precio, 'COP', locale='es_CO')
            format_precio = format_precio.replace(',00', "")

            return  render_template('cotizacion.html', cliente=cliente, usuario=usuario, form=form, precio=precio, format_precio=format_precio)
        
        elif form.submit.data:

            tVehiculo = request.form['tVehiculo']
            mVehiculo = request.form['mVehiculo']
            rVehiculo = request.form['rVehiculo']
        
            # print(rVehiculo)
            # print(precio)
            
            _id = str(uuid.uuid4())
            new_quoting = Cotizar(_id, tVehiculo, mVehiculo, rVehiculo)
            db.quoting.insert_one(new_quoting.__dict__)

            return redirect(url_for('appDash.cotizar', cliente_id=cliente_id))
        

    return render_template('cotizacion.html', cliente=cliente, usuario=usuario, form=form, precio=None)