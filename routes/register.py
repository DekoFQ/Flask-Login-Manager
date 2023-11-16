from flask import Blueprint, render_template, url_for, request, redirect, flash
from forms import Register
from models import User, CreateUser
from extentions import db
import bcrypt
import uuid



blpr = Blueprint("registerApp", __name__, template_folder="./templates", static_folder="./static")


@blpr.route('/register', methods=['GET', 'POST'])
def register():
    form = Register()

    if form.validate_on_submit():

        name = form.name.data
        sede = form.sede.data
        email = form.email.data
        password = request.form['password']
        _id = str(uuid.uuid4())

        salt = bcrypt.gensalt()

        hash_password = bcrypt.hashpw(password.encode('utf-8'), salt)

        if CreateUser.is_email_registered(email):
            flash('El correo electronico ya está registrado')
            return redirect(url_for('registerApp.register'))

        new_user = CreateUser(_id, name, sede, email, hash_password)
        db.usuarios.insert_one(new_user.__dict__)

        return redirect(url_for('loginApp.login')) #Se retorna la vista de registro nuevamente para que al recargar la pagina, el navegador no envie la ultima solicitud POST y que no se genere otro usuario en la base de datos
    
    return render_template('register.html', form=form)