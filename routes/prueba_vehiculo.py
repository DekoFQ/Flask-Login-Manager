from flask import Blueprint, render_template, request, redirect, url_for, session
from forms import VehiculoForm
from flask_login import login_required
from extentions import db
from models import  tVehiculo, mVehiculo, nModelo
import uuid

blppv = Blueprint('pruebaVehiculo', __name__, template_folder="./templates", static_folder="./static")


@blppv.route('/crear_vehiculo1', methods=['GET', 'POST'])
@login_required
def crear_vehiculo1():
    form = VehiculoForm()


   

    opciones = db.vehiculos.find()
    lista_marcas = db.marca.find()
    lista_referencia = db.modelo.find()




    form.tipo_vehiculo.choices = [str(vehiculo['tipo']) for vehiculo in opciones]
    form.marca.choices = [str(marca['nombre']) for marca in lista_marcas]
    form.modelo.choices =[(str(modelo['nombre']), str(modelo['nombre'])) for modelo in lista_referencia if 'nombre' in modelo and modelo['nombre'] is not None]



    if form.validate_on_submit():
        tipo_vehiculo = form.tipo_vehiculo.data
        marca_nombre = form.marca.data
        modelo_nombre = form.modelo.data
        precio_unidad = form.precio.data
        



        tipo_vehiculo_doc = db.vehiculos.find_one({'tipo': tipo_vehiculo})
        if tipo_vehiculo_doc is None:
            _id = str(uuid.uuid4())
            tipo_vehiculo_doc = {'tipo': tipo_vehiculo, '_id': _id}
            db.vehiculos.insert_one(tipo_vehiculo_doc)
            

            # new_tipe = tVehiculo(_id, tipo_vehiculo_doc['tipo'])
            # db.vehiculos.insert_one(new_tipe.__dict__)

            # print('---------------><-------------', new_tipe['_id'])

        marca_doc = db.marca.find_one({'nombre': marca_nombre})
        if marca_doc is None:
            _id =str(uuid.uuid4())
            marca_doc = {'nombre': marca_nombre, '_id': _id, 'vehiculo_id': [tipo_vehiculo_doc['_id']]}
            db.marca.insert_one(marca_doc)

        else:
            if tipo_vehiculo_doc['_id'] not in marca_doc['vehiculo_id']:
                marca_doc['vehiculo_id'].append(tipo_vehiculo_doc['_id'])
                db.marca.update_one({'_id': marca_doc['_id']}, {'$set':{'vehiculo_id': marca_doc['vehiculo_id']}})
        
            

            # new_marc = mVehiculo(_id, marca_doc['nombre'])
            # db.marca.insert_one(new_marc.__dict__)
        # nombre_xd = marca_doc['nombre']
        # print(nombre_xd)
        modelo_doc = db.modelo.find_one({'nombre': modelo_nombre})
        modelo_mar = db.modelo.find_one({'nombre_marca':marca_doc})
        if modelo_doc is None:
            _id =str(uuid.uuid4())
            modelo_doc = {'nombre': modelo_nombre, '_id': _id, 'nombre_marca': marca_doc['nombre'],'marca_id': marca_doc['_id']}
            db.modelo.insert_one(modelo_doc)

        else:
            update_data= {'nombre_marca':marca_doc['nombre'],'marca_id':marca_doc['_id']}
            db.modelo.update_one({'nombre':modelo_nombre},{'$set':update_data})
        

        xd = modelo_doc['nombre']
        precio_doc = db.precioUn.find_one({'nombre_modelo': xd})
        if precio_doc is None:
            _id = str(uuid.uuid4())
            precio_doc = {'valor': precio_unidad, '_id': _id, 'nombre_modelo': modelo_doc['nombre'],'modelo_id': modelo_doc['_id']}
            db.precioUn.insert_one(precio_doc)

        

        return redirect('/crear_vehiculo1')
    
    

    return render_template('prueba_vehiculo.html', form=form)


@blppv.route('/crear_nuevo_elemento', methods=['POST'])
def crear_nuevo_elemento():
    form = VehiculoForm()


    tipos_vehiculos = [tipo['tipo'] for tipo in db.vehiculos.find()]
    print(tipos_vehiculos)
    
    

    if request.method == 'POST':

        tipos_select = [tipo for tipo, field in zip(tipos_vehiculos, form.check) if field.data]

        _id = str(uuid.uuid4())
        nombre = request.form['nuevo_modelo']

        nuevo_elemento = {'nombre':nombre, '_id':_id}
        db.modelo.insert_one(nuevo_elemento) 



        return redirect('/crear_vehiculo1')
    
    return render_template('prueba_vehiculo.html', forms=form)