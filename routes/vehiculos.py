from flask import Blueprint, render_template, request, redirect, url_for
from forms import VehiculoForm
from extentions import db
from models import  tVehiculo, mVehiculo
import uuid

blpv = Blueprint('appVehiculo', __name__, template_folder="./templates", static_folder="./static")


@blpv.route('/crear_vehiculo', methods=['GET', 'POST'])
def crear_vehiculo():
    form = VehiculoForm()

    opciones = db.vehiculos.find()

    form.tipo_vehiculo.choices = [str(vehiculo['tipo']) for vehiculo in opciones]



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
        if modelo_doc is None:
            _id =str(uuid.uuid4())
            modelo_doc = {'nombre': modelo_nombre, '_id': _id, 'nombre_marca': marca_doc['nombre'],'marca_id': marca_doc['_id']}
            db.modelo.insert_one(modelo_doc)


        xd = modelo_doc['nombre']
        precio_doc = db.precioUn.find_one({'nombre_modelo': xd})
        if precio_doc is None:
            _id = str(uuid.uuid4())
            precio_doc = {'valor': precio_unidad, '_id': _id, 'nombre_modelo': modelo_doc['nombre'],'modelo_id': modelo_doc['_id']}
            db.precioUn.insert_one(precio_doc)

        

    


        return redirect('/crear_vehiculo')
    
    # vehiculos = db.vehiculos.find()
    # nombre_vehiculo = [vehiculo['tipo'] for vehiculo in vehiculos]

    # marcas = db.marca.find()
    # nombre_marca = [marca['nombre'] for marca in marcas]

    # modelos = db.modelo.find()
    # nombre_modelo = [modelo['nombre'] for modelo in modelos]



    
    return render_template('crear.html', form=form)